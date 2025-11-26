#!/usr/bin/env python

from conda_matchspec_grammar import parser as grammar
from conda.models.match_spec import MatchSpec


def parse_with_conda(spec):
    print("--- Parsing with conda")
    try:
        ms = MatchSpec(spec)
        print(ms)
        print("name    =", ms.name)
        print("version =", ms.version)
    except Exception as e:
        print("ERROR:", e)


def parse_with_lark(spec):
    print("--- Parsing with Lark")
    try:
        tree = grammar.parse(spec)
        print(tree.pretty())
    except Exception as e:
        print("ERROR:", e)


def matchspec_from_file(filename):
    with open(filename, "r") as infile:
        for line in infile:
            line = line.strip()
            if line and not line.startswith(("#", "//")):
                yield line


if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("--from-file",
                        help="Read specs from a file, rather than CLI args")
    parser.add_argument("--lark",
                        action="store_true",
                        help="Parse provided MatchSpecs using Lark grammar")
    parser.add_argument("--conda",
                        action="store_true",
                        help="Parse provided MatchSpecs using conda")
    parser.add_argument("matchspecs", nargs="*",
                        help="List of MatchSpecs to try parsing")
    args = parser.parse_args()

    if args.from_file:
        spec_list = matchspec_from_file(args.from_file)
    else:
        spec_list = args.matchspecs

    for spec in spec_list:
        print(f"\n*** {spec}")
        if args.lark:
            parse_with_lark(spec)
        if args.conda:
            parse_with_conda(spec)
