import os
import heapq
import numpy as np
import pandas as pd
from openai import AsyncOpenAI
from sqlalchemy.ext.asyncio import AsyncSession
from src.config.settings import settings
from src.answer.services import AnswerManager
from src.answer_document.services import AnswerDocumentManager
from src.question.services import QuestionManager
from src.document.services import DocumentManager
from src.question.schemas import QuestionRequest
from src.answer.schemas import AnswerResponse
from src.utils.general import chunk_text, normalize_v



class RagManager:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """
        Calculate the cosine similarity between two normalized embeddings.
        """
        try:
            vec1 = normalize_v(np.array(vec1))
            vec2 = normalize_v(np.array(vec2))
            return float(np.dot(vec1, vec2))
        except Exception as e:
            raise ValueError({
                "error": "Error calculating cosine similarity",
                "details": str(e),
                "method": "RagManager.cosine_similarity"
            })

    async def get_top_k_documents(self, question_embedding: np.ndarray, documents: list, k: int = 5) -> list:
        """
        Retrieves the top-k most similar documents to the question embedding.
        """
        try:
            scored_docs = []
            for doc in documents:
                doc_embedding = np.array(doc.embedding) 
                score = await self.cosine_similarity(question_embedding, doc_embedding)
                scored_docs.append((score, doc))
            top_k = heapq.nlargest(k, scored_docs, key=lambda x: x[0])
            return [(score, doc) for score, doc in top_k]
        except Exception as e:
            raise ValueError({
                "error": "Error retrieving top K documents",
                "details": str(e),
                "method": "RagManager.get_top_k_documents"
            })

    async def retrieval(self, question_embedding: np.ndarray, k: int = 5) -> list:
        """
        Retrieves relevant documents from the database.
        """
        try:
            all_documents = await DocumentManager(self.db).get_documents_list()
            top_docs = await self.get_top_k_documents(question_embedding, all_documents, k)
            return top_docs
        except Exception as e:
            raise ValueError({
                "error": "Error during retrieval",
                "details": str(e),
                "method": "RagManager.retrieval"
            })

    async def build_context(self, top_docs: list) -> str:
        """
        Builds the context for the question by concatenating the contents of the top documents.
        """
        try:
            return "\n".join(doc.content for _, doc in top_docs)
        except Exception as e:
            raise ValueError({
                "error": "Error building context",
                "details": str(e),
                "method": "RagManager.build_context"
            })

    async def generation(self, context: str, question: str) -> str:
        """
        Generates a response using GPT and the retrieved context.
        """
        try:
            system_prompt = settings.PROMPT_TEMPLATE 
            user_prompt = f"{context}\n\nPregunta:\n{question}"

            response = await self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            raise ValueError({
                "error": "Error during generation",
                "details": str(e),
                "method": "RagManager.generation"
            })

    async def process_question(self, payload: QuestionRequest) -> AnswerResponse:
        """
        Main processing flow for the RAG: retrieval → context → generation → persistence.
        """
        try:
            cache_path = os.path.join(os.path.dirname(__file__), "data", "embeddings_cache.pkl")
            csv_path = os.path.join(os.path.dirname(__file__), "data", "documents.csv")
            await self._load_documents_and_create_embeddings(csv_path, cache_path)


            response_embedding = await self.client.embeddings.create(
                model=settings.OPENAI_EMBEDDING_MODEL,
                input=payload.question
            )
            question_embedding = normalize_v(np.array(response_embedding.data[0].embedding))

            top_docs = await self.retrieval(question_embedding, k=5)
            context = await self.build_context(top_docs)

            answer_text = await self.generation(context, payload.question)

            question = await QuestionManager(self.db).create_question(payload, question_embedding.tolist())
            answer = await AnswerManager(self.db).create_answer(question_id=question.id, answer_text=answer_text)
            await AnswerDocumentManager(self.db).post_link_documents_to_answer(answer.id, top_docs)

            return AnswerResponse(
                answer=answer_text,
                sources=[str(doc.id) for _, doc in top_docs]
            )
        except Exception as e:
            raise ValueError({
                "error": "Error processing question",
                "details": str(e),
                "method": "RagManager.process_question"
            })

    async def _load_documents_and_create_embeddings(self, csv_path: str, cache_path: str):
        """
        Loads documents from a CSV file, chunks them, and creates normalized embeddings in the database.
        """
        try:
            if os.path.exists(cache_path):
                return
            df = pd.read_csv(csv_path)
            raw_documents = df.to_dict(orient="records")

            chunked_documents = []
            for doc in raw_documents:
                chunks = chunk_text(doc["text"], max_chars=800)
                for idx, chunk in enumerate(chunks):
                    chunked_documents.append({
                        "title": f"{doc['title']} [fragment {idx + 1}]",
                        "content": chunk,
                        "doc_id_original": doc["doc_id"]
                    })

            response = await self.client.embeddings.create(
                model=settings.OPENAI_EMBEDDING_MODEL,
                input=[doc["content"] for doc in chunked_documents]
            )
            embeddings = [normalize_v(np.array(e.embedding)).tolist() for e in response.data]

            await DocumentManager(self.db).bulk_create_documents_with_embeddings(
                documents=chunked_documents,
                embeddings=embeddings,  
                cache_path=cache_path
            )
        except Exception as e:
            raise ValueError({
                "error": "Error loading documents and creating embeddings",
                "details": str(e),
                "method": "RagManager._load_documents_and_create_embeddings"
            })
