import numpy as np
a = np.array([1,2])
b = np.array([10,2])
d = np.sqrt(np.sum((a-b)*(a-b)))
print(d)

a = np.array([0, 1, 1],dtype=float)
b = np.array([1, 1, 1],dtype=float)
cos_ = a.dot(b)/(np.sqrt(a.dot(a))*np.sqrt(b.dot(b)))
arccos_ = np.arccos(cos_)
theta = abs(arccos_*180/np.pi)
print(theta)


a = np.array([1, 2, 1])
print(a.dot(a))