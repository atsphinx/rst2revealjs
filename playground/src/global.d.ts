import type { Alpine } from "alpinejs";

declare global {
  interface Window {
    Alpine: Alpine;
    rst2revealjs: (source: string) => Promise<string>;
  }
}
