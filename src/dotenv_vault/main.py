import os
import logging
from typing import (IO, Optional,Union)
from dotenv.main import load_dotenv as load_dotenv_file

from .vault import DotEnvVault

logging.basicConfig(level = logging.INFO)

logger = logging.getLogger(__name__)


def load_dotenv(
    dotenv_path: Union[str, os.PathLike, None] = None,
    stream: Optional[IO[str]] = None,
    verbose: bool = False,
    override: bool = False,
    interpolate: bool = True,
    encoding: Optional[str] = "utf-8",
) -> bool:
    """
    parameters are the same as python-dotenv library.
    This is to inject the parameters to evironment variables.
    """
    dotenv_vault = DotEnvVault()
    if dotenv_vault.dotenv_key:
        logger.info('Getting .env from vault.')
        vault_stream = dotenv_vault.parsed_vault()
        # we're going to override the .vault to any existing keys in local
        return load_dotenv_file(stream=vault_stream, override=True)
    else:
        logger.info('Getting .env from local.')
        return load_dotenv_file()