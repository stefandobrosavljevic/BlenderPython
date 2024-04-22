import numpy as np


def load_data(data_file):
    try:
        with open(data_file, 'r') as file:
            points = [tuple(map(float, line.strip().split(",")))
                      for line in file]
        if len(points) != 4:
            raise ValueError("Fajl mora da ima tacno 4 tačke")
        return points
    except Exception as e:
        print(f"Greška prilikom učitavanja podataka {e}")
        return None


def is_right_angle(p1, p2, p3):
    """
    Odredjuje da li je ugao izmedju A-B-C prav ugao (90 stepeni u tacki B)
    """
    v1 = np.array(p2) - np.array(p1)
    v2 = np.array(p2) - np.array(p3)
    return np.isclose(np.dot(v1, v2), 0)


def check_rectagle_from_points(A, B, C):
    """
    Kod pomocu pitagorine teoreme
    if A == B or A == C or B == C:
        return False
    d1 = (A[0] - B[0])**2 + (A[1] - B[1])**2
    d2 = (B[0] - C[0])**2 + (B[1] - C[1])**2
    d3 = (C[0] - A[0])**2 + (C[1] - A[1])**2
    if d1 == (d2 + d3) or d2 == (d1 + d3) or d3 == (d1 + d2):
        return True
    return False

    """

    return (is_right_angle(A, B, C) or is_right_angle(B, A, C) or is_right_angle(A, C, B))


def is_inside(p1, p2, p3, pX):
    """
    Odredjuje da li se tacka X nalazi unutar cetvorougla sa kordinatama p1,p2,p3
    """
    coords = np.array([p1, p2, p3])
    min_coords = coords.min(axis=0)
    max_coords = coords.max(axis=0)
    return np.all(min_coords <= pX) and np.all(pX <= max_coords)


def distance(A, B):
    """
    Odredjuje distancu pomocu Euklidove udaljenosti
    """
    return np.linalg.norm(np.array(A) - np.array(B))


def calculate_diagonal(A, B, C):
    """
    Izracunava se duzina izmedju svih tacaka i odredjuje se najveca od njih
    """
    AB = distance(A, B)
    AC = distance(A, C)
    BC = distance(B, C)

    return max(AB, AC, BC)


def main():
    points = load_data("data.txt")
    if points is None:
        return

    A, B, C, X = points
    if not check_rectagle_from_points(A, B, C):
        print("Tačke A, B i C ne prave pravougaonik")
        return

    print("Tačke A, B i C prave pravougaonik")
    if is_inside(A, B, C, X):
        print("Tačka X se nalazi unutar pravougaonika")
    else:
        print("Tačka X se ne nalazi unutar pravougaonika")

    diagonal = calculate_diagonal(A, B, C)
    print(f"Dijagonala pravougaonika sa tačkama ABC iznosi {diagonal}")


if __name__ == "__main__":
    main()
