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


def convert_to_ops(dx: int, dy: int):
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


@dataclasses.dataclass
class RouteNode:
    x: int
    y: int
    up_node: "RouteNode"
    right_node: "RouteNode"
    left_node: "RouteNode"
    down_node: "RouteNode"
    prev_node: "RouteNode"
    score: int
    searched: bool


RESPONSE_TIME_LIMIT = 1


@app.post("/v1/next")
def create_user(body: RequestBody):
    # TODO: ここからを独自のアルゴリズムに修正する(5秒以内にレスポンスを返せるようにすること)
    start_time = time.time()
    print(f"start_time: {start_time}")
    head = next(filter(lambda x: x.id == body.id, body.heads), Coordinate(-1, -1, -1))
    # return ResponseModel(
    #     convert_to_ops(*search_longest_route(body.board, head.x, head.y, body.id))
    # )

    max_voronoi_count = 0
    voronoi_tuples = []
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
        count = calculate_voronoi_counts(body.board, _heads).get(body.id, 0)
        voronoi_tuples.append((ops, count))
        if count > max_voronoi_count:
            max_voronoi_count = count
    print(f"voronoi_tuples: {voronoi_tuples}")
    next_voronoi_tuples = list(
        filter(lambda x: x[1] == max_voronoi_count, voronoi_tuples)
    )
    if len(next_voronoi_tuples) > 1:
        return ResponseModel(
            search_longest_route_v2(
                body.board,
                head.x,
                head.y,
                body.id,
                [d for d, _ in next_voronoi_tuples],
                start_time + RESPONSE_TIME_LIMIT,
            )
        )
    elif len(next_voronoi_tuples) == 1:
        return ResponseModel(next_voronoi_tuples[0][0])

    return ResponseModel(EnumOps.checkmated)


@app.get("/health")
async def health():
    return {"status": "up"}


BFS_MAX_VALUE = 10000


def calculate_voronoi_counts(board, heads):
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


