import { defineConfig } from "vite";

export default defineConfig({
  root: "./",
  base: "/rst2revealjs/",
  build: {
    outDir: "dist",
    emptyOutDir: true,
    rollupOptions: {
      input: {
        main: "./index.html",
        playground: "./playground.html",
      },
    },
  },
});
