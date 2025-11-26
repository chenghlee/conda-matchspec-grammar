#!/usr/bin/env python

from lark import Lark
from conda_matchspec_grammar import GRAMMAR_FILE

def parser_factory(start_node):
    return Lark.open(GRAMMAR_FILE,
                     start=start_node,
                     maybe_placeholders=True,
                     ambiguity="explicit",
                     parser="earley",
                     lexer="dynamic_complete",
                     )

TEST_BUILD_STRINGS = (
    "*",
    "h456789a_0",
    "py39h456789a_0",
    "py39*",
    "*_0",
    "*cuda*",
    "*py310*cuda*",
    "**",
    "*py310**cuda*",
)

parser = parser_factory("build_spec")
for build_string in TEST_BUILD_STRINGS:
    print(f"\n***** build_string = '{build_string}'")
    try:
        tree = parser.parse(build_string)
        print(tree.pretty())
    except Exception as err:
        print(err)
