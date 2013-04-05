from math import sqrt

def vAdd(vec1, vec2):
    return ( v1 + v2 for v1, v2 in zip(vec1, vec2) )

def sProd(vec1, vec2):
    return reduce(lambda s,v: s+v[0]*v[1], zip(vec1, vec2), 0)

def sMult(num, vec):
    return ( num * v for v in vec )

def vLen(vec):
    return sqrt(sProd(vec,vec))
