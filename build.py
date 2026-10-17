"""Builds the AllyHeal mod from your own copy of Dark Souls Remastered.

    python build.py                       # default Steam install path
    python build.py --game "D:\\Games\\DARK SOULS REMASTERED"
    python build.py --report              # also print every changed row

Output: dist/AllyHeal/ (ModEngine2 mod folder) and dist/AllyHeal-<version>.zip
Needs only Python 3.10+, no packages.
"""
import argparse
import os
import shutil
import sys
import zipfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))
from soulsformats import Bnd3, Layout, Param, dcx_read, dcx_write, paramdef_parse  # noqa: E402
import allyheal  # noqa: E402

DEFAULT_GAME = r'C:\Program Files (x86)\Steam\steamapps\common\DARK SOULS REMASTERED'
TOUCHED = ('Magic', 'SpEffectParam', 'Bullet')
ROOT = os.path.dirname(os.path.abspath(__file__))


LONG_PREFIX = '\\\\?\\'


def long_path(path):
    """Windows: allow paths over 260 characters."""
    path = os.path.abspath(path)
    if os.name == 'nt' and not path.startswith(LONG_PREFIX):
        return LONG_PREFIX + path
    return path


def param_name(path_bytes):
    return path_bytes.decode('shift_jis').replace('\\', '/').rsplit('/', 1)[-1].removesuffix('.param')


def load(game):
    gp_path = os.path.join(game, 'param', 'GameParam', 'GameParam.parambnd.dcx')
    pd_path = os.path.join(game, 'paramdef', 'paramdef.paramdefbnd.dcx')
    for p in (gp_path, pd_path):
        if not os.path.isfile(p):
            sys.exit(f'Not found: {p}\nPass the game folder with --game.')
    header, gp = dcx_read(gp_path)
    _, pd = dcx_read(pd_path)
    layouts = {}
    for f in Bnd3(pd).files:
        ptype, fields = paramdef_parse(f[3])
        layouts[ptype] = Layout(fields)
    bnd = Bnd3(gp)
    params, files = {}, {}
    for f in bnd.files:
        p = Param(f[3])
        name = param_name(f[2])
        params[name] = (p, layouts[p.ptype])
        files[name] = f
    if not params['Magic'][0].rows or 3400 in params['Bullet'][0]:
        sys.exit('GameParam already looks modded (bullet 3400 exists). Use an unmodified game install.')
    return header, bnd, params, files


def report(before, after, layouts_by_name):
    for name in TOUCHED:
        old, new = before[name], after[name][0]
        lay = layouts_by_name[name]
        added = len(new.rows) - len(old.rows)
        print(f'== {name}: {added} new rows')
        for (rid, a, _), (_, b, _) in zip(old.rows, new.rows):
            if a != b:
                da, db = lay.dump(a), lay.dump(b)
                print(f'   {rid}: ' + ', '.join(f'{k} {da[k]} -> {db[k]}' for k in da if da[k] != db[k]))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--game', default=DEFAULT_GAME, help='Dark Souls Remastered install folder')
    ap.add_argument('--out', default=os.path.join(ROOT, 'dist'))
    ap.add_argument('--report', action='store_true', help='print every changed vanilla row')
    args = ap.parse_args()

    header, bnd, params, files = load(args.game)
    before = {n: Param(files[n][3]) for n in TOUCHED}
    allyheal.apply(params)
    for name in TOUCHED:
        files[name][3] = params[name][0].build()
    if args.report:
        report(before, params, {n: params[n][1] for n in TOUCHED})

    out = long_path(args.out)
    mod_dir = os.path.join(out, 'AllyHeal')
    shutil.rmtree(mod_dir, ignore_errors=True)
    os.makedirs(os.path.join(mod_dir, 'param', 'GameParam'))
    dcx_write(os.path.join(mod_dir, 'param', 'GameParam', 'GameParam.parambnd.dcx'), header, bnd.build())

    zip_path = os.path.join(out, f'AllyHeal-{allyheal.VERSION}.zip')
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
        z.write(os.path.join(mod_dir, 'param', 'GameParam', 'GameParam.parambnd.dcx'),
                'AllyHeal/param/GameParam/GameParam.parambnd.dcx')
        for doc in ('INSTALL.txt', 'INSTALL_RU.txt'):
            z.write(os.path.join(ROOT, 'docs', doc), doc)
    print(f'Built {mod_dir.removeprefix(LONG_PREFIX)}\nPacked {zip_path.removeprefix(LONG_PREFIX)}')


if __name__ == '__main__':
    main()
