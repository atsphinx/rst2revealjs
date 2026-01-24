import type { EditorView } from "@codemirror/view";
import type { AlpineComponent } from "alpinejs";
import { createEditorView } from "../editor";
import { publishRevealjs } from "../rst2revealjs";

type Data = {
  editor: EditorView | null;
  published: string;
};

export default (): AlpineComponent<Data> => ({
  editor: null,
  published: "",
  init() {
    this.editor = createEditorView(this.$refs.editor, async (code) => {
      const html = publishRevealjs(code);
      this.published = html;
    });
    this.published = publishRevealjs(this.editor.state.doc.toString());
  },
});
