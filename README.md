# app-store-download-count-badge-maker

[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

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

- Python 3.10 or later

## Features

- Generate badges for the App Store download count.
  - `app-store-download-count-badge-maker generate` command.
- Generate index.html from config.yml.
  - `app-store-download-count-badge-maker make-index` command.

## Usage

```shell
$ app-store-download-count-badge-maker generate \
  --config config.yml \
  --output dist
```

By default, the `--config (or -c)` option is set to `config.yml` and the `--output (or -o)` options is set to `dist`.

> [!NOTE]
> The count is based on 3 days prior to the execution date.

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
  - `badge_style` (Optional): The style of the badge. Must be one of `flat` (default), `flat-square`, `plastic`, `for-the-badge`, `social`.

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
    badge_style: flat-square
```

## Badge Creation :sparkles:

This tool uses [Shields.io](https://shields.io/) to create badges displaying the number of app downloads from App Store.

### Examples

|  Frequency  | Badge Style                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
|:-----------:|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|   YEARLY    | ![year-flat](https://img.shields.io/badge/download-1.2k%2Fyear-brightgreen?style=flat&cacheSeconds=31536000) ![year-flat-square](https://img.shields.io/badge/download-123%2Fyear-green?style=flat-square&cacheSeconds=31536000) ![year-plastic](https://img.shields.io/badge/download-99%2Fyear-yellowgreen?style=plastic&cacheSeconds=31536000) ![year-for-the-badge](https://img.shields.io/badge/download-9%2Fyear-yellow?style=for-the-badge&cacheSeconds=31536000) ![year-social](https://img.shields.io/badge/download-0%2Fyear-yellow?style=social&cacheSeconds=31536000)           |
|   MONTHLY   | ![month-flat](https://img.shields.io/badge/download-1.2k%2Fmonth-brightgreen?style=flat&cacheSeconds=31536000) ![month-flat-square](https://img.shields.io/badge/download-123%2Fmonth-green?style=flat-square&cacheSeconds=31536000) ![month-plastic](https://img.shields.io/badge/download-99%2Fmonth-yellowgreen?style=plastic&cacheSeconds=31536000) ![month-for-the-badge](https://img.shields.io/badge/download-9%2Fmonth-yellow?style=for-the-badge&cacheSeconds=31536000) ![month-social](https://img.shields.io/badge/download-0%2Fmonth-yellow?style=social&cacheSeconds=31536000) |
|   WEEKLY    | ![week-flat](https://img.shields.io/badge/download-1.2k%2Fweek-brightgreen?style=flat&cacheSeconds=31536000) ![week-flat-square](https://img.shields.io/badge/download-123%2Fweek-green?style=flat-square&cacheSeconds=31536000) ![week-plastic](https://img.shields.io/badge/download-99%2Fweek-yellowgreen?style=plastic&cacheSeconds=31536000) ![week-for-the-badge](https://img.shields.io/badge/download-9%2Fweek-yellow?style=for-the-badge&cacheSeconds=31536000) ![week-social](https://img.shields.io/badge/download-0%2Fweek-yellow?style=social&cacheSeconds=31536000)           |
|    DAILY    | ![day-flat](https://img.shields.io/badge/download-1.2k%2Fday-brightgreen?style=flat&cacheSeconds=31536000) ![day-flat-square](https://img.shields.io/badge/download-123%2Fday-green?style=flat-square&cacheSeconds=31536000) ![day-plastic](https://img.shields.io/badge/download-99%2Fday-yellowgreen?style=plastic&cacheSeconds=31536000) ![day-for-the-badge](https://img.shields.io/badge/download-9%2Fday-yellow?style=for-the-badge&cacheSeconds=31536000) ![day-social](https://img.shields.io/badge/download-0%2Fday-yellow?style=social&cacheSeconds=31536000)                     |

## Projects using `app-store-download-count-badge-maker`

- [nnsnodnb/self-app-store-download-count-badges](https://github.com/nnsnodnb/self-app-store-download-count-badges)

## License

This software is licensed under the MIT License.
