# app-store-download-count-badge-maker

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[![PyPI Package version](https://badge.fury.io/py/app-store-download-count-badge-maker.svg)](https://pypi.org/project/app-store-download-count-badge-maker)
[![Python Supported versions](https://img.shields.io/pypi/pyversions/app-store-download-count-badge-maker.svg)](https://pypi.org/project/app-store-download-count-badge-maker)
[![format](https://img.shields.io/pypi/format/app-store-download-count-badge-maker.svg)](https://pypi.org/project/app-store-download-count-badge-maker)
[![implementation](https://img.shields.io/pypi/implementation/app-store-download-count-badge-maker.svg)](https://pypi.org/project/app-store-download-count-badge-maker)
[![LICENSE](https://img.shields.io/pypi/l/app-store-download-count-badge-maker.svg)](https://pypi.org/project/app-store-download-count-badge-maker)


A command-line tool to create badges displaying the number of app downloads from App Store

## Installation

```shell
$ pip install app-store-download-count-badge-maker
```

or

```shell
$ pipx install app-store-download-count-badge-maker
```

## Required

- Python 3.9 or later

## Usage

```shell
$ app-store-download-count-badge-maker generate \
  --config config.yml \
  --output dist
```

By default, the `--config (or -c)` option is set to `config.yml` and the `--output (or -o)` options is set to `dist`.

## Configuration

Create a configuration file in YAML format.  
The recommended name is `config.yml`.

### Configuration Details

The configuration file `config.yml` should contain the following sections:

- `secrets`: This section holds the credentials required to access the App Store Connect API.
  - `private_key`: Path to the private key file (e.g., `private.p8`). The private key must have access **Finance**.
  - `issuer_id`: The issuer ID from App Store Connect.
  - `key_id`: The key ID from App Store Connect.
  - `vendor_number`: The vendor number associated with your App Store account. [View payments and proceeds](https://developer.apple.com/help/app-store-connect/getting-paid/view-payments-and-proceeds)
- `apps`: A list of applications for which you want to create download count badges.
  - `apple_identifier`: The unique identifier for the app in the App Store.
  - `frequency`: The frequency at which you want to generate the badge. Must be one of `DAILY`, `WEEKLY`, `MONTHLY`, `YEARLY`.

### Example Configuration

```yaml
secrets:
  private_key: private.p8
  issuer_id: 12345678-1234-1234-1234-123456789012
  key_id: 12345678
  vendor_number: 12345678
apps:
  - apple_identifier: 1289764391
    frequency: MONTHLY
  - apple_identifier: 1234567890
    frequency: WEEKLY 
```

## License

This software is licensed under the MIT License.
