import langRst from "@shikijs/langs/rst";
import themeGithubLight from "@shikijs/themes/github-light";
import { EditorView, basicSetup } from "codemirror";
import shiki from "codemirror-shiki";
import { createHighlighterCore } from "shiki/core";
import { createOnigurumaEngine } from "shiki/engine/oniguruma";
import shikiWasm from "shiki/wasm";

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
    extensions: [
      basicSetup,
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
