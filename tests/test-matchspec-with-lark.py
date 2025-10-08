#!/usr/bin/env python
from os.path import dirname
from pathlib import Path

import pytest
from lark.exceptions import ParseError, LexError
from conda_matchspec_grammar import parser

mydir = Path(dirname(__file__))

XPASS_SPEC_FILES = (
    mydir / "data/matchspec-xpass.txt",
)

XFAIL_SPEC_FILES = (
    mydir / "data/matchspec-xfail.txt",
)

SHOULD_PASS_SPEC_FILES = (
    mydir / "data/matchspec-xfail-should-pass.txt",
)

SHOULD_FAIL_SPEC_FILES = (
    mydir / "data/matchspec-xpass-should-fail.txt",
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


@pytest.mark.parametrize("spec", read_specs(XPASS_SPEC_FILES))
def test_xpass(spec):
    tree = parser.parse(spec)


@pytest.mark.parametrize("spec", read_specs(SHOULD_PASS_SPEC_FILES))
def test_should_pass(spec):
    tree = parser.parse(spec)


@pytest.mark.parametrize("spec", read_specs(XFAIL_SPEC_FILES))
def test_xfail(spec):
    with pytest.raises((ParseError, LexError,)):
        tree = parser.parse(spec)


@pytest.mark.parametrize("spec", read_specs(SHOULD_FAIL_SPEC_FILES))
def test_should_fail(spec):
    with pytest.raises((ParseError, LexError,)):
        tree = parser.parse(spec)
