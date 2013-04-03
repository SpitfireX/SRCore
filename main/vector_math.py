from math import sqrt

def vAdd(vec1, vec2):
    return (vec1[0] + vec2[0],
            vec1[1] + vec2[1],
            vec1[2] + vec2[2])

def sProd(vec1, vec2):
    return (vec1[0]*vec2[0] + vec1[1]*vec2[1] + vec1[2]*vec2[2])

def sMult(num, vec):
    return (vec[0]*num, vec[1]*num, vec[2]*num)

def vLen(vec):
    return sqrt(vec[0]**2 + vec[1]**2 + vec[2]**2)
