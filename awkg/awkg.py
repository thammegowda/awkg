#!/usr/bin/env python
#
# Author: Thamme Gowda [tg@isi.edu]
# Created: 2019-07-19

import argparse
import logging as log
from typing import Optional
from pathlib import Path
import sys
import codecs
import os
import re
import io

from . import __version__, __description__

log.basicConfig(level=log.INFO)


class AWKG:
    default_init = Path('~/.awkg.py').expanduser()

    def __init__(self, FS=None, RS=None, OFS=None, ORS=None, inp: Optional[Path] = None,
                 out: Optional[Path] = None, encoding='utf-8', enc_errors='ignore',
                 init_path: Optional[Path] = None):
        self.FS = FS
        self.RS = RS
        self.OFS = OFS or FS or ' '
        self.ORS = ORS or RS or '\n'
        if inp:
            self.inp = inp.open('r', encoding=encoding, newline=self.RS, errors=enc_errors)
        else:
            self.inp = io.TextIOWrapper(buffer=sys.stdin.buffer, encoding=encoding,
                                        errors=enc_errors, newline=self.RS)
        if out:
            self.out = out.open('w', encoding=encoding, errors=enc_errors)
        else:
            self.out = io.TextIOWrapper(buffer=sys.stdout.buffer, encoding=encoding,
                                        errors=enc_errors)

        # Note: these variables are not thread-safe; Right! this is NOT Java; We got GIL ;)
        self.NR = 0
        self.globals = {}
        self.locals = dict(FS=self.FS, RS=self.RS, OFS=self.OFS, ORS=self.ORS,
                           print=self._print, out=self.out, re=re, sys=sys, os=os, Path=Path,
                           FNAME=self.inp.name)
        if init_path:
            if not init_path.exists():
                if init_path == self.default_init:
                    log.debug(f"init_path doesnt exist {init_path}")  # its default, so okay
                else:  # user specified
                    log.error(f"Specified init file {init_path} not found")
            else:
                init_script = init_path.read_text(encoding=encoding, errors=enc_errors)
                self.execute(init_script)

    def _print(self, *args):
        rec = self.OFS.join(x if isinstance(x, str) else str(x) for x in args)
        self.out.write(rec + self.ORS)

    def imports(self, script: Optional[str] = None):
        if script:
            parts = script.split(';')  # delim is semi colon
            parts = [p.strip() for p in parts]
            for i, p in enumerate(parts):
                if p.startswith('import ') or p.startswith('from '):
                    pass  # full specified
                else:
                    parts[i] = ('from ' if ' import ' in p else 'import ') + p
            script = ';'.join(parts)
            self.execute(script)

    def begin(self, script: Optional[str] = None):
        if script:
            self.execute(script)

    def execute(self, code):
        exec(code, self.globals, self.locals)

    def run_rec(self, rec, script):
        # awk used $0; we call this R0 because $0 is invalid identifier in py
        R0 = rec.rstrip(self.RS if self.RS else '\n')
        R = R0.split(sep=self.FS)
        NF = len(R)
        self.locals.update(dict(R0=R0, R=R, NF=NF, NR=self.NR, RET=None))
        self.execute(script)
        if self.locals.get('RET'):
            self._print(*self.locals['R'])

    def run_recs(self, script: str):
        compiled = compile(source=script, filename='inline_script', mode='exec')
        self.NR = 0
        for rec in self.inp:
            self.NR += 1
            self.run_rec(rec, compiled)

    def end(self, script: Optional[str] = None):
        if script:
            self.execute(script)
        self.out.close()
        self.inp.close()

    @staticmethod
    def parse_args(args=sys.argv[1:]):

        def unescaped_str(arg_str):
            return codecs.decode(str(arg_str), 'unicode_escape') if arg_str else arg_str

        p = argparse.ArgumentParser(prog='awkg', description=__description__)
        p.add_argument('-i', '--inp', type=Path, default=None, help='Input file path; None=STDIN')

        p.add_argument('-o', '--out', type=Path, default=None, help='Output file path; None=STDOUT')

        p.add_argument('-F', '-FS', '--field-sep', dest='FS', type=unescaped_str,
                       default=None,
                       help='the input field separator. Default=None implies white space', )
        p.add_argument('-OFS', '--out-field-sep', dest='OFS', type=unescaped_str,
                       default=None,
                       help='the out field separator. Default=None implies same as input FS.')
        # p.add_argument('-RS', '--record-separator', dest='RS', type=unescaped_str, default=None,
        #               help='the input record separator. Default=None implies universal newline.')
        p.add_argument('-ORS', '--out-rec-sep', dest='ORS', type=unescaped_str,
                       default=None,
                       help='the output record separator. Default=None implies same as input RS.')
        p.add_argument('inline_script', type=str, help="Inline python script")

        p.add_argument('-b', '--begin', dest='begin_script', type=str,
                       help="BEGIN block. initialize variables or whatever")
        p.add_argument('-e', '--end', dest='end_script', type=str,
                       help="END block. Print summaries or whatever")
        p.add_argument('-im', '--import', dest='imports', type=str,
                       help="Imports block. Specify a list of module names to be imported."
                            "Semicolon (;) is the delimiter. Ex: json;numpy as np")
        p.add_argument('-it', '--init', dest='init_path', type=Path,
                       default=AWKG.default_init, help="The rc file that initializes environment."
                                                       "Default is $HOME/.awkg.py")
        p.add_argument('-v', '--version', action='version', version=f'%(prog)s {__version__}')
        args = vars(p.parse_args(args=args))
        return args

    @classmethod
    def run(cls, inline_script, begin_script=None, end_script=None, imports=None, **args):
        awk = cls(**args)
        awk.imports(imports)
        awk.begin(begin_script)
        awk.run_recs(inline_script)
        awk.end(end_script)

    @staticmethod
    def main():
        try:
            AWKG.run(**AWKG.parse_args())
        except KeyboardInterrupt as e:
            pass  # keyboard interrupts are cool


if __name__ == '__main__':
    AWKG.main()
