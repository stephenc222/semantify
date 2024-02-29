from typing import List, Dict
from pathlib import Path
import hashlib
import sqlean as sqlite3
from semantify.interfaces import IDBService
from semantify.utils.embedding_util import generate_embeddings
from semantify.utils.download_sqlite_extensions import download_sqlite_extensions

db_base_dir = Path.home() / ".semantify"

# Define base directory for the extensions
extensions_base_dir = Path.home() / ".semantify" / "native_libs"

TABLE_NAME = "blog_posts"
# Limit is actually minus 1 because the current post is excluded from the recommendations
QUERY_LIMIT = 4

# Constants for extension paths
VECTOR_EXTENSION_PATH = str(extensions_base_dir / "vector0")
VSS_EXTENSION_PATH = str(extensions_base_dir / "vss0")

# Table creation SQL
create_table_sql = """
CREATE TABLE IF NOT EXISTS blog_posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT NOT NULL,
    title TEXT NOT NULL,
    post_metadata_hash TEXT NOT NULL,
    additional_metadata TEXT,
    content_embedding BLOB,
    keywords TEXT
);
"""

create_virtual_table_sql = """
CREATE VIRTUAL TABLE IF NOT EXISTS vss_blog_posts USING vss0(content_embedding(768));
"""


class SQLiteDBService(IDBService):
    def __init__(self, db_path: str):
        download_sqlite_extensions()
        [conn, cursor] = self.initialize_database(db_path)
        self.conn = conn
        self.cursor = cursor

    def _generate_db_path(self, content_directory: Path) -> Path:
        """
        Generates a unique database path for the given content directory.

        Args:
        - content_directory: Path to the content directory.

        Returns:
        - Path object representing the unique database file path.
        """
        hash_digest = hashlib.sha256(
            str(content_directory).encode()).hexdigest()
        return Path.home() / ".semantify" / "databases" / f"{hash_digest}.db"

    def initialize_database(self, content_directory: Path):
        # Ensure base directory exists
        db_path = self._generate_db_path(content_directory)

        db_path.parent.mkdir(parents=True, exist_ok=True)

        db_base_dir.mkdir(parents=True, exist_ok=True)

        # Connect to or create the SQLite database
        conn = sqlite3.connect(db_path)

        # Load extensions
        conn.enable_load_extension(True)
        conn.load_extension(VECTOR_EXTENSION_PATH)
        conn.load_extension(VSS_EXTENSION_PATH)
        cursor = conn.cursor()

        # Create tables if they don't exist
        cursor.execute(create_table_sql)
        cursor.execute(create_virtual_table_sql)
        conn.commit()

        print(f"Database initialized at {db_path}")
        return [conn, cursor]

    def clear_embeddings(self):
        # Your method to clear embeddings
        self.cursor.execute("DELETE FROM blog_posts")
        self.cursor.execute("DELETE FROM vss_blog_posts")
        self.conn.commit()

    def create_or_update_embedding(self, slug: str, metadata: str, title: str):
        # Check if the slug already exists in the database
        hash_object = hashlib.sha256(metadata.encode())
        hex_dig = hash_object.hexdigest()
        self.cursor.execute(
            "SELECT post_metadata_hash FROM blog_posts WHERE slug = ?", (slug,))
        result = self.cursor.fetchone()
        if result and hex_dig != result[0]:
            embedding = generate_embeddings(metadata)

            self.cursor.execute(
                "SELECT id FROM blog_posts WHERE slug = ?", (slug,))
            row = self.cursor.fetchone()

            if row is None:
                print("No post found with the given slug:", slug)
            else:
                post_id = row[0]

                # Now perform the update
                self.cursor.execute(
                    "UPDATE blog_posts SET content_embedding = ?, post_metadata_hash = ?, title = ? WHERE slug = ?",
                    (embedding, hex_dig, title, slug)
                )
                self.cursor.execute(
                    "DELETE FROM vss_blog_posts WHERE rowid = ?", (post_id,))
                self.cursor.execute(
                    "INSERT INTO vss_blog_posts (rowid, content_embedding) VALUES (?, ?)", (post_id, embedding))
        elif not result:
            # Insert new post with embedding
            embedding = generate_embeddings(metadata)
            self.cursor.execute(
                "INSERT INTO blog_posts (slug, title, content_embedding, post_metadata_hash) VALUES (?, ?, ?, ?)", (slug, title, embedding, hex_dig))
            last_row_id = self.cursor.lastrowid
            self.cursor.execute(
                "INSERT INTO vss_blog_posts (rowid, content_embedding) VALUES (?, ?)", (last_row_id, embedding))
        self.conn.commit()

    def get_embedding(self, slug: str) -> List[float]:
        # Your method to retrieve embeddings
        self.cursor.execute(
            'SELECT content_embedding FROM blog_posts WHERE slug = ?', (slug,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return []

    def find_similar_posts(self, slug: str) -> List[Dict[str, str]]:
        # Your method to find similar posts
        self.cursor.execute(f"""
            WITH matches AS (
                SELECT rowid, distance
                FROM vss_{TABLE_NAME} 
                WHERE vss_search(content_embedding, (select content_embedding from {TABLE_NAME} where slug = ?))
                LIMIT {QUERY_LIMIT}
            )
            SELECT 
                {TABLE_NAME}.slug, 
                {TABLE_NAME}.title, 
                matches.distance
            FROM matches 
            LEFT JOIN {TABLE_NAME} ON {TABLE_NAME}.id = matches.rowid
            WHERE {TABLE_NAME}.slug != ?
        """, (slug, slug))
        result = self.cursor.fetchall()
        return result
