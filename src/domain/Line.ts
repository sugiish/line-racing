import Phaser from "phaser";
import { BoardIndex } from "./BoardIndex";
import Board from "./Board";
import { Coordinate } from "./Coordinate";

export default class Line {

  private static MAX_DRAW_STEP = 25;
  private static BOLD = 7;

  graphics: Phaser.GameObjects.Graphics;
  src: BoardIndex;
  dest: BoardIndex;
  isCompletedDrawing: boolean = false;
  step: number = 0;

  constructor(scene: Phaser.Scene, src: BoardIndex, dest: BoardIndex, color: number) {
    this.graphics = scene.add.graphics({
      lineStyle: {
        width: Line.BOLD,
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

    this.step++;

    const srcCoordinate = this.calcSquareCoordinate(this.src);
    const destCoordinate = this.calcSquareCoordinate(this.dest);

    const ajustOffsetX = (this.dest.x - this.src.x) * Line.BOLD / 2;
    const ajustOffsetY = (this.dest.y - this.src.y) * Line.BOLD / 2;

    const x = srcCoordinate.x + (destCoordinate.x - srcCoordinate.x) * this.step / Line.MAX_DRAW_STEP + ajustOffsetX;
    const y = srcCoordinate.y + (destCoordinate.y - srcCoordinate.y) * this.step / Line.MAX_DRAW_STEP + ajustOffsetY;
    this.graphics.clear();
    this.graphics.lineBetween(srcCoordinate.x, srcCoordinate.y, x, y);

    if (this.step == Line.MAX_DRAW_STEP) {
      this.isCompletedDrawing = true;
    }
  }

  calcSquareCoordinate(index: BoardIndex): Coordinate {
    const x = Board.BOARD_OFFSET.x + Board.SQUARE_SIZE.width * index.x + Board.SQUARE_SIZE.width / 2;
    const y = Board.BOARD_OFFSET.y + Board.SQUARE_SIZE.height * index.y + Board.SQUARE_SIZE.height / 2;
    return { x: x, y: y };
  }
}
