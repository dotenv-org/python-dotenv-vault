# python-dotenv-vault

<img src="https://raw.githubusercontent.com/motdotla/dotenv/master/dotenv.svg" alt="dotenv-vault" align="right" width="200" />

[![PyPI version](https://badge.fury.io/py/python-dotenv-vault.svg)](http://badge.fury.io/py/python-dotenv-vault)

Extends the proven & trusted foundation of [python-dotenv](https://github.com/theskumar/python-dotenv), with a `.env.vault` file.

The extended standard lets you sync your `.env` files – quickly & securely. Stop sharing them over insecure channels like Slack and email, and never lose an important `.env` file again.

## Installation

```shell
pip install python-dotenv-vault
```

As early as possible in your application bootstrap process, load .env:

```python
from dotenv_vault import load_dotenv

load_dotenv()  # take environment variables from .env.

# Code of your application, which uses environment variables (e.g. from `os.environ` or
# `os.getenv`) as if they came from the actual environment.
```

## Usage

### `.env`

Basic usage works just like [python-dotenv](https://github.com/theskumar/python-dotenv).

Add your application configuration to your `.env` file in the root of your project:

```shell
S3_BUCKET=YOURS3BUCKET
SECRET_KEY=YOURSECRETKEYGOESHERE
```

When your application loads, these variables will be available in `os.environ` or `os.getenv`:

```python
s3_bucket = os.getenv("S3_BUCKET")
print(s3_bucket)
```

### `.env.vault`

The `.env.vault` extends `.env`. It facilitates syncing your .env file across machines, team members, and environments.

Usage is similar to git. In the same directory as your `.env` file, run the command:

```shell
$ npx dotenv-vault new
```

Follow those instructions and then run:

```shell
$ npx dotenv-vault login
```

Then run push and pull:

```shell
$ npx dotenv-vault push
$ npx dotenv-vault pull
```

That's it!

You just synced your `.env` file. Commit your `.env.vault` file to code, and tell your teammates to run `npx dotenv-vault pull`.

[Learn more](https://www.dotenv.org/docs/tutorials/sync)

## Multiple Environments

Run the command:

```shell
$ npx dotenv-vault open production
```

It will open up an interface to manage your production environment variables.

[Learn more](https://www.dotenv.org/docs/tutorials/environments)

## Integrate Anywhere™

Build your encrypted `.env.vault`:

```shell
$ npx dotenv-vault build
```

Safely commit and push your changes:

```shell
$ git commit -am "Updated .env.vault"
$ git push
```

Obtain your `DOTENV_KEY`:

```shell
$ npx dotenv-vault keys
```

Set `DOTENV_KEY` on your infrastructure. For example, on Heroku:

```shell
$ heroku config:set DOTENV_KEY="dotenv://:key_1234@dotenv.org/vault/.env.vault?environment=production"
```

All set! When your app boots, it will recognize a `DOTENV_KEY` is set, decrypt the `.env.vault` file, and load the variables to `ENV`.

Made a change to your production envs? Run `npx dotenv-vault build`, commit that safely to code, and deploy. It's simple and safe like that.

[Learn more](https://www.dotenv.org/docs/tutorials/integrations)

## Dotenv.org

You need a [Dotenv Account](https://dotenv.org) to use Dotenv Vault. It is free to use with premium features.

![](https://api.checklyhq.com/v1/badges/checks/c2fee99a-38e7-414e-89b8-9766ceeb1927?style=flat&theme=dark&responseTime=true)
![](https://api.checklyhq.com/v1/badges/checks/4f557967-1ed1-486a-b762-39a63781d752?style=flat&theme=dark&responseTime=true)
<br>
![](https://api.checklyhq.com/v1/badges/checks/804eb6fa-6599-4688-a649-7ff3c39a64b9?style=flat&theme=dark&responseTime=true)
![](https://api.checklyhq.com/v1/badges/checks/6a94504e-e936-4f07-bc0b-e08fee2734b3?style=flat&theme=dark&responseTime=true)
<br>
![](https://api.checklyhq.com/v1/badges/checks/06ac4f4e-3e0e-4501-9987-580b4d2a6b06?style=flat&theme=dark&responseTime=true)
![](https://api.checklyhq.com/v1/badges/checks/0ffc1e55-7ef0-4c2c-8acc-b6311871f41c?style=flat&theme=dark&responseTime=true)

Visit [health.dotenv.org](https://health.dotenv.org) for more information.

## FAQ

#### What happens if `DOTENV_KEY` is not set?

Dotenv Vault gracefully falls back to [dotenv](https://github.com/bkeepers/dotenv) when `DOTENV_KEY` is not set. This is the default for development so that you can focus on editing your `.env` file and save the `build` command until you are ready to deploy those environment variables changes.

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
