import csv


def getLevel(filename):
    file = open(filename)
    type(file)
    reader = csv.reader(file)

    ret = []
    for row in reader:
        cells = []
        for cell in row:
            cells.append(int(cell))
        ret.append(cells)

    file.close()
    return ret
