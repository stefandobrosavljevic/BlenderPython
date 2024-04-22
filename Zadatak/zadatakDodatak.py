import math
import numpy as np


class Shape:
    def __init__(self, points):
        self.points = points

    def checkIfShape(self):
        raise NotImplementedError(
            "This method should be implemented by subclasses")

    def isPointInside(self, X):
        raise NotImplementedError(
            "This method should be implemented by subclasses")

    def distanceBetweenPoints(self, A, B):
        return math.sqrt((B[0] - A[0])**2 + (B[1] - A[1])**2)

    def calculateDiagonal(self):
        raise NotImplementedError(
            "This method should be implemented by subclasses")

    def isRightAngle(A, B, C):
        v1 = np.array(B) - np.array(A)
        v2 = np.array(B) - np.array(C)
        return np.isclose(np.dot(v1, v2), 0)


class Rectangle(Shape):
    def __init__(self, points):
        super().__init__(points)
        self.A, self.B, self.C = self.points

    def checkIfShape(self):
        if self.A == self.B or self.A == self.C or self.B == self.C:
            return False

        # setX = set([self.A[0], self.B[0], self.C[0]])
        # setY = set([self.A[1], self.B[1], self.C[1]])
        # return len(setX) == len(setY) == 2

        d1 = (self.A[0] - self.B[0])**2 + (self.A[1] - self.B[1])**2
        d2 = (self.B[0] - self.C[0])**2 + (self.B[1] - self.C[1])**2
        d3 = (self.C[0] - self.A[0])**2 + (self.C[1] - self.A[1])**2

        if d1 == d2 + d3 or d2 == d1 + d3 or d3 == d1 + d2:
            return True
        else:
            return False

    def isPointInside(self, X):
        min_x = min(self.A[0], self.B[0], self.C[0])
        max_x = max(self.A[0], self.B[0], self.C[0])
        min_y = min(self.A[1], self.B[1], self.C[1])
        max_y = max(self.A[1], self.B[1], self.C[1])

        if min_x <= X[0] <= max_x and min_y <= X[1] <= max_y:
            return True
        else:
            return False

    def calculateDiagonal(self):
        AB = self.distanceBetweenPoints(self.A, self.B)
        AC = self.distanceBetweenPoints(self.A, self.C)
        BC = self.distanceBetweenPoints(self.B, self.C)

        return max(AB, AC, BC)


class Cuboid(Shape):
    def __init__(self, points):
        super().__init__(points)
        self.A, self.B, self.C, self.D = self.points

    def checkIfShape(self):
        # if self.A == self.B or self.A == self.C or self.A == self.D or self.B == self.C or self.B == self.D or self.C == self.D:
        #     return False

        # setX = set([self.A[0], self.B[0], self.C[0], self.D[0]])
        # setY = set([self.A[1], self.B[1], self.C[1], self.D[1]])
        # setZ = set([self.A[2], self.B[2], self.C[2], self.D[2]])

        # return len(setX) == len(setY) == len(setZ) == 2
        pass

    def isPointInside(self, X):
        return False

    def calculateDiagonal(self):
        return 1


def loadData(data_file):
    with open(data_file, 'r') as file:
        try:
            points = [tuple(map(float, line.strip().split(",")))
                      for line in file]
            return points
        except ValueError:
            print("Kordinate tačaka u fajlu nisu ispravne")
            return None


def identifyRectangleType(points):
    if len(points) == 4 and len(points[0]) == 2:
        rectangle = Rectangle(points[:3])
        return rectangle
    if len(points) == 5 and len(points[0]) == 3:
        cuboid = Cuboid(points[:4])
        return cuboid


def main():
    points = loadData("data.txt")
    if not points:
        print("Nije učitano nista iz datoteke")
        return False

    shape = identifyRectangleType(points)
    if shape.checkIfShape():
        print(
            f"Tačke A, B i C prave {'pravougaonik' if len(points)==4 else 'kvadar'}")
    else:
        print(
            f"Tačke A, B i C ne prave {'pravougaonik' if len(points)==4 else 'kvadar'}")
        return False

    if shape.isPointInside(points[-1]):
        print(
            f"Tačka X se nalazi unutar {'pravougaonik' if len(points)==4 else 'kvadar'}")
    else:
        print(
            f"Tačka X se ne nalazi unutar {'pravougaonik' if len(points)==4 else 'kvadar'}")

    diagonal = shape.calculateDiagonal()
    print(f"Dijagonala iznosi {diagonal}")


if __name__ == "__main__":
    main()
