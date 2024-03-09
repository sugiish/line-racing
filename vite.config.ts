import { defineConfig } from 'vite'

export default defineConfig({
  server: {
    proxy: {
      "/player1": {
        target: "http://localhost:8000",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/player1/, ''),
      }
    },
  },
});
