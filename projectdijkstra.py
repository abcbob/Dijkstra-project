import tkinter
import tkinter.messagebox
import tkinter.font
import time
import heapq
from copy import deepcopy
import ast
import random

GUI_HEIGHT = 720
GUI_WIDTH = 1280


# reference https://github.com/johnsliao/python-maze-generator/blob/master/maze.py
# support: Thành I1922
def CheckNeighborTiles(maze, point, w, h):
    # a list (maximum of 4) of possible tiles
    possible = []
    up = {'x': point['x'], 'y': point['y'] - 1}
    down = {'x': point['x'], 'y': point['y'] + 1}
    left = {'x': point['x'] - 1, 'y': point['y']}
    right = {'x': point['x'] + 1, 'y': point['y']}

    if up['y'] > 0 and maze[up['y'] * 2 - 1][up['x'] * 2 - 1] == "*":
        possible.append(up)
    if down['y'] <= h and maze[down['y'] * 2 - 1][down['x'] * 2 - 1] == "*":
        possible.append(down)
    if left['x'] > 0 and maze[left['y'] * 2 - 1][left['x'] * 2 - 1] == "*":
        possible.append(left)
    if right['x'] <= w and maze[right['y'] * 2 - 1][right['x'] * 2 - 1] == "*":
        possible.append(right)

    if len(possible) == 0:
        return point
    else:  # only choose one of them
        return random.choice(possible)


# Depth-first search algorithm
def createmap(height, width):  # This only include movable line ( * . * . * ) mean a width of 2

    Maze = [['*' for i in range(width * 2 + 1)] for j in range(height * 2 + 1)]
    Path = []  # backtrack path

    Visited = 1  # The Visited Tile, the map is completed when Visited is equal to total tiles (w*h)

    Pos = {'x': random.randint(1, width), 'y': random.randint(1, height)}

    Maze[Pos['y'] * 2 - 1][Pos['x'] * 2 - 1] = "."

    Path.append(Pos)  # Add first tile to Path

    while Visited < width * height:
        Next = CheckNeighborTiles(Maze, Pos, width,
                                  height)  # Check if any possible tile is expandable (not already used)

        if Next == Pos:  # No tile available: backtrack to previous tile
            Path.pop()
            Pos = Path[-1]
        else:  # tile available: expand, go to new tile, add tile to path to backtrack later
            Maze[Next['y'] * 2 - 1][Next['x'] * 2 - 1] = '.'
            Maze[Next['y'] + Pos['y'] - 1][Next['x'] + Pos['x'] - 1] = '.'
            Path.append(Next)
            Pos = Next
            Visited += 1
    # return a fully random maze
    return Maze


def convert_map_to_vertices(maze, startPos, verticesGap):
    verticesAmount = (len(maze) - 1) * (len(maze[0]) - 1)
    verticesVisited = 0

    verticesList = []

    startP = [0, 0]
    r = [0, 0]
    direction = 1  # Direction: 0. up, 1. right, 2. down, 3. left.

    verticesList.append(r)

    while verticesAmount > verticesVisited:
        # Check all available route
        up = [r[0], r[1] - 1]
        down = [r[0], r[1] + 1]
        left = [r[0] - 1, r[1]]
        right = [r[0] + 1, r[1]]

        available = []

        # check availability of up
        if not direction == 2 and (maze[r[1]][r[0]] == "." or maze[r[1]][r[0] + 1] == '.'):
            available.append(0)

        # check availability of down
        if not direction == 0 and (maze[r[1] + 1][r[0]] == "." or maze[r[1] + 1][r[0] + 1] == '.'):
            available.append(2)

        # check availability of left
        if not direction == 1 and (maze[r[1]][r[0]] == "." or maze[r[1] + 1][r[0]] == '.'):
            available.append(3)

        # check availability of right
        if not direction == 3 and (maze[r[1]][r[0] + 1] == "." or maze[r[1] + 1][r[0] + 1] == '.'):
            available.append(1)

        chosenDir = -1
        priority = random.randint(0, 1)

        for dir in available:
            if dir == (direction + 3) % 4:
                chosenDir = dir
                priority = 3

            if priority < 3 and dir == direction:
                chosenDir = dir
                priority = 2

            if priority < 2 and dir == (direction + 1) % 4:
                chosenDir = dir

        chosenVer = []

        if chosenDir == 0: chosenVer = up
        if chosenDir == 1: chosenVer = right
        if chosenDir == 2: chosenVer = down
        if chosenDir == 3: chosenVer = left

        verticesVisited += 1

        if not direction == chosenDir:
            verticesList.append(r)

        r = chosenVer
        direction = chosenDir

        # Maze not fully filled and runner have comeback to starting point
        if r == startP:
            break

    # Vertices Gap: 1. Height, 2. Width
    # convert to vertice
    for ver in verticesList:
        ver[0] = ver[0] * verticesGap[1] + startPos[1]
        ver[1] = ver[1] * verticesGap[0] + startPos[0]

    return verticesList


