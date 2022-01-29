# Miniflux Block

A simple enough Python script to connect to a Miniflux instance via the API and set to "read" any feed entries that match words or phrases in a blocklist.

## Usage

Run the script at regular intervals via a cron job. 

## Configuration File

You must create a file named `config.yml`, which should contain values for the following keys.

**Note:** The script is currently set to use a custom certificate authority as I host Miniflux locally. To use the script without a custom CA, remove all references to `verify=custom_ca_path` (there should currently be two lines).

```yaml
miniflux_api_token: <api-token-value>
miniflux_base_url: https://<path-to-miniflux-instance>
custom_ca_path: <path-to-custom-ca-file>
blocklist:
  - words
  - phrases to block
```

## Regular Expression Matching

You can supply a list of words or phrases as items to the `blocklist` list in `config.yml`. 

Currently, matches are all case insensitive, and use the below regex, which does the trick for me.

```python
(\b{word}\b)
```

## Logging

When the script finds a match it will output a log entry to a file in the same directory named `blocked.log`.

