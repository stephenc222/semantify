import os
from semantify.interfaces import IMetadataManager, IDBService, IRecommender


class BlogRecommender(IRecommender):
    def __init__(self, metadata_manager: IMetadataManager, db_service: IDBService, blog_directory: str = None):
        blog_directory = blog_directory or os.environ.get("BLOG_DIRECTORY")
        if not blog_directory:
            raise ValueError("Blog directory must be provided.")
        self.blog_directory = blog_directory
        self.metadata_manager = metadata_manager
        self.db_service = db_service

    def ensure_embeddings(self):
        """Ensure all blog posts have up-to-date embeddings."""
        if not self.blog_directory:
            print("Blog directory not set. Cannot ensure embeddings.")
            return

        for root, _, files in os.walk(self.blog_directory):
            for filename in files:
                if filename.endswith('.mdx'):
                    mdx_path = os.path.join(root, filename)
                    metatada, _, metadata_str = self.metadata_manager.read_metadata(
                        mdx_path)
                    slug = metatada.get('slug')
                    title = metatada.get('title')

                    # Create or update embedding as necessary
                    self.db_service.create_or_update_embedding(
                        slug, metadata_str, title)

    def clear_embeddings(self):
        """Clear all embeddings from the database."""
        self.db_service.clear_embeddings()

    def generate_recommendations(self, slug: str):
        """Main method to generate recommendations for a given post and update its MDX file."""
        # Ensure all embeddings are up-to-date before generating recommendations
        self.ensure_embeddings()

        current_embedding = self.db_service.get_embedding(slug)
        if not current_embedding:
            print(f"No embedding found for slug: {slug}")
            return

        recommendations = self.db_service.find_similar_posts(slug)
        return [{"slug": slug, "title": title} for slug, title, _ in recommendations]
