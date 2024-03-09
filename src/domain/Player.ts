import { UP } from "phaser";
import Board from "./Board";
import { BoardIndex } from "./BoardIndex";
import Line from "./Line";
import { Direction } from "./Direction";

export default class Player {

  name: string;
  id: number;
  color: number;
  isDefeated: boolean = false;

  head: BoardIndex;
  lines: Line[] = new Array();

  constructor(name: string, id: number, color: number, initailPosition: BoardIndex) {

    if (id == 0) {
      throw new Error("ID は 0 を使用できない");
    }

    this.name = name;
    this.id = id;
    this.color = color;
    this.head = initailPosition;
  }

  init(board: Board | null) {
    board?.update(this.head, this.id);
  }

  next(scene: Phaser.Scene, board: Board | null) {

    if (this.isDefeated || board === null) {
      return;
    }

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
      this.isDefeated = true;
      return;
    }
    board.update(nextPosition, this.id);

    this.lines.push(new Line(scene, this.head, nextPosition, this.color));
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
}
