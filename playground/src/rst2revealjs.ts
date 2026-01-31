import { loadPyodide, version as pyodideVersion } from "pyodide";
import mainPy from "./main.py?raw";

const pyodide = await loadPyodide({
  indexURL: `https://cdn.jsdelivr.net/pyodide/v${pyodideVersion}/full/`,
});

await pyodide.loadPackage("docutils");
await pyodide.loadPackage("pygments");
await pyodide.loadPackage("jinja2");
// TODO: This is temporary path in development. Change it after release.
await pyodide.loadPackage("/rst2revealjs-0.0.0-py3-none-any.whl");
await pyodide.runPython(mainPy);

function publishRevealjs(source: string, settings: string): string {
  return pyodide.globals.get("publish_revealjs")(source, settings);
}

export { publishRevealjs };