def dijkstra(point, connect, start, end, startPconnectlist, endPconnectlist):
    if start == [] or end == []:
        return []
    # khởi tạo cho dijkstra
    # điểm đầu và cuối
    pointlist = deepcopy(point)
    # useful for calculating
    pointlist.append(start)
    pointlist.append(end)
    startpoint = len(pointlist) - 2
    endpoint = len(pointlist) - 1
    pAmount = len(pointlist)

    connectlist = deepcopy(connect)

    for i in range(len(connect)):
        connectlist[i].append(startPconnectlist[i])
        connectlist[i].append(endPconnectlist[i])

    connectlist.append(startPconnectlist)
    connectlist.append(endPconnectlist)

    # Dijkstra
    # priority queue (heap)
    waitS = [(0, startpoint)]
    heapq.heapify(waitS)
    prev = []
    visited = []
    weight = []
    for i in range(pAmount):
        prev.append(-1)  # để quay lui
        visited.append(False)
        weight.append(2222222222)

    weight[startpoint] = 0

    # add the start point to the mainQueue
    prev[startpoint] = startpoint

    while not visited[endpoint] and len(waitS) > 0:
        currentdistance, curr = heapq.heappop(waitS)
        visited[curr] = True

        for i in range(pAmount):
            cmpweight = weight[curr] + (
                        (pointlist[curr][0] - pointlist[i][0]) ** 2 + (pointlist[curr][1] - pointlist[i][1]) ** 2) \
                        ** (1 / 2)  # pythagorean theorem
            if connectlist[curr][i] and not visited[i] and weight[i] > cmpweight:
                weight[i] = cmpweight
                prev[i] = curr

                heapq.heappush(waitS, (weight[i], i))

    resultgraph = []

    # quay lui
    if visited[endpoint]:
        while not prev[endpoint] == endpoint:
            resultgraph.append(endpoint)
            endpoint = prev[endpoint]

        resultgraph.append(endpoint)

    return resultgraph[::-1]


# kiểm tra 3 điểm thẳng hàng/ theo chiều kim đồng hồ/ ngược chiều kim đồng hồ
# 1. Clockwise
# 2. Counter-clockwise
# 0. Collinear
def checkMiddle(a, b, c):
    if ((b[0] <= max(a[0], c[0])) and (b[0] >= min(a[0], c[0])) and
            (b[1] <= max(a[1], c[1])) and (b[1] >= min(a[1], c[1]))):
        return True
    return False


def checkOrientation(a, b, c):
    # Calculate the change of slope
    val = ((b[1] - a[1]) * (c[0] - b[0])) - ((b[0] - a[0]) * (c[1] - b[1]))

    if val > 0:
        return 1
    if val < 0:
        return 2
    return 0


# 0. No Intersect
# 1. Intersect 100%
# 2. Intersect through a start/end
def checkIntersect(d1, c1, d2, c2):
    if d1 == d2 or c1 == d2 or d1 == c2 or c1 == c2:
        return 0

    o1 = checkOrientation(d1, c1, d2)
    o2 = checkOrientation(d1, c1, c2)
    o3 = checkOrientation(d2, c2, d1)
    o4 = checkOrientation(d2, c2, c1)

    if not o1 == o2 and not o3 == o4:
        return 1

    # All Collinear. Might be good to return 1
    if ((o1 == 0) or (o2 == 0) or (o3 == 0) or (o4 == 0)) and (checkMiddle(d1, d2, c1) or checkMiddle(d1, c2, c1)):
        return 0

    if o1 == 0 and checkMiddle(d1, d2, c1):
        return 2
    if o2 == 0 and checkMiddle(d1, c2, c1):
        return 2
    if o3 == 0 and checkMiddle(d2, d1, c2):
        return 2
    if o4 == 0 and checkMiddle(d2, d1, c2):
        return 2
    return 0


