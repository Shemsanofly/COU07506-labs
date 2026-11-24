"""Run Lab 0 with this interpreter, save outputs, and validate the notebook."""
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
runtime = ROOT.parent / '.lab0-runtime'
runtime.mkdir(exist_ok=True)
os.environ['MPLCONFIGDIR'] = str(runtime / 'matplotlib')
os.environ['JUPYTER_RUNTIME_DIR'] = str(runtime / 'jupyter')
os.environ['IPYTHONDIR'] = str(runtime / 'ipython')

import nbformat
from nbclient import NotebookClient
from jupyter_client import AsyncKernelManager

path = ROOT / 'COU07506_Week01_YOUR_REGNO.ipynb'
notebook = nbformat.read(path, as_version=4)
manager = AsyncKernelManager(kernel_name='python3')
manager.kernel_spec.argv = [sys.executable, '-m', 'ipykernel_launcher', '-f', '{connection_file}']
client = NotebookClient(
    notebook, km=manager, timeout=120,
    resources={'metadata': {'path': str(ROOT)}},
)
client.execute(cleanup_kc=True)
nbformat.validate(notebook)
code_cells = [cell for cell in notebook.cells if cell.cell_type == 'code']
assert all(cell.execution_count is not None for cell in code_cells)
assert not any(output.output_type == 'error' for cell in code_cells for output in cell.outputs)
images = sum('image/png' in output.get('data', {}) for cell in code_cells for output in cell.outputs)
assert images >= 4, f'Expected at least four embedded figures, found {images}.'
assert any('audio/' in str(output.get('data', {})) for cell in code_cells for output in cell.outputs)
nbformat.write(notebook, path)
print(f'PASS: {len(code_cells)} code cells executed, {images} figures embedded, audio player embedded.')
for cell in code_cells:
    for output in cell.outputs:
        if output.output_type == 'stream':
            print(output.text.strip())
