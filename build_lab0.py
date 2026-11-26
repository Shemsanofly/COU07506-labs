"""Render the saved Week 1 notebook to HTML without replacing it."""
from pathlib import Path
import nbformat
from nbconvert import HTMLExporter
root = Path(__file__).resolve().parent
path = root / 'COU07506_Week01_240242454734.ipynb'
notebook = nbformat.read(path, as_version=4)
nbformat.validate(notebook)
html, _ = HTMLExporter().from_notebook_node(notebook)
destination = root / 'submission' / (path.stem+'.html')
destination.parent.mkdir(exist_ok=True)
destination.write_text(html, encoding='utf-8')
print(destination)
