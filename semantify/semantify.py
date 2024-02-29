#!/usr/bin/env python3
import os
import argparse
from semantify.recommender.blog_recommender import BlogRecommender
from semantify.summarizer.qa_generator import QAGenerator
from semantify.utils.calculate_reading_time import calculate_reading_time
from semantify.utils.frontmatter_utils import FrontmatterUtils
from semantify.services.sqlite import SQLiteDBService
from semantify.services.openai import OpenAIService
from semantify.interfaces import IMetadataManager, IRecommender


class Semantify:
    def __init__(self, metadata_manager: IMetadataManager = None, blog_directory=None, recommender: IRecommender = None, qa_generator=None):
        self.metadata_manager = metadata_manager
        self.blog_directory = blog_directory
        self.qa_generator = qa_generator
        self.recommender = recommender

    @staticmethod
    def parse_arguments():
        parser = argparse.ArgumentParser(description='Process blog posts.')
        parser.add_argument('--openai-api-key',
                            help='Pass your OpenAI API Key. Default is to use the OPENAI_API_KEY environment variable.')
        parser.add_argument('--blog-directory',
                            help='Path to the blog directory. Default is to use the BLOG_DIRECTORY environment variable.')
        parser.add_argument('--replace-reading-time',
                            action='store_true',
                            help='Remove and replace reading time estimate for all blog posts')
        parser.add_argument('--replace-recommendations',
                            action='store_true',
                            help='Remove and replace recommendations for all blog posts')
        parser.add_argument('--replace-qa',
                            action='store_true',
                            help='Remove and replace Q&A for all blog posts')
        return parser.parse_args()

    def process_blog_post(self, mdx_path):
        if not os.path.exists(mdx_path):
            print(f"Path {mdx_path} does not exist.")
            return

        try:
            metadata, content, _ = self.metadata_manager.read_metadata(
                mdx_path)
            slug = metadata.get('slug')
        except Exception as e:
            print(f"Error processing {mdx_path}: {e}")
            return

        if not slug:
            print(f"Skipping {mdx_path}: No slug found.")
            return

        needs_update = False
        if not 'readingTime' in metadata:
            print('calculating reading time for:', slug)
            reading_time = calculate_reading_time(content)
            metadata['readingTime'] = reading_time
            needs_update = True
        else:
            print('skipping reading time for:', slug)

        needs_qa_update = False
        if not 'qaSection' in metadata:
            print('generating qa summary for:', slug)
            qa_summary = self.qa_generator.generate_qa_summary(
                content, metadata, slug)
            if qa_summary:
                needs_update = True
                needs_qa_update = True
                metadata['qaSection'] = qa_summary
        else:
            print('skipping qa summary for:', slug)

        if needs_qa_update:
            self.metadata_manager.update_metadata(
                mdx_path, metadata, content)
            print(f"Updated {slug} metadata with Q&A Summary.")

        if not 'recommendations' in metadata:
            recommendations = self.recommender.generate_recommendations(slug)
            if recommendations:
                metadata['recommendations'] = recommendations
                needs_update = True
        else:
            print('skipping recommendations for:', slug)

        if needs_update:
            self.metadata_manager.update_metadata(mdx_path, metadata, content)
            print(
                f"Processed {slug}: Reading Time, Q&A, Recommendations updated.")

    def start(self, args):
        replace_sections = []

        if args.replace_reading_time:
            replace_sections.append('readingTime')

        if args.replace_recommendations:
            replace_sections.append('recommendations')

        if args.replace_qa:
            replace_sections.append('qaSection')

        if len(replace_sections) > 0:
            self.metadata_manager.clear_sections(
                self.blog_directory, replace_sections)
            self.recommender.clear_embeddings()

        for root, _, files in os.walk(self.blog_directory):
            for file in filter(lambda f: f.endswith('.mdx'), files):
                mdx_path = os.path.join(root, file)
                try:
                    self.process_blog_post(mdx_path)
                except ValueError as e:
                    print(e)


def main():
    args = Semantify.parse_arguments()
    db_service = SQLiteDBService(db_path=args.blog_directory)
    metadata_manager = FrontmatterUtils()
    recommender = BlogRecommender(db_service=db_service,
                                  metadata_manager=metadata_manager,
                                  blog_directory=args.blog_directory)
    llm_service = OpenAIService(api_key=args.openai_api_key)
    qa_generator = QAGenerator(llm_service=llm_service)

    semantify = Semantify(metadata_manager=metadata_manager,
                          blog_directory=args.blog_directory,
                          qa_generator=qa_generator,
                          recommender=recommender)
    semantify.start(args)


if __name__ == "__main__":
    main()
