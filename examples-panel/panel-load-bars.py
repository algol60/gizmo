#

# Demonstrate that a dag can be loaded from a dump.
# First, run panel-bars.py to create a dumped dag in dag.json.
# Then run this to load and start the dumped dag.
#

import holoviews as hv
import panel as pn
import json
from pathlib import Path
import tempfile

from gizmo import Library
from gizmo.panel import show_dag

from _panel_widgets import QueryWidget, BarchartWidget

NTHREADS = 2

hv.extension('bokeh', inline=True)
pn.extension(nthreads=NTHREADS, loading_spinner='bar', inline=True)
# hv.renderer('bokeh').theme = 'dark_minimal'

def main():
    print('Run panel-bars first.')

    # Load the dag.
    #
    p = Path(tempfile.gettempdir()) / 'dag.json'
    print(f'Loading dag from {p} ...')
    with open(p, encoding='utf-8') as f:
        dump = json.load(f)

    dag = Library.load_dag(dump)
    title = dump['panel']['title']

    show_dag(dag, site='Barchart dag', title=title)

if __name__=='__main__':
    # Gizmos that are loaded from a dumped dag must be in the dag library.
    # Because this is a demonstration, we load the required gizmo classes manually.
    #
    Library.add(QueryWidget)
    Library.add(BarchartWidget)

    main()
