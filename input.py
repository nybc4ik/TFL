from io import TextIOWrapper
from typing import Optional
from parsing.table import SYNTHETIC_START, Grammarinfo


def split_string(target: str, sep: str) -> Optional[tuple[str, str]]:
    search_res = target.find(sep)
    if search_res == -1:
        return None
    return target[:search_res].strip(), target[search_res + 2 :].strip()


def read_word(r: TextIOWrapper, name: str) -> str:
    inputLine = r.readline().strip()
    if len(inputLine) == 0:
        raise RuntimeError(f"expected number of lines of {name}")

    w0Size = int(inputLine)

    w = ""
    for _ in range(w0Size):
        inputLine = r.readline()
        if len(inputLine) == 0:
            raise RuntimeError(f"expected more input for {name}")
        w += str(inputLine)
    return w


def ParseInput(r: TextIOWrapper) -> tuple[str, str, str, Grammarinfo]:
    strat = str(r.readline().strip())
    info = Grammarinfo()

    nonTerminalsStr = str(r.readline()).strip()
    for term in nonTerminalsStr.split(","):
        term = term.strip()
        if len(term) != 1:
            raise RuntimeError(
                "wrong terminal declaration [1]: terminal length has to be 1"
            )

        info.Terms.add(term)

    lineNumber = 1
    while True:
        productionStr = r.readline()
        if len(productionStr) == 0:
            raise RuntimeError("no input was given to parse")
        lineNumber += 1
        productionStr = productionStr.strip()
        if len(productionStr) == 0:
            break

        splitRes = split_string(str(productionStr), "->")
        if splitRes is None:
            raise RuntimeError(f"[{lineNumber}]: wrong production")

        lhs, rhs = splitRes

        if lhs == SYNTHETIC_START:
            raise RuntimeError(
                f"[{lineNumber}]: {SYNTHETIC_START} is reserved, pick another name"
            )

        if lhs in info.Productions:
            raise RuntimeError(f"[{lineNumber}]: {lhs} was already defined")

        info.Productions[lhs] = []

        rightProductions = rhs.split("|")
        for i in range(len(rightProductions)):
            rightProductions[i] = rightProductions[i].strip()
            if len(rightProductions[i]) == 0:
                raise RuntimeError(f"[{lineNumber}]: {lhs} has empty production")

            vars = rightProductions[i].split()
            info.Productions[lhs].append(vars)

    w0 = read_word(r, "w0").strip()
    w1 = read_word(r, "w1").strip()

    return strat, w0, w1, info
