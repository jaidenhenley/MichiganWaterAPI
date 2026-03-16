from pydantic import BaseModel


class Beach(BaseModel):
    id: int
    name: str
    county: str
    status: str
    ecoli_value: int


sample_beaches = [
    {
        "id": 1,
        "name": "Belle Isle Beach",
        "county": "Wayne",
        "status": "safe",
        "ecoli_value": 120,
    },
    {
        "id": 2,
        "name": "Grand Haven State Park",
        "county": "Ottawa",
        "status": "advisory",
        "ecoli_value": 310,
    },
    {
        "id": 3,
        "name": "Silver Lake Beach",
        "county": "Oceana",
        "status": "safe",
        "ecoli_value": 95,
    },
]
