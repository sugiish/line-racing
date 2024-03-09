import Phaser from "phaser";
import Line from "../domain/Line";
import Board from "../domain/Board";

export default class MyScene extends Phaser.Scene {

  board: Board | null = null;
  line: Line | null = null;

  constructor() {
    super("main");
  }

  preload() {
  }

  create() {
    // 盤面描画
    this.board = new Board(this, 30, 20);
    this.board.draw();

    this.line = new Line(this, { x: 0, y: 0 }, { x: 500, y: 500 }, 0xff0000);
  }

  update() {
    this.line?.draw();
  }
}
