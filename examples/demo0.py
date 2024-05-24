#

# A basic demonstration of connecting gizmos into a flow.
#

from gizmo import Gizmo, GizmoManager
import param

class P(Gizmo):
    """A gizmo with a single output parameter."""

    one = param.Integer(label='output P')

class Q(Gizmo):
    """A gizmo with a single input and a single output."""

    two = param.Integer(label='Int 2', doc='input Q', allow_refs=True)
    three = param.Integer(label='Int 3', doc='output Q')

    def execute(self, *args, **kwargs):
        print(f'Q acting {self.two=} {args=} {kwargs=}')
        self.three = self.two + 1

class R(Gizmo):
    """A gizmo with a single input."""

    four = param.Integer(label='Int 4', doc='input R', allow_refs=True)

    def execute(self):
        print(f'R acting {self.four=}')

p = P()
q = Q()
r = R()
GizmoManager.connect(p, q, ['one:two'])
GizmoManager.connect(q, r, ['three:four'])

p.one = 1
print(f'''
    {p.one=} (1)
    {q.two=} (1)
    {q.three=} (2)
    {r.four=} (2)
''')
