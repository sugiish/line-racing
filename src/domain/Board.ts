import { BoardIndex } from "./BoardIndex";
import { Coordinate } from "./Coordinate";

export default class Board {

  static BOARD_OFFSET = { x: 75, y: 75 };
  static SQUARE_SIZE = { width: 30, height: 30 };

  square: Phaser.GameObjects.Graphics;

  // = 0: 空のマス
  // > 0: 任意のプレイヤーが通過済みのマス
  board: number[][];

  constructor(scene: Phaser.Scene, sizeX: number, sizeY: number) {
    this.square = scene.add.graphics({
      lineStyle: {
        width: 2,
        color: 0xf0f0f0,
      },
      fillStyle: {
        color: 0x000000,
      }
    });
    this.board = new Array(sizeY).fill(new Array(sizeX).fill(0));
  }

  draw() {
    for (let y = 0; y < this.board.length; y++) {
      for (let x = 0; x < this.board[y].length; x++) {
        const coordinate = this.calcSquareCoordinate({ x: x, y: y });
        this.square.strokeRect(coordinate.x, coordinate.y, Board.SQUARE_SIZE.width, Board.SQUARE_SIZE.height);
        this.square.fillRect(coordinate.x, coordinate.y, Board.SQUARE_SIZE.width, Board.SQUARE_SIZE.height);
      }
    }
  }

  calcSquareCoordinate(index: BoardIndex): Coordinate {
    const x = Board.BOARD_OFFSET.x + Board.SQUARE_SIZE.width * index.x;
    const y = Board.BOARD_OFFSET.y + Board.SQUARE_SIZE.height * index.y;
    return { x: x, y: y };
  }
}
