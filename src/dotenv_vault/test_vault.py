from io import StringIO
import os
import unittest

from dotenv.main import DotEnv

import dotenv_vault.main as vault

class TestParsing(unittest.TestCase):
    TEST_KEYS = [
        # OK.
        ["dotenv://:key_0dec82bea24ada79a983dcc11b431e28838eae59a07a8f983247c7ca9027a925@dotenv.local/vault/.env.vault?environment=development",
         True, "DOTENV_VAULT_DEVELOPMENT"],

        # Key too short (must be 64 characters + prefix).
        ["dotenv://:key_1234@dotenv.org/vault/.env.vault?environment=production",
         False, "DOTENV_VAULT_PRODUCTION"],

        # Missing key value.
        ["dotenv://dotenv.org/vault/.env.vault?environment=production",
         False, "DOTENV_VAULT_PRODUCTION"],

        # Missing environment.
        ["dotenv://:key_1234@dotenv.org/vault/.env.vault", False, ""]
    ]
    
    def test_key_parsing(self):
        for test in self.TEST_KEYS:
            dotenv_key, should_pass, environment_key_check = test
            old_dotenv_key = os.environ.get("DOTENV_KEY")
            os.environ["DOTENV_KEY"] = dotenv_key
            try:
                key, environment_key = vault.parse_key(dotenv_key)
                self.assertTrue(should_pass)
                self.assertEqual(environment_key, environment_key_check)
            except Exception as exc:
                self.assertFalse(should_pass)
            finally:
                os.unsetenv("DOTENV_KEY")
                if old_dotenv_key:
                    os.environ["DOTENV_KEY"] = old_dotenv_key

    PARSE_TEST_KEY = "dotenv://:key_0dec82bea24ada79a983dcc11b431e28838eae59a07a8f983247c7ca9027a925@dotenv.local/vault/.env.vault?environment=development"

    PARSE_TEST_VAULT = """# .env.vault (generated with npx dotenv-vault local build)
DOTENV_VAULT_DEVELOPMENT="H2A2wOUZU+bjKH3kTpeua9iIhtK/q7/VpAn+LLVNnms+CtQ/cwXqiw=="
"""
                
    def test_vault_parsing(self):
        old_dotenv_key = os.environ.get("DOTENV_KEY")
        os.environ["DOTENV_KEY"] = self.PARSE_TEST_KEY
        try:
            stream = vault.parse_vault(StringIO(self.PARSE_TEST_VAULT))
            dotenv = DotEnv(dotenv_path=".env.vault", stream=stream)
            self.assertEqual(dotenv.dict().get("HELLO"), "world")
        finally:
            os.unsetenv("DOTENV_KEY")
            if old_dotenv_key:
                os.environ["DOTENV_KEY"] = old_dotenv_key
        