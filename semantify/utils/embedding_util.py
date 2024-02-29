import json
import torch
import torch.nn.functional as F
from torch import Tensor
import os
os.environ["TOKENIZERS_PARALLELISM"] = "true"

EMBEDDING_MODEL = 'thenlper/gte-base'

# Initialize global variables to None
global tokenizer, model
tokenizer, model = None, None


def load_tokenizer_and_model():
    global tokenizer, model
    # Only load if tokenizer and model are not already loaded
    if tokenizer is None or model is None:
        print(
            f'Loading pretrained \"{EMBEDDING_MODEL}\" tokenizer and model...')

        # Import the module
        from transformers import AutoTokenizer, AutoModel

        tokenizer = AutoTokenizer.from_pretrained(EMBEDDING_MODEL)
        model = AutoModel.from_pretrained(EMBEDDING_MODEL)
        print(f" \"{EMBEDDING_MODEL}\" tokenizer and model loaded.")


def average_pool(last_hidden_states: Tensor, attention_mask: Tensor) -> Tensor:
    last_hidden = last_hidden_states.masked_fill(
        ~attention_mask[..., None].bool(), 0.0)
    return last_hidden.sum(dim=1) / attention_mask.sum(dim=1)[..., None]


def generate_embeddings(text, metadata={}):
    # Ensure tokenizer and model are loaded
    load_tokenizer_and_model()

    combined_text = " ".join(
        [text] + [v for k, v in metadata.items() if isinstance(v, str)])

    inputs = tokenizer(combined_text, return_tensors='pt',
                       max_length=512, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)

    attention_mask = inputs['attention_mask']
    embeddings = average_pool(outputs.last_hidden_state, attention_mask)

    # normalize embeddings
    embeddings = F.normalize(embeddings, p=2, dim=1)

    return json.dumps(embeddings.numpy().tolist()[0])
