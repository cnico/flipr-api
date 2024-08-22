# coding: utf-8
"""Tests Flipr api module."""

import logging
import os
import time

import pytest
from flipr_api import FliprAPIRestClient

_LOGGER = logging.getLogger(__name__)

USERNAME = os.environ.get("FLIPR_USERNAME")
PASSWORD = os.environ.get("FLIPR_PASSWORD")
FLIPR_ID = os.environ.get("FLIPR_ID")
HUB_ID = os.environ.get("FLIPR_HUB_ID")


@pytest.mark.skip("Not an automated test but an example of usage with real values.")
def test_integration_flipr() -> None:
    """Test authentification then get basic pool measures."""
    # Init client
    client = FliprAPIRestClient(USERNAME, PASSWORD)

    list_fliprs = client.search_flipr_ids()
    _LOGGER.debug("Identifiants flipper trouvés : %s", list_fliprs)

    assert FLIPR_ID in list_fliprs

    data = client.get_pool_measure_latest(FLIPR_ID)
    _LOGGER.debug(
        "Valeurs de la piscine : le %s temperature = %.2f, redox = %.2f, chlorine = %.5f,"
        + " ph = %.2f, Alerte PH = %s, Alerte chlore = %s, Battery = %.2f",
        data["date_time"].strftime("%Y-%m-%d %H:%M:%S"),
        data["temperature"],
        data["red_ox"],
        data["chlorine"],
        data["ph"],
        data["ph_status"],
        data["chlorine_status"],
        data["battery"],
    )

    assert data["temperature"] > 0
    assert data["red_ox"] > 0
    assert data["chlorine"] > 0
    assert data["ph"] > 0
    assert data["date_time"] is not None
    assert data["battery"] > 0


@pytest.mark.skip("Not an automated test but an example of usage with real values.")
def test_integration_hub() -> None:
    """Test authentification then get hub operation."""

    _LOGGER.debug("Starting test_integration_hub")

    # Init client
    client = FliprAPIRestClient(USERNAME, PASSWORD)

    list_hubs = client.search_hub_ids()
    _LOGGER.debug("Identifiants hub trouvés : %s", list_hubs)

    assert HUB_ID in list_hubs

    data = client.get_hub_state(HUB_ID)
    original_mode = data["mode"]
    original_state = data["state"]
    original_planning = data["planning"]
    _LOGGER.debug("Hub state: %s, mode: %s, planning: %s", original_state, original_mode, original_planning)
    assert original_mode in ["auto", "manual", "planning"]
    assert original_state in [True, False]

    time.sleep(5)

    _LOGGER.debug("set hub mode to manual and active")

    data = client.set_hub_state(HUB_ID, True)
    _LOGGER.debug("Hub state: %s, mode: %s, planning: %s", data["state"], data["mode"], data["planning"])
    assert data["state"] is True
    assert data["mode"] == "manual"
    time.sleep(5)

    data = client.set_hub_state(HUB_ID, False)
    _LOGGER.debug("Hub state: %s, mode: %s, planning: %s", data["state"], data["mode"], data["planning"])
    assert data["state"] is False
    assert data["mode"] == "manual"
    time.sleep(5)

    _LOGGER.debug("Restore the original state")
    if original_planning == "manual":
        data = client.set_hub_state(HUB_ID, original_state)
    else:
        data = client.set_hub_mode(HUB_ID, original_mode)

    _LOGGER.debug("Hub state: %s, mode: %s, planning: %s", data["state"], data["mode"], data["planning"])
    assert data["mode"] == original_mode

    _LOGGER.debug("end of the test")
