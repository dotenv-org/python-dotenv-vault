from io import StringIO
import os
import unittest
from unittest import mock

from dotenv.main import load_dotenv

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

    PARSE_TEST_KEY = "dotenv://:key_ff6456d445b08c289eec891ba1944e3ae09b00b33387d046624214aff27173d5@dotenv.org/vault/.env.vault?environment=production"

    PARSE_TEST_VAULT = """
    DOTENV_VAULT=vlt_993de4634508b7d119adc8010781346341a142250aa1df5a20ad53bf0d9d8992
    DOTENV_VAULT_DEVELOPMENT="BINHFMl8zRRSt5cLMe9BNHDdsH1D5zX45tRrL05WYYbXCuBDsLF2YiAT7VKDdrbk1eg/X5n4FKO76lE1UQ5QTA=="
    DOTENV_VAULT_CI="nWcJP28Z7w16aBuh9sg/zFACTqWcBXgJnykPNDkF7RqjOwESQDFSO5cymC4="
    DOTENV_VAULT_STAGING="uGHOx986lAWGU9s5mN5+b0jl0HAvNj4Mqs/zwN7Bl8UeV+C6hBg5JuKdi2AGGLka5g=="
    DOTENV_VAULT_PRODUCTION="YpDpGGf+eqiOPibziIQQbw4gBW/zfOBR6jow5B1UHYTTu6Kak6xy+qP/vXZWaPp4HOh2/Nu7gRK2CWfrbtk="
    """

    def test_vault_parsing(self):
        old_dotenv_key = os.environ.get("DOTENV_KEY")
        os.environ["DOTENV_KEY"] = self.PARSE_TEST_KEY
        try:
            stream = vault.parse_vault(StringIO(self.PARSE_TEST_VAULT))
            load_dotenv(stream=stream, override=True)
            self.assertEqual(os.environ.get("HELLO"), "Production")
        finally:
            os.unsetenv("DOTENV_KEY")
            if old_dotenv_key:
                os.environ["DOTENV_KEY"] = old_dotenv_key

    @mock.patch("dotenv.main.find_dotenv")
    def test_load_dotenv_vault(self, find_dotenv):
        find_dotenv.return_value = '/some/path/'
        with mock.patch('os.listdir') as mocked_listdir:
            mocked_listdir.return_value = ['.env', '.env.vault', 'some_file']
            path = vault.load_dotenv_vault()
            self.assertEqual(path, '/some/path/.env.vault')

    @mock.patch("dotenv.main.find_dotenv")
    def test_load_dotenv_vault_not_there(self, find_dotenv):
        find_dotenv.return_value = '/some/path/'
        with mock.patch('os.listdir') as mocked_listdir:
            mocked_listdir.return_value = ['.env', 'some_file']
            path = vault.load_dotenv_vault()
            self.assertEqual(path, '/some/path/.env')


class TestLoadDotenv:

    @mock.patch.dict(os.environ, {"DOTENV_KEY": "secret_key"}, clear=True)
    @mock.patch("builtins.open", new_callable=mock.mock_open, read_data="KEY=VALUE")
    @mock.patch("dotenv_vault.main.parse_vault")
    @mock.patch("dotenv_vault.main.load_dotenv_vault")
    @mock.patch("dotenv_vault.main.dotenv.load_dotenv")
    def test_load_encrypted_env(
        self, mock_load_dotenv,
        mock_load_dotenv_vault,
        mock_parse_vault,
        mock_open
    ):
            mock_parse_vault.return_value = "stream_with_decrypted_data"
            mock_load_dotenv_vault.return_value = "this_is_the_valut"
            mock_load_dotenv.return_value = True

            assert vault.load_dotenv() == True
            mock_load_dotenv_vault.assert_called_once()
            mock_parse_vault.assert_called_once()
            mock_open.assert_called_once_with(mock_load_dotenv_vault.return_value)
            mock_load_dotenv.assert_called_once_with(
                stream=mock_parse_vault.return_value, 
                verbose=False, 
                override=True, 
                interpolate=True, 
                encoding="utf-8"
            )

    @mock.patch.dict(os.environ, {"NOT_DOTENV_KEY": "shouldnt_be_detected"}, clear=True)
    @mock.patch("builtins.open", new_callable=mock.mock_open, read_data="KEY=VALUE")
    @mock.patch("dotenv_vault.main.dotenv.find_dotenv")
    @mock.patch("dotenv_vault.main.dotenv.load_dotenv")
    @mock.patch.dict(os.environ, {}, clear=True)
    def test_load_unencrypted_env(self, 
            mock_load_dotenv,
            mock_find_dotenv,
            mock_open
        ):
        mock_find_dotenv.return_value = "path_to_dotenv_file"
        mock_load_dotenv.return_value = True

        assert vault.load_dotenv() == True
        mock_open.assert_called_once_with(mock_find_dotenv.return_value)
        mock_find_dotenv.assert_called_once_with(usecwd=True)
        mock_load_dotenv.assert_called_once_with(
                stream=mock_open.return_value, 
                verbose=False, 
                override=True, 
                interpolate=True, 
                encoding="utf-8"
        )

    @mock.patch.dict(os.environ, {"NOT_DOTENV_KEY": "shouldnt_be_detected"}, clear=True)
    @mock.patch("builtins.open", new_callable=mock.mock_open, read_data="KEY=VALUE")
    @mock.patch("dotenv_vault.main.dotenv.find_dotenv")
    @mock.patch("dotenv_vault.main.dotenv.load_dotenv")
    @mock.patch.dict(os.environ, {}, clear=True)
    def test_load_with_stream_provided(self, 
            mock_load_dotenv,
            mock_find_dotenv,
            mock_open
        ):
        mock_find_dotenv.return_value = "path_to_dotenv_file"
        mock_load_dotenv.return_value = True
        test_stream_value = "test_stream_value"

        assert vault.load_dotenv(stream=test_stream_value) == True
        mock_open.assert_not_called()
        mock_find_dotenv.assert_called_once_with(usecwd=True)
        mock_load_dotenv.assert_called_once_with(
                stream=test_stream_value, 
                verbose=False, 
                override=True, 
                interpolate=True, 
                encoding="utf-8"
        )