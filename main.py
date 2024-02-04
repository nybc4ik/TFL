from input import ParseInput
from parsing.parser import LL1Parser, incremental
from parsing.table import BuildTable


def main():
    f = open("input.txt")
    info = ParseInput(f)
    f.close()

    siblingStart = "sibling"
    
    w0=input("Please, write w0 word\n")
    w1=input("Please, write w1 word\n")

    table = BuildTable(info)
    p = LL1Parser(table, info.Terms)

    T0 = p.BuildTree(w0)
    assert T0 is not None

    print("T0:")
    print(T0.Print(4))

    T1 = incremental(w0, T0, w1, info, siblingStart)
    print("T1:")
    print(T1.Print(4))


if __name__ == "__main__":
    main()
