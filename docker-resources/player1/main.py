from fastapi import FastAPI
import dataclasses
import uvicorn

app = FastAPI()

@dataclasses.dataclass
class Coordinate:
  x: int
  y: int


@dataclasses.dataclass
class RequestBody:
  id: int
  head: Coordinate
  board: list[list[int]]


@app.post("/next")
def create_user(body: RequestBody):
    return body


@app.get("/health")
async def health():
    return {"status": "up"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
