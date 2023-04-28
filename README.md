# python-dotenv-vault [![PyPI version](https://badge.fury.io/py/python-dotenv-vault.svg)](http://badge.fury.io/py/python-dotenv-vault)

<img src="https://raw.githubusercontent.com/motdotla/dotenv/master/dotenv.svg" alt="dotenv-vault" align="right" width="200" />

Extends the proven & trusted foundation of [python-dotenv](https://github.com/theskumar/python-dotenv), with a `.env.vault` file.

The extended standard lets you load encrypted secrets from your `.env.vault` file in production (and other) environments. Brought to you by the same people that pioneered [dotenv-nodejs](https://github.com/motdotla/dotenv).

* [🌱 Install](#-install)
* [🏗️ Usage (.env)](#%EF%B8%8F-usage)
* [🚀 Deploying (.env.vault) 🆕](#-deploying)
* [🌴 Multiple Environments](#-manage-multiple-environments)
* [❓ FAQ](#-faq)
* [⏱️ Changelog](./CHANGELOG.md)

## 🌱 Install

```shell
pip install python-dotenv-vault
```

## 🏗️ Usage

Development usage works just like [python-dotenv](https://github.com/theskumar/python-dotenv).

Add your application configuration to your `.env` file in the root of your project:

```shell
S3_BUCKET=YOURS3BUCKET
SECRET_KEY=YOURSECRETKEYGOESHERE
```

As early as possible in your application bootstrap process, load .env:

```python
from dotenv_vault import load_dotenv

load_dotenv()  # take environment variables from .env.

# Code of your application, which uses environment variables (e.g. from `os.environ` or
# `os.getenv`) as if they came from the actual environment.
```

When your application loads, these variables will be available in `os.environ` or `os.getenv`:

```python
s3_bucket = os.getenv("S3_BUCKET")
print(s3_bucket)
```

## 🚀 Deploying

Encrypt your environment variables by doing:

```shell
npx dotenv-vault local build
```

This will create an encrypted `.env.vault` file along with a `.env.keys` file containing the encryption keys. Set the `DOTENV_KEY` environment variable by copying and pasting the key value from the `.env.keys` file onto your server or cloud provider. For example in heroku:

```shell
heroku config:set DOTENV_KEY=<key string from .env.keys>
```

Commit your .env.vault file safely to code and deploy. Your .env.vault fill be decrypted on boot, its environment variables injected, and your app work as expected.

Note that when the `DOTENV_KEY` environment variable is set, environment settings will *always* be loaded from the `.env.vault` file in the project root. For development use, you can leave the `DOTENV_KEY` environment variable unset and fall back on the `dotenv` behaviour of loading from `.env` or a specified set of files (see [here in the `dotenv` README](https://github.com/bkeepers/dotenv#usage) for the details).

## 🌴 Manage Multiple Environments

You have two options for managing multiple environments - locally managed or vault managed - both use [dotenv-vault](https://github.com/dotenv-org/dotenv-vault).

Locally managed never makes a remote API call. It is completely managed on your machine. Vault managed adds conveniences like backing up your .env file, secure sharing across your team, access permissions, and version history. Choose what works best for you.

#### 💻 Locally Managed

Create a `.env.production` file in the root of your project and put your production values there.

```shell
# .env.production
S3_BUCKET="PRODUCTION_S3BUCKET"
SECRET_KEY="PRODUCTION_SECRETKEYGOESHERE"
```

Rebuild your `.env.vault` file.

```shell
npx dotenv-vault local build
```

View your `.env.keys` file. There is a production `DOTENV_KEY` that pairs with the `DOTENV_VAULT_PRODUCTION` cipher in your `.env.vault` file.

Set the production `DOTENV_KEY` on your server, recommit your `.env.vault` file to code, and deploy. That's it!

Your .env.vault fill be decrypted on boot, its production environment variables injected, and your app work as expected.

#### 🔐 Vault Managed

Sync your .env file. Run the push command and follow the instructions. [learn more](/docs/sync/quickstart)

```
$ npx dotenv-vault push
```

Manage multiple environments with the included UI. [learn more](/docs/tutorials/environments)

```
$ npx dotenv-vault open
```

Build your `.env.vault` file with multiple environments.

```
$ npx dotenv-vault build
```

Access your `DOTENV_KEY`.

```
$ npx dotenv-vault keys
```

Set the production `DOTENV_KEY` on your server, recommit your `.env.vault` file to code, and deploy. That's it!

## ❓ FAQ

#### What happens if `DOTENV_KEY` is not set?

Dotenv Vault gracefully falls back to [python-dotenv](https://github.com/theskumar/python-dotenv) when `DOTENV_KEY` is not set. This is the default for development so that you can focus on editing your `.env` file and save the `build` command until you are ready to deploy those environment variables changes.

#### Should I commit my `.env` file?

No. We **strongly** recommend against committing your `.env` file to version control. It should only include environment-specific values such as database passwords or API keys. Your production database should have a different password than your development database.

#### Should I commit my `.env.vault` file?

Yes. It is safe and recommended to do so. It contains your encrypted envs, and your vault identifier.

#### Can I share the `DOTENV_KEY`?

No. It is the key that unlocks your encrypted environment variables. Be very careful who you share this key with. Do not let it leak.

## Contributing

1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Added some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create new Pull Request

## Changelog

See [CHANGELOG.md](CHANGELOG.md)

## License

MIT
