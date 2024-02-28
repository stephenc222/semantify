#!/bin/bash
source .env
semantify --openai-api-key $OPENAI_API_KEY --blog-directory $BLOG_DIRECTORY "$@"
