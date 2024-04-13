import dataclasses
import random
import time
from collections import deque
from enum import Enum

import numpy as np
import uvicorn
from fastapi import FastAPI

app = FastAPI()
np.set_printoptions(
    threshold=10000,
    linewidth=1000,
)

WIDTH = 30
HEIGHT = 20


@dataclasses.dataclass
class Coordinate:
    id: int
    x: int
    y: int


@dataclasses.dataclass
class RequestBody:
    id: int
    heads: list[Coordinate]
    board: list[list[int]]  # 左上原点。x 軸右向き、y 軸左向き。(x, y) = board[y][x]


class EnumOps(Enum):
    up = "up"
    right = "right"
    left = "left"
    down = "down"
    checkmated = "checkmated"

    @classmethod
    def values(cls):
        return [i.value for i in cls]


def direction(ops):
    if ops == EnumOps.up:
        return (0, -1)
    elif ops == EnumOps.right:
        return (1, 0)
    elif ops == EnumOps.left:
        return (-1, 0)
    elif ops == EnumOps.down:
        return (0, 1)
    return (0, 0)


def convert_to_ops(dx, dy):
    if dx == 0 and dy == -1:
        return EnumOps.up
    elif dx == 1 and dy == 0:
        return EnumOps.right
    elif dx == -1 and dy == 0:
        return EnumOps.left
    elif dx == 0 and dy == 1:
        return EnumOps.down
    return EnumOps.checkmated


@dataclasses.dataclass
class ResponseModel:
    ops: EnumOps


@app.post("/v1/next")
def create_user(body: RequestBody):
    # TODO: ここからを独自のアルゴリズムに修正する(5秒以内にレスポンスを返せるようにすること)
    start_time = time.time()
    head = next(filter(lambda x: x.id == body.id, body.heads), Coordinate(-1, -1, -1))
    # return ResponseModel(
    #     convert_to_ops(*search_longest_route(body.board, head.x, head.y, body.id))
    # )

    next_ops = EnumOps.checkmated
    next_voronoi_count = 0
    for ops in [EnumOps.up, EnumOps.right, EnumOps.left, EnumOps.down]:
        dx, dy = direction(ops)
        next_head = (head.x + dx, head.y + dy)
        if not (0 <= next_head[0] < WIDTH and 0 <= next_head[1] < HEIGHT):
            continue
        if body.board[next_head[1]][next_head[0]] != 0:
            continue
        _heads = [
            body.heads[i] if h.id != body.id else Coordinate(body.id, *next_head)
            for i, h in enumerate(body.heads)
        ]
        counts = voronoi_counts(body.board, _heads)
        count = counts.get(body.id, 0)
        print(f"time: {time.time() - start_time}, ops: {ops}, count: {count}")
        if count > next_voronoi_count:
            next_voronoi_count = count
            next_ops = ops
    return ResponseModel(next_ops)


#
# for ops in EnumOps:
# if ops == EnumOps.up:
# dest = Coordinate(body.id, head.x, head.y - 1)
# elif ops == EnumOps.right:
# dest = Coordinate(body.id, head.x + 1, head.y)
# elif ops == EnumOps.left:
# dest = Coordinate(body.id, head.x - 1, head.y)
# elif ops == EnumOps.down:
# dest = Coordinate(body.id, head.x, head.y + 1)
#
# if (
# dest.x >= 0
# and dest.y >= 0
# and dest.x < len(body.board[0])
# and dest.y < len(body.board)
# and body.board[dest.y][dest.x] == 0
# ):
# return ResponseModel(ops)
#
# TODO: ここまでを独自のアルゴリズムに修正する


#
# return ResponseModel(EnumOps.checkmated)


@app.get("/health")
async def health():
    return {"status": "up"}


BFS_MAX_VALUE = 10000


def voronoi_counts(board, heads):
    CONFLICT = 10
    voronoi_board = np.zeros((HEIGHT, WIDTH))
    bfs_boards = [bfs(board, head.x, head.y) for head in heads]
    for y in range(HEIGHT):
        for x in range(WIDTH):
            min_distance = BFS_MAX_VALUE
            for i, head in enumerate(heads):
                if bfs_boards[i][y, x] == BFS_MAX_VALUE:
                    continue
                elif min_distance > bfs_boards[i][y, x]:
                    voronoi_board[y, x] = head.id
                    min_distance = bfs_boards[i][y, x]
                elif min_distance == bfs_boards[i][y, x]:
                    voronoi_board[y, x] = CONFLICT
    voronoi_heads, counts = np.unique(voronoi_board, return_counts=True)
    return dict(zip(voronoi_heads, counts))


def bfs(board, x, y):
    queue = deque()
    bfs_board = np.full((HEIGHT, WIDTH), BFS_MAX_VALUE)
    bfs_board[y, x] = 0
    queue.append((x, y))
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    while len(queue) > 0:
        x, y = queue.popleft()
        for dx, dy in directions:
            next_x, next_y = x + dx, y + dy
            if next_x < 0 or next_x >= WIDTH or next_y < 0 or next_y >= HEIGHT:
                continue
            if board[next_y][next_x] != 0:
                continue
            if bfs_board[next_y, next_x] > bfs_board[y, x] + 1:
                bfs_board[next_y, next_x] = bfs_board[y, x] + 1
                queue.append((next_x, next_y))
            continue
    return bfs_board


TIME_LIMIT = 1


def search_longest_route(board, x, y, id):
    start_time = time.time()
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    longest_distance = 0
    best_direction = (0, 0)
    loop_count = 0
    while time.time() - start_time < TIME_LIMIT:
        loop_count += 1
        route_board = np.array(board)
        route = deque()
        next_directions = list(
            filter(
                lambda d: 0 <= x + d[0] < WIDTH
                and 0 <= y + d[1] < HEIGHT
                and route_board[y + d[1], x + d[0]] == 0,
                directions,
            )
        )
        if len(next_directions) == 0:
            break
        next_direction = random.choice(next_directions)
        route.append(next_direction)
        next_x, next_y = x + next_direction[0], y + next_direction[1]
        route_board[y + next_direction[1], x + next_direction[0]] = id
        while True:
            if time.time() - start_time > TIME_LIMIT:
                break
            next_directions = list(
                filter(
                    lambda d: 0 <= next_x + d[0] < WIDTH
                    and 0 <= next_y + d[1] < HEIGHT
                    and route_board[next_y + d[1], next_x + d[0]] == 0,
                    directions,
                )
            )
            if len(next_directions) == 0:
                if len(route) > longest_distance:
                    longest_distance = len(route)
                    best_direction = route[0]
                break
            next_direction = random.choice(next_directions)
            route.append(next_direction)
            next_x += next_direction[0]
            next_y += next_direction[1]
            route_board[next_y, next_x] = id
    print(f"loop_count: {loop_count}")
    return best_direction


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
