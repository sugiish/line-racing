import Phaser from "phaser";
import Board from "../domain/Board";
import Player from "../domain/Player";

export default class MyScene extends Phaser.Scene {

  isStarted: boolean = false;
  frameTime: number = 0;

  board: Board | null = null;
  players: Player[] = new Array(0);

  constructor() {
    super("main");
  }

  preload() {
  }

  create() {
    // 盤面描画
    this.board = new Board(this, 30, 20);
    this.board.draw();

    this.players.push(new Player("yoda", 1, 0xff0000, { x: 7, y: 7 }))
    this.players.push(new Player("dappo", 2, 0x00ff00, { x: 22, y: 7 }))
    this.players.push(new Player("harasho", 3, 0x00ffff, { x: 7, y: 12 }))
    this.players.push(new Player("yharry", 4, 0x0000ff, { x: 22, y: 12 }))
    this.players.forEach((player) => {
      player.init(this.board);
    });

    this.input.on("pointerdown", () => {
      this.isStarted = true;
    })
  }

  update(time: number, delta: number) {
    this.frameTime += delta

    if (this.frameTime > 16.5) {
      this.frameTime = 0;

      if (!this.isStarted) {
        return;
      }

      if (this.players.filter(p => !p.isDefeated).length == 1) {
        return;
      }

      this.players.forEach((player) => {

        if (!player.isDefeatedOrDrawing()) {
          player.next(this, this.board);
        }

        player.draw()
      })
    }
  }
}
