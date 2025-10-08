import os.path

from lark import Lark
from lark import Transformer

from os.path import dirname
from pathlib import Path

GRAMMAR_FILE = os.path.join(os.path.dirname(__file__), "matchspec.lark")

parser = Lark.open(GRAMMAR_FILE,
                   start="matchspec",
                   maybe_placeholders=True,
                   ambiguity="explicit",
                   #parser="lalr",
                   )
