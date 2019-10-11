from contextlib import suppress
import inspect

import pyparsing as pp
from pyparsing import pyparsing_common as ppc

from ast import *


def make_parser():
    col_name = ppc.identifier
    star = pp.Word('*')
    SELECT = pp.Keyword("SELECT")
    table_name = ppc.identifier
    FROM = pp.Keyword('FROM')
    DISTINCT = pp.Keyword('DISTINCT')
    from_node = FROM + table_name + ';' #pp.ZeroOrMore(table_name)
    select_node = SELECT + pp.Optional(DISTINCT) + ((col_name + pp.ZeroOrMore(',' + col_name)) | (star)) + '|'

    query = select_node + from_node
    start = query


    def set_parse_action_magic(rule_name: str, parser: pp.ParserElement)->None:
        if rule_name == rule_name.upper():
            return
        if rule_name == 'col_name':
            def col_name_action(s, loc, tocs):
                print('tocs len is ',len(tocs))
                for i in range(10):
                    print(tocs[i])
                node = ColumnNode(tocs[0])
                return node
            parser.setParseAction(col_name_action)
        elif rule_name == 'table_name':
            def table_name_action(s, loc, tocs):
                node = TableNode(tocs[0])
                return node
            parser.setParseAction(table_name_action)

        elif rule_name == 'star':
            def star_action(s, loc, tocs):
                node = StarNode()
                return node
            parser.setParseAction(star_action)
        elif rule_name == 'select_node':
            def select_action(s, loc, tocs):
                for sep_pos, i in enumerate(tocs):
                    if i == '|':
                        break
                if tocs[1] == 'DISTINCT':
                    node = SelectNode(True, tocs[2:sep_pos:2])
                else:
                    node = SelectNode(False, tocs[1:sep_pos:2])
                return node
            parser.setParseAction(select_action)
        elif rule_name == 'query':
            def query_action(s, loc, tocs):
                node = QueryNode(tocs[0], tocs[1])
                return node
            parser.setParseAction(query_action)
        elif rule_name == 'from_node':
            def from_action(s, loc, tocs):
                node = FromNode(tocs[1])
                return node
            parser.setParseAction(from_action)

    for var_name, value in locals().copy().items():
        if isinstance(value, pp.ParserElement):
            set_parse_action_magic(var_name, value)
    return start


parser = make_parser()


def parse(prog: str)->QueryNode:
    return parser.parseString(str(prog))[0]