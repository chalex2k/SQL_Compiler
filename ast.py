from abc import ABC, abstractmethod
from typing import Callable, Tuple, Optional, Union
from enum import Enum


class AstNode(ABC):
    @property
    def childs(self)->Tuple['AstNode', ...]:
        return ()

    @abstractmethod
    def __str__(self)->str:
        pass

    @property
    def tree(self)->[str, ...]:
        res = [str(self) + "   " + str(type(self))]
        childs = self.childs
        for i, child in enumerate(childs):
            ch0, ch = '├', '│'
            if i == len(childs) - 1:
                ch0, ch = '└', ' '
            #print(child)
            res.extend(((ch0 if j == 0 else ch) + ' ' + s for j, s in enumerate(child.tree)))
        return res

    def visit(self, func: Callable[['AstNode'], None])->None:
        func(self)
        map(func, self.childs)

    def __getitem__(self, index):
        return self.childs[index] if index < len(self.childs) else None


class NumNode(AstNode):
    def __init__(self, num: str):
        super().__init__()
        self.num = float(num)

    def __str__(self) -> str:
        return str(self.num)


class StrConstNode(AstNode):
    def __init__(self, l_par: str, string: str, r_par: str):
        super().__init__()
        self.string = str(string)

    def __str__(self) -> str:
        return str(self.string)


class ColumnNode(AstNode):
    def __init__(self, name: str):
        super().__init__()
        self.name = str(name)

    def __str__(self) -> str:
        return str(self.name)


class BinOp(Enum):
    ADD = '+'
    SUB = '-'
    MUL = '*'
    DIV = '/'
    CON = '||'


class BinOpNode(AstNode):
    def __init__(self, op: BinOp, arg1: AstNode, arg2: AstNode):  # arg1, arg2: NumNode | ColumnNode | StrConstNode | и др.
        super().__init__()
        self.op = op
        self.arg1 = arg1
        self.arg2 = arg2

    @property
    def childs(self) -> Tuple[AstNode, AstNode]:
        return self.arg1, self.arg2

    def __str__(self) -> str:
        return str(self.op.value)


class FuncSelectNode(AstNode):
    def __init__(self, func_name: str, param: AstNode):
        self.param = param
        self.name = func_name

    @property
    def childs(self) -> Tuple['AstNode', ...]:
        return self.param,

    def __str__(self) -> str:
        return str(self.name)


class StarNode(AstNode):
    def __init__(self, star: str):
        super().__init__()

    def __str__(self) -> str:
        return "*"


class SelectNode(AstNode):
    def __init__(self, *args): # 'SELECT' ['DISTINCT'] *|Tuple(...)
        if type(args[-1]) == StarNode:
            self.col = args[-1],
        else:
            self.col = args[-1]
        self.distinct = len(args) == 3

    @property
    def childs(self) -> Tuple[AstNode]:
        return self.col

    def __str__(self) -> str:
        return 'SELECT' if not self.distinct else "SELECT DISTINCT"



class CompOp(Enum):
    EQ = '='
    GR = '>'
    LESS = '<'
    GR_OR_EQ = '>='
    LESS_OR_EQ = '<='
    NOT_EQ = '<>'


class BoolExprOnNode(AstNode):
    def __init__(self, expr1: AstNode, op: CompOp, expr2: AstNode):  # select_expr + COMP_OP + select_expr
        self.arg1 = expr1
        self.arg2 = expr2
        self.com_op = op

    @property
    def childs(self) -> Tuple[AstNode]:
        return self.arg1, self.arg2

    def __str__(self) -> str:
        return str(self.com_op.value)


class BoolFromNode(AstNode):
    def __init__(self, arg1: BoolExprOnNode, op: str = '', arg2: BoolExprOnNode = None):
        self.arg1 = arg1
        self.arg2 = arg2
        self.op = op
    @property
    def childs(self) -> Tuple[BoolExprOnNode]:
        return self.arg1, self.arg2

    def __str__(self):
        return str(self.op)


class TableNode(AstNode):
    def __init__(self, table_name: str, alias: str = None):
        super().__init__()
        self.name = str(table_name)
        self.alias = alias

    def __str__(self) -> str:
        return self.name + " " + str(self.alias) if self.alias else self.name


class FromNode(AstNode):
    def __init__(self, from_, tables: Tuple[AstNode]):  # TableNode | JoinExprNode
        self.args = tables

    @property
    def childs(self) -> Tuple[TableNode]:
        return self.args

    def __str__(self) -> str:
        return 'FROM'


class OnNode(AstNode):
    def __init__(self, on: str, cond: BoolExprOnNode):
        self.cond = cond

    @property
    def childs(self) -> Tuple[ColumnNode]:
        return self.cond,

    def __str__(self):
        return "ON"


class JoinExprNode(AstNode):
    def __init__(self, table1: TableNode, join: str,  table2: TableNode, on: OnNode):  #, table1: TableNode, join: str,  table2: TableNode, on: OnNode):
        self.join = join
        self.table1 = table1
        self.table2 = table2
        self.on = on

    @property
    def childs(self) -> (TableNode, TableNode, OnNode):
        return self.table1, self.table2, self.on

    def __str__(self) -> str:
        return str(self.join)



class SubqueryExistsNode(AstNode):
    def __init__(self, exists,  query):
        self.query = query
        self.exists = str(exists)

    @property
    def childs(self):
        return (self.query,)

    def __str__(self):
        return self.exists


class SubqueryInNode(AstNode):
    def __init__(self, expr, in_, query):
        self.expr = expr
        self.query = query
        self.in_ = str(in_)

    @property
    def childs(self):
        return (self.expr, self.query)

    def __str__(self):
        return self.in_


class SubqueryAnyAllNode(AstNode):
    def __init__(self, expr, comp_op, any_all: str, query):
        self.expr = expr
        self.copm_op = comp_op
        self.any_all = any_all
        self.query = query

    @property
    def childs(self):
        return (self.expr, self.query)

    def __str__(self):
        return str(self.copm_op.value) + str(self.any_all)


class WhereNode(AstNode):
    def __init__(self, where: str, bool_node: Tuple[AstNode]):
        self.arg = bool_node

    @property
    def childs(self) -> Tuple[AstNode]:
        return self.arg

    def __str__(self) -> str:
        return 'WHERE'


class QueryNode(AstNode):
    def __init__(self, *blocks: Tuple):
        super().__init__()
        self.blocks = blocks[:-1]

    @property
    def childs(self) -> Tuple[SelectNode]:
        return self.blocks

    def __str__(self)->str:
        return str("query")
