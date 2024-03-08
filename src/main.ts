import Phaser from 'phaser';
import MyScene from "./scenes/MyScene";

const config: Phaser.Types.Core.GameConfig = {
  type: Phaser.AUTO,
  width: 800,
  height: 600,
  parent: 'app',
  physics: {
    default: 'arcade',
    arcade: {
      gravity: { x: 0, y: 200 },
    },
  },
  scene: MyScene,
};

new Phaser.Game(config);
