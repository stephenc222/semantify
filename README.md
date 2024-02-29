# Semantify

Semantify is a powerful CLI tool designed to enhance long-form content by leveraging Generative AI. It enriches MDX blog posts with AI-generated summaries, Q&A sections, and semantically similar recommendations, providing a richer and more engaging reader experience. Ideal for content creators, marketers, and anyone looking to elevate their written content, Semantify automates the process of adding valuable, semantic information and establishing deeper connections between blog posts.

## Features

- **AI-Generated Summaries**: Automatically generates concise summaries for your blog posts, making it easier for readers to grasp the essence of your content quickly.
- **Q&A Sections**: Creates engaging Q&A sections from your content, adding interactive and informative elements that enhance reader engagement.
- **Semantic Recommendations**: Analyzes your content to recommend your other relevant blog posts, helping to increase page views and keep readers engaged with your site longer.
- **Customizable Enhancements**: Offers options to selectively update reading time estimates, recommendations, and Q&A sections for all blog posts.

## Installation

Semantify requires Python 3.9 or later. You can install Semantify directly from PyPI:

```bash
pip install semantify
```

This command will install Semantify and all required dependencies.

## Usage

After installation, you can run Semantify from the command line. Here's how to get started:

```bash
semantify --blog-directory "/path/to/your/blog/directory"
```

### Basic Commands

- **Specify an OpenAI API Key**: To use the AI features, you must provide an OpenAI API key. You can pass this key directly through the command line or set it as an environment variable (`OPENAI_API_KEY`).

  ```bash
  semantify --openai-api-key "your_openai_api_key"
  ```

- **Replace Reading Time**: To update the reading time estimates for your blog posts:

  ```bash
  semantify --replace-reading-time
  ```

- **Replace Recommendations**: To refresh the recommendations for your blog posts:

  ```bash
  semantify --replace-recommendations
  ```

- **Replace Q&A**: To update the Q&A sections for your blog posts:

  ```bash
  semantify --replace-qa
  ```

## Configuration

Semantify works out of the box with minimal configuration. However, you can customize various aspects of its behavior through command-line options or environment variables.

## Running the Examples

To run the examples, you need to have [poetry](https://python-poetry.org/) installed. Then, from the root of this repository run:

```bash
poetry install
poetry build
```

With the project built, you can install with pip:

```bash
pip install dist/semantify-0.0.1-py3-none-any.whl
```

Now, you can run the [Astro.js](https://astro.build/) example using the provided `run_semantify.sh` script

## Contributing

Contributions to Semantify are welcome! Whether it's bug reports, feature requests, or code contributions, please feel free to reach out or submit a pull request.

## License

Semantify is released under the Apache 2.0 License. See the LICENSE file for more details.
