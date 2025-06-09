from typing import cast

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.pipelines import pipeline

from utils.config import load_config
from utils.constants import Constants
from utils.logger import setup_logger

logger = setup_logger()
config = load_config()


class LanguageModel:
    """Class to create an instance of the configured language model and run inference based
    on prompt received from the Retriever.
    """

    def __init__(self) -> None:
        gen_config = config[Constants.GENERATOR]
        model_key = gen_config[Constants.LM].lower()
        temperature = gen_config[Constants.TEMPERATURE]
        max_tokens = gen_config[Constants.MAX_TOKENS]
        hf_key = gen_config[Constants.HF_KEY]

        self.is_mock = False

        if model_key == "mistral":
            model_id = "mistralai/Mistral-7B-v0.1"
        elif model_key == "phi":
            model_id = "microsoft/phi-2"
        elif model_key == "gpt2":
            model_id = "openai-community/gpt2"
        elif model_key == "mock":
            model_id = "mock"
        else:
            model_id = "openai-community/gpt2"
            logger.warning(f"Unknown LM '{model_key}', falling back to gpt2")

        if model_key == "mock":
            self.is_mock = True
            # Hardcoded summary for mock mode
            self.mock_summary = (
                "Universal Transformers introduce recurrence over depth to improve generalization "
                "in sequence tasks [UT]. We can use different algorithms that involve transforms to solve "
                "a reinforcement problem. [TR]."
            )
            logger.info("Mock model selected: returning hardcoded summary")
            return

        logger.info(f"Loading LM model '{model_id}'")
        self.tokenizer = AutoTokenizer.from_pretrained(model_id, token=hf_key)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_id,
            device_map="auto"
        )
        # Create a text-generation pipeline
        self.generator = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            max_new_tokens=max_tokens,
            do_sample=True,
            temperature=temperature
        )

    def generate(self, prompt: str) -> str:
        if self.is_mock:
            return self.mock_summary

        outputs = self.generator(prompt)
        if isinstance(outputs, list) and "generated_text" in outputs[0]:
            return str(outputs[0]["generated_text"])
        else:
            logger.error(
                "Unexpected output format from language model pipeline.")
            return ""
