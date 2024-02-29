from semantify.interfaces import ILLMService
from typing import Dict


class QAGenerator:
    def __init__(self, llm_service: ILLMService):
        self.llm_service = llm_service

    def generate_qa_summary(self, content: str, frontmatter: Dict[str, str], slug: str):
        if self.check_existing_qa_section(frontmatter):
            print(
                f"Q&A Section already exists in the frontmatter of {slug}. Skipping generation.")
            return

        q_and_a = self.llm_service.generate_qa_pairs(content)
        return q_and_a

    def check_existing_qa_section(self, frontmatter: Dict[str, str]) -> bool:
        return 'qa_section' in frontmatter and bool(frontmatter['qa_section'])
