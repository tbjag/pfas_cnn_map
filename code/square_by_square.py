import numpy as np

x_size, y_size = 9, 12

random_array = np.random.randint(0, 10, size=(x_size, y_size))
print(random_array)

square_size = 3

range_length_x = x_size - (square_size // 2) - 1 # so cut down range by square size
range_length_y = y_size - (square_size // 2) - 1
print(f'range_length x: {range_length_x}, range_length y: {range_length_y}, square_size: {square_size}')
cnt = 0


for i in range(0, range_length_x, square_size): 
    
    for j in range(0, range_length_y, square_size):
        print(i, j) # should not go that far
        temp = np.empty((square_size, square_size), dtype=object) # dont need to initialize here
        for x in range(square_size):
            for y in range(square_size):
                temp[x, y] = random_array[i + x, j + y]
        print(temp)
        cnt +=1

# print(cnt)

# print(x_size, range_length_x)
# for j in range(0, range_length_y, 3):
#     print(j)