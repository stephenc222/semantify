import json
import os
from openai import OpenAI
from typing import List, Dict
from semantify.interfaces import ILLMService


class OpenAIService(ILLMService):
    def __init__(self, api_key: str, model: str = 'gpt-4-0125-preview'):
        api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key is required.")
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate_qa_pairs(self, content: str) -> List[Dict[str, str]]:
        prompt = "Create questions and answers from the following content:\n\n" + content
        response = self.client.chat.completions.create(
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": '''You are a helpful assistant designed to produce question and answer pairs from the given content, returning the top 5 most relevant questions and answers in the JSON format - only.
    OUTPUT FORMAT:
    {
       "questions": [{
            "question": "What is the capital of France?",
            "answer": "Paris"
         }],
    }''',
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=self.model,
        )
        return json.loads(response.choices[0].message.content)['questions']
