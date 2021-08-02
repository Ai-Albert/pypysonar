class Position:
    def __init__(self, startRow, startCol, endRow, endCol):
        self.startRow = startRow
        self.startCol = startCol
        self.endRow = endRow
        self.endCol = endCol

    def __str__(self):
        return [self.startRow, self.startCol, self.endRow, self.endCol]










