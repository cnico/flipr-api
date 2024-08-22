# -*- coding: utf-8 -*-
"""Client for the Flipr REST API."""

import logging
import time
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from dateutil.parser import parse

from .exceptions import FliprError
from .session import FliprClientSession

_LOGGER = logging.getLogger(__name__)


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
        json_list = resp.json()

        _LOGGER.debug("Réponse brute de GET /modules : %s", json_list)

        if len(json_list) == 0:
            _LOGGER.debug("No module found")
            return results
        else:
            results["flipr"] = [str(item["Serial"]) for item in json_list if item["ModuleType_Id"] == 1]
            results["hub"] = [str(item["Serial"]) for item in json_list if item["ModuleType_Id"] == 2]
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

        Raises:
            FliprError: when flipr API returns an incorrect response

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
        resp = self._get_session().rest_request("GET", f"modules/{flipr_id}/NewResume")
        json_resp = resp.json()
        if not json_resp:
            raise FliprError(
                f"Error : No data received for flipr {flipr_id} by the API. "
                + "You should test on flipr official app and contact goflipr if it is not working. "
                + "Or perhaps API has changed :(."
            )

        _LOGGER.debug("Réponse brute de get_pool_latest_values : %s", json_resp)

        if not json_resp["Current"] or not json_resp["Current"]["Temperature"]:
            raise FliprError(
                f"Error : No measure found for flipr {flipr_id} by the API. "
                + "Your flipr is probably not calibrated or in Winter mode. "
                + "You should deactive the integration until you resolve the problem via the flipr official app. "
            )

        return {
            "temperature": float(json_resp["Current"]["Temperature"]),
            "ph": float(json_resp["Current"]["PH"]["Value"]),
            "chlorine": float(json_resp["Current"]["Desinfectant"]["Value"]),
            "red_ox": float(json_resp["Current"]["OxydoReductionPotentiel"]["Value"]),
            "date_time": parse(json_resp["Current"]["DateTime"]),
            "ph_status": json_resp["Current"]["PH"]["DeviationSector"],
            "chlorine_status": json_resp["Current"]["Desinfectant"]["DeviationSector"],
            "battery": float(json_resp["Current"]["Battery"]["Deviation"] * 100),
        }

    def get_hub_state(self, hub_id: str) -> Dict[str, Any]:
        """Retrieve current state for the given Hub ID.

        Args:
            hub_id: string containing hub's

        Returns:
            A dict whose keys are :
                state : A bool representing the status of the Hub.
                mode : A string representing current mode in : auto, manual, planning.
                planning : A string representing current planning id.
        """
        resp = self._get_session().rest_request("GET", f"hub/{hub_id}/state")
        json_resp = resp.json()
        _LOGGER.debug("Réponse brute de get_hub_state : %s", json_resp)

        return {
            "state": bool(json_resp["stateEquipment"]),
            "mode": json_resp["behavior"],
            "planning": json_resp["planning"],
        }

    def set_hub_mode(self, hub_id: str, mode: str) -> Dict[str, Any]:
        """Set current mode for the given Hub ID.

        Args:
            hub_id : string containing hub's
            mode : target mode in auto, manual, planning

        Returns:
            A dict whose keys are :
                state : A bool representing the current status of the Hub.
                mode : A string representing current mode in : auto, manual, planning.
                planning: A string representing current planning id.

        Raises:
             ValueError : if mode is not valid.
        """
        if str(mode) not in ["auto", "manual", "planning"]:
            raise ValueError(f"{mode} is not an valid mode (auto/planning/manual)")

        mode = str(mode)

        resp = self._get_session().rest_request("PUT", f"hub/{hub_id}/mode/{mode}")
        json_resp = resp.json()
        _LOGGER.debug("Réponse brute de set_hub_mode : %s", json_resp)

        return {
            "state": bool(json_resp["stateEquipment"]),
            "mode": json_resp["behavior"],
        }

    def set_hub_state(self, hub_id: str, state: bool) -> Dict[str, Any]:
        """Set current state for the given Hub ID (which is setting mode to manual).

        Args:
            hub_id : string containing hub's
            state : boolean (True On / False Off)

        Returns:
            A dict whose keys are :
                state : A bool representing the final status of the Hub.
                mode : A string representing final mode in : auto, manual, planning.
                planning : A string representing current planning id.

        """
        state_str = str(state)

        # put hub to manual mode (required to work)
        self.set_hub_mode(hub_id, "manual")
        self._get_session().rest_request("POST", f"hub/{hub_id}/Manual/{state_str}")

        # wait for change to happen
        time.sleep(1)

        # return new status
        return self.get_hub_state(hub_id)
