import indexer
import parser


def main(filename):
    # code -> ast -> index
    with open(filename, 'r') as file:
        code = file.read()
        tree = parser.parse(code)
        index = indexer.index(tree)
        return index


if __name__ == "__main__":
    print(main("a.py"))
