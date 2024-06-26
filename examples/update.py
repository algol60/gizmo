#

# A demonstration of gizmos and individual vs batch updates.
#
# Assigning values to outputs separately triggers an event for each assignment.
# Assigning values to outputs using ``update()`` triggers a single event.
#

import param
from gizmo import Gizmo, Dag, Connection

class Gizmo1(Gizmo):
    """A gizmo that creates pointless outputs.

    This gizmo has no inputs.
    """

    # Use param to specify outputs.
    #
    a_string = param.String(
        label='Alphanumeric',
        regex=r'(?i)^[s|b]\w*$',
        doc='A word string starting with U or B',
        default='s'
    )
    length = param.Number(
        label='String length',
        doc='A floating point number',
        default=-1
    )

    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)

    def separate(self, s):
        """Updates the outputs separately, triggering two events."""

        self.a_string = s
        self.length = len(s)

    def update(self, s):
        """Updates the outputs together, triggering a single event."""

        self.param.update({'a_string': s, 'length': len(s)})

class Gizmo2(Gizmo):
    """A gizmo that depends on the outputs of Gizmo1."""

    length = param.Number(label='A number', doc='I am given this number')
    a_string = param.String(label='A string', doc='I am given this string')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def execute(self):
        print(f'Action in {self.__class__.__name__}: {self.a_string=} {self.length=}')

# Get gizmo instances and connect them via their params.
#
g1 = Gizmo1(name='Input')
g2 = Gizmo2(name='Output')

dag = Dag(doc='Example: assign vs update')
dag.connect(g1, g2, Connection('a_string'), Connection('length'))

print('Entering a string in gizmo1 will cause output of two params to gizmo2.')

print('To see the difference between separate and batch updating;')
print('S: strings that start with S will do separate assignments,')
print('B: strings that start with B will do an update of all parameters with only one event triggered.')
print()

while (s:=input('Enter an alphanumeric string [Enter to quit]: ').strip()):
    try:
        g1.param.a_string._validate(s)
        if s[0] in 'Ss':
            g1.separate(s)
        else:
            g1.update(s)
    except ValueError as e:
        print(e)
        raise
