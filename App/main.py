from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Michigan Water API is running"}

@app.get("/health")
def health(): 
    return {"status": "ok"}

@app.get("/beaches")
def get_beaches():
    return [
        {
            "id": 1,
            "name": "Belle Isle Beach",
            "county": "Wayne",
            "status": "safe",
            "ecoli_value": 120
        }
    ]

