import Phaser from "phaser";
import Line from "../domain/Line";

export default class MyScene extends Phaser.Scene {

  // = 0: 空のマス
  // > 0: 任意のプレイヤーが通過済みのマス
  board: number[][] = new Array(20).fill(new Array(30).fill(0));

  line: Line | null = null;

  constructor() {
    super("main");
  }
  preload() {
  }

  create() {
    // 盤面描画
    const area = this.add.graphics({
      lineStyle: {
        width: 2,
        color: 0xf0f0f0,
      },
      fillStyle: {
        color: 0x000000,
      }
    });

    for (let y = 0; y < this.board.length; y++) {
      for (let x = 0; x < this.board[y].length; x++) {
        let width = 35;
        let height = 35;
        area.strokeRect(75 + width * x, 75 + height * y, width, height);
        area.fillRect(75 + width * x, 75 + height * y, width, height);
      }
    }

    this.line = new Line(this, { x: 0, y: 0 }, { x: 500, y: 500 }, 0xff0000);
  }

  update() {
    this.line?.draw();
  }
}
