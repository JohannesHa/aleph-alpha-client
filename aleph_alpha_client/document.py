import base64
from typing import Dict, List, Union

from aleph_alpha_client.image import ImagePrompt
from aleph_alpha_client.prompt_item import _to_prompt_item


class Document:
    """
    A document that can be either a docx document or text/image prompts.
    """

    def __init__(
        self, base_64: str = None, prompt: List[Union[str, ImagePrompt]] = None
    ):
        # We use a base_64 representation for docx documents, because we want to embed the file
        # into a prompt send in JSON.
        self.base_64 = base_64

        self.prompt = prompt

    @classmethod
    def from_docx_bytes(cls, bytes: bytes):
        """
        Pass a docx file in bytes and prepare it to be used as a document
        """
        docx_base64 = base64.b64encode(bytes).decode()
        return cls(base_64=docx_base64)

    @classmethod
    def from_docx_file(cls, path: str):
        """
        Load a docx file from disk and prepare it to be used as a document
        """
        with open(path, "rb") as f:
            docx = f.read()
        return cls.from_docx_bytes(docx)

    @classmethod
    def from_prompt(cls, prompt: List[Union[str, ImagePrompt]]):
        """
        Pass a prompt and prepare it to be used as a document
        """
        return cls(prompt=prompt)

    def _to_serializable_document(self) -> Dict[str, str]:
        """
        A dict if serialized to JSON is suitable as a document element
        """
        if self.base_64 is not None:
            # Serialize docx to Document JSON format
            return {
                "docx": self.base_64,
            }
        elif self.prompt is not None:
            # Serialize prompt to Document JSON format
            prompt_data = [_to_prompt_item(prompt_item) for prompt_item in self.prompt]
            return {"prompt": prompt_data}