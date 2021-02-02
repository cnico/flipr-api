# -*- coding: utf-8 -*-
"""Client for the Flipr REST API."""
from typing import List

from .model import PoolMeasure
from .session import FliprClientSession

# TODO: not all API of Flipr servers methods implemented


class FliprAPIRestClient:
    """Proxy to the Flipr REST API."""

    def __init__(self, username: str, password: str) -> None:
        """Initialize the API and authenticate so we can make requests.

        Args:
            username: string containing your flipr's app username
            password: string containing your flipr's app password
        """
        self.session = FliprClientSession(username, password)

    #
    # search for flipr ids. Generally not useful since flipr ID is to
    # be known by the user.
    #
    def search_flipr_ids(self) -> List[str]:
        """Search the flipr IDs.

        Returns:
            A list of flipr ids registered to the user.
        """
        # Send the API resuest
        resp = self.session.rest_request("GET", "modules")
        # print("Réponse brute de GET /modules : " + str(resp.json()))

        json_list = resp.json()

        if len(json_list) == 0:
            # print("No Flipr found")
            return []

        results = [str(item["Serial"]) for item in json_list]
        return results

    def get_pool_measure_latest(self, flipr_id: str) -> PoolMeasure:
        """Retrieve most recents measure for the given flipr ID.

        Args:
            flipr_id: string containing flipr's id to measure

        Returns:
            A PoolMeasure object that holds the datas.
        """
        resp = self.session.rest_request("GET", f"modules/{flipr_id}/survey/last")
        # print("Réponse brute de get_pool_latest_values : " + str(resp.json()))

        return PoolMeasure(resp.json())
