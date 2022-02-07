# Miniflux Block

A simple Python script to connect to a Miniflux instance via the [API](https://miniflux.app/docs/api.html) and set to "read" any feed entries that match words or phrases in a blocklist. It aims to be an effective way to cut 99% of the endless stream of utter rubbish some feeds contain, retaining the 1% I actually want to know about.

Miniflux's own solution to this problem, and other solutions I have found allow you to specify a blocklist on a per feed basis, which is annoying to maintain. This script allows you to set _one_ blocklist to apply to _all_ feeds instead.

## Usage

Run the script at regular intervals via a cron job. I have it running every 5 minutes on my home server.

```sh
*/5 * * * * cd miniflux-block/ && /usr/bin/python3 miniflux-block/main.py
```

## Configuration File

You must create a file named `config.yml` which contains the key/values below. A commented example file named `config_template.yml` is also provided in the repository.

```yaml
miniflux_api_token: <api-token-value>
miniflux_base_url: https://<path-to-miniflux-instance>
miniflux_entries_limit: <max-number-of-entries> # Default is 100. Set to something high like 10000.
log_path: <path-to-log-directory>
blocklist_regex:
  - \$\d+
  - \b(\% off)\b
  - \b(\d+ best)\b
  - \b(accessories)\b
  - \b(app store)\b
  - \b(best deals)\b
```

## Blocklist

You can supply a list of regular expressions that you want the script to "mark as read" to the `blocklist_regex` list in `config.yml`. 

## Logging

When the script finds a match it will output a log entry to a file in the same directory named `blocked.log` as below.

```log
2022-01-29 16:01:02 - [INFO] - 7749 - 2022-01-28T16:16:00Z - Slashdot - Matched 'apple' - Samsung Led Smartphone Shipments For 2021, Beating Out Apple
2022-01-29 16:01:02 - [INFO] - 7781 - 2022-01-28T19:19:00Z - Slashdot - Matched 'apple' - Apple Finally Removing Python 2 In macOS 12.3
```

