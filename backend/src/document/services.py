import pickle
from sqlalchemy.ext.asyncio import AsyncSession
from src.document.models import Document
from sqlalchemy import Sequence, select


class DocumentManager:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def bulk_create_documents_with_embeddings(self, documents: list[dict], embeddings: list, cache_path: str):
        """
        Bulk creates documents in the database and saves their embeddings in cache.
        """
        cache_data = []

        for i, doc in enumerate(documents):
            embedding = embeddings[i].embedding
            db_doc = await self._create({
                "title": doc["title"],
                "content": doc["content"],
                "embedding": pickle.dumps(embedding)
            })
            cache_data.append((doc["title"], doc["content"], embedding))

        with open(cache_path, "wb") as f:
            pickle.dump(cache_data, f)
    
    async def get_documents_list(self) -> Sequence[Document]:
        """
        Retrieves a list of all documents from the database.
        """
        try:
            query = select(Document)
            result = await self.db.execute(query)
            return result.scalars().all()
        except Exception as e:
            raise ValueError({
                "error": "Error retrieving documents",
                "details": str(e),
                "method": "DocumentManager.get_documents_list"
            })
        

    async def _create(self, payload: dict, is_flush: bool = False) -> Document:
        try:
            document = Document(**payload)
            self.db.add(document)
            if is_flush:
                await self.db.flush()
            else:
                await self.db.commit()
            await self.db.refresh(document)
            return document
        except Exception as e:
            raise ValueError({
                "error": "Error creating document",
                "details": str(e),
                "method": "DocumentManager._create"
            })
        
               