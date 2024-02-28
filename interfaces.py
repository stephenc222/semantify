from typing import Dict, List, Optional, Tuple
from abc import ABC, abstractmethod
from pathlib import Path


class IRecommender(ABC):
    @abstractmethod
    def ensure_embeddings(self):
        """Ensure that embeddings are available for all posts."""

    @abstractmethod
    def clear_embeddings(self):
        """Clear existing embeddings."""

    @abstractmethod
    def generate_recommendations(self, slug: str) -> List[Dict[str, str]]:
        """Generate recommendations for a given post."""


class IDBService(ABC):
    @abstractmethod
    def initialize_database(self, content_directory: Path):
        """Initialize the database."""

    @abstractmethod
    def clear_embeddings(self):
        """Clear existing embeddings."""

    @abstractmethod
    def create_or_update_embedding(self, slug: str, metadata: str, title: str):
        """Create or update embeddings."""

    @abstractmethod
    def get_embedding(self, slug: str) -> List[float]:
        """Retrieve embeddings."""

    @abstractmethod
    def find_similar_posts(self, slug: str) -> List[Dict[str, str]]:
        """Find similar posts."""


class IMetadataManager(ABC):
    @abstractmethod
    def read_metadata(self, identifier: str) -> Tuple[Optional[Dict], Optional[str], Optional[str]]:
        """Read metadata and content based on an identifier (e.g., file path)."""
        pass

    @abstractmethod
    def update_metadata(self, identifier: str, metadata: Dict, content: str) -> None:
        """Update metadata and content for a given identifier."""
        pass

    @abstractmethod
    def clear_sections(self, directory: str, sections: List[str]) -> None:
        """Clear specified sections from metadata in all files within a directory."""
        pass


class ILLMService(ABC):
    @abstractmethod
    def generate_qa_pairs(self, content: str) -> List[Dict[str, str]]:
        """
        Generate a list of question and answer pairs from the given content.

        Parameters:
        - content (str): The text content from which to generate Q&A pairs.

        Returns:
        - List[Dict[str, str]]: A list of dictionaries, each containing a 'question' and an 'answer' key.
        """
        pass
