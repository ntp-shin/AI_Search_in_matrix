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

def distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

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

# Ham phuc vu
def top(p):
    return p[0], p[1] - 1
def bot(p):
    return p[0], p[1] + 1
def left(p):
    return p[0] - 1, p[1]
def right(p):
    return p[0] + 1, p[1]
def isInList(p, list):
    for arr in list:
        if p in arr:
            return True
    return False

# DFS - Search
DFS_Stack = []
temp_DFS = []
DFS_Stack.append(source_point)
while goal_point not in DFS_Stack:
    if DFS_Stack == []:
        break
    topPoint = DFS_Stack[-1]
    x = topPoint[0]
    y = topPoint[1]
    tren = top(topPoint)
    duoi = bot(topPoint)
    phai = right(topPoint)
    trai = left(topPoint)
    if (phai not in DFS_Stack and phai not in temp_DFS and 0 <= phai[0] < length and 0 <= phai[1] < width):
        if not isInList(phai, obstacles_arr):
            DFS_Stack.append(phai)
        else:
            temp_DFS.append(phai)
    elif (duoi not in DFS_Stack and duoi not in temp_DFS and 0 <= duoi[0] < length and 0 <= duoi[1] < width):
        if not isInList(duoi, obstacles_arr):
            DFS_Stack.append(duoi)
        else:
            temp_DFS.append(duoi)
    elif (trai not in DFS_Stack and trai not in temp_DFS and 0 <= x - 1 < length and 0 <= y < width):
        if not isInList(trai, obstacles_arr):
            DFS_Stack.append(trai)
        else:
            temp_DFS.append(trai)
    elif (tren not in DFS_Stack and tren not in temp_DFS and 0 <= x < length and 0 <= y - 1 < width):
        if not isInList(tren, obstacles_arr):
            DFS_Stack.append(tren)
        else:
            temp_DFS.append(tren)
    else:
        temp = DFS_Stack.pop()
        temp_DFS.append(temp)

print("\n\n", DFS_Stack, "\n\n")

# BFS -Search
BFS_Queue = []
temp_BFS = []
path_BFS = []
BFS_Queue.append(source_point)
current = source_point
find = True
while goal_point not in temp_BFS:
    tren = top(current)
    duoi = bot(current)
    phai = right(current)
    trai = left(current)
    if (phai not in BFS_Queue and phai not in temp_BFS and 0 <= phai[0] < length and 0 <= phai[1] < width):
        if not isInList(phai, obstacles_arr):
            BFS_Queue.insert(0, phai)
    if (duoi not in BFS_Queue and duoi not in temp_BFS and 0 <= duoi[0] < length and 0 <= duoi[1] < width):
        if not isInList(duoi, obstacles_arr):
            BFS_Queue.insert(0, duoi)
    if (trai not in BFS_Queue and trai not in temp_BFS and 0 <= trai[0] < length and 0 <= trai[1] < width):
        if not isInList(trai, obstacles_arr):
            BFS_Queue.insert(0, trai)
    if (tren not in BFS_Queue and tren not in temp_BFS and 0 <= tren[0] < length and 0 <= tren[1] < width):
        if not isInList(tren, obstacles_arr):
            BFS_Queue.insert(0, tren)

    current = BFS_Queue.pop()
    if BFS_Queue == []:
        find = False
        break
    if current not in temp_BFS:
        temp_BFS.append(current)

BFS_Queue = []
BFS_Queue.append(source_point)
notOk = []
while find and goal_point not in BFS_Queue:
    current = BFS_Queue[len(BFS_Queue) - 1]
    tren = top(current)
    duoi = bot(current)
    phai = right(current)
    trai = left(current)
    if(phai in temp_BFS and not phai in notOk):
        BFS_Queue.append(phai)
        notOk.append(phai)
    elif duoi in temp_BFS and not duoi in notOk:
        BFS_Queue.append(duoi)
        notOk.append(duoi)
    elif trai in temp_BFS and not trai in notOk:
        BFS_Queue.append(trai)
        notOk.append(trai)
    elif tren in temp_BFS and not tren in notOk:
        BFS_Queue.append(tren)
        notOk.append(tren)
    else:
        nOk = BFS_Queue.pop()
        notOk.append(nOk) 
    
print("This is BFS: ")
print(BFS_Queue)

