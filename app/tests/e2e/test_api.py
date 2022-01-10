from http import HTTPStatus

import pytest
from starlette.testclient import TestClient

URL_RISK_PROFILE = "api/v1/risk-profile"


def test_risk_profile__all_inputs(client: TestClient):
    response = client.post(
        URL_RISK_PROFILE,
        json={
            "age": 50,
            "dependents": 2,
            "income": 20000,
            "marital_status": "married",
            "risk_questions": [True, True, True],
            "house": {"ownership_status": "mortgaged"},
            "vehicle": {"year": 2019},
        },
    )
    assert response.status_code == HTTPStatus.OK

    payload = response.json()
    test_result_payload__all_eligible(payload)


def test_risk_profile__vehicle_missing(client: TestClient):
    response = client.post(
        URL_RISK_PROFILE,
        json={
            "age": 50,
            "dependents": 2,
            "income": 20000,
            "marital_status": "married",
            "risk_questions": [True, True, True],
            "house": {"ownership_status": "mortgaged"},
        },
    )
    assert response.status_code == HTTPStatus.OK

    payload = response.json()
    test_result_payload__auto_ineligible(payload)


def test_risk_profile__home_missing(client: TestClient):
    response = client.post(
        URL_RISK_PROFILE,
        json={
            "age": 50,
            "dependents": 2,
            "income": 20000,
            "marital_status": "married",
            "risk_questions": [True, True, True],
            "vehicle": {"year": 2019},
        },
    )
    assert response.status_code == HTTPStatus.OK

    payload = response.json()
    test_result_payload__home_ineligible(payload)


def test_risk_profile__unprocessable_entity_invalid_marital_status(client: TestClient):
    response = client.post(
        URL_RISK_PROFILE,
        json={
            "age": 50,
            "dependents": 2,
            "income": 20000,
            "marital_status": "widowed",
            "risk_questions": [True, True, True],
            "house": {"ownership_status": "mortgaged"},
            "vehicle": {"year": 2019},
        },
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_risk_profile__unprocessable_entity_missing_dependents_field(
    client: TestClient,
):
    response = client.post(
        URL_RISK_PROFILE,
        json={
            "age": 50,
            "income": 20000,
            "marital_status": "single",
            "risk_questions": [True, True, True],
            "house": {"ownership_status": "mortgaged"},
            "vehicle": {"year": 2019},
        },
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_risk_profile__unprocessable_entity_wrong_risk_profile_length(
    client: TestClient,
):
    response = client.post(
        URL_RISK_PROFILE,
        json={
            "age": 50,
            "dependents": 2,
            "income": 20000,
            "marital_status": "single",
            "risk_questions": [True, True, True, True],
            "house": {"ownership_status": "mortgaged"},
            "vehicle": {"year": 2019},
        },
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.skip(reason="function used in another test")
def test_result_payload__all_eligible(payload):
    assert payload == {
        "auto": "responsible",
        "disability": "responsible",
        "home": "responsible",
        "life": "responsible",
    }


@pytest.mark.skip(reason="function used in another test")
def test_result_payload__auto_ineligible(payload):
    assert payload == {
        "auto": "ineligible",
        "disability": "responsible",
        "home": "responsible",
        "life": "responsible",
    }


@pytest.mark.skip(reason="function used in another test")
def test_result_payload__home_ineligible(payload):
    assert payload == {
        "auto": "responsible",
        "disability": "responsible",
        "home": "ineligible",
        "life": "responsible",
    }
