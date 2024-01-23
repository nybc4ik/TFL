from dataclasses import dataclass, field
from common import Color
from graphs import utils

EPSILON = "ε"
EOS = "$"
START = "S"
SYNTHETIC_START = "S'"


@dataclass
class Grammarinfo:
    Terms: set[str] = field(default_factory=lambda: set((EOS, EPSILON)))
    Productions: dict[str, list[list[str]]] = field(
        default_factory=lambda: {SYNTHETIC_START: [[START, EOS]]}
    )


def safeKeyRemove(s: set[str], k: str):
    try:
        s.remove(k)
    except KeyError:
        ...


def getEpsInfo(info: Grammarinfo) -> dict[str, bool]:
    res: dict[str, bool] = {}
    visited: dict[str, Color] = {}
    for key in info.Productions:
        res[key] = False
        visited[key] = Color.WHITE

    def visitVar(v: str) -> bool:
        if visited[v] == Color.GREY:
            return True
        elif visited[v] == Color.BLACK:
            return res[v]
        visited[v] = Color.GREY

        isNullGenerating = False
        for _, prod in info.Productions[v]:
            isEpsProduction = True
            for c in prod:
                if c in info.Terms is not None:
                    if c == EPSILON:
                        continue
                    isEpsProduction = False
                    break
                isEpsProduction = isEpsProduction and visitVar(c)
                if not isEpsProduction:
                    break

            isNullGenerating = isNullGenerating or isEpsProduction
            if isNullGenerating:
                break

        res[v] = isNullGenerating
        visited[v] = Color.BLACK
        return isNullGenerating

    return res


def getFirstInfo(info: Grammarinfo, epsInfo: dict[str, bool]) -> dict[str, set[str]]:
    res: dict[str, set[str]] = {}

    dependencies: dict[str, set[str]] = {}
    for variable in info.Productions:
        res[variable] = set()
        dependencies[variable] = set()

    for v, prods in info.Productions.items():
        for prod in prods:
            for c in prod:
                if c in info.Terms:
                    res[v].add(c)
                    if c == EPSILON:
                        continue
                    break

                dependencies[v].add(c)
                if not epsInfo[c]:
                    break

    order = utils.TopoSort(dependencies)
    for v in order:
        for dep in dependencies[v]:
            res[v] = res[v].union(res[dep])

    return res


def strInfo(
    alpha: list[str],
    terms: set[str],
    epsInfo: dict[str, bool],
    firstInfo: dict[str, set[str]],
) -> set[str]:
    first: set[str] = set()
    if len(alpha) == 0:
        return first

    for c in alpha:
        if c in terms:
            if c == EPSILON:
                continue
            first.add(c)
            return first

        first = first.union(firstInfo[c])
        safeKeyRemove(first, EPSILON)
        if not epsInfo[c]:
            return first

    first.add(EPSILON)
    return first


def getFollowInfo(
    info: Grammarinfo, epsInfo: dict[str, bool], firstInfo: dict[str, set[str]]
) -> dict[str, set[str]]:
    followSets: dict[str, set[str]] = {}
    dependencies: dict[str, set[str]] = {}

    for variable in info.Productions:
        followSets[variable] = set()
        dependencies[variable] = set()

    for v, prods in info.Productions.items():
        for prod in prods:
            suffix = prod
            for f in prod:
                suffix = suffix[1:]
                if f in info.Terms:
                    continue
                suffixFirst = strInfo(suffix, info.Terms, epsInfo, firstInfo)
                producesEps = False
                if EPSILON in suffixFirst:
                    producesEps = True
                try:
                    safeKeyRemove(suffixFirst, EPSILON)
                except KeyError:
                    ...

                followSets[f].update(suffixFirst)
                if producesEps or len(suffixFirst) == 0:
                    dependencies[f].add(v)

    order = utils.TopoSort(dependencies)
    for v in order:
        for dep in dependencies[v]:
            followSets[v].update(followSets[dep])
            safeKeyRemove(followSets[v], EPSILON)

    return followSets


Table = dict[str, dict[str, list[str]]]


def BuildTable(info: Grammarinfo) -> Table:
    epsInfo = getEpsInfo(info)
    firstInfo = getFirstInfo(info, epsInfo)
    followInfo = getFollowInfo(info, epsInfo, firstInfo)

    res: Table = {}
    for v in info.Productions:
        res[v] = {}
        for t in info.Terms:
            res[v][t] = []

    for v, prods in info.Productions.items():
        for prod in prods:
            firstSet = strInfo(prod, info.Terms, epsInfo, firstInfo)
            eps = False
            if EPSILON in firstSet:
                eps = True

            safeKeyRemove(firstSet, EPSILON)
            for a in firstSet:
                if len(res[v][a]) != 0:
                    raise RuntimeError("provided grammar is NOT LL(1)")
                res[v][a] = prod

            if eps:
                if EOS in firstSet:
                    res[v][EOS].append(EPSILON)
                else:
                    for b in followInfo[v]:
                        res[v][b].append(EPSILON)

    return res
