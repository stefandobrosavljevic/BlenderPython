import numpy as np


class Shape:
    def __init__(self, points):
        self.points = np.array(points)

    def check_shape(self):
        raise NotImplementedError(
            "This method should be implemented by subclasses")

    def is_point_inside(self, X):
        raise NotImplementedError(
            "This method should be implemented by subclasses")

    def distance_between_points(self, p1, p2):
        return np.linalg.norm(p1 - p2)

    def calculate_diagonal(self):
        raise NotImplementedError(
            "This method should be implemented by subclasses")

    def is_right_angle(self, A, B, C):
        v1 = B - A
        v2 = B - C
        return np.isclose(np.dot(v1, v2), 0)


class Rectangle(Shape):
    def __init__(self, points):
        super().__init__(points)

    def __str__(self) -> str:
        return "Četvorougao"

    def check_if_inside(self):
        # Da su stranice pravougaonika paralelene sa koordinatnim sistemom
        # ne bi morali da koristimo matematiku, moglo je samo racunanjem
        # broja kordinata pomocu seta i taj broj bi morao da bude 2 za 2D
        # setX = set([self.A[0], self.B[0], self.C[0]])
        # setY = set([self.A[1], self.B[1], self.C[1]])
        # return len(setX) == len(setY) == 2

        A, B, C = self.points[:3]

        return (self.is_right_angle(A, B, C) or
                self.is_right_angle(B, A, C) or
                self.is_right_angle(A, C, B))

    def is_point_inside(self, X):
        min_coords = self.points.min(axis=0)
        max_coords = self.points.max(axis=0)
        return np.all(min_coords <= X) and np.all(X <= max_coords)

    def calculate_diagonal(self):
        A, B, C = self.points[:3]
        AB = self.distance_between_points(A, B)
        AC = self.distance_between_points(A, C)
        BC = self.distance_between_points(B, C)

        return max(AB, AC, BC)


class Cuboid(Shape):
    def __init__(self, points):
        super().__init__(points)

    def __str__(self) -> str:
        return "Kvadar"

    def check_if_shape(self):
        # da su stranice kvadra paralelne sa XYZ koordinatnim sistemom moglo bi ovako bez matematike
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
        A, B, C, D = self.points[:4]
        # Tacka A, a je u sredini
        dotA = self.is_right_angle(B, A, C) and self.is_right_angle(
            D, A, C) and self.is_right_angle(D, A, B)

        # Tacka B, a je u sredini
        dotB = self.is_right_angle(A, B, C) and self.is_right_angle(
            D, B, C) and self.is_right_angle(D, B, A)

        # Tacka C, a je u sredini
        dotC = self.is_right_angle(A, C, B) and self.is_right_angle(
            A, C, D) and self.is_right_angle(B, C, D)

        # Tacka D, a je u sredini
        dotD = self.is_right_angle(A, D, B) and self.is_right_angle(
            A, D, C) and self.is_right_angle(B, D, C)

        return dotA or dotB or dotC or dotD

    def is_point_inside(self, X):
        min_coords = self.points.min(axis=0)
        max_coords = self.points.max(axis=0)
        return np.all(min_coords <= X) and np.all(X <= max_coords)

    def calculate_diagonal(self):
        """
        Nađu se sve tačke kvadra, zatim se nađe svaka dužina između svih tačaka
        i od njih se nađe maksimalna.
        """
        all_points = np.concatenate(
            (self.points, self.find_remain_points()), axis=0)
        max_distance = 0
        for i in range(len(all_points)):
            for j in range(i + 1, len(all_points)):
                distance = self.distance_between_points(
                    all_points[i], all_points[j])
                if distance > max_distance:
                    max_distance = distance
        return max_distance

    def find_remain_points(self):
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

        return np.array([E, F, G, H])


def load_data(data_file):
    try:
        with open(data_file, 'r') as file:
            points = [tuple(map(float, line.strip().split(",")))
                      for line in file]
        return points
    except ValueError:
        print("Kordinate tačaka u fajlu nisu ispravne")
        return None


def identify_shape(points):
    if len(points) == 3 and all(len(p) == 2 for p in points):
        return Rectangle(points)
    elif len(points) == 4 and all(len(p) == 3 for p in points):
        return Cuboid(points)
    else:
        raise ValueError("Neispravan broj tačaka ili dimenzija")


def main():
    points = load_data("data.txt")
    if points is None:
        print("Nije učitano nista iz datoteke")
        return

    try:
        if not all(len(p) == len(points[0]) for p in points):
            raise ValueError("Neispravan broj dimenzija tačaka")
        points = np.array(points)
        shape = identify_shape(points[:-1])
        if shape.check_if_shape():
            print(
                f"Tačke iz datoteke kreiraju {shape}")
        else:
            print(
                f"Tačke iz datoteke ne kreiraju {shape}")
            return

        if shape.is_point_inside(points[-1]):
            print(
                f"TRUE. Tačka X se NALAZI unutar {shape}.")
        else:
            print(
                f"FALSE. Tačka X se NE NALAZI unutar {shape}.")

        print(f"Dijagonala {shape} iznosi {shape.calculate_diagonal()}")
    except Exception as e:
        print(f"Greška {e}")


if __name__ == "__main__":
    main()
