import argparse
import os
import unittest
from unittest.mock import patch, MagicMock, call
from .semantify import Semantify


class TestSemantify(unittest.TestCase):
    @patch.dict('os.environ', {'OPENAI_API_KEY': 'your-api-key', 'BLOG_DIRECTORY': '/path/to/blog/directory'})
    def test_initialize_qa_generator(self):
        semantify_instance = Semantify()
        result = semantify_instance.initialize_qa_generator('your-api-key')
        self.assertIsNotNone(result)

    @patch.dict('os.environ', {'OPENAI_API_KEY': 'your-api-key', 'BLOG_DIRECTORY': '/path/to/blog/directory'})
    def test_initialize_recommender(self):
        semantify_instance = Semantify()
        db_path = "path/to/database.db"
        blog_directory = "path/to/blog/directory"
        result = semantify_instance.initialize_recommender(
            db_path, blog_directory)
        self.assertIsNotNone(result)

    @patch.dict('os.environ', {'OPENAI_API_KEY': 'your-api-key', 'BLOG_DIRECTORY': '/path/to/blog/directory'})
    def test_process_blog_post(self):
        semantify_instance = Semantify()
        mdx_path = "path/to/blog_post.mdx"
        recommender = MagicMock()
        qa_generator = MagicMock()
        result = semantify_instance.process_blog_post(
            mdx_path, recommender, qa_generator)
        self.assertIsNone(result)

    @patch.dict('os.environ', {'OPENAI_API_KEY': 'your-api-key', 'BLOG_DIRECTORY': '/path/to/blog/directory'})
    @patch('os.walk')
    @patch('os.path.join')
    def test_run_pipeline(self, mock_join, mock_walk):
        # Mock the return value of os.walk
        mock_walk.return_value = [
            ('/path/to/blog/directory', [], ['test_post1.mdx', 'test_post2.mdx'])]

        # Mock the behavior of os.path.join
        mock_join.side_effect = lambda root, file: f"{root}/{file}"

        # Instantiate Semantify class
        semantify_instance = Semantify()

        # Mock objects
        recommender = MagicMock()
        qa_generator = MagicMock()
        mock_metadata = {'slug': 'test_slug'}

        # Patch the read_metadata method to return mock metadata
        with patch('utils.frontmatter_utils.FrontmatterUtils.read_metadata', return_value=mock_metadata):
            # Patch the process_blog_post method
            with patch.object(semantify_instance, 'process_blog_post', return_value=None) as mock_process_blog_post:
                # Call the run_pipeline method
                semantify_instance.run_pipeline(
                    '/path/to/blog/directory', recommender, qa_generator)

        # Define the expected calls for os.path.join and process_blog_post
        expected_join_calls = [call('/path/to/blog/directory', 'test_post1.mdx'),
                               call('/path/to/blog/directory', 'test_post2.mdx')]
        expected_process_calls = [
            call('/path/to/blog/directory/test_post1.mdx',
                 recommender=recommender, qa_generator=qa_generator),
            call('/path/to/blog/directory/test_post2.mdx',
                 recommender=recommender, qa_generator=qa_generator)
        ]

        # Assert that os.path.join was called with the correct arguments for each file
        mock_join.assert_has_calls(expected_join_calls, any_order=True)

        # Assert that process_blog_post was called with the correct arguments for each file
        mock_process_blog_post.assert_has_calls(
            expected_process_calls, any_order=True)


@patch.dict('os.environ', {'OPENAI_API_KEY': 'your-api-key', 'BLOG_DIRECTORY': '/path/to/blog/directory'})
def test_start():
    with patch(
            'argparse.ArgumentParser.parse_args',
            return_value=argparse.Namespace(
                blog_directory='/path/to/blog/directory',
                openai_api_key='some-api-key',
                replace_reading_time=False,
                replace_recommendations=False,
                replace_qa=False)):
        semantify_instance = Semantify()
        args = Semantify.parse_arguments()
        semantify_instance.start(args)


if __name__ == "__main__":
    unittest.main()
