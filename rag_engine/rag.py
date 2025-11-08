from langchain_chroma import Chroma
from langchain_core.documents import Document

from dotenv import load_dotenv
import os
import shutil


class Rag:

    def __init__(
        self,
        db_path: str,
        chunks: list[Document],
        embeddings,
        embedding_model: str = "llama3",
        force_recreate: bool = False,
        persist: bool = True,
    ):
        """
        Initialize RAG system.

        Args:
            db_path: Path to vector database
            chunks: Document chunks to embed
            embeddings: Embedding function
            embedding_model: Model name for embeddings
            force_recreate: If True, delete existing DB and recreate
            persist: If True, save DB to disk; if False, use in-memory only
        """
        self.db_path: str = db_path
        self.chunks: list[Document] = chunks
        self.embeddings = embeddings
        self.embedding_model: str = embedding_model
        self.persist: bool = persist
        self.db = self._initialize_rag(
            collection_name="rag_collection", force_recreate=force_recreate
        )

    def _initialize_rag(
        self, collection_name: str, force_recreate: bool = False
    ) -> Chroma:
        """
        Initialize vector database with smart caching.

        - If force_recreate=True: Delete existing DB and rebuild
        - If DB exists and persist=True: Load existing DB (fast!)
        - Otherwise: Create new DB
        """
        db_exists = os.path.exists(self.db_path)

        # Only delete if explicitly requested
        if force_recreate and db_exists:
            print(f"Force recreating database at: {self.db_path}")
            shutil.rmtree(self.db_path)
            db_exists = False

        if not db_exists:
            # Create new database
            if self.persist:
                db = Chroma.from_documents(
                    self.chunks,
                    self.embeddings,
                    persist_directory=self.db_path,
                    collection_name=collection_name,
                )
                print(
                    f"Created database with {len(self.chunks)} chunks: {self.db_path}"
                )
            else:
                # In-memory only (for temporary use)
                db = Chroma.from_documents(
                    self.chunks,
                    self.embeddings,
                    collection_name=collection_name,
                )
                print(f"Created in-memory database with {len(self.chunks)} chunks")
        else:
            # Load existing database (FAST - no re-embedding!)
            db = Chroma(
                persist_directory=self.db_path,
                embedding_function=self.embeddings,
                collection_name=collection_name,
            )
            print(f"Loaded existing database from: {self.db_path}")

        return db

    def cleanup(self):
        """Cleanup resources when done."""
        if hasattr(self, "db") and self.db:
            self.db = None

    def __enter__(self):
        """Context manager support for proper resource cleanup."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Cleanup on context exit."""
        self.cleanup()
        return False

    def query_rag(self, query: str, n_results: int) -> str:
        """Retrieve relevant context from vector database."""
        if self.db is None:
            raise RuntimeError("RAG database not initialized. Call __init__ first.")
        results = self.db.similarity_search(query, k=n_results)
        return "\n\n---\n\n".join([doc.page_content for doc in results])
