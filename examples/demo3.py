#

# A demonstration of two gizmos.
# - NumberGizmo outputs a number.
# - AddGizmo takes outputs from two instances of NumberGizmo and adds them.
#   This demonstrates that different input/output param names cab be connected.
#

import random

from gizmo import Gizmo, GizmoManager
import param

class NumberGizmo(Gizmo):
    """Produce a random number."""

    n = param.Integer(
        label='An integer',
        doc='What else is there to say',
        default=None
    )

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    def go(self):
        self.n = random.randint(1, 100)

class AddGizmo(Gizmo):
    """Add two numbers.

    The action does not happen if either of the inputs is None.
    """

    a = param.Integer(label='First integer', default=None, allow_refs=True)
    b = param.Integer(label='Second integer', default=None, allow_refs=True)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    def execute(self):
        print(f'Action {self.__class__.__name__} {self.a=} {self.b=}')

        # If some args aren't set, don't do anything.
        #
        if any(arg is None for arg in (self.a, self.b)):
            print('  Not all args set; ducking out.')
            return

        print(f'{self.a} + {self.b} = {self.a+self.b}')

def main():
    """Pretend to be a gizmo manager."""

    nga = NumberGizmo()
    ngb = NumberGizmo()
    addg = AddGizmo()

    GizmoManager.connect(nga, addg, ['n:a'])
    GizmoManager.connect(ngb, addg, ['n:b'])

    print(f'\nSet gizmo {nga}')
    nga.go()

    print(f'\nSet gizmo {ngb}')
    ngb.go()

if __name__=='__main__':
    main()
