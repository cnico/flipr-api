# coding: utf-8
"""Tests Flipr api module."""
import pytest

from flipr_api import FliprAPIRestClient
from flipr_api.const import FLIPR_API_URL
from flipr_api.const import FLIPR_AUTH_URL
from flipr_api.exceptions import FliprError


def test_integration_simple(requests_mock) -> None:  # type: ignore
    """Test authentification then get basic pool measures."""
    # mock behaviour :
    requests_mock.post(
        FLIPR_AUTH_URL,
        json={
            "access_token": "abcd-dummy_token_value",
            "token_type": "bearer",
            "expires_in": 23327999,
            "refresh_token": "dummy_refresh_token",
        },
    )
    requests_mock.get(
        f"{FLIPR_API_URL}/modules",
        json=[
            {
                "ActivationKey": "12345",
                "IsSuspended": False,
                "Status": {
                    "Comment": None,
                    "DateTime": "2020-04-13T14:26:53.563",
                    "Status": "Activated",
                },
                "BatteryPlugDate": "2019-07-01T00:00:00",
                "Comments": None,
                "NoAlertUnil": "2000-01-01T00:00:00",
                "Serial": "AB256C",
                "PAC": "123456B",
                "ResetsCounter": 4,
                "SigfoxStatus": "Activated",
                "OffsetOrp": 0.0,
                "OffsetTemperature": 0.0,
                "OffsetPh": 0.0,
                "OffsetConductivite": 0,
                "IsForSpa": False,
                "Version": 3,
                "LastMeasureDateTime": "2021-02-01T07:40:23.663",
                "CommercialType": {"Id": 2, "Value": "Pro"},
                "SubscribtionValidUntil": 1565947747,
                "ModuleType_Id": 1,
                "Eco_Mode": 0,
                "IsSubscriptionValid": True,
            },
            {
                "ActivationKey": "12345",
                "IsSuspended": False,
                "Status": {
                    "Comment": None,
                    "DateTime": "2020-04-13T14:26:53.563",
                    "Status": "Activated",
                },
                "BatteryPlugDate": "2019-07-01T00:00:00",
                "Comments": None,
                "NoAlertUnil": "2000-01-01T00:00:00",
                "Serial": "CD256C",
                "PAC": "123456B",
                "ResetsCounter": 0,
                "SigfoxStatus": "Inactive",
                "OffsetOrp": 0.0,
                "OffsetTemperature": 0.0,
                "OffsetPh": 0.0,
                "OffsetConductivite": 0,
                "IsForSpa": False,
                "Version": 3,
                "LastMeasureDateTime": "2021-02-01T07:40:23.663",
                "CommercialType": {"Id": 1, "Value": "Start"},
                "SubscribtionValidUntil": 1565947747,
                "ModuleType_Id": 2,
                "Eco_Mode": 0,
                "IsSubscriptionValid": True,
            },
        ],
    )
    requests_mock.get(
        f"{FLIPR_API_URL}/modules/AB256C/NewResume",
        json={
            "Current": {
                "MeasureId": 405698,
                "DateTime": "2021-02-01T07:40:21Z",
                "Temperature": 10.0,
                "PH": {
                    "Label": "PH",
                    "Message": "Parfait",
                    "Deviation": -0.47,
                    "Value": 7.01,
                    "DeviationSector": "Medium",
                },
                "OxydoReductionPotentiel": {"Label": "Potentiel Redox.", "Value": 474.0},
                "Conductivity": {"Label": "Conductivité", "Level": "Low"},
                "UvIndex": 0.0,
                "Battery": {"Label": "Batterie", "Deviation": 0.75},
                "Desinfectant": {
                    "Label": "Chlore",
                    "Message": "Trop faible",
                    "Deviation": -1.01,
                    "Value": 0.31986785186370315,
                    "DeviationSector": "TooLow",
                },
            },
        },
    )

    requests_mock.get(
        f"{FLIPR_API_URL}/hub/CD256C/state",
        json={
            "stateEquipment": 1,
            "behavior": "manual",
            "planning": "",
            "internalKeepAlive": None,
            "messageModeAutoFiltration": None,
            "ErrorCode": None,
            "ErrorMessage": None,
        },
    )
    requests_mock.put(
        f"{FLIPR_API_URL}/hub/CD256C/mode/manual",
        json={
            "stateEquipment": 1,
            "behavior": "manual",
            "planning": "",
            "internalKeepAlive": None,
            "messageModeAutoFiltration": None,
            "ErrorCode": None,
            "ErrorMessage": None,
        },
    )

    requests_mock.put(
        f"{FLIPR_API_URL}/hub/CD256C/mode/auto",
        json={
            "stateEquipment": 1,
            "behavior": "auto",
            "planning": "",
            "internalKeepAlive": None,
            "messageModeAutoFiltration": None,
            "ErrorCode": None,
            "ErrorMessage": None,
        },
    )

    requests_mock.put(
        f"{FLIPR_API_URL}/hub/CD256C/mode/planning",
        json={
            "stateEquipment": 1,
            "behavior": "planning",
            "planning": "",
            "internalKeepAlive": None,
            "messageModeAutoFiltration": None,
            "ErrorCode": None,
            "ErrorMessage": None,
        },
    )

    requests_mock.post(
        f"{FLIPR_API_URL}/hub/CD256C/Manual/True",
    )

    # Init client
    client = FliprAPIRestClient("USERNAME", "PASSWORD")

    # Test all id search
    list_all = client.search_all_ids()
    print("Identifiants  trouvés : " + str(list_all))

    assert "AB256C" in list_all["flipr"]
    assert "CD256C" in list_all["hub"]

    # Test flipr id search
    list_fliprs = client.search_flipr_ids()
    print("Identifiants flipper trouvés : " + str(list_fliprs))

    assert "AB256C" in list_fliprs

    # Test pool measure retrieval
    data = client.get_pool_measure_latest("AB256C")

    date_time = data["date_time"]
    temperature = data["temperature"]
    red_ox = data["red_ox"]
    chlorine = data["chlorine"]
    ph = data["ph"]
    battery = data["battery"]

    print(
        "Valeurs de la piscine : le {:s} temperature = {:.2f}, redox = {:.2f}, chlorine = {:.5f}, ph = {:.2f}, battery = {:.2f}".format(
            date_time.strftime("%Y-%m-%d %H:%M:%S"),
            temperature,
            red_ox,
            chlorine,
            ph,
            battery,
        )
    )

    assert temperature == 10.0
    assert red_ox == 474.0
    assert chlorine == 0.31986785186370315
    assert ph == 7.01
    assert date_time.strftime("%Y-%m-%d %H:%M:%S") == "2021-02-01 07:40:21"
    assert battery == 75

    # Test hub id search
    list_hub = client.search_hub_ids()
    print("Identifiants hub trouvés : " + str(list_hub))

    assert "CD256C" in list_hub

    # Test hub get_hub_state

    data = client.get_hub_state("CD256C")

    state = data["state"]
    mode = data["mode"]

    assert state is True
    assert mode == "manual"

    # Test hub set_hub_mode

    for target_mode in ["manual", "auto", "planning"]:

        data = client.set_hub_mode("CD256C", target_mode)
        assert data["mode"] == target_mode

    # Test hub set_hub_mode with wrong value
    with pytest.raises(ValueError):
        data = client.set_hub_mode("CD256C", "Manual")

    # Test hub set_hub_state

    data = client.set_hub_state("CD256C", True)

    state = data["state"]
    mode = data["mode"]

    assert state is True
    assert mode == "manual"

    # Test flipr id not found
    requests_mock.get(f"{FLIPR_API_URL}/modules", json=[])

    list_fliprs = client.search_flipr_ids()

    assert len(list_fliprs) == 0


def test_integration_fliprerror(requests_mock) -> None:  # type: ignore
    """Test a get pool measures that raises an error."""
    # mock behaviour :
    requests_mock.post(
        FLIPR_AUTH_URL,
        json={
            "access_token": "abcd-dummy_token_value",
            "token_type": "bearer",
            "expires_in": 23327999,
            "refresh_token": "dummy_refresh_token",
        },
    )

    # This behaviour is a real one I encountered for an unknown reason of non functionning goflipr API.
    requests_mock.get(
        f"{FLIPR_API_URL}/modules/AB256C/NewResume",
        json={},
    )

    # Init client
    client = FliprAPIRestClient("USERNAME", "PASSWORD")

    # Test pool measure retrieval that should Raise a FliprError.
    with pytest.raises(FliprError) as error_info:
        client.get_pool_measure_latest("AB256C")

    assert (
        str(error_info.value)
        == "Error : No data received for flipr AB256C by the API. You should test on flipr official app and contact goflipr if it is not working. Or perhaps API has changed :(."
    )
