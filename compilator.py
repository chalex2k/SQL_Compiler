import myparser, ast, table
from enum import Enum
import os
import myparser
from typing import Callable, Tuple, Optional, Union
from table import Table
import random


def compile_join(node, data):
    join = str(node)
    if join in ('JOIN', 'INNER JOIN'):
        return
    #elif join == 'LEFT JOIN':
    #elif join == 'RIGHT JOIN':
    #elif join == 'FULL JOIN':
    else:
        print('Неизвестный вид join')

def compile_from(*childs, data):
    for c in childs:
        if type(c) == ast.TableNode:
            for i in data:
                if i.name == c.table_name:
                    c.value = i
                    break
            else:
                print('Неизвестное имя таблицы', c.table_name)
        else:
            c.value = compile_join(c, data)


def compile_query(query, data):
    for block in query.childs:
        if type(block) == ast.FromNode:
            block.value = compile_from(block.childs, data)


def compilate(tables: Tuple[Table], query: ast.QueryNode) -> Table:
    context = ast.QueryContext()
    for t in tables:
        context.db[t.name] = t
    res = query.execute(context)
    return res
