"""
Mark Miniflux RSS entries as read if they match word/phrase in blocklist.
"""

import re
import logging
import json
import requests
import sys
import yaml


def main():

    """
    Main functionality
    """

    # Configuration file:
    with open("config.yml", "r", encoding="utf-8") as config:

        # Load config file:
        config_file = yaml.safe_load(config)

    # API Configuration:
    auth_token = config_file["miniflux_api_token"]
    base_url = config_file["miniflux_base_url"]
    api_url = "/v1"
    api_entries = "/entries"
    api_entries_params = {
        "status": "unread",
        "limit": config_file["miniflux_entries_limit"],
        "order": "id",
        "direction": "asc",
    }
    api_endpoint = base_url + api_url + api_entries

    # API call:
    entries = requests.get(
        api_endpoint,
        params=api_entries_params,
        headers={"X-Auth-Token": auth_token},
    )

    # Load config file:
    for entry in entries.json()["entries"]:

        # Entry values:
        entry_title = entry["title"]
        entry_id = entry["id"]
        entry_published_at = entry["published_at"]
        entry_feed_title = entry["feed"]["title"]

        for word in config_file["blocklist_regex"]:

            # Check against title only:
            blocklist_match = re.search(rf"{word}", entry_title, re.IGNORECASE)

            if blocklist_match:

                # Mark matches entries as read:
                requests.put(
                    api_endpoint,
                    data=json.dumps({"entry_ids": [entry_id], "status": "read"}),
                    headers={
                        "X-Auth-Token": auth_token,
                        "Content-Type": "application/json",
                    },
                )

                # Logging config:
                logging.basicConfig(
                    level=logging.INFO,
                    stream=sys.stdout,
                    format="%(asctime)s - [%(levelname)s] - %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
                )

                # Log output:
                logging.info(
                    "%s - %s - %s - Matched '%s' - %s",
                    entry_id,
                    entry_published_at,
                    entry_feed_title,
                    word,
                    entry_title,
                )


if __name__ == "__main__":
    main()
