# line-racing

## Description

line-racing is a game for for me and my friends to play bot-programming battle.
This project is inspired by [codingame/tron-battle](https://www.codingame.com/multiplayer/bot-programming/tron-battle).

## Usage

```shell
docker compose up -d
```

をしてから、`http://localhost:8000` にアクセス。

## Development

### bot

`docker-resources/player${N}` 配下の `main.py` を修正する。
live-reload が効いているため、docker コンテナを立ち上げている状態でソースコードを更新すると、コンテナ側のサーバーに自動で更新内容が反映される。

### API

対戦画面からは、下記の HTTP リクエストが送られてくる。
5秒以内にレスポンスが無いと失格となる。

- POST /v1/next
  - RequestBody
    - id:
      - player の id
    - head:
      - player の現在位置
    - board:
      - 盤面状態
      - 1行30個で、それが20行分
      - 0 は空白。id と一致する数値は自分の通過した位置
      - 現在位置は `board[head.y][head.x]` で取得できる
  - Response
    - ops:
      - up, right, left, down, checkmated のいずれかを返す

RequestBody の例

```json
{
  "id": 1,
  "head": {
    "x": 8,
    "y": 0,
  },
  "board": [
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ...
  ]
}
```

Response の例

```json
{
  "ops": str
}
```

### 対戦画面

#### Installation

```shell
asdf install
corepack enable
asdf reshim
```

#### Build

```shell
yarn build
```

#### BootRun

```shell
yarn dev
```