# check available route
def PolygonRouteCheck(point, a, b):
    if len(point) < 3:
        return 0

    if a == b:
        return 0

    # check 2 điểm giao với tường
    smooth = True

    # the midpoint of the two vertices of the path. Maze is a polygon, so it is used to check if it inside maze
    middle_point = [b[0] / 2 + a[0] / 2, b[1] / 2 + a[1] / 2]
    middle_inside = False
    for v1 in range(len(point)):
        v2 = (v1 + 1) % (len(point))

        # kiểm tra đa giác
        if not ((point[v1][1] >= middle_point[1]) == (point[v2][1] >= middle_point[1])):
            if middle_point[0] <= (point[v2][0] - point[v1][0]) * (middle_point[1] - point[v1][1]) / (
                    point[v2][1] - point[v1][1]) + point[v1][0]:
                middle_inside = not middle_inside
        # wall check
        if checkIntersect(a, b, point[v1], point[v2]) != 0:
            smooth = False
            break
    if middle_inside and smooth:
        return 1

    return 0


# check route
def PolygonRoute(point):
    if len(point) < 3:
        return []

    result = []

    # Setting up a new, empty connect list
    for i in range(len(point)):
        resrow = []
        for j in range(len(point)):
            resrow.append(0)
        result.append(resrow)
    # Check available path from i to j
    for i in range(len(point)):
        for j in range(i + 1, len(point)):
            if j - i == 1 or (i == 0 and j == len(point) - 1):
                result[i][j] = 1
                result[j][i] = 1
            else:
                res = PolygonRouteCheck(point, point[i], point[j]) # Check if they are connected through a line
                result[i][j] = res
                result[j][i] = res

    return result


