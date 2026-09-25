# eClipsebord_lab_yousif

En fullstack-dashboard för sol- och månförmörkelser, byggd med FastAPI, Streamlit,
Docker och deployad till Azure. Byggt som labb åt FastlyDep i kursen: Big Data and
Cloud – Practical development and NoSQL.

Datan kommer från NASA:s Five Millennium Catalog, 
över sol- och månförmörkelser (-1999 till år 3000).
(https://eclipse.gsfc.nasa.gov/)

## Innehåll

- [Funktioner](#funktioner)
- [Arkitektur](#arkitektur)
- [Köra lokalt](#köra-lokalt)
- [EDA](#eda)

## Funktioner

- **Nästa förmörkelse** - visar nästa kommande solförmörkelse räknat från dagens
  datum, med datum, tid, position, typ och magnitud.
- **Månförmörkelser** - kort sammanfattning: totalt antal, fördelning per typ,
  och nästa kommande månförmörkelse.
- **Utforska historik** - filtrera solförmörkelser på typ "Total/Annular/
  Partial/Hybrid" och årsintervall "-1999 till 3000".

## Arkitektur

Projektet är uppdelat i tre nivåer:

1. **Lokalt** - ett [uv workspace] med två separata Python-paket:
   - `backend/` - FastAPI, läser eclipse-datan med pandas och exponerar den via
     ett litet REST-API.
   - `frontend/` - Streamlit, hämtar data från backend via `httpx` och visar
     upp den i en dashboard.
2. **Docker** - varje tjänst har sin egen `Dockerfile`, och en gemensam
   `docker-compose.yml` kör dem tillsammans lokalt på ett internt nätverk.
3. **Azure** - images byggs och pushas till **Azure Container Registry**,
   backend körs som en **Container App**, och frontend som en **Web App for Containers**. Kommunikationen mellan dem styrs av miljövariabeln
   `BACKEND_URL`, som pekar på rätt adress beroende på miljö.

## För att köra lokalt

Kräver [uv] installerat.

```bash
# Installera alla beroenden för hela workspacet
uv sync --all-packages

# Terminal 1: starta backend
uv run uvicorn backend.api:app --reload --port 8000

# Terminal 2: starta frontend
uv run streamlit run frontend/src/frontend/app.py
```

Backend nås på `http://localhost:8000` och Swagger-dokumentation på `/docs`,
frontend på `http://localhost:8501`.

## EDA

En kort exploration av datasetet finns i [EDA/eda.ipynb](EDA/eda.ipynb) —
struktur, saknade värden, fördelning av förmörkelsetyper över tid, samt vilka
kolumner som är relevanta för dashboarden.

---

*Vissa delar av koden i detta projekt är LLM-genererade (se kommentarer i
respektive fil) och har granskats och förståtts av utvecklaren, i enlighet
med kursens riktlinjer för LLM-användning.*