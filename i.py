"""Streamlit dashboard for the airplane strikes dataset."""
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


DATA_FILE = Path(__file__).resolve().parent / "Airplane Strikes Dataset.csv"
DAMAGE_COLUMN_START = 37


def load_data(path=DATA_FILE):
    """Load the checked-in airplane strikes CSV (or a supplied CSV path)."""
    return pd.read_csv(path)


def count_incidents(data, column):
    """Return incident counts grouped by *column*."""
    return data.groupby(column).size().reset_index(name="Incident Count")


def aggregate_incidents(data):
    """Calculate the incident counts used by the dashboard charts."""
    return {
        "year": count_incidents(data, "Incident Year"),
        "state": count_incidents(data, "State"),
        "species": count_incidents(data, "Species Name"),
        "flight_phase": count_incidents(data, "Flight Phase"),
    }


def calculate_damage_percentages(data):
    """Calculate the percentage share of each strike/damage field."""
    damage_totals = data.iloc[:, DAMAGE_COLUMN_START:].sum()
    total = damage_totals.sum()
    percentages = damage_totals / total * 100
    return pd.DataFrame(
        {"Damage Type": percentages.index, "%": percentages.values}
    )


def create_charts(aggregates, damage_percentages):
    """Build and return the dashboard's Plotly figures."""
    year_counts = aggregates["year"]
    state_incidents = aggregates["state"]
    species_incidents = aggregates["species"]
    flight_phase_incidents = aggregates["flight_phase"]

    yearly_chart = px.line(
        year_counts,
        x="Incident Year",
        y="Incident Count",
        title="Incidents per Year",
        line_shape="linear",
    )
    state_chart = px.bar(
        state_incidents,
        x="State",
        y="Incident Count",
        title="Incidents Per State",
    )
    state_map = px.scatter_geo(
        state_incidents,
        locations="State",
        locationmode="USA-states",
        color="Incident Count",
        hover_name="State",
        title="Incidents Per State (Map)",
        scope="usa",
        color_continuous_scale=["#87CEFA", "darkred"],
    )
    state_map.update_geos(
        showland=True,
        landcolor="rgb(245, 245, 245)",
        showsubunits=True,
        subunitcolor="rgb(200, 200, 200)",
        countrycolor="rgb(200, 200, 200)",
        showlakes=True,
        lakecolor="rgb(255, 255, 255)",
    )

    species_chart = px.bar(
        species_incidents,
        x="Species Name",
        y="Incident Count",
        title="Incidents per Species",
    )
    flight_phase_chart = px.bar(
        flight_phase_incidents,
        x="Flight Phase",
        y="Incident Count",
        title="Incidents per phase of flight",
    )
    damage_chart = px.bar(
        damage_percentages,
        x="Damage Type",
        y="%",
        title="Percentage of Incidents",
    )
    return (
        yearly_chart,
        state_chart,
        state_map,
        species_chart,
        flight_phase_chart,
        damage_chart,
    )


def render_dashboard(charts):
    """Render the dashboard title and its Plotly charts in order."""
    st.title("Raymond Yang Data Analysis")
    for chart in charts:
        st.plotly_chart(chart)


def main():
    """Load, analyze, and render the airplane strikes dashboard."""
    data = load_data()
    aggregates = aggregate_incidents(data)
    damage_percentages = calculate_damage_percentages(data)
    charts = create_charts(aggregates, damage_percentages)
    render_dashboard(charts)


if __name__ == "__main__":
    main()
