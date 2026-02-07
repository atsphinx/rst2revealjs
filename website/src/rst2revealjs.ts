import { loadPyodide, version as pyodideVersion } from "pyodide";
import mainPy from "./main.py?raw";

const pyodide = await loadPyodide({
  indexURL: `https://cdn.jsdelivr.net/pyodide/v${pyodideVersion}/full/`,
});

await pyodide.loadPackage("micropip");
await pyodide.runPythonAsync(`
  import micropip
  
  await micropip.install(["docutils", "jinja2"])
`);
if (import.meta.env.VITE_LOCAL_VERSION) {
  console.log("Use local wheel file");
  const wheel = `./rst2revealjs-${import.meta.env.VITE_LOCAL_VERSION}-py3-none-any.whl`;
  await pyodide.loadPackage(wheel);
} else {
  await pyodide.loadPackage("rst2revealjs");
}
await pyodide.runPython(mainPy);

function publishRevealjs(source: string, settings: string): string {
  return pyodide.globals.get("publish_revealjs")(source, settings);
}

export { publishRevealjs };
