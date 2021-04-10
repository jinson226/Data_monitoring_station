import numpy as np
a=[[['aaa',22],['bbb',33],['ccc',44],['aaa',33],['jj',89],['jj',99]]]
arr = []
b = []
c = []
d = []
for i in range(len(a[0])):
    if a[0][i][0] not in b:
        arr.append(a[0][i])
    b.append(a[0][i][0])
for i in range(len(arr)):
    c.append(arr[i][0])
    d.append(arr[i][1])
print(arr)
