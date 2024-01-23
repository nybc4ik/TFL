from collections.abc import Iterator
from dataclasses import dataclass, field
from typing import Deque, Optional, no_type_check_decorator

from parsing.table import EOS, EPSILON, SYNTHETIC_START, BuildTable, Grammarinfo, Table
from collections import deque


@dataclass
class Node:
    name: str
    parent: Optional["Node"] = None
    children: list["Node"] = field(default_factory=list, init=False)
    pos: Optional[int] = field(default=None, init=False)
    index: Optional[int] = field(default=None, init=False)
    _inherited: bool = field(default=False, init=False)

    def Print(self, indent: int) -> str:
        def printHelper(n: Node, d: int, indent: int) -> str:
            if n is None:
                return ""
            pref = ""
            for _ in range(d):
                pref += "┊" + " " * (indent - 1)
            pref += f"{n.name}[{n.pos},{n.index},{n._inherited}]\n"
            for c in n.children:
                pref += printHelper(c, d + 1, indent)
            return pref

        return printHelper(self, 0, indent)

    def findPos(self, pos: int) -> Optional["Node"]:
        if self.pos is not None:
            if self.pos == pos:
                return self
            elif self.pos > pos:
                return None

        res: Optional[Node] = None
        for c in self.children:
            res = c.findPos(pos)
            if res is not None and not (
                len(res.children) == 1 and res.children[0].name == EPSILON
            ):
                break
        return res

    def rightSibling(self) -> Optional["Node"]:
        if self.index is None:
            return None

        if self.parent is None:
            return None
        if self.index == len(self.parent.children) - 1:
            return self.parent.rightSibling()

        return self.parent.children[self.index + 1]

    def deduceNodePosition(self) -> Optional[int]:
        if self.pos is not None:
            return self.pos

        right = self.rightSibling()
        if right is None:
            return None

        res = right.deduceNodePosition()
        if res is not None:
            propogatePosition(self, res)
        return res

    def fixPos(self, e: int):
        if self.pos is None:
            return
        self.pos -= e
        for c in self.children:
            c.fixPos(e)


def propogatePosition(n: Node, p: int):
    assert n is not None

    n.pos = p
    while n.parent is not None and n.parent.pos is None:
        n = n.parent
        n.pos = p


def iterString(s: str) -> Iterator[str]:
    for c in s:
        yield c
    yield EOS


@dataclass
class LL1Parser:
    table: Table
    terms: set[str]
    d: Deque[Node] = field(init=False, default_factory=deque)

    def BuildTreeIncremental(self, s: str, lastParsedPos: int, n: int, d: Deque[Node]):
        if len(s) == 0:
            raise RuntimeError("cannot parse empty string")
        if n == 0:
            return

        charGen = iterString(s)
        current = next(charGen)

        self.d = d
        q: Deque[Node] = deque()
        i = 1
        while i <= n and len(self.d) > 0:
            front = self.d.popleft()
            if front.name in self.terms:
                if front.name != EPSILON:
                    propogatePosition(front, i + lastParsedPos)
                    i += 1
                    if front.name == EOS:
                        break
                    current = next(charGen)
                elif front.parent is not None and len(front.parent.children) == 1:
                    q.append(front)
                continue
            nextStack = self.table[front.name][current]
            if len(nextStack) == 0:
                raise RuntimeError("s ∉ L")

            buf: list[Node] = []
            for j in range(len(nextStack) - 1, -1, -1):
                item = nextStack[j]
                node = Node(item, front)
                node.index = j
                buf.append(node)
                self.d.appendleft(node)

            for j in range(len(buf) - 1, -1, -1):
                front.children.append(buf[j])

        while len(q) > 0:
            q.popleft().deduceNodePosition()

    def BuildTree(self, w: str) -> Optional[Node]:
        SPrime = Node(SYNTHETIC_START, None)

        d: Deque[Node] = deque()
        d.appendleft(SPrime)

        self.BuildTreeIncremental(w, 0, 10**10, d)
        return SPrime


def CopyUntil(pos: Optional[int], root: Node, d: Deque[Node]) -> Optional[Node]:
    if pos is None or pos == 0:
        return None
    return CopyUntilHelper(pos, root, None, d)


def CopyUntilHelper(pos: int, c: Node, p: Optional[Node], d: Deque[Node]) -> Node:
    n = Node(c.name, p)
    n.pos = c.pos
    n.index = c.index
    n._inherited = True

    if c.pos is None or c.pos > pos:
        n.pos = None
        d.append(n)
        return n

    for grandchild in c.children:
        n.children.append(CopyUntilHelper(pos, grandchild, n, d))

    return n


def incremental(w0: str, T0: Node, w1: str, info: Grammarinfo, greedy: bool) -> Node:
    t = BuildTable(info)
    p = LL1Parser(t, info.Terms)

    xLen = 0
    for xLen in range(len(w0)):
        if xLen == len(w1):
            break
        if w0[xLen] != w1[xLen]:
            break

    i = len(w0) - 1
    j = len(w1) - 1
    zLen = 0
    while i >= xLen and j >= xLen:
        if w0[i] != w1[j]:
            break
        zLen += 1
        i -= 1
        j -= 1

    T1: Node
    if xLen == 0:
        T1 = Node(SYNTHETIC_START, None)
        p.d.append(T1)
    else:
        T1 = CopyUntil(xLen, T0, p.d)

    NmPos = len(w0) - zLen + 1
    Nm = T0.findPos(NmPos)

    NmPrimePos = len(w1) - zLen + 1
    nToParse = len(w1) - xLen - zLen + 1
    w1 = f"{w1[xLen:]}{EOS}"
    lastParsedPos = xLen
    while True:
        p.BuildTreeIncremental(w1, lastParsedPos, nToParse, p.d)
        lastParsedPos += nToParse

        if nToParse >= len(w1):
            break
        else:
            w1 = w1[nToParse:]

        NmPrime = T1.findPos(NmPrimePos)
        if NmPrime is None:
            raise RuntimeError("w_1 ∉  L")

        oldNmPos = Nm.pos
        if Nm.name == NmPrime.pos:
            NmCopy = CopyUntil(10**10, Nm, deque())

            NmPrime.parent.children[NmPrime.index] = NmCopy
            NmCopy.parent = NmPrime.parent
            NmCopy.index = NmPrime.index

            posErr = NmCopy.pos - NmPrime.pos
            NmCopy.fixPos(posErr)

            Nm = Nm.rightSibling()
            if Nm is None:
                nToParse = len(w1)
                NmPrimePos += nToParse
                NmPos += nToParse
            else:
                nToParse = Nm.pos - oldNmPos
                NmPrimePos += nToParse
                NmPos += nToParse
        else:
            if greedy:
                Nm = Nm.rightSibling()
                if Nm is None:
                    nToParse = len(w1)
                    NmPrimePos += nToParse
                    NmPos += nToParse
                else:
                    nToParse = Nm.pos - oldNmPos
                    NmPrimePos += nToParse
                    NmPos += nToParse
            else:
                nToParse = 1
                NmPrimePos += 1
                NmPos += 1
                Nm = T0.findPos(NmPos)
    return T1
