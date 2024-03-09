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

    this.players.push(new Player("Player1", 1, 0xff0000, { x: 7, y: 7 }, this.add.text(1030, 100, "")))
    this.players.push(new Player("Player2", 2, 0x00ff00, { x: 22, y: 7 }, this.add.text(1030, 200, "")))
    this.players.push(new Player("Player3", 3, 0x00ffff, { x: 7, y: 12 }, this.add.text(1030, 300, "")))
    this.players.push(new Player("Player4", 4, 0xf5b2b2, { x: 22, y: 12 }, this.add.text(1030, 400, "")))
    this.players.forEach((player) => {
      player.init(this.board);
    });

    const readyText = this.add.text(1000, 735, "Click to Start..");
    this.input.on("pointerdown", () => {
      this.isStarted = true;
      readyText.setVisible(false);
    })
  }

  update(delta: number) {
    this.frameTime += delta

    if (this.frameTime > 16.5) {
      this.frameTime = 0;

      if (!this.isStarted) {
        return;
      }

      const currentPlayers = this.players.filter(p => !p.isDefeated)
      if (currentPlayers.length == 1) {
        currentPlayers[0].win();
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
