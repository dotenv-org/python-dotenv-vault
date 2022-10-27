
import logging
import os
import sys
import io

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from base64 import b64decode
from urllib.parse import urlparse, parse_qsl

from dotenv.main import DotEnv, find_dotenv, load_dotenv


logging.basicConfig(level = logging.INFO)

logger = logging.getLogger(__name__)


class DotEnvVaultError(Exception):
    pass


class DotEnvVault(): #vault stuff
    def __init__(self) -> None:
        logger.info('initializing DotEnvVault')
        self.dotenv_key = os.environ.get('DOTENV_KEY')
        

    def parsed_vault(self) -> bytes:
        """
        Parse information from DOTENV_KEY, and decrypt vault key.
        """
        if self.dotenv_key is None: raise DotEnvVaultError("NOT_FOUND_DOTENV_KEY: Cannot find ENV['DOTENV_KEY']")
            
        # .env.vault needs to be present.
        env_vault_path = find_dotenv(filename='.env.vault', usecwd=True)
        if env_vault_path == '':
            raise DotEnvVaultError("ENV_VAULT_NOT_FOUND: .env.vault is not present.")

        # parse DOTENV_KEY, format is a URI
        uri = urlparse(self.dotenv_key)
        # Get encrypted key
        key = uri.password
        # Get environment from query params.
        params = dict(parse_qsl(uri.query))
        vault_environment = params.get('environment').upper()

        if vault_environment is None or vault_environment not in ['PRODUCTION', 'DEVELOPMENT', 'CI', 'STAGING']:
            raise DotEnvVaultError('Incorrect Vault Environment.')

        # Getting ciphertext from correct environment in .env.vault
        environment_key = f'DOTENV_VAULT_{vault_environment}'
        logging.info(f'Getting key from {environment_key}.')

        # use python-dotenv library class.
        dotenv = DotEnv(dotenv_path=env_vault_path)
        ciphertext = dotenv.dict().get(environment_key)

        if not ciphertext:
            raise DotEnvVaultError('Environment Key is not found. Run `npx dotenv-vault build`.')

        decrypted = self._decrypt(ciphertext=ciphertext, key=key)
        return self._to_text_stream(decrypted)


    def _decrypt(self, ciphertext: str, key: str) -> bytes:
        """
        decrypt method will decrypt via AES-GCM 
        return: decrypted keys in bytes
        """
        _key = key[4:]
        if len(_key) < 64: raise DotEnvVault('INVALID_DOTENV_KEY: Key part must be 64 characters long (or more)')

        _key = bytes.fromhex(_key)
        ciphertext = b64decode(ciphertext)

        aesgcm = AESGCM(_key)
        return aesgcm.decrypt(ciphertext[:12], ciphertext[12:], b'')

    def _to_text_stream(self, decrypted_obj: bytes) -> io.StringIO:
        """
        convert decrypted object (in bytes) to io.StringIO format.
        Python-dotenv is expecting stream to be text stream (such as `io.StringIO`).
        return: io.StringIO
        """
        decoded_str = decrypted_obj.decode('utf-8')
        return io.StringIO(decoded_str)