
from fastapi import FastAPI, HTTPException
import httpx
from pydantic import BaseModel

app = FastAPI(title="SciSpace‑Style API", version="1.0")

class DOIMetadata(BaseModel):
    doi: str
    title: str
    creators: list[dict]
    publisher: str
    publicationYear: int
    url: str

@app.get("/dois/{doi}", response_model=DOIMetadata)
async def get_doi(doi: str):
    url = f"https://api.datacite.org/dois/{doi}"
    async with httpx.AsyncClient() as client:
        r = await client.get(url)
    if r.status_code != 200:
        raise HTTPException(status_code=404, detail="DOI not found")
    data = r.json()["data"]["attributes"]
    return DOIMetadata(
        doi=data["doi"],
        title=data["titles"][0]["title"],
        creators=data["creators"],
        publisher=data["publisher"],
        publicationYear=data.get("publicationYear"),
        url=data["url"],
    )
