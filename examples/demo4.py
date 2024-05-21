#

# Demonstrate finding gizmos that have compatible outputs.
# An output is compatible with this gizmos inputs by type.
#
# **** NOT WORKING YET ****
#

from gizmo import Gizmo, GizmoManager
import param

class ThisGizmo(Gizmo):
    # Inputs.
    #
    intp = param.Integer(label='An integer', allow_refs=True)
    strp = param.Integer(label='A string', allow_refs=True)
    dfp = param.DataFrame(label='A dataframe', allow_refs=True)

class Gizmo1(Gizmo):
    # Outputs.
    #
    dfp = param.DataFrame(label='A dataframe')
    intp = param.Integer(label='An integer')
    strp = param.Integer(label='A string')

class Gizmo2(Gizmo):
    # Outputs.
    #
    dataframep = param.DataFrame(label='A dataframe')
    numberp = param.Integer(label='An integer')
    boolp = param.Boolean(label='A boolean')

class Gizmo3(Gizmo):
    # Outputs.
    #
    nump = param.Integer(label='An integer')
    boolp = param.Boolean(label='A boolean')

class Gizmo4(Gizmo):
    # Outputs.
    #
    boolp = param.Boolean(label='A boolean')

if __name__=='__main__':
    thisg = ThisGizmo()

    from pprint import pprint
    g1 = Gizmo1()
    pprint(GizmoManager.compatible_outputs(thisg, g1))

    g2 = Gizmo2()
    pprint(GizmoManager.compatible_outputs(thisg, g2))

    g3 = Gizmo3()
    pprint(GizmoManager.compatible_outputs(thisg, g3))