# IDF - Search
IDF_Stack = []
temp_IDF = []
IDF_Stack.append(source_point)
depth = 2
NotFind = True
while NotFind:
    if(goal_point in IDF_Stack):
        NotFind = False
        break

    topStack = IDF_Stack[len(IDF_Stack) - 1]
    x = topStack[0]
    y = topStack[1]
    tren = top(topStack)
    duoi = bot(topStack)
    phai = right(topStack)
    trai = left(topStack)

    if (phai not in IDF_Stack) and (phai not in temp_IDF) and (0 <= phai[0] < length) and (0 <= phai[1] < width) and (len(IDF_Stack) <= depth):
        temp_IDF.append(phai)
        if not isInList(phai, obstacles_arr):
            IDF_Stack.append(phai)
            
    elif (duoi not in IDF_Stack) and (duoi not in temp_IDF) and (0 <= duoi[0] < length) and (0 <= duoi[1] < width) and (len(IDF_Stack) <= depth):
        temp_IDF.append(duoi)
        if not isInList(duoi, obstacles_arr):
            IDF_Stack.append(duoi)
        
    elif (trai not in IDF_Stack and trai not in temp_IDF and 0 <= trai[0] < length and 0 <= trai[1] < width and len(IDF_Stack) <= depth):
        temp_IDF.append(trai)
        if not isInList(trai, obstacles_arr):
            IDF_Stack.append(trai)

    elif (top(topStack) not in IDF_Stack and top(topStack) not in temp_IDF and 0 <= x < length and 0 <= y - 1 < width and len(IDF_Stack) <= depth):
        temp_IDF.append(top(topStack))
        if not isInList(top(topStack), obstacles_arr):
            IDF_Stack.append(top(topStack))

    else:
        temp = IDF_Stack.pop()
        temp_IDF.append(temp)

    if(IDF_Stack == []):
        if depth == length * width:
            break
        temp_IDF = []
        IDF_Stack.append(source_point)
        depth = depth + 1


print("\n\n", IDF_Stack, "\n\n")
print("Depth = ", depth)
print("Len IDF = ", len(IDF_Stack))

# Greedy-best first search _ GFS
GFS_arr = []
temp_GFS = []
current = source_point
GFS_arr.append(current)

while goal_point not in GFS_arr:
    if GFS_arr == []:
        break
    x = current[0]
    y = current[1]

    tempPoint = []
    tren = top(current)
    duoi = bot(current)
    phai = right(current)
    trai = left(current)
    if (phai not in GFS_arr and phai not in temp_GFS and 0 <= phai[0] < length and 0 <= phai[1] < width):
        if not isInList(phai, obstacles_arr):
            tempPoint.append(phai)
    if (duoi not in GFS_arr and duoi not in temp_GFS and 0 <= duoi[0] < length and 0 <= duoi[1] < width):
        if not isInList(duoi, obstacles_arr):
            tempPoint.append(duoi)
    if (trai not in GFS_arr and trai not in temp_GFS and 0 <= trai[0] < length and 0 <= trai[1] < width):
        if not isInList(trai, obstacles_arr):
            tempPoint.append(trai)
    if (tren not in GFS_arr and tren not in temp_GFS and 0 <= tren[0] < length and 0 <= tren[1] < width):
        if not isInList(tren, obstacles_arr):
            tempPoint.append(tren)
        
    if tempPoint == []:
        temp = GFS_arr.pop()
        temp_GFS.append(temp)
        current = GFS_arr[-1]
    else:
        min = distance(tempPoint[0], goal_point)
        minP = tempPoint[0]
        for point in tempPoint:
            dis = distance(point, goal_point)
            if dis < min:
                min = dis
                minP = point
        GFS_arr.append(minP)
        current = minP
print("Greedy-best First Search")
print(GFS_arr)

temp = []
search = []
did = []
path = []
run = True
ii = 0
jj = 0
while run:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                did = temp_BFS
                path = BFS_Queue
            if event.key == pygame.K_2:
                did = temp_IDF
                path = IDF_Stack
            if event.key == pygame.K_3:
                did = temp_GFS
                path = GFS_arr
            if event.key == pygame.K_0:
                path = DFS_Stack
            if event.key == pygame.K_SPACE:
                did  = []
                path = []
                temp = []
                search = []
                ii = 0
                jj = 0

    for i in range(0, length):
        for j in range(0, width):
            if (i + j) % 2 == 0:
                draw_rect(BLACK_1, (i, j))

    for i in range(0, len(temp)):
        draw_rect(COLOR_ARR[4], temp[i])
    if(ii < len(did)):
        temp.append(did[i])
        ii = ii + 1
    elif(jj < len(path)):
        search.append(path[jj])
        jj = jj + 1


    for i in range(0, len(search)):
        if(i % 5 == 0):
            draw_rect(COLOR_ARR[0], search[i])
        else:
            draw_rect(COLOR_ARR[2], search[i])
    for i in range(0, obstacles_n + 1):
        for j in range(0, len(obstacles_arr[i])):
            draw_rect(RED, obstacles_arr[i][j])
            if i == obstacles_n:
                draw_rect(RED, obstacles_arr[i][j])
    draw_rect(BLUE, source_point)
    draw_rect(BLUE, goal_point)

    pygame.display.flip()