# coding: utf-8
"""Tests Flipr api module."""
import pytest

from flipr_api import FliprAPIRestClient

# Enter correct real values here for the tests to complete successfully with real Flipr Server calls.
USERNAME = "USERNAME"
PASSWORD = "PASSWORD"
FLIPR_ID = "FLIPR_ID"
HUB_ID = "HUB_ID"


@pytest.mark.skip("Not an automated test but an example of usage with real values.")
def test_integration_simple() -> None:
    """Test authentification then get basic pool measures."""
    # Init client
    client = FliprAPIRestClient(USERNAME, PASSWORD)

    list_fliprs = client.search_flipr_ids()
    print("Identifiants flipper trouvés : " + str(list_fliprs))

    assert FLIPR_ID in list_fliprs

    data = client.get_pool_measure_latest(FLIPR_ID)
    print(
        "Valeurs de la piscine : le {:s} temperature = {:.2f}, redox = {:.2f}, chlorine = {:.5f}, ph = {:.2f}".format(
            data["date_time"].strftime("%Y-%m-%d %H:%M:%S"),
            data["temperature"],
            data["red_ox"],
            data["chlorine"],
            data["ph"],
        )
    )

    assert data["temperature"] > 0
    assert data["red_ox"] > 0
    assert data["chlorine"] > 0
    assert data["ph"] > 0
    assert data["date_time"] is not None


@pytest.mark.skip("Not an automated test but an example of usage with real values.")
def test_integration_hub() -> None:
    """Test authentification then get hub operation."""
    # Init client
    client = FliprAPIRestClient(USERNAME, PASSWORD)

    list_hubs = client.search_hub_ids()
    print("Identifiants hub trouvés : " + str(list_hubs))

    assert HUB_ID in list_hubs

    data = client.get_hub_state(HUB_ID)
    print("Hub state: {:b}, mode: {:s}".format(data["state"], data["mode"]))

    assert data["state"] in [True, False]
    assert data["mode"] in ["auto", "manual", "planning"]

    print("set hub mode to auto")

    data = client.set_hub_mode(HUB_ID, "auto")
    print("Hub state: {:b}, mode: {:s}".format(data["state"], data["mode"]))

    assert data["state"] in [True, False]
    assert data["mode"] == "auto"

    print("set hub state to On")

    data = client.set_hub_state(HUB_ID, True)
    print("Hub state: {:b}, mode: {:s}".format(data["state"], data["mode"]))

    assert data["state"] is True
    assert data["mode"] == "manual"
