
from fastapi import FastAPI, Query

from . import data_processing as dp

app = FastAPI(title="eClipseBord API")

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/eclipses/next")
def next_eclipse():
    """Nästa kommande solförmörkelse, från dagens datum."""
    result = dp.get_next_solar_eclipse()
    if result is None:
        return {"message": "Ingen kommande förmörkelse hittades i datasetet."}
    return result


@app.get("/eclipses")
def eclipses(
    type: str | None = Query(default=None, description="T, A, P, H m.fl."),
    year_min: int | None = Query(default=None),
    year_max: int | None = Query(default=None),
    limit: int = Query(default=200, le=1000),
):
    """Filtrerbar lista över historiska eller framtida solförmörkelser."""
    return dp.filter_solar_eclipses(
        eclipse_type=type, year_min=year_min, year_max=year_max, limit=limit
    )


@app.get("/eclipses/lunar/summary")
def lunar_summary():
    """Kort sammanfattning av månförmörkelser. Typ, antal och nästa."""
    return dp.get_lunar_summary()
