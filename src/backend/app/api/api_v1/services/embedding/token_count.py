<<<<<<< HEAD
import tiktoken
from loguru import logger

OPENAI_PRICING = {
    "gpt-3.5-turbo"          : {"prompt": 0.0015, "completion": 0.002},
    "gpt-3.5-turbo-0613"     : {"prompt": 0.0015, "completion": 0.002},
    "gpt-3.5-turbo-16k"      : {"prompt": 0.003,  "completion": 0.004},
    "gpt-3.5-turbo-16k-0613" : {"prompt": 0.003,  "completion": 0.004},
    "gpt-4"                  : {"prompt": 0.03,   "completion": 0.06},        
    'gpt-4-0613'             : {'prompt': 0.03, 'completion': 0.06},
    'gpt-4-32k'              : {'prompt': 0.06, 'completion': 0.12},
    "gpt-4-32k-0613"         : {"prompt": 0.06,   "completion": 0.12},    
    'embedding'              : {'hugging_face': 0, 'text-embedding-ada-002': 0.0001}
    }


OPENAI_MODEL_CONTEXT_LENGTH = {
    'gpt-35-turbo': 4097,
    'gpt-35-turbo-16k': 16385,
    'gpt-4-0613': 8192,
    'gpt-4-32k': 32768
    }



def llm_call_cost(response):
    """Returns the cost of the LLM call in dollars"""
    model = response["model"]
    usage = response["usage"]
    prompt_cost = OPENAI_PRICING[model]["prompt"]
    completion_cost = OPENAI_PRICING[model]["completion"]
    prompt_token_cost = (usage["prompt_tokens"] * prompt_cost)/1000
    completion_token_cost = (usage["completion_tokens"] * completion_cost)/1000
    return prompt_token_cost + completion_token_cost

=======
import tiktoken 
>>>>>>> bc1f253 (changes for embedding service)

def get_encoder_for_model(model_name: str): 
    try:
        encoding = tiktoken.encoding_for_model(model_name)
    except KeyError:
<<<<<<< HEAD
        # logger.info("Warning: model not found. Using cl100k_base encoding.")
=======
        # print("Warning: model not found. Using cl100k_base encoding.")
>>>>>>> bc1f253 (changes for embedding service)
        encoding = tiktoken.get_encoding("cl100k_base")
    return encoding 

def num_tokens_from_string(string: str, model_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding =   get_encoder_for_model(model_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens
 

def compare_encodings(example_string: str) -> None:
    """Prints a comparison of three string encodings."""
    # print the example string
    print(f'\nExample string: "{example_string}"')
    # for each encoding, print the # of tokens, the token integers, and the token bytes
    for encoding_name in ["r50k_base", "p50k_base", "cl100k_base"]:
        encoding = tiktoken.get_encoding(encoding_name)
        token_integers = encoding.encode(example_string)
        num_tokens = len(token_integers)
        token_bytes = [encoding.decode_single_token_bytes(token) for token in token_integers]
        print()
        print(f"{encoding_name}: {num_tokens} tokens")
        print(f"token integers: {token_integers}")
        print(f"token bytes: {token_bytes}")
        
def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613"):
    """Return the number of tokens used by a list of messages."""
    encoding= get_encoder_for_model(model)
    if model in {
        "gpt-3.5-turbo-0613",
        "gpt-3.5-turbo-16k-0613",
        "gpt-4-0314",
        "gpt-4-32k-0314",
        "gpt-4-0613",
        "gpt-4-32k-0613",
        }:
        tokens_per_message = 3
        tokens_per_name = 1
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif "gpt-3.5-turbo" in model:
        print("Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0613.")
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613")
    elif "gpt-4" in model:
        print("Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613.")
        return num_tokens_from_messages(messages, model="gpt-4-0613")
    else:
        raise NotImplementedError(
            f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens."""
        )
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens

