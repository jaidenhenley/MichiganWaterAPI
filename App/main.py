from fastapi import FastAPI, HTTPException
from app.data import sample_beaches, Beach

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Michigan Water API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/beaches", response_model=list[Beach])
def get_beaches():
    return sample_beaches


@app.get("/beaches/{beach_id}", response_model=Beach)
def get_beach(beach_id: int):
    for beach in sample_beaches:
        if beach["id"] == beach_id:
            return beach
    raise HTTPException(status_code=404, detail="Beach not found")