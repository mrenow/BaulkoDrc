x = dict(bananas = [2,4,6,7], oranges = [3,9,10,0], dildos = [69,8,7,5], apples = [1,2,3,4])
print(x)
y = list(x.items())
print(y)
print(y[0][1])
#x.update(vibrators = 69)
#print(x)

def takeSecond(elem):
    return elem[1][0]


y.sort(key = takeSecond)
print(y)
print(len(y))

z = sum([[(key,el) for el in x[key]] for key in x.keys()], [])
print(z)