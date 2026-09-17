"""Inläsning och filtrering av eClipse-data."""
from datetime import datetime
from functools import lru_cache

import pandas as pd

from .constants import LUNAR_CSV, SOLAR_CSV


def _extract_year(date_str: str) -> int:
    """Plockar ut året från till exempel: -1999 June 12 eller 2026 August 12."""
    return int(date_str.split()[0])


def _parse_datetime(date_str: str, time_str: str) -> pd.Timestamp | None:
    """Kombinerar Calendar Date + Eclipse Time till en riktig datetime.
    Fungerar bara för år >= 1 för att Python/pandas datetime stödjer inte år f.Kr.."""
    try:
        return pd.to_datetime(f"{date_str} {time_str}", format="%Y %B %d %H:%M:%S")
    except (ValueError, pd.errors.OutOfBoundsDatetime):
        return None


@lru_cache
def load_solar_eclipses() -> pd.DataFrame:
    df = pd.read_csv(SOLAR_CSV)
    df["Year"] = df["Calendar Date"].apply(_extract_year)
    return df


@lru_cache
def load_lunar_eclipses() -> pd.DataFrame:
    df = pd.read_csv(LUNAR_CSV)
    df["Year"] = df["Calendar Date"].apply(_extract_year)
    return df


def _solar_row_to_dict(row: pd.Series) -> dict:
    return {
        "date": row["Calendar Date"],
        "time": row["Eclipse Time"],
        "type": row["Eclipse Type"],
        "magnitude": row["Eclipse Magnitude"],
        "latitude": row["Latitude"],
        "longitude": row["Longitude"],
        "path_width_km": row["Path Width (km)"] if pd.notna(row["Path Width (km)"]) else None,
    }


def get_next_solar_eclipse() -> dict | None:
    """Hittar den första solförmörkelsen som ligger i framtiden."""
    df = load_solar_eclipses()
    current_year = datetime.now().year
    # Filtrera på år först, detta ger en stor prestandavinst innan vi parsar fulla datum
    candidates = df[df["Year"] >= current_year].copy()

    candidates["Datetime"] = candidates.apply(
        lambda r: _parse_datetime(r["Calendar Date"], r["Eclipse Time"]), axis=1
    )
    candidates = candidates.dropna(subset=["Datetime"])
    candidates = candidates[candidates["Datetime"] >= datetime.now()]

    if candidates.empty:
        return None

    next_row = candidates.sort_values("Datetime").iloc[0]
    return _solar_row_to_dict(next_row)


def filter_solar_eclipses(
    eclipse_type: str | None = None,
    year_min: int | None = None,
    year_max: int | None = None,
    limit: int = 200,
) -> list[dict]:
    """Filtrerar solförmörkelser på typ och/eller årsintervall."""
    df = load_solar_eclipses()

    if eclipse_type:
        df = df[df["Eclipse Type"] == eclipse_type]
    if year_min is not None:
        df = df[df["Year"] >= year_min]
    if year_max is not None:
        df = df[df["Year"] <= year_max]

    df = df.sort_values("Year").head(limit)
    return [_solar_row_to_dict(row) for _, row in df.iterrows()]


def get_lunar_summary() -> dict:
    """Kort sammanfattning av månförmörkelser: totalt antal, typer, nästa."""
    df = load_lunar_eclipses()
    current_year = datetime.now().year

    candidates = df[df["Year"] >= current_year].copy()
    candidates["Datetime"] = candidates.apply(
        lambda r: _parse_datetime(r["Calendar Date"], r["Eclipse Time"]), axis=1
    )
    candidates = candidates.dropna(subset=["Datetime"])
    candidates = candidates[candidates["Datetime"] >= datetime.now()]

    next_lunar = None
    if not candidates.empty:
        row = candidates.sort_values("Datetime").iloc[0]
        next_lunar = {
            "date": row["Calendar Date"],
            "time": row["Eclipse Time"],
            "type": row["Eclipse Type"],
        }

    return {
        "total_count": len(df),
        "type_counts": df["Eclipse Type"].value_counts().to_dict(),
        "next_lunar_eclipse": next_lunar,
    }
