from enum import Enum
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
  board: list[list[int]] # 左上原点。x 軸右向き、y 軸左向き。(x, y) = board[y][x]


class EnumOps(Enum):
    up = "up"
    right = "right"
    left = "left"
    down = "down"
    checkmated = "checkmated"

    @classmethod
    def values(cls):
        return [i.value for i in cls]


@dataclasses.dataclass
class ResponseModel:
  ops: EnumOps


@app.post("/v1/next")
def create_user(body: RequestBody):

  # TODO: ここを独自のアルゴリズムに修正する

  for ops in EnumOps:
      if(ops == EnumOps.up):
        dest = Coordinate(body.head.x, body.head.y - 1)
      elif(ops == EnumOps.right):
        dest = Coordinate(body.head.x + 1, body.head.y)
      elif(ops == EnumOps.left):
        dest = Coordinate(body.head.x - 1, body.head.y)
      elif(ops == EnumOps.down):
        dest = Coordinate(body.head.x, body.head.y + 1)

      if(dest.x >= 0 and dest.y >= 0 and dest.x < len(body.board[0]) and dest.y < len(body.board) and body.board[dest.y][dest.x] == 0):
        return ResponseModel(ops)

  return ResponseModel(EnumOps.checkmated)


@app.get("/health")
async def health():
    return {"status": "up"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
