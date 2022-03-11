# from matplotlib.pyplot import draw
import pygame
pygame.init()
size = 40

#Set-up Color:
BLACK = (5, 5, 5)
BLACK_1 = (10, 10, 10)
WHITE = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
COLOR_ARR = [(106, 141, 132), (164, 121, 195), (184, 221, 171), (62, 216, 197), (179, 178, 44), (49, 218, 86)]

#Draw Rectangle function:
def draw_rect(color, point):
    pygame.draw.rect(screen, color, (int(point[0]) * size, int(point[1]) * size, size, size))

def to_int(arr_point):
    for i in range(0, len(arr_point)):
        arr_point[i] = (int(arr_point[i][0]), int(arr_point[i][1]))

def add_obs(arr, point1, point2):
    delta_x = point2[0] - point1[0]
    delta_y = point2[1] - point1[1]
    
    x, y = point1[0], point1[1]
    if delta_x > 0 and delta_y > 0:
        while(x != point2[0] and y != point2[1]):
            x = x + 1
            y = y + 1
            arr.append((x, y))
    elif delta_x > 0 and delta_y < 0:
        while(x != point2[0] and y != point2[1]):
            x = x + 1
            y = y - 1
            arr.append((x, y))
    elif delta_x < 0 and delta_y > 0:
        while(x != point2[0] and y != point2[1]):
            x = x - 1
            y = y + 1
            arr.append((x, y))
    elif delta_x < 0 and delta_y < 0:
        while(x != point2[0] and y != point2[1]):
            x = x - 1
            y = y - 1
            arr.append((x, y))

    if x == point2[0]:
        if y < point2[1]:
            for i in range(y + 1, point2[1]):
                arr.append((x, i))
        else:
            for i in range(point2[1] + 1, y):
                arr.append((x, i))
    if y == point2[1]:
        if x < point2[0]:
            for i in range(x + 1, point2[0]):
                arr.append((i, y))
        else:   
            for i in range(point2[0] + 1, x):
                arr.append((i, y))
f = open("text.txt",mode = 'r',encoding = 'utf-8')


#Lay size - kich thuoc ma tran
arr1 = f.readline()
arr1 = arr1.split()
length = int(arr1[0])
width =  int(arr1[1])

screen = pygame.display.set_mode((length * size, width * size))


#Lay start, end - diem bat dau, ket thuc
arr2 = f.readline()
arr2 = arr2.split()
source_point = (int(arr2[0]), int(arr2[1]))
goal_point   = (int(arr2[2]), int(arr2[3]))
print(goal_point)

#Lay obstacles -chuong ngai vat
obstacles_n = int(f.readline())
obstacles_arr = []
for i in range(0, obstacles_n):
    arr = f.readline()
    arr = arr.split()
    temp = []

    for j in range(0, len(arr) // 2):
        temp.append((arr[2 * j], arr[2 * j + 1]))
    to_int(temp)
    obstacles_arr.append(temp)

arr = []
# Add Obstacles
for obs in obstacles_arr:
    for i in range(0, len(obs) - 1):
        add_obs(arr, obs[i], obs[i + 1])
    add_obs(arr, obs[len(obs) - 1], obs[0])
obstacles_arr.append(arr)
print("Obstacles: ")
print(obstacles_arr)


# DFS - Search
DFS_Stack = []
temp_arr = []
DFS_Stack.append(source_point)
while goal_point not in DFS_Stack:
    topPoint = DFS_Stack[len(DFS_Stack) - 1]
    x = topPoint[0]
    y = topPoint[1]
    if ((x + 1, y) not in DFS_Stack and (x + 1, y) not in temp_arr and 0 <= x + 1 < length and 0 <= y < width):
        check = True
        for obs in obstacles_arr:
            if (x + 1, y) in obs:
                check = False
                break
        if check:
            DFS_Stack.append((x + 1, y))
        else:
            temp_arr.append((x + 1, y))
    elif ((x, y + 1) not in DFS_Stack and (x, y + 1) not in temp_arr and 0 <= x < length and 0 <= y + 1 < width):
        check = True
        for obs in obstacles_arr:
            if (x, y + 1) in obs:
                check = False
                break
        if check:
            DFS_Stack.append((x, y + 1))
        else:
            temp_arr.append((x, y + 1))
    elif ((x - 1, y) not in DFS_Stack and (x - 1, y) not in temp_arr and 0 <= x - 1 < length and 0 <= y < width):
        check = True
        for obs in obstacles_arr:
            if (x - 1, y) in obs:
                check = False
                break
        if check:
            DFS_Stack.append((x - 1, y))
        else:
            temp_arr.append((x - 1, y))
    elif ((x, y - 1) not in DFS_Stack and (x, y - 1) not in temp_arr and 0 <= x < length and 0 <= y - 1 < width):
        check = True
        for obs in obstacles_arr:
            if (x, y - 1) in obs:
                check = False
                break
        if check:
            DFS_Stack.append((x, y - 1))
        else:
            temp_arr.append((x, y - 1))
    else:
        temp = DFS_Stack.pop()
        temp_arr.append(temp)

print("\n\n", DFS_Stack, "\n\n")
run = True
while run:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    for i in range(0, length):
        for j in range(0, width):
            if (i + j) % 2 == 0:
                draw_rect(BLACK_1, (i, j))
    for i in range(0, obstacles_n + 1):
        for j in range(0, len(obstacles_arr[i])):
            draw_rect(RED, obstacles_arr[i][j])
            if i == obstacles_n:
                draw_rect(RED, obstacles_arr[i][j])

    for i in range(0, len(DFS_Stack)):
        if(i % 5 == 0):
            draw_rect(COLOR_ARR[0], DFS_Stack[i])
        else:
            draw_rect(COLOR_ARR[2], DFS_Stack[i])


    draw_rect(BLUE, source_point)
    draw_rect(BLUE, goal_point)
    pygame.display.flip()

