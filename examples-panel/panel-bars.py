import holoviews as hv
import panel as pn
import json
from pathlib import Path
import tempfile

from gizmo import Dag, Connection
from gizmo.panel import show_dag

from _panel_widgets import QueryWidget, BarchartWidget

NTHREADS = 2

hv.extension('bokeh', inline=True)
pn.extension(nthreads=NTHREADS, loading_spinner='bar', inline=True)
# hv.renderer('bokeh').theme = 'dark_minimal'

def main():
    # Build a dag.
    #
    q = QueryWidget(name='Run a query', user_input=True)
    b = BarchartWidget(name='Results bars')
    bi = BarchartWidget(inverted=True, name='Results bars (inverted)')

    dag = Dag(doc='Example: generate bar charts', site='Example', title='Bars')
    dag.connect(q, b, Connection('out_df', 'in_df'))
    dag.connect(q, bi, Connection('out_df', 'in_df'))

    title = 'Random weighted barcharts'

    # Dump the dag and add panel information.
    #
    dump = dag.dump()
    dump['panel'] = {
        'title': title
    }

    # Save the dump.
    #
    p = Path(tempfile.gettempdir()) / 'dag.json'
    print(f'Saving dag to {p} ...')
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(dump, f, indent=2)

    show_dag(dag)#, site='Barchart dag', title='demonstrate passing a dataframe')

    # # Build a panel app.
    # #
    # template = pn.template.MaterialTemplate(
    #     title=title,
    #     theme='dark',
    #     site='PoC ',
    #     sidebar=pn.Column('## Gizmos'),
    #     collapsed_sidebar=True
    # )
    # template.main.objects = [pn.Column(q, b, bi)]
    # template.sidebar.objects = [pn.panel(dag.hv_graph().opts(invert_yaxis=True, xaxis=None, yaxis=None))]
    # template.show(threaded=False)

if __name__=='__main__':
    main()
