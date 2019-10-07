from abc import ABC, abstractmethod
from typing import Callable, Tuple, Optional, Union


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


class TableNode(AstNode):
    def __init__(self, table_name: str):
        super().__init__()
        self.table_name = table_name

    def __str__(self)->str:
        return self.table_name


class SelectNode(AstNode):
    def __init__(self, col: ColumnNode):
        self.col = col

    @property
    def childs(self) -> Tuple[ColumnNode]:
        return self.col,

    def __str__(self)->str:
        return 'SELECT'


class FromNode(AstNode):
    def __init__(self, *table: Tuple[TableNode]):
        self.arg = (table[0])

    @property
    def childs(self) -> Tuple[TableNode]:
        return self.arg

    def __str__(self)->str:
        return 'FROM'


class QueryNode(AstNode):
    def __init__(self, select: SelectNode, from_: FromNode):
        super().__init__()
        self.select = select
        self.from_ = from_

    @property
    def childs(self) -> Tuple[SelectNode, FromNode]:
        return self.select, self.from_

    def __str__(self)->str:
        return str("query")
