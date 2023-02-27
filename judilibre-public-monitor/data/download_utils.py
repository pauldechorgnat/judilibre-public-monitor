import datetime
import logging
import os
import time

import requests
from dotenv import load_dotenv

load_dotenv()

PISTE_API_KEY = os.environ.get("PISTE_API_KEY")
PISTE_API_URL = os.environ.get("PISTE_API_URL")

PISTE_API_HEADERS = {"KeyId": PISTE_API_KEY}

DEFAULT_KEYS = [
    "id",
    "source",
    "jurisdiction",
    "chamber",
    "number",
    "location",
    "decision_date",
    "update_date",
    "type",
    "nac",
]


def download_data_between_update_dates(
    start_date: datetime.date,
    end_date: datetime.date,
    jurisdiction: str = "cc",
    headers: str = PISTE_API_HEADERS,
    base_url: str = PISTE_API_URL,
    timeout: int = 5,
    mask: list[str] = DEFAULT_KEYS,
):
    params = {
        "date_start": str(start_date),
        "date_end": str(end_date),
        "jurisdiction": jurisdiction,
        "date_type": "update",
        "batch_size": 1_000,
        "batch": 0,
    }

    data = {m: [] for m in mask}
    n_results = 0

    has_next_batch = True

    while has_next_batch:
        response = requests.get(
            url=f"{base_url}/export", headers=headers, params=params
        )

        if response.status_code != 200:
            logging.debug(
                f"Request received a non 200 status code {response.status_code}"
            )
            time.sleep(timeout)
        else:
            response_json = response.json()
            has_next_batch = response_json["next_batch"] is not None

            results = response_json["results"]

            for r in results:
                n_results += 1
                for m in mask:
                    data[m].append(r.get(m))

            params["batch"] += 1

    logging.debug(f"Collected {n_results} decisions from {start_date} to {end_date}")

    return data


def download_specific_document_by_id(
    document_id: str,
    headers: str = PISTE_API_HEADERS,
    base_url: str = PISTE_API_URL,
    mask: list[str] = DEFAULT_KEYS,
):
    response = requests.get(
        url=f"{base_url}/decision", headers=headers, params={"id": document_id}
    )

    if response.status_code == 200:
        result = response.json()

        return {m: result.get(m) for m in mask}

    logging.debug(f"Received status code {response.status_code}")

    return dict()
