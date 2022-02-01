import asyncio
import json
import random
import sys

from bandbox.core import Tree


async def _analyse_engines(args):
    """Run engines concurrently"""
    from bandbox import engines
    import inspect
    engines_ = inspect.getmembers(engines, inspect.isfunction)
    awaitables = list()
    for engine_name, engine in engines_:
        awaitables.append(engine(random.random(), args))
    await asyncio.gather(*awaitables)


def analyse(args):
    """Analyse the given dataset"""
    # decide which engines we will include
    # e.g. n2_long_names -> list of entities with long names
    # entry point
    asyncio.run(_analyse_engines(args))


def view(args):
    """View the given dataset"""
    import glob, pathlib, os
    if args.input_file:
        with open(args.input_file) as f:
            data = f.read().strip().split(', ')
    else:
        data = glob.glob(str(pathlib.Path(os.path.expanduser(args.path)) / "**"), recursive=True)
    tree = Tree.from_data(data, prefix=args.prefix, show_file_counts=args.hide_file_counts)
    if args.verbose:
        print(data, file=sys.stderr)
        print(tree.data, file=sys.stderr)
        print(json.dumps(tree.data, indent=4), file=sys.stderr)
    try:
        print(tree)
    except BrokenPipeError:
        pass


if __name__ == "__main__":
    analyse('test')
