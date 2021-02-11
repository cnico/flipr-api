# -*- coding: utf-8 -*-
"""Client for the Flipr REST API."""
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from dateutil.parser import parse

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
        self.username = username
        self.password = password
        self.session: Optional[FliprClientSession] = None

    def _get_session(self) -> FliprClientSession:
        if self.session is None:
            self.session = FliprClientSession(self.username, self.password)
        return self.session

    def search_flipr_ids(self) -> List[str]:
        """Search the flipr IDs.

        Returns:
            A list of flipr ids registered to the user.
        """
        # Send the API resuest
        resp = self._get_session().rest_request("GET", "modules")
        # print("Réponse brute de GET /modules : " + str(resp.json()))

        json_list = resp.json()

        if len(json_list) == 0:
            # print("No Flipr found")
            return []

        results = [str(item["Serial"]) for item in json_list]
        return results

    def get_pool_measure_latest(self, flipr_id: str) -> Dict[str, Any]:
        """Retrieve most recents measure for the given flipr ID.

        Args:
            flipr_id: string containing flipr's id to measure

        Returns:
            A dict whose keys are :
                temperature: A float representing the temperature of the pool.
                ph: A float representing the ph of the pool.
                chlorine: A float representing the chlore of the pool.
                red_ox: A float representing the oxydo reduction level of the pool.
                date_time: The date time when the measure was taken.
                ph_status : Alert status for PH value in : TooLow, MediumLow, Medium, MediumHigh, TooHigh
                chlorine_status : Alert status for chlorine value in : TooLow, MediumLow, Medium, MediumHigh, TooHigh
        """
        resp = self._get_session().rest_request(
            "GET", f"modules/{flipr_id}/survey/last"
        )
        json_resp = resp.json()
        # print("Réponse brute de get_pool_latest_values : " + str(json_resp))

        return {
            "temperature": float(json_resp["Temperature"]),
            "ph": float(json_resp["PH"]["Value"]),
            "chlorine": float(json_resp["Desinfectant"]["Value"]),
            "red_ox": float(json_resp["OxydoReductionPotentiel"]["Value"]),
            "date_time": parse(json_resp["DateTime"]),
            "ph_status": json_resp["Desinfectant"]["DeviationSector"],
            "chlorine_status": json_resp["PH"]["DeviationSector"],
        }
