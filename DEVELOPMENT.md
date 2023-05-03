# DEVELOPMENT

## Publishing

1. Tag master branch `git tag v0.0.0` and `git push --tags`
2. Visit [https://github.com/dotenv-org/python-dotenv-vault/tags](https://github.com/dotenv-org/python-dotenv-vault/tags)
3. Click '...' > 'Create Release' next to the new tag
4. Put changelog details in body and name release by the same tag `v0.0.0`
5. Click 'Publish release'
6. `.github/workflows/python-publish.yml` will take care of publishing the latest version


