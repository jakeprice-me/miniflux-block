# Miniflux Block

A simple enough Python script to connect to a Miniflux instance via the [API](https://miniflux.app/docs/api.html) and set to "read" any feed entries that match words or phrases in a blocklist. 

Miniflux's own solution to this problem, and other solutions I have found allow you to specify a blocklist on a per feed basis, which is annoying to maintain. This script allows you to set one blocklist for all feeds instead.

## Usage

Run the script at regular intervals via a cron job. I have it running every 5 minutes on my home server.

```sh
*/5 * * * * /usr/bin/python3 <path-to-script>
```

## Configuration File

You must create a file named `config.yml`, which should contain values for the following keys.

**Note:** The script is currently set to use a custom certificate authority as I host Miniflux locally. To use the script without a custom CA, remove all references to `verify=custom_ca_path` (there should currently be two lines).

```yaml
miniflux_api_token: <api-token-value>
miniflux_base_url: https://<path-to-miniflux-instance>
custom_ca_path: <path-to-custom-ca-file>
log_path: <path-to-log-directory>
blocklist:
  - lorem
  - ipsum
  - dolor
  - sit amet
```

## Regular Expression Matching

You can supply a list of words or phrases as items to the `blocklist` list in `config.yml`. 

Currently, matches are all case insensitive, and use the below regex, which does the trick for me.

```python
(\b{word}\b)
```

## Logging

When the script finds a match it will output a log entry to a file in the same directory named `blocked.log` as below.

```log
2022-01-29 16:01:02 - [INFO] - 7749 - 2022-01-28T16:16:00Z - Slashdot - Matched 'apple' - Samsung Led Smartphone Shipments For 2021, Beating Out Apple
2022-01-29 16:01:02 - [INFO] - 7781 - 2022-01-28T19:19:00Z - Slashdot - Matched 'apple' - Apple Finally Removing Python 2 In macOS 12.3
```

