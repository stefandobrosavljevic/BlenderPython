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

    def isRightAngle(self, A, B, C):
        v1 = np.array(B) - np.array(A)
        v2 = np.array(B) - np.array(C)
        return np.isclose(np.dot(v1, v2), 0)


class Rectangle(Shape):
    def __init__(self, points):
        super().__init__(points)
        self.A, self.B, self.C = self.points

    def checkIfShape(self):
        # Da su stranice pravougaonika paralelene sa koordinatnim sistemom
        # ne bi morali da koristimo matematiku, moglo je samo racunanjem
        # broja kordinata pomocu seta i taj broj bi morao da bude 2 za 2D
        # setX = set([self.A[0], self.B[0], self.C[0]])
        # setY = set([self.A[1], self.B[1], self.C[1]])
        # return len(setX) == len(setY) == 2

        return (self.isRightAngle(self.A, self.B, self.C) or
                self.isRightAngle(self.B, self.A, self.C) or
                self.isRightAngle(self.A, self.C, self.B))

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
        # da su stranice kvadra palalelne sa XYZ koordinatnim sistemom moglo bi ovako bez matematike
        # if self.A == self.B or self.A == self.C or self.A == self.D or self.B == self.C or self.B == self.D or self.C == self.D:
        #     return False
        # setX = set([self.A[0], self.B[0], self.C[0], self.D[0]])
        # setY = set([self.A[1], self.B[1], self.C[1], self.D[1]])
        # setZ = set([self.A[2], self.B[2], self.C[2], self.D[2]])
        # return len(setX) == len(setY) == len(setZ) == 2
        """
        Treba proveriti da li jedna tacka ima 3 ugla od 90 stepeni sa ostalim tackama
        pomocu skalarnog mnozenja vektora.
        Treba proveriti za svaku tacku u odnosu na sve ostale. 4x3=12 dot mnozenja.

        !! jedini slucaj koji se ne pokriva je taj ako se daju tacke izmedju kojih ne postoji ni jedan
        ugao od 90 stepeni, mogu da se daju tacke suprotne u odnosu na dijagonalu, ali to nema smisla.
        """
        # Tacka A, a je u sredini
        dotA = self.isRightAngle(self.B, self.A, self.C) and self.isRightAngle(
            self.D, self.A, self.C) and self.isRightAngle(self.D, self.A, self.B)

        # Tacka B, a je u sredini
        dotB = self.isRightAngle(self.A, self.B, self.C) and self.isRightAngle(
            self.D, self.B, self.C) and self.isRightAngle(self.D, self.B, self.A)

        # Tacka C, a je u sredini
        dotC = self.isRightAngle(self.A, self.C, self.B) and self.isRightAngle(
            self.A, self.C, self.D) and self.isRightAngle(self.B, self.C, self.D)

        # Tacka D, a je u sredini
        dotD = self.isRightAngle(self.A, self.D, self.B) and self.isRightAngle(
            self.A, self.D, self.C) and self.isRightAngle(self.B, self.D, self.C)

        return dotA or dotB or dotC or dotD

    def isPointInside(self, X):
        points = np.array(self.points)
        min_x = min(points[:, 0])
        max_x = max(points[:, 0])
        min_y = min(points[:, 1])
        max_y = max(points[:, 1])
        min_z = min(points[:, 2])
        max_z = max(points[:, 2])

        if min_x <= X[0] <= max_x and min_y <= X[1] <= max_y and min_z <= X[2] <= max_z:
            return True
        else:
            return False

    def calculateDiagonal(self):
        remain_points = self.findRemainPoints()
        all_points = []
        for p in self.points:
            all_points.append(np.array(p))

        all_points += remain_points
        print(all_points)
        max_distance = 0
        n = len(all_points)

        # Calculate the distance between each pair of points
        for i in range(n):
            for j in range(i + 1, n):
                distance = np.linalg.norm(all_points[i] - all_points[j])
                if distance > max_distance:
                    max_distance = distance

        return max_distance

    def findRemainPoints(self):
        """
        uslov je da je A korner i da su ostale tacke direktni susedi
        """
        A, B, C, D = self.points  # Assuming you know A, B, C, D are correctly part of a cuboid
        vec_AB = np.array(B) - np.array(A)
        vec_AD = np.array(D) - np.array(A)
        vec_AC = np.array(C) - np.array(A)
        E = C + vec_AD
        F = C + vec_AB
        G = D + vec_AB
        H = G + vec_AC

        return [E, F, G, H]


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
