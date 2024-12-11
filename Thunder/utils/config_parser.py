# Thunder/utils/config_parser.py

import os
from typing import Dict, Optional
from Thunder.utils.logger import logger


class TokenParser:
    """
    A class to parse multiple bot tokens from environment variables.
    """

    def __init__(self, config_file: Optional[str] = None, prefix: str = "MULTI_TOKEN"):
    self.tokens: Dict[int, str] = {}
    self.config_file = config_file
    self.prefix = prefix


   def parse_from_env(self) -> Dict[int, str]:
    multi_tokens = {
        key: value for key, value in os.environ.items() if key.startswith("MULTI_TOKEN")
    }

    if not multi_tokens:
        logger.error("No MULTI_TOKEN environment variables found.")
        raise ValueError("No MULTI_TOKEN environment variables found.")

    try:
        sorted_tokens = sorted(
            multi_tokens.items(),
            key=lambda item: int(''.join(filter(str.isdigit, item[0])) or 0)
        )
    except ValueError as e:
        logger.error(f"Error parsing token keys: {e}")
        raise ValueError("Invalid MULTI_TOKEN key format.") from e

    self.tokens = {
        index + 1: token for index, (key, token) in enumerate(sorted_tokens)
    }

    if not self.tokens:
        logger.error("No valid MULTI_TOKEN environment variables found.")
        raise ValueError("No valid MULTI_TOKEN environment variables found.")

    logger.debug(f"Parsed tokens: {self.tokens}")
    return self.tokens
