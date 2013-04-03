from math import sqrt

class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
def vadd(vec1, vec2):
    return Vector(vec1.x + vec2.x,
                  vec1.y + vec2.y,
                  vec1.z + vec2.z)
    
def sprod(vec1, vec2):
    return vec1.x*vec2.x + vec1.y*vec2.y + vec1.z*vec2.z

def smult(vec, num):
    return Vector(vec.x*num, vec.y*num, vec.z*num)

def vlen(vec):
    return sqrt(vec.x**2 + vec.y**2 + vec.z**2)