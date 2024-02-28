# Example Semantify Astro.js Project

## Getting Started

Before integrating Semantify into your Astro.js project, ensure you have Poetry installed on your system. Poetry is a dependency management and packaging tool in Python that simplifies the installation and management of libraries and tools like Semantify.

### Prerequisites

- Python 3.7 or higher
- Poetry

### Installation

1. **Install Poetry**: If you haven't already installed Poetry, you can do so by following the official installation instructions [here](https://python-poetry.org/docs/#installation).

2. **Activate Poetry Shell**: Navigate to your project directory where Semantify will be used and activate the poetry shell to create a virtual environment for your Python dependencies.

   ```bash
   poetry shell
   ```

3. **Install Semantify**: With the virtual environment activated, install Semantify using Poetry.

   ```bash
   poetry install
   ```

## Usage

To use Semantify with your Astro.js project, follow these steps:

1. **Navigate to Your Blog Content Directory**: Make sure you are in the directory that contains your MDX-based blog content. For Astro.js projects, this will typically be under `src/content/blog`.

2. **Run Semantify**: Use the `semantify` command to analyze your blog posts and add the AI-generated content. You will need to provide your OpenAI API key via the `--openai-api-key` option.

   ```bash
   semantify --openai-api-key $OPENAI_API_KEY --blog-directory ./path/to/your/blog/content
   ```

Replace `$OPENAI_API_KEY` with your actual OpenAI API key, and `./path/to/your/blog/content` with the relative path to your blog's content directory.
