from dataclasses import dataclass, field

from common import Color


@dataclass
class condensedNode:
    Next: set[int] = field(default_factory=set, init=False)
    Nodes: list[str] = field(default_factory=list, init=False)


Stack = list


@dataclass
class tarjanTraverser:
    graph: dict[str, set[str]]
    visited: dict[str, Color] = field(default_factory=dict, init=False)
    compCount: int = field(default=0, init=False)
    s: Stack = field(default_factory=list, init=False)
    time: int = field(default=0, init=False)
    node2group: dict[str, int] = field(default_factory=dict, init=False)
    group2component: dict[int, int] = field(default_factory=dict, init=False)
    components: dict[int, condensedNode] = field(default_factory=dict, init=False)

    def __post_init__(self) -> None:
        for key in self.graph:
            self.visited[key] = Color.WHITE
            self.node2group[key] = 0

        for parent in self.graph:
            if self.visited[parent] == Color.WHITE:
                self.visit(parent)

    def visit(self, p: str):
        self.time += 1
        self.s.append(p)
        tin = self.time
        self.node2group[p] = tin

        self.visited[p] = Color.GREY
        for c in self.graph[p]:
            if self.visited[c] == Color.WHITE:
                self.visit(c)
                self.node2group[p] = min(self.node2group[p], self.node2group[c])
            elif self.visited[c] == Color.GREY:
                self.node2group[p] = min(self.node2group[p], self.node2group[c])

        self.visited[p] = Color.BLACK

        if self.node2group[p] != tin:
            return

        self.group2component[self.node2group[p]] = self.compCount
        condNode = condensedNode()
        while True:
            top = self.s.pop()
            condNode.Nodes.append(top)
            for child in self.graph[top]:
                childComp = self.group2component[self.node2group[child]]
                if childComp == self.compCount:
                    continue
                condNode.Next.add(childComp)

            if top == p:
                break

        self.components[self.compCount] = condNode
        self.compCount += 1


def buildCondensedGraph(graph: dict[str, set[str]]) -> dict[int, condensedNode]:
    tr = tarjanTraverser(graph)
    return tr.components
