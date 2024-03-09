import Phaser from "phaser";

export default class MyScene extends Phaser.Scene {

  // = 0: 空のマス
  // > 0: 任意のプレイヤーが通過済みのマス
  board: number[][] = new Array(20).fill(new Array(30).fill(0));

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
  }
}
