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
        res = [str(self)]
        childs = self.childs
        for i, child in enumerate(childs):
            ch0, ch = '├', '│'
            if i == len(childs) - 1:
                ch0, ch = '└', ' '
            print(child)
            res.extend(((ch0 if j == 0 else ch) + ' ' + s for j, s in enumerate(child.tree)))
        return res

    def visit(self, func: Callable[['AstNode'], None])->None:
        func(self)
        map(func, self.childs)

    def __getitem__(self, index):
        return self.childs[index] if index < len(self.childs) else None


class ColumnNode(AstNode):
    def __init__(self, col_name: str):
        super().__init__()
        self.col_name = col_name

    def __str__(self)->str:
        return self.col_name

class NumNode(AstNode):
    def __init__(self, num: float):
        super().__init__()
        self.num = float(num)

    def __str__(self)->str:
        return str(self.num)

class StrConstNode(AstNode):
    def __init__(self, l_par: str, string: str, rpar:str):
        super().__init__()
        self.string = str(string)

    def __str__(self)->str:
        return str(self.string)


class BinOp(Enum):
    ADD = '+'
    SUB = '-'
    MUL = '*'
    DIV = '/'
    CON = '||'


class BinOpNode(AstNode):
    def __init__(self, op: BinOp, arg1: AstNode, arg2: AstNode):
        super().__init__()
        self.op = op
        self.arg1 = arg1
        self.arg2 = arg2

    @property
    def childs(self) -> Tuple[AstNode, AstNode]:
        return self.arg1, self.arg2

    def __str__(self)->str:
        return str(self.op.value)


class TableNode(AstNode):
    def __init__(self, table_name: str):
        super().__init__()
        self.table_name = table_name

    def __str__(self)->str:
        return self.table_name

class SelectExprNode(AstNode):
    pass

class StarNode(AstNode):
    def __init__(self, star: str):
        super().__init__()

    def __str__(self):
        return "*"

class AddNode(AstNode):
    pass

class ConcNode(AstNode):
    def __init__(self, group: Tuple[AstNode]):
        self.operans = group

    @property
    def childs(self) -> Tuple[AstNode]:
        return self.operans

    def __str__(self):
        return "||"


class SelectNode(AstNode):
    def __init__(self, *args): # 'SELECT' ['DISTINCT'] *|Tuple(...)
        if type(args[-1]) == StarNode:
            self.col = args[-1],
        else:
            self.col = args[-1]
        self.distinct = len(args) == 3

    @property
    def childs(self) -> Tuple[ColumnNode]:
        return self.col

    def __str__(self)->str:
        return 'SELECT' if not self.distinct else "SELECT DISTINCT"


class FromNode(AstNode):
    def __init__(self, from_,  table: Tuple[TableNode]):
        self.arg = table

    @property
    def childs(self) -> Tuple[TableNode]:
        return self.arg

    def __str__(self)->str:
        return 'FROM'

class OnExprNode(AstNode):
    def __init__(self, col1: ColumnNode, op: str, col2: ColumnNode):
        self.col1 = col1
        self.col2 = col2
        self.op = op

    @property
    def childs(self) -> Tuple[ColumnNode]:
        return self.col1, self.col2

    def __str__(self):
        return self.op

class OnNode(AstNode):
    def __init__(self, on: str, cond: OnExprNode):
        self.cond = cond

    @property
    def childs(self) -> Tuple[ColumnNode]:
        return self.cond,

    def __str__(self):
        return "ON"


class JoinExprNode(AstNode):
    def __init__(self, table1: TableNode, join: str,  table2: TableNode, on: OnNode):
        self.join = join
        self.table1 = table1
        self.table2 = table2
        self.on = on

    @property
    def childs(self) -> (TableNode, TableNode, OnNode):
        return (self.table1, self.table2, self.on)

    def __str__(self)->str:
        return self.join


class OpBlockNode(AstNode):
    def __init__(self, sign: str, col_nodes: Tuple[ColumnNode]):
        self.sign = sign
        self.arg = col_nodes
        super().__init__()

    @property
    def childs(self) -> Tuple[ColumnNode]:
        return self.arg

    def __str__(self):
        return self.sign


class AndNode(AstNode):
    def __init__(self, arg1: OnExprNode, and_: str = '', arg2: OnExprNode = None):
        if arg2:
            self.args = (arg1, arg2)
        else:
            self.args = [arg1]

    @property
    def childs(self) -> Tuple[OnExprNode]:
        return self.args

    def __str__(self):
        return "AND"

class OrNode(AstNode):
    def __init__(self, arg1: AndNode, or_: str = '', arg2: AndNode = None):
        if arg2:
            self.args = (arg1, arg2)
        else:
            self.args = [arg1]

    @property
    def childs(self) -> Tuple[AndNode]:
        return self.args

    def __str__(self)->str:
        return "OR"

class WhereNode(AstNode):
    def __init__(self, where: str, or_nodes: Tuple[OrNode]):
        self.arg = or_nodes

    @property
    def childs(self) -> Tuple[OrNode]:
        return self.arg

    def __str__(self)->str:
        return 'WHERE'


'''
class QueryNode(AstNode):
    def __init__(self, select: SelectNode, from_: FromNode, where: WhereNode = None):
        super().__init__()
        self.select = select
        self.from_ = from_
        self.where = where

    @property
    def childs(self) -> Tuple[SelectNode, FromNode]:
        if self.where is None:
            return self.select, self.from_
        else:
            return self.select, self.from_, self.where

    def __str__(self)->str:
        return str("query")
'''
class QueryNode(AstNode):
    def __init__(self, *blocks: Tuple):
        super().__init__()
        self.blocks = blocks[:-1]

    @property
    def childs(self) -> Tuple[SelectNode]:
        return self.blocks

    def __str__(self)->str:
        return str("query")

