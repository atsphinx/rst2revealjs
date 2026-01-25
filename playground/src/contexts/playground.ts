import type { EditorView } from "@codemirror/view";
import type { AlpineComponent } from "alpinejs";
import { createEditorView } from "../editor";
import { publishRevealjs } from "../rst2revealjs";

type Data = {
  sourceEditor: EditorView | null;
  published: string;
};

export default (): AlpineComponent<Data> => ({
  sourceEditor: null,
  published: "",
  init() {
    const sourceEditor = createEditorView("rst", undefined, async (code) => {
      const html = publishRevealjs(code);
      this.published = html;
    });
    this.published = publishRevealjs(sourceEditor.state.doc.toString());
    this.sourceEditor = sourceEditor;
  },
});
