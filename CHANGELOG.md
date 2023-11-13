# Changelog

All notable changes to this project will be documented in this file. See [standard-version](https://github.com/conventional-changelog/standard-version) for commit guidelines.

## [Unreleased](https://github.com/dotenv-org/python-dotenv-vault/compare/v0.5.1...master)

## 0.6.4

### Changed

- Bump Cryptography above 41.0.3 to resolve [#19](https://github.com/dotenv-org/python-dotenv-vault/issues/19) (High severity [CVE-2023-38325](https://nvd.nist.gov/vuln/detail/CVE-2023-38325))

## 0.6.3

### Changed

- Fixed a bug where it was looking up .env instead of .env.vault [#18](https://github.com/dotenv-org/python-dotenv-vault/pull/18)

## 0.6.2

### Changed

- Look for .env.vault file at same location as .env file. Finds .env file anywhere in app (just like original python lib) [#13](https://github.com/dotenv-org/python-dotenv-vault/pull/13)

## 0.6.1

### Changed

- Fix fallback issue with gunicorn not respecting the current working directory when attempting to call `find_dotenv`. [#17](https://github.com/dotenv-org/python-dotenv-vault/pull/17)

## 0.6.0

### Changed

- Fix environment variable load [#12](https://github.com/dotenv-org/python-dotenv-vault/pull/12)

## 0.5.1

### Changed

- Fix error reference [#10](https://github.com/dotenv-org/python-dotenv-vault/pull/10)

## 0.5.0

### Added

- Reorganise and simplify code
- Make API correspond more closely to `python-dotenv`
- Improve error handling
- Add tests and CI
- Upgrade to `build` for release build
 
## 0.4.1

### Added

- expand cryptography library version range for better support

## 0.4.0

### Added

- Added feature to allow custom .env.vault path

## 0.3.0

### Added

- Added backward compatibility python version 3.7+

## 0.2.0

### Added

- Added comma separated capability to `DOTENV_KEY`. Add multiple keys to your DOTENV_KEY for use with decryption. Separate with a comma.

## 0.1.1

### Added

- Added support for handling any environment

## 0.1.0

### Added

- Added README and CHANGELOG

## 0.0.9

### Added

- Decrypting .env.vault file when `DOTENV_KEY` is set.

## 0.0.8 and prior

Please see commit history.
