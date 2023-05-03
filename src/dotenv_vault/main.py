from __future__ import annotations

from base64 import b64decode
import io
import os
from typing import (IO, Optional, Union)
from urllib.parse import urlparse, parse_qsl

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidTag
import dotenv.main as dotenv


def load_dotenv(
    dotenv_path: Union[str, os.PathLike, None] = None,
    stream: Optional[IO[str]] = None,
    verbose: bool = False,
    override: bool = False,
    interpolate: bool = True,
    encoding: Optional[str] = "utf-8",
) -> bool:
    """This function will read your encrypted env file and load it
    into the environment for this process.

    Call this function as close as possible to the start of your
    program (ideally in main).

    If the `DOTENV_KEY` environment variable is set, `load_dotenv`
    will load encrypted environment settings from the `.env.vault`
    file in the current path.

    If the `DOTENV_KEY` environment variable is not set, `load_dotenv`
    falls back to the behavior of the python-dotenv library, loading a
    specified (unencrypted) environment file.

    Other parameters to `load_dotenv` are passed througg to the
    python-dotenv loader. In particular, whether `load_dotenv`
    overrides existing environment settings or not is determined by
    the `override` flag.

    """
    if "DOTENV_KEY" in os.environ:
        vault_stream = parse_vault(open(".env.vault"))
        return dotenv.load_dotenv(
            dotenv_path=".env.vault",
            stream=vault_stream,
            verbose=verbose,
            override=override,
            interpolate=interpolate
        )
    else:
        return dotenv.load_dotenv(
            dotenv_path=dotenv_path,
            stream=stream, 
            verbose=verbose, 
            override=override, 
            interpolate=interpolate, 
            encoding=encoding
        )


class DotEnvVaultError(Exception):
    pass


KEY_LENGTH = 64


def parse_vault(vault_stream: io.IOBase) -> io.StringIO:
    """Parse information from DOTENV_KEY, and decrypt vault.
    """
    dotenv_key = os.environ.get("DOTENV_KEY")
    if dotenv_key is None:
        raise DotEnvVaultError("NOT_FOUND_DOTENV_KEY: Cannot find ENV['DOTENV_KEY']")

    # Use the python-dotenv library to read the .env.vault file.
    vault = dotenv.DotEnv(dotenv_path=".env.vault", stream=vault_stream)

    # Extract segments from the DOTENV_KEY environment variable one by
    # one and retrieve the corresponding ciphertext from the vault
    # data.
    keys = []
    for dotenv_key_entry in [i.strip() for i in dotenv_key.split(',')]:
        key, environment_key = parse_key(dotenv_key_entry)

        ciphertext = vault.dict().get(environment_key)

        if not ciphertext:
            raise DotEnvVaultError(f"NOT_FOUND_DOTENV_ENVIRONMENT: Cannot locate environment {environment_key} in your .env.vault file. Run 'npx dotenv-vault build' to include it.")

        keys.append({
            'encrypted_key': key,
            'ciphertext': ciphertext
        })

    # Try decrypting environments one-by-one in the order they appear
    # in the DOTENV_KEY environment variable.
    decrypted = _key_rotation(keys=keys)

    # Return the decrypted data as a text stream that we can pass to
    # the python-dotenv library.
    return io.StringIO(decrypted.decode('utf-8'))


def parse_key(dotenv_key):
    # Parse a single segment of the DOTENV_KEY environment variable.
    # These segments are in the form of URIs (see
    # https://www.dotenv.org/docs/security/dotenv-key).
    uri = urlparse(dotenv_key)
    
    # The 64-character encryption key is stored in the password field
    # of the URI, possibly with a prefix.
    key = uri.password
    if len(key) < KEY_LENGTH: 
        raise DotEnvVault('INVALID_DOTENV_KEY: Key part must be 64 characters long (or more)')
        
    # The environment is provided in the URI's query parameters.
    params = dict(parse_qsl(uri.query))
    vault_environment = params.get('environment')
    if not vault_environment:
        raise DotEnvVaultError('INVALID_DOTENV_KEY: Missing environment part')

    # Form the key used to store the ciphertext for this environment's
    # settings in the .env.vault file.
    environment_key = f'DOTENV_VAULT_{vault_environment.upper()}'

    return key, environment_key


def _decrypt(ciphertext: str, key: str) -> bytes:
    """decrypt method will decrypt via AES-GCM 
    return: decrypted keys in bytes
    """
    # Remove any prefix from the encryption key (at this point, we
    # know that the key is at least 64 characters in length) and set
    # up the AES cipher.
    aesgcm = AESGCM(bytes.fromhex(key[-KEY_LENGTH:]))

    # Decrypt the ciphertext: this is base64-encoded in the .env.vault
    # file, and the first 12 bytes of the decoded data are used as the
    # AES nonce value.
    ciphertext = b64decode(ciphertext)
    return aesgcm.decrypt(ciphertext[:12], ciphertext[12:], b'')


def _key_rotation(keys: list[dict]) -> str:
    """Iterate through list of keys to check for correct one.
    """
    for k in keys:
        try:
            return _decrypt(ciphertext=k['ciphertext'], key=k['encrypted_key'])
        except InvalidTag:
            continue
    raise DotEnvVaultError('INVALID_DOTENV_KEY: Key must be valid.')
        