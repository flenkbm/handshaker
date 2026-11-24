import numpy as np
import mediapipe.python.solutions.hands as mph
import mediapipe as mp
from math import sqrt


class Point3D():
    def __init__(self, x, y, z):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    @classmethod
    def ld(self, landmark):
        return self(landmark.x, landmark.y, landmark.z)

    def dist2D(self, other: "Point3D"):
        return sqrt((self.x - other.x)**2 + (self.y - other.x)**2)

    def dist3D(self, other: "Point3D"):
        return sqrt((self.x - other.x)**2 + (self.y - other.x)**2 + (self.z - other.z)**2)

    def ix(self): return int(self.x)
    def iy(self): return int(self.y)
    def iz(self): return int(self.z)