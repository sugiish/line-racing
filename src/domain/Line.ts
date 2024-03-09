import Phaser from "phaser";
import { Coordinate } from "./Coordinate"

export default class Line {

  private static MAX_DRAW_STEP = 1000;

  graphics: Phaser.GameObjects.Graphics;
  src: Coordinate;
  dest: Coordinate;
  isCompletedDrawing: boolean = false;
  step: number = 0;

  constructor(scene: Phaser.Scene, src: Coordinate, dest: Coordinate, color: number) {
    this.graphics = scene.add.graphics({
      lineStyle: {
        width: 5,
        color: color,
      }
    });
    this.src = src;
    this.dest = dest;
  }

  draw() {
    if (this.isCompletedDrawing) {
      return;
    }

    const x = this.src.x + (this.dest.x - this.src.x) * this.step / Line.MAX_DRAW_STEP;
    const y = this.src.y + (this.dest.y - this.src.y) * this.step / Line.MAX_DRAW_STEP;
    this.graphics.clear();
    this.graphics.lineBetween(this.src.x, this.src.y, x, y);

    this.step++;

    if (this.step == Line.MAX_DRAW_STEP) {
      this.isCompletedDrawing = true;
    }
  }
}
