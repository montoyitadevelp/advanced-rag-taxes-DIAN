import os
import pickle
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
from src.utils.general import chunk_text


class RagManager:

    def __init__(self, db: AsyncSession):
        self.db = db
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """
        Calculates the cosine similarity between two vectors.

        Args:
            vec1 (np.ndarray): The first vector.
            vec2 (np.ndarray): The second vector.

        Returns:
            float: The cosine similarity between vec1 and vec2.

        Raises:
            ValueError: If an error occurs during calculation, with details about the error.

        Example:
            similarity = await cosine_similarity([1, 2, 3], [4, 5, 6])
        """
        try:
            vec1 = np.array(vec1)
            vec2 = np.array(vec2)
            return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
        except Exception as e:
            raise ValueError({
                "error": "Error calculating cosine similarity",
                "details": str(e),
                "method": "RagManager.cosine_similarity"
            })

    async def get_top_k_documents(self, question_embedding: np.ndarray, documents: list, k: int = 5) -> list:
        """
        Retrieves the top K documents most similar to a given question embedding.

        Args:
            question_embedding (np.ndarray): The embedding vector representing the question.
            documents (list): A list of document objects, each containing an 'embedding' attribute (serialized).
            k (int, optional): The number of top documents to retrieve. Defaults to 5.

        Returns:
            list: A list of tuples (score, doc), where 'score' is the cosine similarity between the question and document embeddings,
                  and 'doc' is the corresponding document object.

        Raises:
            ValueError: If an error occurs during the retrieval or similarity computation process. The exception contains details about the error.
        """
        try:
            scored_docs = []
            for doc in documents:
                doc_embedding = pickle.loads(doc.embedding)
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
        Asynchronously retrieves the top-k most relevant documents based on a given question embedding.

        Args:
            question_embedding (Any): The embedding vector representing the user's question.
            k (int, optional): The number of top documents to retrieve. Defaults to 5.

        Returns:
            List[Any]: A list of the top-k relevant documents.

        Raises:
            ValueError: If an error occurs during the retrieval process, with details about the error and method.
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

    async def augmented(self, question_embedding: np.ndarray, k: int = 5) -> str:
        """
        Retrieves the top-k most relevant documents based on the provided question embedding,
        concatenates their content, and returns the resulting context string.

        Args:
            question_embedding (Any): The embedding vector representing the user's question.
            k (int, optional): The number of top documents to retrieve. Defaults to 5.

        Returns:
            str: A single string containing the concatenated content of the top-k documents.

        Raises:
            ValueError: If an error occurs during the retrieval or augmentation process, 
                        with details about the error and the method name.
        """
        try:
            top_docs = await self.retrieval(question_embedding, k)
            context = "\n".join(doc.content for _, doc in top_docs)
            return context
        except Exception as e:
            raise ValueError({
                "error": "Error during augmentation",
                "details": str(e),
                "method": "RagManager.augmented"
            })


    async def generation(self, context: str, question: str) -> str:
        """
        Asynchronously generates a response to a given question based on the provided context using the GPT-4o model.

        Args:
            context (str): The context information to base the answer on.
            question (str): The user's question to be answered.

        Returns:
            str: The generated response from the language model.

        Raises:
            ValueError: If an error occurs during the generation process, with details about the error and method.
        """
        try:
            prompt = settings.PROMPT_TEMPLATE.format(context=context, question=question)
            response = await self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[{"role": "user", "content": prompt}]
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
        Processes a user's question by generating an answer using retrieval-augmented generation (RAG).
        This method performs the following steps:
            1. Loads documents and creates embeddings if necessary.
            2. Generates an embedding for the input question.
            3. Retrieves the top relevant documents based on the question embedding.
            4. Constructs an augmented context from the retrieved documents.
            5. Generates an answer using the context and the original question.
            6. Stores the question and answer in the database.
            7. Links the retrieved documents to the generated answer.
            8. Returns the answer and the sources used.
        Args:
            payload (QuestionRequest): The request payload containing the user's question.
        Returns:
            AnswerResponse: An object containing the generated answer and the list of source document IDs.
        Raises:
            ValueError: If any error occurs during processing, with details about the error and method.
        """
        try:
            cache_path = os.path.join(os.path.dirname(__file__), "data", "embeddings_cache.pkl")
            csv_path = os.path.join(os.path.dirname(__file__), "data", "documents.csv")
            await self._load_documents_and_create_embeddings(csv_path, cache_path)

            response_embedding = await self.client.embeddings.create(
                model=settings.OPENAI_EMBEDDING_MODEL,
                input=payload.question
            )
            question_embedding = response_embedding.data[0].embedding

            top_docs = await self.retrieval(question_embedding, k=5)
            context = await self.augmented(question_embedding, k=5)
            answer_text = await self.generation(context, payload.question)

            question = await QuestionManager(self.db).create_question(payload, question_embedding)
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
        Asynchronously loads documents from a CSV file, splits their text content into manageable chunks,
        generates embeddings for each chunk using an external embedding client, and stores the resulting
        documents and embeddings in the database with optional caching.
        Args:
            csv_path (str): Path to the CSV file containing the documents. The CSV is expected to have at least
                'title', 'text', and 'doc_id' columns.
            cache_path (str): Path to the cache file. If this file exists, the function returns early and skips processing.
        Raises:
            ValueError: If any error occurs during loading, chunking, embedding creation, or database insertion,
                a ValueError is raised with details about the error and the method name.
        """
        try:
            if os.path.exists(cache_path):
                return 
            df = pd.read_csv(csv_path)
            raw_documents = df.to_dict(orient="records")

            chunked_documents = []
            for doc in raw_documents:
                chunks = chunk_text(doc["text"], max_chars=1500)
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
            embeddings = response.data

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
