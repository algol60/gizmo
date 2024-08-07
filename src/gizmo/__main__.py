import argparse
from importlib.metadata import version
from param.ipython import ParamPager

from gizmo import Library
from ._library import _find_gizmos, _find_dags, run_dag

def gizmos_cmd(args):
    """Display the gizmos found via plugin entry points."""

    curr_ep = None
    for entry_point, gi in _find_gizmos():
        show = not args.gizmo or gi.key.endswith(args.gizmo)
        if curr_ep is None or entry_point!=curr_ep:
            if show:
                s = f'In {entry_point.module} v{version(entry_point.module)}'
                u = '#' * len(s)
                print(f'\n\x1b[1;37m{s}\n{u}\x1b[0m')
                # print(f'\x1b[1mIn {entry_point.module} v{version(entry_point.module)}:\x1b[0m')
                curr_ep = entry_point

        if show:
            print(f'\x1b[1;37m{gi.key}: {gi.doc}\x1b[0m')

            if args.verbose:
                G = Library.get(gi.key)
                print(ParamPager()(G))
                print()

def dags_cmd(args):
    """Display the dags found via plugin entry points."""

    curr_ep = None
    for entry_point, gi in _find_dags():
        show = not args.dag or gi.key.endswith(args.dag)
        if curr_ep is None or entry_point!=curr_ep:
            if show:
                s = f'In {entry_point.module} v{version(entry_point.module)}'
                u = '#' * len(s)
                print(f'\n\x1b[1;37m{s}\n{u}\x1b[0m')
                curr_ep = entry_point

        if show:
            print(f'\x1b[1;37m{gi.key}: {gi.doc}\x1b[0m')

def run_cmd(args):
    run_dag(args.dag)

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='sub-command help')

    run = subparsers.add_parser('run', help='Run a dag')
    run.add_argument('dag', type=str, help='A dag to run')
    run.set_defaults(func=run_cmd)

    gizmos = subparsers.add_parser('gizmos', help='Show available gizmos')
    gizmos.add_argument('-v', '--verbose', action='store_true', help='Show help')
    gizmos.add_argument('gizmo', nargs='?', help='Show all gizmos ending with this string')
    gizmos.set_defaults(func=gizmos_cmd)

    dags = subparsers.add_parser('dags', help='Show available dags')
    dags.add_argument('dag', nargs='?', help='Show all dags ending with this string')
    dags.set_defaults(func=dags_cmd)

    args = parser.parse_args()
    if 'func' in args:
        args.func(args)
    else:
        parser.print_help()

if __name__=='__main__':
    main()
