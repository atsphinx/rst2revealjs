import { loadPyodide, version as pyodideVersion } from "pyodide";
import Alpine from "alpinejs";
import "bulma/css/bulma.css";

const pyodide = await loadPyodide({
  indexURL: `https://cdn.jsdelivr.net/pyodide/v${pyodideVersion}/full/`,
});

window.Alpine = Alpine;

// Prepare docutils writer
await pyodide.loadPackage("docutils");

window.rst2revealjs = async (source: string): Promise<string> => {
  await pyodide.runPython(`
    from docutils.core import publish_string

    def publish_revealjs(source):
        output = publish_string(source, writer_name="html5").decode()
        return output
  `);
  const publishRevealjs = pyodide.globals.get("publish_revealjs");
  return publishRevealjs(source);
};

Alpine.start();
