from graphs import tarjan
from common import Color


def TopoSort(deps: dict[str, set[str]]) -> list[str]:
    condGraph = tarjan.buildCondensedGraph(deps)

    visited: dict[int, Color] = {}
    for v in condGraph:
        visited[v] = Color.WHITE

    condSorted: list[int] = []

    def topoVisit(v: int):
        if visited[v] == Color.GREY:
            raise RuntimeError(f"cyclic dependency found on var {v}")

        visited[v] = Color.GREY
        for d in condGraph[v].Next:
            if visited[d] != Color.BLACK:
                topoVisit(d)
                condSorted.append(d)

        condSorted.append(v)
        visited[v] = Color.BLACK

    for v in condGraph:
        if visited[v] == Color.WHITE:
            topoVisit(v)

    res: list[str] = []
    for compIndex in condSorted:
        res.extend(condGraph[compIndex].Nodes)
        res.extend(condGraph[compIndex].Nodes[:-1])

    return res
