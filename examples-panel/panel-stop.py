import holoviews as hv
import panel as pn
from panel.viewable import Viewer
import random
import pandas as pd
import threading
import time
import ctypes

from gizmo import Gizmo, Dag, Connection
from gizmo.panel import show_dag
import param

NTHREADS = 2

hv.extension('bokeh', inline=True)
pn.extension(nthreads=NTHREADS, loading_spinner='bar', inline=True)
# hv.renderer('bokeh').theme = 'dark_minimal'

def interrupt_thread(tid, exctype):
    """Raise exception exctype in thread tid."""

    r = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        ctypes.c_ulong(tid),
        ctypes.py_object(exctype)
    )
    if r==0:
        raise ValueError('Invalid thread id')
    elif r!=1:
        # "if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"
        #
        ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_ulong(tid), None)
        raise SystemError('PyThreadState_SetAsyncExc failed')

class QueryWidget(Gizmo):
    """A plain Python gizmo that accepts a "query" (a maximum count value) and outputs a dataframe."""

    out_timer = param.Integer(default=5, bounds=(1, 10))

    def __panel__(self):
        return pn.Param(self, widgets={
            'out_timer': {
                'widget_type': pn.widgets.IntInput},
                'name': 'Timer period'
            },
            parameters=['out_timer'],
            sizing_mode='stretch_width'
        )

class ProgressWidget(Gizmo):
    """A progress widget."""

    in_timer = param.Integer()
    out_timer = param.Integer()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.progress = pn.indicators.Progress(name='Progress', value=0, max=self.in_timer)

    def execute(self): #, stopper):
        self.progress.value = 0
        self.progress.max = self.in_timer
        for t in range(1, self.in_timer+1):
            time.sleep(1)
            self.progress.value = t
            print(f'Progress {self.name} {self.progress.value}')

            # if stopper.is_stopped:
            #     return

        self.out_timer = self.in_timer

    def __panel__(self):
        return self.progress

# class StatusContext:
#     def __init__(self, status):
#         self.status = status

#     def __enter__(self):
#         print('ENTER')
#         self.status.value = True

#     def __exit__(self, exc_type, exc_val, exc_tb):
#         print('EXIT')
#         # self.status.value = False
#         if exc_type is None:
#             self.status.color = 'success'
#         else:
#             self.status.color = 'danger'

def main():
    title = 'Stop'

    template = pn.template.MaterialTemplate(
        title=title,
        theme='dark',
        site='PoC ',
        sidebar=pn.Column('## Gizmos'),
        collapsed_sidebar=True
    )

    q = QueryWidget(name='Specify timer interval', user_input=True)
    b1 = ProgressWidget(name='Progress1')
    b2 = ProgressWidget(name='Progress2')

    dag = Dag(doc='Example: stopping and unstopping a dag in panel')
    dag.connect(q, b1, Connection('out_timer', 'in_timer'))
    dag.connect(b1, b2, Connection('out_timer', 'in_timer'))

    show_dag(dag, site='Example stopper', title='demonstrate stopping a dag')

    # switch = pn.widgets.Switch(name='Stop')

    # def on_switch(event):
    #     if switch.value:
    #         dag.stop()
    #         reset()

    #         # Which thread are we running on?
    #         #
    #         current_tid = threading.current_thread().ident

    #         # What other threads are running?
    #         # There are multiple threads running, including the main thread
    #         # and the bokeh server thread. We need to find the panel threads.
    #         # Unfortunately, there is nothing special about them.
    #         #
    #         all_threads = [t for t in threading.enumerate() if t.name.startswith('ThreadPoolExecutor')]
    #         assert len(all_threads)==NTHREADS, f'{all_threads=}'
    #         other_thread = [t for t in all_threads if t.ident!=current_tid][0]
    #         interrupt_thread(other_thread.ident, KeyboardInterrupt)
    #     else:
    #         dag.unstop()
    #         # TODO reset status for each card

    # pn.bind(on_switch, switch, watch=True)

    # def wrap(w: Gizmo):
    #     running_status = pn.indicators.BooleanStatus(value=False, color='primary', align=('end', 'center'))
    #     w._gizmo_context = StatusContext(running_status)
    #     return pn.Card(
    #         w,
    #         header=pn.Row(
    #             running_status,
    #             pn.pane.HTML(f'<h3 class="card-title">{w.name}</h3>', css_classes=['card-title'], margin=(0, 0))
    #         ),
    #         sizing_mode='stretch_width'
    #     )

    # def reset():
    #     """Experiment."""
    #     col = template.main.objects[0]
    #     for card in col:
    #         status = card.header[0]

    # template.main.objects = [pn.Column(*(wrap(gw) for gw in (q, b1, b2)))]
    # template.sidebar.objects = [
    #     pn.Column(
    #         switch,
    #         pn.panel(dag.hv_graph().opts(invert_yaxis=True, xaxis=None, yaxis=None))
    #     )
    # ]
    # template.show(threaded=False)

if __name__=='__main__':
    main()

