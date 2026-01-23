import langRst from "@shikijs/langs/rst";
import themeGithubLight from "@shikijs/themes/github-light";
import { EditorView, basicSetup } from "codemirror";
import shiki from "codemirror-shiki";
import { createHighlighterCore } from "shiki/core";
import { createOnigurumaEngine } from "shiki/engine/oniguruma";
import shikiWasm from "shiki/wasm";
import DEFAULT_SOURCE from "./default-source.rst?raw";

const fixedHeightEditor = EditorView.theme({
  "&": {
    height: "50dvh",
  },
  ".cm-scroller": { overflow: "auto" },
});

const highlighter = createHighlighterCore({
  langs: [langRst],
  themes: [themeGithubLight],
  engine: createOnigurumaEngine(shikiWasm),
});

export function createEditorView(
  parent: HTMLElement,
  onUpdate: (code: string) => void | Promise<void>,
): EditorView {
  return new EditorView({
    doc: DEFAULT_SOURCE,
    extensions: [
      basicSetup,
      fixedHeightEditor,
      shiki({ highlighter, language: "rst", theme: "github-light" }),
      EditorView.updateListener.of((update) => {
        if (update.docChanged) {
          onUpdate(update.state.doc.toString());
        }
      }),
    ],
    parent,
  });
}
