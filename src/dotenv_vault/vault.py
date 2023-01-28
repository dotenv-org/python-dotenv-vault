from __future__ import annotations

import os
import io

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidTag
from base64 import b64decode
from urllib.parse import urlparse, parse_qsl
from dotenv.main import DotEnv, find_dotenv


class DotEnvVaultError(Exception):
    pass


class DotEnvVault(): #vault stuff
    def __init__(self) -> None:
        self.dotenv_key = os.environ.get('DOTENV_KEY')
        

    def parsed_vault(self, dotenv_path: str) -> bytes:
        """
        Parse information from DOTENV_KEY, and decrypt vault key.
        """
        if self.dotenv_key is None: raise DotEnvVaultError("NOT_FOUND_DOTENV_KEY: Cannot find ENV['DOTENV_KEY']")

        # if dotenv_path is not present, then it will try to find default .env.vault file
        env_vault_path = dotenv_path if dotenv_path else find_dotenv(filename='.env.vault', usecwd=True)

        if not env_vault_path:
            raise DotEnvVaultError("ENV_VAULT_NOT_FOUND: .env.vault is not present.")

        keys = []
        dotenv_keys = [i.strip() for i in self.dotenv_key.split(',')]
        for _key in dotenv_keys:    
            # parse DOTENV_KEY, format is a URI
            uri = urlparse(_key)
            # Get encrypted key
            key = uri.password
            # Get environment from query params.
            params = dict(parse_qsl(uri.query))
            vault_environment = params.get('environment')

            if not vault_environment:
                raise DotEnvVaultError('INVALID_DOTENV_KEY: Missing environment part')

            # Getting ciphertext from correct environment in .env.vault
            environment_key = f'DOTENV_VAULT_{vault_environment.upper()}'

            # use python-dotenv library class.
            dotenv = DotEnv(dotenv_path=env_vault_path)
            ciphertext = dotenv.dict().get(environment_key)

            if not ciphertext:
                raise DotEnvVaultError(f"NOT_FOUND_DOTENV_ENVIRONMENT: Cannot locate environment {environment_key} in your .env.vault file. Run 'npx dotenv-vault build' to include it.")

            keys.append({
                'encrypted_key': key,
                'ciphertext': ciphertext
            })

        decrypted = self._key_rotation(keys=keys)
        return self._to_text_stream(decrypted)
            

    def _decrypt(self, ciphertext: str, key: str) -> bytes:
        """
        decrypt method will decrypt via AES-GCM 
        return: decrypted keys in bytes
        """
        _key = key[4:]
        if len(_key) < 64: 
            raise DotEnvVault('INVALID_DOTENV_KEY: Key part must be 64 characters long (or more)')

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

    def _key_rotation(self, keys: list[dict]) -> str:
        """
        Iterate through list of keys to check for correct one.
        """
        _len = len(keys)
        for i, k in enumerate(keys):
            try:
                return self._decrypt(ciphertext=k['ciphertext'], key=k['encrypted_key'])
            except InvalidTag:
                if i + 1 >= _len: # exhaust all keys
                    raise DotEnvVaultError('INVALID_DOTENV_KEY: Key must be valid.')
                else:
                    continue
