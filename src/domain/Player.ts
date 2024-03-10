import Board from "./Board";
import { BoardIndex } from "./BoardIndex";
import Line from "./Line";
import apiClient from "./ApiClient";

export default class Player {

  name: string;
  id: number;
  color: number;
  isDefeated: boolean = false;

  head: BoardIndex;
  lines: Line[] = new Array();

  url: string;

  text: Phaser.GameObjects.Text;

  constructor(name: string, id: number, color: number, initailPosition: BoardIndex, url: string, text: Phaser.GameObjects.Text) {

    if (id == 0) {
      throw new Error("ID は 0 を使用できない");
    }

    this.name = name;
    this.id = id;
    this.color = color;
    this.head = initailPosition;
    this.url = url;
    this.text = text.setText(`${this.name}: ${this.lines.length}`).setTint(this.color);
  }

  async next(scene: Phaser.Scene, board: Board | null): Promise<void> {

    if (this.isDefeated || board === null) {
      return;
    }

    let response;
    try {
      response = await apiClient.post(this.url, { id: this.id, head: this.head, board: board.board });
    } catch (err) {
      console.log(err);
      this.defeat();
      return;
    }

    if (response.status != 200) {
      console.log(response);
      this.defeat();
      return;
    }

    let nextPosition: Promise<BoardIndex>;
    switch (response.data.ops) {
      case "up":
        nextPosition = Promise.resolve({ x: this.head.x, y: this.head.y - 1 });
        break;
      case "right":
        nextPosition = Promise.resolve({ x: this.head.x + 1, y: this.head.y });
        break;
      case "left":
        nextPosition = Promise.resolve({ x: this.head.x - 1, y: this.head.y });
        break;
      case "down":
        nextPosition = Promise.resolve({ x: this.head.x, y: this.head.y + 1 });
        break;
      default:
        this.defeat();
        return;
    }

    nextPosition.then(value => {

      if (board.isExist(value)) {
        this.defeat();
        return;
      }

      this.lines.push(new Line(scene, this.head, value, this.color));
      this.text.setText(`${this.name}: ${this.lines.length}`)
      this.head = value;
    })
  }

  draw() {
    this.lines.forEach((line) => {
      line.draw();
    })
  }

  isDrawing(): boolean {
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