# MAIN CLASS
class DjikstraGUI:
    def __init__(self):
        # Setting up the main window
        self.w_main = tkinter.Tk(className='Dijkstraproject')

        # Setting up the default font
        thefont = tkinter.font.Font(family='Times New Roman', size=15)
        self.cont = tkinter.Frame(self.w_main, padx=5, pady=2, bg='#ffffff')
        self.cont.columnconfigure(0, weight=1)

        # The program section, thing that are generally unrelated to tkinter
        gap_width = (GUI_WIDTH - 20) / (8 * 2)
        gap_height = (GUI_HEIGHT - 20) / (6 * 2)
        self.point = self.point = convert_map_to_vertices(createmap(6, 8), [30, 30], [gap_height, gap_width])
        self.startP = []
        self.endP = []

        # The two last connection indicate the start and end. Will usually get update after a reload
        self.pointConnect = []

        # Exclusive connect for the start point and end point. This is to reduce wait time on changing them
        self.startConnect = []
        self.endConnect = []

        # The result of a dijkstra run, only update when the user run in order to get the time
        self.path = []
        self.distance = -1

        # time-related
        self.graphMapTime = 0
        self.graphSETime = 0
        self.pathTime = 0

        # The Drawing section, thing that related to the drawing part are here
        self.previous = []

        # Data
        self.f_data = tkinter.Frame(self.cont, padx=10, pady=1, bg='#ffffff')

        self.l_tPath = tkinter.Label(self.f_data, text=' Dijkstra: ', bg='#ffffff', fg='#000000')
        self.l_tGraph = tkinter.Label(self.f_data, text=' Tổng thời gian tạo đồ thị: ', bg='#ffffff', fg='#000000')
        self.v_tPath = tkinter.StringVar()
        self.v_tGraph = tkinter.StringVar()
        self.v_tTotal = tkinter.StringVar()
        self.l_vTPath = tkinter.Label(self.f_data, textvariable=self.v_tPath, bg='#ffffff', fg='#000000', width=15)
        self.l_vTGraph = tkinter.Label(self.f_data, textvariable=self.v_tGraph, bg='#ffffff', fg='#000000', width=15)

        self.v_distance = tkinter.StringVar()
        self.v_distance.set('KHOẢNG CÁCH 2 ĐIỂM: 0 cm')
        self.l_distanceV = tkinter.Label(self.f_data, textvariable=self.v_distance, bg='#ffffff', fg='#000000')

        self.l_tPath.grid(column=1, row=0, sticky=tkinter.W)
        self.l_tGraph.grid(column=3, row=0, sticky=tkinter.W)
        self.l_vTPath.grid(column=2, row=0, sticky=tkinter.W)
        self.l_vTGraph.grid(column=4, row=0, sticky=tkinter.W)

        self.l_distanceV.grid(column=8, row=0, columnspan=5, sticky=tkinter.W, padx=300)

        self.f_controlmain = tkinter.Frame(self.cont, bg='#ffffff')

        # Bảng điều khiển
        self.f_control1 = tkinter.Frame(self.f_controlmain, bg='#ffffff')

        self.v_pathCheck = tkinter.IntVar()
        self.v_pathCheck.set(0)
        self.cbt_run = tkinter.Checkbutton(self.f_control1, text="Đường đi", variable=self.v_pathCheck,
                                           command=self.reload_map, padx=20, bg='#ffffff', fg='#000000',
                                           activebackground='#ffffff', activeforeground='#000000',
                                           selectcolor='#ffffff')

        self.v_graphCheck = tkinter.IntVar()
        self.v_graphCheck.set(0)
        self.cbt_graph = tkinter.Checkbutton(self.f_control1, text="Tạo đồ thị", variable=self.v_graphCheck,
                                             command=self.reload_map, padx=20, bg='#ffffff', fg='#000000',
                                             activebackground='#ffffff', activeforeground='#000000',
                                             selectcolor='#ffffff')

        self.v_colorCheck = tkinter.IntVar()
        self.v_colorCheck.set(0)
        self.cbt_color = tkinter.Checkbutton(self.f_control1, text="Đổi màu", variable=self.v_colorCheck,
                                             command=self.reload_map, padx=20, bg='#ffffff', fg='#000000',
                                             activebackground='#ffffff', activeforeground='#000000',
                                             selectcolor='#ffffff')

        self.v_clickEvent = tkinter.StringVar()

        self.f_control2 = tkinter.Frame(self.f_controlmain, bg='#ffffff')
        self.bt_clear = tkinter.Button(self.f_control2, text="Xoá map", command=self.clear_map, width=10, bg='#ffffff',
                                       fg='#000000')
        self.bt_clear['font'] = thefont
        self.bt_newrandom = tkinter.Button(self.f_control2, text="Tạo map random", command=self.random_map, width=15,
                                           bg='#ffffff', fg='#000000')
        self.bt_importGraph = tkinter.Button(self.f_control2, text="Nhập đồ thị", command=self.import_graph, width=10,
                                             bg='#ffffff', fg='#000000')
        self.bt_importGraph['font'] = thefont
        self.e_imported = tkinter.Entry(self.f_control2, width=20, bg='#fefefe', fg='#000000')
        self.e_imported['font'] = thefont

        self.l_width = tkinter.Label(self.f_control2, text="Chiều dài: ", bg='#ffffff', fg='#000000')
        tracewidth = tkinter.StringVar()
        self.e_width = tkinter.Entry(self.f_control2, width=5, textvariable=tracewidth, bg='#fefefe', fg='#000000')
        self.e_width.insert(tkinter.END, '8')
        self.l_height = tkinter.Label(self.f_control2, text="Chiều cao: ", bg='#ffffff', fg='#000000')
        traceheight = tkinter.StringVar()

        self.e_height = tkinter.Entry(self.f_control2, width=5, textvariable=traceheight, bg='#fefefe', fg='#000000')
        self.e_height.insert(tkinter.END, '6')
        self.v_tMapestimation = tkinter.StringVar()
        self.l_vTMapestimation = tkinter.Label(self.f_control2, textvariable=self.v_tMapestimation, bg='#ffffff',
                                               fg='#000000', width=15)

        tracewidth.trace_add('write', self.traceres)
        traceheight.trace_add('write', self.traceres)

        self.f_control1.grid(column=1, row=0, sticky=tkinter.N)
        self.cbt_run.grid(column=0, row=0, sticky=tkinter.W)
        self.cbt_graph.grid(column=0, row=1, sticky=tkinter.W)
        self.cbt_color.grid(column=15, row=1, sticky=tkinter.W)

        self.f_control2.grid(column=0, row=0, sticky=tkinter.NSEW)
        self.bt_clear.grid(column=15, row=0, rowspan=2, padx=50)
        self.bt_newrandom.grid(column=7, row=0, columnspan=2, rowspan=1, padx=50)
        self.bt_importGraph.grid(column=0, row=0, rowspan=2, columnspan=3, sticky=tkinter.EW, padx=5)
        self.e_imported.grid(column=4, row=0, rowspan=2, padx=5)
        self.l_width.grid(column=10, row=0, rowspan=2, padx=5)
        self.e_width.grid(column=11, row=0, rowspan=2, padx=5)
        self.l_height.grid(column=12, row=0, rowspan=2, padx=5)
        self.e_height.grid(column=13, row=0, rowspan=2, padx=5)
        self.l_vTMapestimation.grid(column=7, row=1, columnspan=2, sticky=tkinter.EW, padx=5)
        # Phần bản đồ
        self.f_map = tkinter.Frame(self.cont, bg='#ffffff')
        self.c_map = tkinter.Canvas(self.f_map, width=GUI_WIDTH, height=GUI_HEIGHT, highlightthickness=1,
                                    relief='ridge')

        self.reload_map(code=2)

        self.c_map.grid(column=0, row=0)

        # main frame
        self.cont.pack(expand=1)
        self.f_data.grid(column=0, row=2, sticky=tkinter.EW)
        self.f_controlmain.grid(column=0, row=0, sticky=tkinter.W)
        self.f_map.grid(column=0, row=1)

        # Mainloop
        tkinter.mainloop()

    # A load/reload canvas function to update canvas from diffrent event
    # Code:
    # 0. Reload to enable/disable some visual, no need for an info reload
    # 1. There's change to the start/end point, reload thing related to that only
    # 2. There's change to the map, reload all

    def reload_map(self, code=0):
        # prevent memory overflow
        self.c_map.delete('all')

        # start and end related things
        self.c_map.unbind("<Button-1>")
        self.c_map.unbind("<Button-3>")
        self.c_map.bind("<Button-1>", self.update_start)
        self.c_map.bind("<Button-3>", self.update_end)

        # Update anything that changed due to user input (example: reconnect all available path)
        if code == 2:
            startTime = time.time()
            self.pointConnect = PolygonRoute(self.point)
            self.graphMapTime = time.time() - startTime

        # Update thing that related to the start/end point .aka everything that isn't the main route graph
        if code > 0:
            self.path = []
            self.v_tPath.set(-1)

            startTime = time.time()

            if not self.startP == []:
                self.startConnect = []
                for p in self.point:
                    self.startConnect.append(PolygonRouteCheck(self.point, self.startP, p))

                # The 2nd to last element represent the start's connection to itself,handy when using dijkstra
                self.startConnect.append(0)

                if not self.endP == []:
                    self.startConnect.append(PolygonRouteCheck(self.point, self.startP, self.endP))
                else:
                    self.startConnect.append(0)

            if not self.endP == []:
                self.endConnect = []
                for p in self.point:
                    self.endConnect.append(PolygonRouteCheck(self.point, self.endP, p))

                if not self.startP == []:
                    self.endConnect.append(PolygonRouteCheck(self.point, self.startP, self.endP))
                else:
                    self.endConnect.append(0)

                # The last element represent the end's connection to itself, since this will be handy when using dijkstra
                self.endConnect.append(0)

            self.graphSETime = time.time() - startTime

        # Redraw everything
        if self.v_colorCheck.get():
            self.c_map.create_rectangle(0, 0, GUI_WIDTH, GUI_HEIGHT, fill='#aa3333')

        else:
            self.c_map.create_rectangle(0, 0, GUI_WIDTH, GUI_HEIGHT, fill='#123456')

        if len(self.point) > 2:
            self.c_map.create_polygon(self.point + self.point[0], fill='#fefefe')

        if self.v_graphCheck.get():
            k = 0
            # Draw all connection between point
            for i in range(len(self.pointConnect)):
                for j in range(len(self.pointConnect)):
                    if self.pointConnect[i][j]:
                        k = k + 1
                        if self.v_colorCheck.get():
                            self.c_map.create_line(self.point[i], self.point[j], fill="#d9d900")
                        else:
                            self.c_map.create_line(self.point[i], self.point[j], fill="#696969")
            # Draw start connection
            for i in range(len(self.startConnect)):
                if self.startConnect[i]:
                    if i >= len(self.point):
                        if not self.endP == []:
                            if self.v_colorCheck.get():
                                self.c_map.create_line(self.startP, self.endP, fill="#d9d900")
                            else:
                                self.c_map.create_line(self.startP, self.endP, fill="#696969")
                    else:
                        if self.v_colorCheck.get():
                            self.c_map.create_line(self.startP, self.point[i], fill="#d9d900")
                        else:
                            self.c_map.create_line(self.startP, self.point[i], fill="#696969")

            # Draw end connection
            for i in range(len(self.endConnect)):
                if self.endConnect[i] and i < len(self.point):
                    if self.v_colorCheck.get():
                        self.c_map.create_line(self.endP, self.point[i], fill="#d9d900")
                    else:
                        self.c_map.create_line(self.endP, self.point[i], fill="#696969")
        # start and end point
        if not self.startP == []:
            if self.v_colorCheck.get():
                self.c_map.create_oval(self.startP[0] - 4, self.startP[1] - 4, self.startP[0] + 4, self.startP[1] + 4,
                                       fill='#f000ee', width=0)
                self.c_map.create_text(self.startP[0], self.startP[1] + 5, text="START", anchor=tkinter.N,
                                       fill="#f000ee")
            else:
                self.c_map.create_oval(self.startP[0] - 4, self.startP[1] - 4, self.startP[0] + 4, self.startP[1] + 4,
                                       fill='#de3333', width=0)
                self.c_map.create_text(self.startP[0], self.startP[1] + 5, text="START", anchor=tkinter.N,
                                       fill="#de3333")

        if not self.endP == []:
            if self.v_colorCheck.get():
                self.c_map.create_oval(self.endP[0] - 4, self.endP[1] - 4, self.endP[0] + 4, self.endP[1] + 4,
                                       fill='#1500ff', width=0)
                self.c_map.create_text(self.endP[0], self.endP[1] + 5, text="END", anchor=tkinter.N, fill="#1500ff")
            else:
                self.c_map.create_oval(self.endP[0] - 4, self.endP[1] - 4, self.endP[0] + 4, self.endP[1] + 4,
                                       fill='#00c2c2', width=0)
                self.c_map.create_text(self.endP[0], self.endP[1] + 5, text="END", anchor=tkinter.N, fill="#00c2c2")

        if self.v_pathCheck.get():
            # Run Dijkstra if there isn't an already calculated path yet
            if len(self.path) == 0:
                startTime = time.time()
                self.path = dijkstra(self.point, self.pointConnect, self.startP, self.endP, self.startConnect,
                                     self.endConnect)
                self.pathTime = time.time() - startTime
                self.distance = 0

                # Find the distance from start to finish
                if len(self.path) == 2:
                    self.distance = self.distance + ((self.startP[0] - self.endP[0]) ** 2
                                                     + (self.startP[1] - self.endP[1]) ** 2) ** (1 / 2)

                elif len(self.path) > 2:
                    for i in range(1, len(self.path) - 2):
                        self.distance = self.distance + (
                                (self.point[self.path[i + 1]][0] - self.point[self.path[i]][0]) ** 2
                                + (self.point[self.path[i + 1]][1] - self.point[self.path[i]][1]) ** 2) ** (1 / 2)
                    self.distance += ((self.startP[0] - self.point[self.path[1]][0]) ** 2 + (
                            self.startP[1] - self.point[self.path[1]][1]) ** 2) ** (1 / 2)
                    self.distance += ((self.endP[0] - self.point[self.path[-2]][0]) ** 2 + (
                            self.endP[1] - self.point[self.path[-2]][1]) ** 2) ** (1 / 2)

            # If there's only 2 points in the path => only start and end point => just draw one line there
            if len(self.path) == 2:
                if self.v_colorCheck.get():
                    self.c_map.create_line(self.startP, self.endP, fill='#00cc00', width=3)
                else:
                    self.c_map.create_line(self.startP, self.endP, fill='#000000', width=3)
            else:
                for i in range(1, len(self.path) - 2):
                    if self.v_colorCheck.get():
                        self.c_map.create_line(self.point[self.path[i]], self.point[self.path[i + 1]], fill='#00cc00',
                                               width=3)
                    else:
                        self.c_map.create_line(self.point[self.path[i]], self.point[self.path[i + 1]], fill='#000000',
                                               width=3)

                if len(self.path) > 2:
                    if self.v_colorCheck.get():
                        self.c_map.create_line(self.startP, self.point[self.path[1]], fill='#00cc00', width=3)
                        self.c_map.create_line(self.endP, self.point[self.path[-2]], fill='#00cc00', width=3)
                    else:
                        self.c_map.create_line(self.startP, self.point[self.path[1]], fill='#000000', width=3)
                        self.c_map.create_line(self.endP, self.point[self.path[-2]], fill='#000000', width=3)

            self.v_distance.set("KHOẢNG CÁCH 2 ĐIỂM: " + str(round(self.distance * 0.0264583333 / 1.2, 2)) + " cm")

        self.v_tGraph.set(str(round(self.graphMapTime + self.graphSETime, 3)) + "s")
        self.v_tPath.set(str(round(self.pathTime, 3)) + "s")
        self.v_tTotal.set(str(round(self.graphMapTime + self.graphSETime + self.pathTime, 3)) + "s")

    def clear_map(self):
        self.point = []
        self.pointConnect = []
        self.startP = []
        self.startConnect = []
        self.endP = []
        self.endConnect = []

        self.reload_map(code=2)

    def traceres(self, var, index, mode):
        w = self.e_width.get()
        h = self.e_height.get()
        if not h.isdigit() or not w.isdigit() or int(w) <= 0 or int(h) <= 0:
            w = 8
            h = 6
        else:
            h = int(h)
            w = int(w)
        self.v_tMapestimation.set("Thời gian ước tính: " + str(round((w * h / 48) ** 3 * 0.09 / 1.2 ** 3, 3)) + "s")

    def random_map(self):
        w = self.e_width.get()
        h = self.e_height.get()
        if not h.isdigit() or not w.isdigit() or int(w) <= 0 or int(h) <= 0:
            w = 8
            h = 6
            msg = "Chỉ nhận giá trị nguyên dương làm tham số cho bản đồ.\n sử dụng tham số 8 và 6 để tạo map"
            tkinter.messagebox.showwarning(title="Not Valid Input", message=msg)
        else:
            h = int(h)
            w = int(w)
        self.v_tMapestimation.set("Thời gian ước tính: " + str(round((w * h / 48) ** 3 * 0.09 / 1.2 ** 3, 3)) + "s")
        gapWidth = (GUI_WIDTH - 20) / (w * 2)
        gapHeight = (GUI_HEIGHT - 20) / (h * 2)
        self.point = convert_map_to_vertices(createmap(h, w), [30, 30], [gapHeight, gapWidth])

        self.reload_map(code=2)

    def update_start(self, event):
        self.startP = [event.x, event.y]
        self.reload_map(code=1)

    def update_end(self, event):
        self.endP = [event.x, event.y]
        self.reload_map(code=1)

    def import_graph(self):
        try:
            self.point = ast.literal_eval(self.e_imported.get())
            self.reload_map(code=2)
        except:
            msg = "Cách nhập đồ thị: [[x1, y1],[x2, y2],[x3, y3]] \n VD: [[5, 63][23, 98][35, 15]]"
            tkinter.messagebox.showwarning(title="Nhập sai kiểu dữ liệu", message=msg)


mainGI = DjikstraGUI()
