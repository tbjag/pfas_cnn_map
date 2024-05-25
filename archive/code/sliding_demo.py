from collections import deque
import numpy as np

x = deque()
y = deque()
z = deque()

random_array = np.random.randint(0, 10, size=(9, 9))
print(random_array)

range_length = 9 - (3 // 2) - 1 # so cut down range by square size
print(range_length)

def pre_load(a, b, c, t):
    a.clear()
    b.clear()
    c.clear()

    for x in range(3):
        a.append(random_array[t, x])
        b.append(random_array[t + 1, x])
        c.append(random_array[t + 2, x])
    
    return a, b, c



# 9 * 9 -> 7 * 7
for t in range(range_length): 
    x, y, z = pre_load(x, y, z, t)
    print(f'x: {x}')
    print(f'y: {y}')
    print(f'z: {z}')
    for s in range(1, range_length):
        x.popleft()
        x.append(random_array[t, s + 2])
        y.popleft()
        y.append(random_array[t + 1, s + 2])
        z.popleft()
        z.append(random_array[t + 2, s + 2])


        print(f'x: {x}')
        print(f'y: {y}')
        print(f'z: {z}')



