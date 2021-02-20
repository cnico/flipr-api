# -*- coding: utf-8 -*-
"""Client for the Flipr REST API."""
import time
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

    def search_all_ids(self) -> Dict[str, List[str]]:
        """Search  fliprs and hubs IDs.

        Returns:
            A list of flipr ids registered to the user.
        """
        # init result
        results = {"flipr": [], "hub": []}  # type: Dict[str,List[str]]

        # Send the API resuest
        resp = self._get_session().rest_request("GET", "modules")
        # print("Réponse brute de GET /modules : " + str(resp.json()))

        json_list = resp.json()

        if len(json_list) == 0:
            # print("No Flipr found")
            return results
        else:
            results["flipr"] = [
                str(item["Serial"]) for item in json_list if item["ModuleType_Id"] == 1
            ]
            results["hub"] = [
                str(item["Serial"]) for item in json_list if item["ModuleType_Id"] == 2
            ]
            return results

    def search_flipr_ids(self) -> List[str]:
        """Search the flipr IDs.

        Returns:
            A list of flipr ids registered to the user.
        """
        results = self.search_all_ids()

        return results["flipr"]

    def search_hub_ids(self) -> List[str]:
        """Search the Hub IDs.

        Returns:
            A list of Hub ids registered to the user.
        """
        results = self.search_all_ids()

        return results["hub"]

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

    def get_hub_state(self, hub_id: str) -> Dict[str, Any]:
        """Retrieve current state for the given Hub ID.

        Args:
            hub_id: string containing hub's

        Returns:
            A dict whose keys are :
                state: A bool representing the status of the Hub.
                mode: A string representing current mode in : auto, manual, planning.
        """
        resp = self._get_session().rest_request("GET", f"hub/{hub_id}/state")
        json_resp = resp.json()
        # print("Réponse brute de get_hub_state : " + str(json_resp))

        return {
            "state": bool(json_resp["stateEquipment"]),
            "mode": json_resp["behavior"],
        }

    def set_hub_mode(self, hub_id: str, mode: str) -> Dict[str, Any]:
        """Set current mode for the given Hub ID.

        Args:
            hub_id: string containing hub's
            mode: target mode in auto, manual, planning

        Returns:
            A dict whose keys are :
                state: A bool representing the current status of the Hub.
                mode: A string representing current mode in : auto, manual, planning.

        Raises:
             ValueError: if mode is not valid.
        """
        if str(mode) not in ["auto", "manual", "planning"]:
            raise ValueError(f"{mode} is not an valid mode (auto/planning/manual)")

        mode = str(mode)

        resp = self._get_session().rest_request("PUT", f"hub/{hub_id}/mode/{mode}")
        json_resp = resp.json()
        # print("Réponse brute de set_hub_mode : " + str(json_resp))

        return {
            "state": bool(json_resp["stateEquipment"]),
            "mode": json_resp["behavior"],
        }

    def set_hub_state(self, hub_id: str, state: bool) -> Dict[str, Any]:
        """Set current state for the given Hub ID (which is setting mode to manual).

        Args:
            hub_id: string containing hub's
            state: boolean (True On / False Off)

        Returns:
            A dict whose keys are :
                state: A bool representing the final status of the Hub.
                mode: A string representing final mode in : auto, manual, planning.

        """
        state_str = str(state)

        # put hub to manual mode (required to work)
        self.set_hub_mode(hub_id, "manual")
        self._get_session().rest_request("POST", f"hub/{hub_id}/Manual/{state_str}")

        # wait for change to happen
        time.sleep(1)

        # return new status
        return self.get_hub_state(hub_id)
