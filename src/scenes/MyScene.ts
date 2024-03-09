import Phaser from "phaser";
import Line from "../domain/Line";

const BOARD_OFFSET = { x: 75, y: 75 };
const SQUARE_SIZE = { width: 30, height: 30 };

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
    const square = this.add.graphics({
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
        square.strokeRect(BOARD_OFFSET.x + SQUARE_SIZE.width * x, BOARD_OFFSET.y + SQUARE_SIZE.height * y, SQUARE_SIZE.width, SQUARE_SIZE.height);
        square.fillRect(BOARD_OFFSET.x + SQUARE_SIZE.width * x, BOARD_OFFSET.y + SQUARE_SIZE.height * y, SQUARE_SIZE.width, SQUARE_SIZE.height);
      }
    }

    this.line = new Line(this, { x: 0, y: 0 }, { x: 500, y: 500 }, 0xff0000);
  }

  update() {
    this.line?.draw();
  }
}
