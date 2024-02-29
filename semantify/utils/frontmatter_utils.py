import os
import yaml
import re
from typing import Tuple, Optional, Dict, List
from semantify.models import Frontmatter
from semantify.interfaces import IMetadataManager


class FrontmatterUtils(IMetadataManager):
    def __init__(self):
        pass

    @classmethod
    def read_metadata(cls, identifier: str) -> Tuple[Optional[Dict], Optional[str], Optional[str]]:
        return cls.get_frontmatter_and_content(identifier)

    @classmethod
    def update_metadata(cls, identifier: str, metadata: Dict, content: str) -> None:
        cls.update_frontmatter_and_content(identifier, metadata, content)

    @classmethod
    def clear_sections(cls, directory: str, sections: List[str]) -> None:
        cls.clear_sections_from_frontmatter(directory, sections)

    @staticmethod
    def _read_mdx_file(mdx_path: str) -> str:
        """
        Utility function to read the content of an MDX file and split it into parts.
        """
        with open(mdx_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content

    @staticmethod
    def _split_frontmatter(content: str) -> Tuple[str, str]:
        """
        Utility function to split MDX content into frontmatter and body.
        """
        parts = re.split(r'^---\s*$', content, flags=re.MULTILINE)
        if len(parts) < 3:
            raise ValueError("MDX content does not have proper frontmatter.")
        return parts[1], '\n---\n'.join(parts[2:])

    @staticmethod
    def _parse_frontmatter(frontmatter_str: str) -> dict:
        """
        Utility function to parse YAML frontmatter.
        """
        try:
            return yaml.safe_load(frontmatter_str)
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing YAML frontmatter: {e}")

    @classmethod
    def get_frontmatter_and_content(cls, mdx_path: str) -> Tuple[Optional[Frontmatter], Optional[str], Optional[str]]:
        """
        Extract 'slug', frontmatter, and main_content from the MDX frontmatter.
        """
        try:
            content = cls._read_mdx_file(mdx_path)
            frontmatter_str, main_content = cls._split_frontmatter(content)
            frontmatter = cls._parse_frontmatter(frontmatter_str)
            return frontmatter, main_content, frontmatter_str
        except ValueError as e:
            print(e)
            return None, None, None

    @staticmethod
    def update_frontmatter_and_content(mdx_path: str, new_frontmatter: dict, new_content: str):
        """
        Update MDX file with new frontmatter and content.
        """
        frontmatter_str = yaml.safe_dump(
            new_frontmatter, allow_unicode=True, default_flow_style=False, sort_keys=False)
        updated_content = f"---\n{frontmatter_str}---\n{new_content}"
        with open(mdx_path, 'w', encoding='utf-8') as file:
            file.write(updated_content)

    @classmethod
    def clear_sections_from_frontmatter(cls, blog_directory: str, sections: list[str]):
        """
        Clear recommendations from all MDX files in a directory.
        """
        for root, _, files in os.walk(blog_directory):
            for file in files:
                if file.endswith('.mdx'):
                    mdx_path = os.path.join(root, file)
                    try:
                        frontmatter, content, _ = cls.get_frontmatter_and_content(
                            mdx_path)
                        modified = False
                        for section in sections:
                            if section in frontmatter:
                                del frontmatter[section]
                                modified = True
                        if modified:
                            cls.update_frontmatter_and_content(
                                mdx_path, frontmatter, content)
                            print(
                                f"Removed {', '.join(sections)} from {mdx_path}.")
                    except ValueError as e:
                        print(e)
