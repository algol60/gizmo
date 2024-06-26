import holoviews as hv
import panel as pn
import json
from pathlib import Path
import tempfile

from gizmo import Gizmo, Dag, Connection
import param

from _panel_widgets import QueryWidget, BarchartWidget

hv.extension('bokeh', inline=True)
pn.extension(inline=True)
# hv.renderer('bokeh').theme = 'dark_minimal'

def main():
    # Build a dag.
    #
    q = QueryWidget(name='Run a query')
    b = BarchartWidget(name='Results bars')
    bi = BarchartWidget(inverted=True, name='Results bars (inverted)')

    dag = Dag(doc='Example: generate bar charts')
    dag.connect(q, b, Connection('df_out', 'df_in'))
    dag.connect(q, bi, Connection('df_out', 'df_in'))

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

    # Build a panel app.
    #
    template = pn.template.MaterialTemplate(
        title=title,
        theme='dark',
        site='PoC ',
        sidebar=pn.Column('## Gizmos'),
        collapsed_sidebar=True
    )
    template.main.objects = [pn.Column(q, b, bi)]
    template.sidebar.objects = [pn.panel(dag.hv_graph().opts(invert_yaxis=True, xaxis=None, yaxis=None))]
    template.show(threaded=False)

if __name__=='__main__':
    main()
