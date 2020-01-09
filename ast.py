from abc import ABC, abstractmethod
from typing import Callable, Tuple, Optional, Union
from enum import Enum
from table import Table
import exceptions

class Type(Enum):
    STR = 1
    NUM = 2
    TABLE = 3
    BOOL = 4
    STAR = 5
    NULL = 6

class QueryContext:
    def __init__(self):
        self.db = {}
        self.aliases = {}

class ContextOn:
    def __init__(self):
        self.tables = {}

    def find_col(self, name: str):
        for t in self.tables:
            if name in t:
                return t[name]
                break
        else:
            raise exceptions.UnknownColumn("unknowm column " + name)

class AstNode(ABC):
    @property
    def childs(self)->Tuple['AstNode', ...]:
        return ()

    @property
    def value(self): # str, float, table, bool
        return self.value

    @property
    def typ(self) -> Type:
        return self.type_

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

    def full_up_context_table(self, context: QueryContext):
        if isinstance(self, TableNode):
            if self.name in context.db:
                context.aliases[self.name] = context.db[self.name]
                if self.alias:
                    if str(self.alias) not in context.aliases:
                        context.aliases[str(self.alias)] = context.db[self.name]
                    else:
                        raise exceptions.RepeatedDeclareAlias("Alias " + str(self.alias) + " were declare before")
            else:
                raise exceptions.UnknownTable('Unknown table ' + self.name)
        if self.childs:
            for child in self.childs:
                child.full_up_context_table(context)


    def visit(self, func: Callable[['AstNode'], None])->None:
        func(self)
        map(func, self.childs)

    def __getitem__(self, index):
        return self.childs[index] if index < len(self.childs) else None



class NumNode(AstNode):
    def __init__(self, num: str):
        super().__init__()
        self.num = float(num)
        self.type_ = Type.NUM

    def __str__(self) -> str:
        return str(self.num)


class StrConstNode(AstNode):
    def __init__(self, l_par: str, string: str, r_par: str):
        super().__init__()
        self.string = str(string)
        self.type_ = Type.STR

    def __str__(self) -> str:
        return str(self.string)


class ColumnNode(AstNode):
    def __init__(self, name: str):
        super().__init__()
        self.name = str(name)

    def __str__(self) -> str:
        return str(self.name)

    def get_value(self, context: ContextOn):
        if len(self.name.split('.')) == 1: # название стобца без названия таблицы
            return context.find_col(self.name)
        else:
            table_name = self.name.split('.')[0]
            col_name = self.name.split('.')[1]
            if table_name in context.tables:
                if col_name in context.tables[table_name]:
                    return context.tables[table_name][col_name]
                else:
                    raise exceptions.UnknownColumn("Unknown column" + col_name)
            else:
                raise exceptions.UnknownTable('Unknow table ' + table_name)

    def get_type(self, context: ContextOn):
        v = self.get_value(context)
        if len(str(v)) == 0: return Type.NULL
        try:
            v_i = int(v)
            return Type.NUM
        except:
            return Type.STR




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
        self.type_ = Type.STAR

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
        self.type_ = Type.BOOL

    @property
    def childs(self) -> Tuple[AstNode]:
        return self.arg1, self.arg2

    def __str__(self) -> str:
        return str(self.com_op.value)

    def get_value(self, context: ContextOn) -> bool:
        if self.arg1.get_type(context) != self.arg2.get_type(context):
            raise exceptions.TypeMismatch('Type Mismatch ' + str(self.arg1) + ' and' + str(self.arg2))
        v1 = self.arg1.get_value(context)
        v2 = self.arg2.get_value(context)
        if self.com_op == CompOp.EQ:
            return v1 == v2
        elif self.com_op == CompOp.GR:
            return v1 > v2
        if self.com_op == CompOp.LESS:
            return v1 < v2
        if self.com_op == CompOp.GR_OR_EQ:
            return v1 >= v2
        if self.com_op == CompOp.LESS_OR_EQ:
            return v1 <= v2
        if self.com_op == CompOp.NOT_EQ:
            return v1 != v2




class BoolFromNode(AstNode):
    def __init__(self, arg1: BoolExprOnNode, op: str = '', arg2: BoolExprOnNode = None):
        self.arg1 = arg1
        self.arg2 = arg2
        self.op = op
        self.type_ = Type.BOOL

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

    def get_value(self, context) -> Table:
        return context.aliases[str(self.alias) if self.alias else self.name]


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

    def get_value(self, context: ContextOn) -> bool:
        return self.cond.get_value(context)


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

    def inner_join(self, context: QueryContext) -> Table:
        table = []
        for l1 in self.table1.get_value(context).table:
            for l2 in self.table2.get_value(context).table:
                line = l1.copy()
                for key in self.table2.get_value(context).titles:
                    line[key] = l2[key]
                context_on = ContextOn()
                #context_on.tables[self.table1.get_value(context).name] = l1.copy()
                context_on.tables[self.table1.name] = l1.copy()
                if self.table1.alias:
                    context_on.tables[str(self.table1.alias)] = l1.copy()
                context_on.tables[self.table2.name] = l2.copy()
                if self.table2.alias:
                    context_on.tables[self.table2.alias] = l2.copy()
                if self.on.get_value(context_on):
                    table.append(line)
        titles = []
        titles.extend(self.table1.get_value(context).titles)
        titles.extend(self.table2.get_value(context).titles)
        return Table(self.table2.name + '_' + self.table1.name, titles, table)

    def get_value(self, context: QueryContext) -> Table:
        return self.inner_join(context)



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

    def __str__(self) -> str:
        return str("query")

    def cartesian_product(self, table1: Table, table2: Table) -> Table:
        table = []
        for l1 in table1.table:
            for l2 in table2.table:
                line = l1.copy()
                for key in table2.titles:
                    line[key] = l2[key]
                table.append(line)
        titles = []
        titles.extend(table1.titles)
        titles.extend(table2.titles)
        return Table(table2.name + '_' + table1.name, titles, table)


    def execute(self, context: QueryContext) -> Table:
        for child in self.childs:
            if isinstance(child, FromNode):
                child.full_up_context_table(context) # заносим таблицы из from в контекст
                table = child.childs[0].get_value(context)
                for i in range(1, len(child.childs)): # таблица может получиться с несколькими одинаковыми именами столбцов
                    table = self.cartesian_product(table, child.childs[i].get_value(context))

                return table

