import langRst from "@shikijs/langs/rst";
import langToml from "@shikijs/langs/toml";
import themeGithubLight from "@shikijs/themes/github-light";
import { basicSetup, EditorView } from "codemirror";
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

const highlighters = new Map();
highlighters.set(
  "rst",
  createHighlighterCore({
    langs: [langRst],
    themes: [themeGithubLight],
    engine: createOnigurumaEngine(shikiWasm),
  }),
);
highlighters.set(
  "toml",
  createHighlighterCore({
    langs: [langToml],
    themes: [themeGithubLight],
    engine: createOnigurumaEngine(shikiWasm),
  }),
);

export function createEditorView(
  language: string,
  doc: string = DEFAULT_SOURCE,
  onUpdate: (code: string) => void | Promise<void> = () => {},
): EditorView {
  return new EditorView({
    doc,
    extensions: [
      basicSetup,
      fixedHeightEditor,
      shiki({
        highlighter: highlighters.get(language),
        language,
        theme: "github-light",
      }),
      EditorView.updateListener.of((update) => {
        if (update.docChanged) {
          onUpdate(update.state.doc.toString());
        }
      }),
    ],
  });
}
