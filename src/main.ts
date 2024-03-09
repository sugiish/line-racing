import Phaser from 'phaser';
import MyScene from "./scenes/MyScene";

const config: Phaser.Types.Core.GameConfig = {
  type: Phaser.AUTO,
  width: 1200,
  height: 800,
  parent: 'app',
  scene: MyScene,
};

new Phaser.Game(config);
