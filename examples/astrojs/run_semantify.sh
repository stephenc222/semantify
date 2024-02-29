#!/bin/bash
source .env

# Assumes semantify is installed locally
# See the root README.md for more information on installing semantify locally
semantify --openai-api-key $OPENAI_API_KEY --blog-directory $BLOG_DIRECTORY "$@"
