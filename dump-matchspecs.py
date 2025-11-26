#!/usr/bin/env python3
from os.path import dirname
from pathlib import Path

mydir = Path(dirname(__file__))

XPASS_SPEC_FILES = (
    mydir / "tests/data/matchspec-xpass.txt",
    mydir / "tests/data/matchspec-xpass-should-fail.txt",
)

XFAIL_SPEC_FILES = (
    mydir / "tests/data/matchspec-xfail.txt",
    mydir / "tests/data/matchspec-xfail-should-pass.txt",
)

def read_specs(filename_or_list):
    if isinstance(filename_or_list, (str, Path)):
        with open(filename_or_list, "r") as infile:
            for lineno, spec in enumerate(infile):
                spec = spec.strip()
                if not spec or spec[0] == "#":
                    continue
                yield spec
    else:
        for item in filename_or_list:
            yield from read_specs(item)


if __name__ == "__main__":
    from conda.models.match_spec import MatchSpec
    from conda_matchspec_grammar import parser

    for spec in read_specs(XPASS_SPEC_FILES):
        ms = MatchSpec(spec)
        try:
            tree = parser.parse(spec)
            print(f"\n*****  {spec}",
                  repr(ms),
                  tree.pretty() if tree else "<FAILED>",
                  sep="\n")
        except:
            tree = None
            pass
