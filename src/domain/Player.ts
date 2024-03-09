import Board from "./Board";
import { BoardIndex } from "./BoardIndex";
import Line from "./Line";
import { Direction } from "./Direction";
import player1ApiClient from "./ApiClient";
import apiClient from "./ApiClient";

export default class Player {

  name: string;
  id: number;
  color: number;
  isDefeated: boolean = false;

  head: BoardIndex;
  lines: Line[] = new Array();

  text: Phaser.GameObjects.Text;

  constructor(name: string, id: number, color: number, initailPosition: BoardIndex, text: Phaser.GameObjects.Text) {

    if (id == 0) {
      throw new Error("ID は 0 を使用できない");
    }

    this.name = name;
    this.id = id;
    this.color = color;
    this.head = initailPosition;
    this.text = text.setText(`${this.name}: ${this.lines.length}`).setTint(this.color);
  }

  init(board: Board | null) {
    board?.update(this.head, this.id);
  }

  next(scene: Phaser.Scene, board: Board | null) {

    if (this.isDefeated || board === null) {
      return;
    }

    apiClient.post("/player1/v1/next", { id: this.id, head: this.head, board: board.board }).then((response) => {
      console.log(response.status);
      console.log(response.data);
    }).catch((err) => {
      console.log(err);
    });

    let nextPosition = { x: -1, y: -1 };
    for (let i = 0; i < 4; i++) {
      switch (i) {
        case Direction.up:
          nextPosition = { x: this.head.x, y: this.head.y - 1 }
          break;
        case Direction.right:
          nextPosition = { x: this.head.x + 1, y: this.head.y }
          break;
        case Direction.left:
          nextPosition = { x: this.head.x - 1, y: this.head.y }
          break;
        case Direction.down:
          nextPosition = { x: this.head.x, y: this.head.y + 1 }
          break;
        default:
          return;
      }

      if (!board.isExist(nextPosition)) {
        break;
      }
    }

    if (board.isExist(nextPosition)) {
      this.defeat();
      return;
    }
    board.update(nextPosition, this.id);

    this.lines.push(new Line(scene, this.head, nextPosition, this.color));
    this.text.setText(`${this.name}: ${this.lines.length}`)
    this.head = nextPosition;
  }

  draw() {
    if (this.isDefeated) {
      return;
    }

    this.lines.forEach((line) => {
      line.draw();
    })
  }

  isDefeatedOrDrawing(): boolean {
    if (this.isDefeated) {
      return true;
    }

    return this.lines.some((line) => {
      return !line.isCompletedDrawing
    })
  }

  defeat() {
    this.isDefeated = true;
    this.text.setText(`${this.name}: ${this.lines.length}\nDefeated..`);
  }

  win() {
    this.isDefeated = false;
    this.text.setText(`${this.name}: ${this.lines.length}☆\nWin!!`);
  }
}