def search_longest_route_v2(board, x, y, id, root_ops_list, abort_time):
    ops_list = [EnumOps.up, EnumOps.right, EnumOps.left, EnumOps.down]
    root = RouteNode(
        x=x,
        y=y,
        up_node=None,
        right_node=None,
        left_node=None,
        down_node=None,
        prev_node=None,
        score=0,
        searched=False,
    )
    while time.time() < abort_time:
        route = deque()
        route_board = np.array(board)
        next_ops_list = list(
            filter(
                lambda ops: 0 <= x + direction(ops)[0] < WIDTH
                and 0 <= y + direction(ops)[1] < HEIGHT
                and route_board[y + direction(ops)[1], x + direction(ops)[0]] == 0,
                root_ops_list,
            )
        )
        if (
            EnumOps.up in next_ops_list
            and root.up_node is not None
            and root.up_node.searched
        ):
            next_ops_list.remove(EnumOps.up)
        if (
            EnumOps.right in next_ops_list
            and root.right_node is not None
            and root.right_node.searched
        ):
            next_ops_list.remove(EnumOps.right)
        if (
            EnumOps.left in next_ops_list
            and root.left_node is not None
            and root.left_node.searched
        ):
            next_ops_list.remove(EnumOps.left)
        if (
            EnumOps.down in next_ops_list
            and root.down_node is not None
            and root.down_node.searched
        ):
            next_ops_list.remove(EnumOps.down)
        if len(next_ops_list) == 0:
            break
        next_ops = random.choice(next_ops_list)
        match next_ops:
            case EnumOps.up:
                if root.up_node is None:
                    root.up_node = RouteNode(
                        x=x,
                        y=y - 1,
                        up_node=None,
                        right_node=None,
                        left_node=None,
                        down_node=None,
                        prev_node=root,
                        score=0,
                        searched=False,
                    )
                next_node = root.up_node
            case EnumOps.right:
                if root.right_node is None:
                    root.right_node = RouteNode(
                        x=x + 1,
                        y=y,
                        up_node=None,
                        right_node=None,
                        left_node=None,
                        down_node=None,
                        prev_node=root,
                        score=0,
                        searched=False,
                    )
                next_node = root.right_node
            case EnumOps.left:
                if root.left_node is None:
                    root.left_node = RouteNode(
                        x=x - 1,
                        y=y,
                        up_node=None,
                        right_node=None,
                        left_node=None,
                        down_node=None,
                        prev_node=root,
                        score=0,
                        searched=False,
                    )
                next_node = root.left_node
            case EnumOps.down:
                if root.down_node is None:
                    root.down_node = RouteNode(
                        x=x,
                        y=y + 1,
                        up_node=None,
                        right_node=None,
                        left_node=None,
                        down_node=None,
                        prev_node=root,
                        score=0,
                        searched=False,
                    )
                next_node = root.down_node
        route.append(next_node)
        route_board[next_node.y, next_node.x] = id
        while time.time() < abort_time:
            next_ops_list = list(
                filter(
                    lambda ops: 0 <= x + direction(ops)[0] < WIDTH
                    and 0 <= y + direction(ops)[1] < HEIGHT
                    and route_board[y + direction(ops)[1], x + direction(ops)[0]] == 0,
                    ops_list,
                )
            )
            if (
                EnumOps.up in next_ops_list
                and next_node.up_node is not None
                and next_node.up_node.searched
            ):
                next_ops_list.remove(EnumOps.up)
            if (
                EnumOps.right in next_ops_list
                and next_node.right_node is not None
                and next_node.right_node.searched
            ):
                next_ops_list.remove(EnumOps.right)
            if (
                EnumOps.left in next_ops_list
                and next_node.left_node is not None
                and next_node.left_node.searched
            ):
                next_ops_list.remove(EnumOps.left)
            if (
                EnumOps.down in next_ops_list
                and next_node.down_node is not None
                and next_node.down_node.searched
            ):
                next_ops_list.remove(EnumOps.down)
            if len(next_ops_list) == 0:
                next_node.searched = True
                next_node.score = len(route)
                for node in reversed(route):
                    if next_node.score > node.score:
                        node.score = next_node.score
                    route_board[node.y, node.x] = 0
                break
            next_ops = random.choice(next_ops_list)
            match next_ops:
                case EnumOps.up:
                    if next_node.up_node is None:
                        next_node.up_node = RouteNode(
                            x=x,
                            y=y - 1,
                            up_node=None,
                            right_node=None,
                            left_node=None,
                            down_node=None,
                            prev_node=next_node,
                            score=0,
                            searched=False,
                        )
                    next_node = next_node.up_node
                case EnumOps.right:
                    if next_node.right_node is None:
                        next_node.right_node = RouteNode(
                            x=x + 1,
                            y=y,
                            up_node=None,
                            right_node=None,
                            left_node=None,
                            down_node=None,
                            prev_node=next_node,
                            score=0,
                            searched=False,
                        )
                    next_node = next_node.right_node
                case EnumOps.left:
                    if next_node.left_node is None:
                        next_node.left_node = RouteNode(
                            x=x - 1,
                            y=y,
                            up_node=None,
                            right_node=None,
                            left_node=None,
                            down_node=None,
                            prev_node=next_node,
                            score=0,
                            searched=False,
                        )
                    next_node = next_node.left_node
                case EnumOps.down:
                    if next_node.down_node is None:
                        next_node.down_node = RouteNode(
                            x=x,
                            y=y + 1,
                            up_node=None,
                            right_node=None,
                            left_node=None,
                            down_node=None,
                            prev_node=next_node,
                            score=0,
                            searched=False,
                        )
                    next_node = next_node.down_node
            route.append(next_node)
            route_board[next_node.y, next_node.x] = id
    best_ops = EnumOps.checkmated
    best_score = 0
    if root.up_node is not None and root.up_node.score > best_score:
        best_score = root.up_node.score
        best_ops = EnumOps.up
    if root.right_node is not None and root.right_node.score > best_score:
        best_score = root.right_node.score
        best_ops = EnumOps.right
    if root.left_node is not None and root.left_node.score > best_score:
        best_score = root.left_node.score
        best_ops = EnumOps.left
    if root.down_node is not None and root.down_node.score > best_score:
        best_score = root.down_node.score
        best_ops = EnumOps.down

    print(root)

    return best_ops


def search_longest_route(board, x, y, id, root_directions, abort_time):
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    longest_distance = 0
    best_direction = (0, 0)
    loop_count = 0
    print(f"root_directions: {root_directions}")
    while time.time() < abort_time:
        loop_count += 1
        route_board = np.array(board)
        route = deque()
        next_directions = list(
            filter(
                lambda d: 0 <= x + d[0] < WIDTH
                and 0 <= y + d[1] < HEIGHT
                and route_board[y + d[1], x + d[0]] == 0,
                root_directions,
            )
        )
        if len(next_directions) == 0:
            break
        next_direction = random.choice(next_directions)
        route.append(next_direction)
        next_x, next_y = x + next_direction[0], y + next_direction[1]
        route_board[y + next_direction[1], x + next_direction[0]] = id
        while True:
            if time.time() >= abort_time:
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
                    print(
                        f"longest_distance: {longest_distance}, best_direction: {best_direction}, time: {time.time()}, abort_time: {abort_time}"
                    )
                break
            next_direction = random.choice(next_directions)
            route.append(next_direction)
            next_x += next_direction[0]
            next_y += next_direction[1]
            route_board[next_y, next_x] = id
    print(f"loop_count: {loop_count}")
    print(f"best_direction: {best_direction}")
    return best_direction


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
