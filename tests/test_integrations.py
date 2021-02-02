# coding: utf-8
"""Tests Flipr api module."""
import pytest

from flipr_api import FliprAPIRestClient

# Enter correct real values here for the tests to complete successfully with real Flipr Server calls.
USERNAME = "DUMMY_USER"
PASSWORD = "DUMMY_PWD"
FLIPR_ID = "DUM_ID"


@pytest.mark.skip("Not an automated test but an example of usage with real values.")
def test_integration_simple() -> None:
    """Test authentification then get basic pool measures."""
    # Init client
    client = FliprAPIRestClient(USERNAME, PASSWORD)

    list_fliprs = client.search_flipr_ids()
    print("Identifiants flipper trouvés : " + str(list_fliprs))

    assert FLIPR_ID in list_fliprs

    pool_measure = client.get_pool_measure_latest(FLIPR_ID)
    print(
        "Valeurs de la piscine : le {:s} temperature = {:.2f}, redox = {:.2f}, chlore = {:.5f}, ph = {:.2f}".format(
            pool_measure.date_mesure.strftime("%Y-%m-%d %H:%M:%S"),
            pool_measure.temperature,
            pool_measure.red_ox,
            pool_measure.chlore,
            pool_measure.ph,
        )
    )

    assert pool_measure.temperature > 0
    assert pool_measure.red_ox > 0
    assert pool_measure.chlore > 0
    assert pool_measure.ph > 0
    assert pool_measure.date_mesure is not None
