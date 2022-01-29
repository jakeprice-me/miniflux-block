import re
import logging
import json
import requests
import yaml
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def main():

    # Configuration file:
    with open("config.yml", "r") as config:

        # Load config file:
        config_file = yaml.safe_load(config)

        # Get config values:
        miniflux_api_token = config_file["miniflux_api_token"]
        miniflux_base_url = config_file["miniflux_base_url"]
        blocklist = config_file["blocklist"]

    # API Configuration:
    auth_token = miniflux_api_token
    base_url = miniflux_base_url
    api_url = "/v1"
    api_entries = "/entries"
    api_entries_params = {"status": "unread", "order": "published_at", "direction": "asc"}
    api_endpoint = base_url + api_url + api_entries

    # API call:
    entries = requests.get(
        api_endpoint,
        params=api_entries_params,
        verify=False,
        headers={"X-Auth-Token": auth_token},
    )

    entries_list = entries.json()["entries"]

    # Load config file:
    for entry in entries_list:

        # Entry values:
        entry_title = entry["title"]
        entry_id = entry["id"]
        entry_published_at = entry["published_at"]
        entry_feed_title = entry["feed"]["title"]

        for word in blocklist:

            # Regex to check:
            blocklist_regex = rf"({word})"

            # Check against title only:
            blocklist_match = re.search(blocklist_regex, entry_title, re.IGNORECASE)

            if blocklist_match:

                # Set entry status to read:
                api_entries_json = {"entry_ids": [entry_id], "status": "read"}

                # Mark matches entries as read:
                read_entries = requests.put(
                    api_endpoint,
                    data=json.dumps(api_entries_json),
                    verify=False,
                    headers={
                        "X-Auth-Token": auth_token,
                        "Content-Type": "application/json",
                    },
                )

                # Logging config:
                logging.basicConfig(
                    level=logging.INFO,
                    format="%(asctime)s - [%(levelname)s] - %(message)s",
                    handlers=[logging.FileHandler("blocked.log"), logging.StreamHandler()],
                    datefmt="%Y-%m-%d %H:%M:%S",
                )

                # Log output:
                logging.info(f"{entry_id} - {entry_published_at} - {entry_feed_title} - Blocked: {word} - {entry_title}")

if __name__=="__main__":
    main()
