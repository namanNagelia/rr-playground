"""Tests for the import-safe data and analysis helpers in i.py."""

import pandas as pd
import pytest

import i


def test_load_data_uses_csv_next_to_module_when_cwd_changes(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    data = i.load_data()

    assert not data.empty
    assert data.iloc[0]["Record ID"] == 127128


def test_load_data_accepts_a_local_csv_path(tmp_path):
    csv_path = tmp_path / "strikes.csv"
    pd.DataFrame({"Incident Year": [2024], "State": ["CA"]}).to_csv(
        csv_path, index=False
    )

    data = i.load_data(csv_path)

    assert data.to_dict("records") == [{"Incident Year": 2024, "State": "CA"}]


def make_analysis_data():
    """Make a compact frame with dashboard and damage fields in CSV positions."""
    columns = [f"unused_{index}" for index in range(i.DAMAGE_COLUMN_START)]
    columns[1] = "Incident Year"
    columns[21] = "State"
    columns[24] = "Flight Phase"
    columns[31] = "Species Name"
    columns += ["Radome Strike", "Radome Damage", "Nose Strike", "Nose Damage"]
    rows = [
        [None] * i.DAMAGE_COLUMN_START + [1, 1, 0, 0],
        [None] * i.DAMAGE_COLUMN_START + [1, 0, 1, 1],
        [None] * i.DAMAGE_COLUMN_START + [0, 0, 1, 0],
    ]
    data = pd.DataFrame(rows, columns=columns)
    data["Incident Year"] = [2020, 2020, 2021]
    data["State"] = ["CA", "CA", "NV"]
    data["Species Name"] = ["GULL", "GULL", "HAWK"]
    data["Flight Phase"] = ["CLIMB", "CLIMB", "APPROACH"]
    return data


def test_aggregate_incidents_counts_each_dashboard_category():
    aggregates = i.aggregate_incidents(make_analysis_data())

    assert aggregates["year"].to_dict("records") == [
        {"Incident Year": 2020, "Incident Count": 2},
        {"Incident Year": 2021, "Incident Count": 1},
    ]
    assert aggregates["state"].to_dict("records") == [
        {"State": "CA", "Incident Count": 2},
        {"State": "NV", "Incident Count": 1},
    ]
    assert aggregates["species"].to_dict("records") == [
        {"Species Name": "GULL", "Incident Count": 2},
        {"Species Name": "HAWK", "Incident Count": 1},
    ]
    assert aggregates["flight_phase"].to_dict("records") == [
        {"Flight Phase": "APPROACH", "Incident Count": 1},
        {"Flight Phase": "CLIMB", "Incident Count": 2},
    ]


def test_calculate_damage_percentages_returns_each_damage_field_share():
    percentages = i.calculate_damage_percentages(make_analysis_data())

    assert percentages["Damage Type"].tolist() == [
        "Radome Strike",
        "Radome Damage",
        "Nose Strike",
        "Nose Damage",
    ]
    assert percentages["%"].tolist() == pytest.approx(
        [100 / 3, 100 / 6, 100 / 3, 100 / 6]
    )
