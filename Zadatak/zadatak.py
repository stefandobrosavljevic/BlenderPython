import math


def loadData(data_file):
    with open(data_file, 'r') as file:
        points = [tuple(map(float, line.strip().split(","))) for line in file]
        return points


def checkRectagleFromPoints(A, B, C):
    if A == B or A == C or B == C:
        return False

    d1 = (A[0] - B[0])**2 + (A[1] - B[1])**2
    d2 = (B[0] - C[0])**2 + (B[1] - C[1])**2
    d3 = (C[0] - A[0])**2 + (C[1] - A[1])**2

    if d1 == (d2 + d3) or d2 == (d1 + d3) or d3 == (d1 + d2):
        return True

    return False


def isInside(A, B, C, X):
    min_x = min(A[0], B[0], C[0])
    max_x = max(A[0], B[0], C[0])
    min_y = min(A[1], B[1], C[1])
    max_y = max(A[1], B[1], C[1])

    if min_x <= X[0] <= max_x and min_y <= X[1] <= max_y:
        return True
    else:
        return False


def distanceBetweenPoints(A, B):
    return math.sqrt((B[0] - A[0])**2 + (B[1] - A[1])**2)


def calculateDiagonal(A, B, C):
    AB = distanceBetweenPoints(A, B)
    AC = distanceBetweenPoints(A, C)
    BC = distanceBetweenPoints(B, C)

    return max(AB, AC, BC)


def main():
    points = loadData("data.txt")
    if not points or len(points) != 4:
        print("Nije učitano 4 tačaka iz datoteke")
        return False

    A, B, C, X = points
    if not checkRectagleFromPoints(A, B, C):
        print("Tačke A, B i C ne prave pravougaonik")
        return False

    print("Tačke A, B i C prave pravougaonik")

    if isInside(A, B, C, X):
        print("Tačka X se nalazi unutar pravougaonika")
    else:
        print("Tačka X se ne nalazi unutar pravougaonika")

    diagonal = calculateDiagonal(A, B, C)

    print(f"Dijagonala pravougaonika sa tačkama ABC iznosi {diagonal}")


if __name__ == "__main__":
    main()
