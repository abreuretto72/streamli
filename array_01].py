your_list = [1,2,3]
a = [i for i in your_list]
print( a )


a = [x+i for i in your_list for x in a]

print( a )



your_list = [1,2,3]
a = [i for i in your_list]
print( a )



b = []
for i in your_list:
    for x in a:
        b.append(x + i)
a = b

print( a )