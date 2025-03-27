import random, pygame, time
from for_game.end import start_final_window


def start_the_game():
    class Maze:
        def __init__(
            self,
            length,
            wall,  # дробь отношения (например 10 к 1): 1 - что стенка есть, 10 - что нет.
            sizes,  # размер окна в клетках
            start,  
            pl_start_coord,  # стартовая точка игрока
        ):
            self.size = sizes
            self.wall = wall
            self.walls = [] 
            self.test_walls = (
                []
            )  
            self.num_vertex = 1 
            self.vertex_coord = []  
            self.edge_list = []  # Список смежности клеток
            self.graphs = []
            self.start = start
            self.finish = 0
            self.length = length
            self.test_solution_length = 0
            self.test_solution_path = []
            self.solution_length = 0
            self.solution_path = []
            self.create_flag = False
            self.player_coord = (
                pl_start_coord  
            )
            self.player_cell = (
                1 + self.player_coord[1] * self.size[0] + self.player_coord[0]
            )
            self.steps = 0
            self.weights = []
            self.amt_points = 0

        def get_random_walls(self):
            self.test_walls = []
            c = []
            for i in range(self.wall[0] * self.size[0] + 1):
                c.append(0)
            for i in range(self.wall[1] * self.size[1] + 1):
                c.append(1)
            self.test_walls.append(
                list(
                    random.sample(c, self.size[0] + 1) for _ in range(self.size[1] + 1)
                )
            )
            self.test_walls.append(
                list(
                    random.sample(c, self.size[0] + 1) for _ in range(self.size[1] + 1)
                )
            )
            for i in range(self.size[0] + 1):
                self.test_walls[0][0][self.size[0] - i] = 1
                self.test_walls[0][self.size[1]][self.size[0] - i] = 1
            for i in range(self.size[1] + 1):
                self.test_walls[0][i][self.size[0]] = 0
            for i in range(self.size[1] + 1):
                self.test_walls[1][i][0] = 1
                self.test_walls[1][i][self.size[0]] = 1
            for i in range(self.size[0] + 1):
                self.test_walls[1][0][i] = 0

        def cell2coord(self, vert):
            vertex_coord = []
            vertex_coord.append((vert - 1) // self.size[0])
            vertex_coord.append((vert - 1) % self.size[0])
            return vertex_coord

        def coord2cell(self, coord):
            cell = 1 + coord[1] * self.size[0] + coord[0]
            return cell

        def get_edge_list(self):
            self.vertex_coord = self.cell2coord(self.num_vertex)
            self.edge_list = []

            for i in range(self.vertex_coord[1], self.size[0]):
                if self.test_walls[1][self.vertex_coord[0] + 1][i + 1]:
                    num = self.size[0] * self.vertex_coord[0] + i + 1
                    if num != self.num_vertex:
                        self.edge_list.append(num)
                    break

            for i in range(self.vertex_coord[1], -1, -1):
                if self.test_walls[1][self.vertex_coord[0] + 1][i]:
                    num = self.size[0] * self.vertex_coord[0] + i + 1
                    if num != self.num_vertex:
                        self.edge_list.append(num)
                    break

            for i in range(self.vertex_coord[0], self.size[1]):
                if self.test_walls[0][i + 1][self.vertex_coord[1]]:
                    num = self.size[0] * i + self.vertex_coord[1] + 1
                    if num != self.num_vertex:
                        self.edge_list.append(num)
                    break

            for i in range(self.vertex_coord[0], -1, -1):
                if self.test_walls[0][i][self.vertex_coord[1]]:
                    num = self.size[0] * i + self.vertex_coord[1] + 1
                    if num != self.num_vertex:
                        self.edge_list.append(num)
                    break

            self.edge_list.sort()

        def print(self):
            for i in range(self.size[1] + 1):
                line = ""
                for j in range(self.size[0] + 1):
                    if self.test_walls[1][i][j]:
                        line += "|"
                    else:
                        line += " "
                    if self.test_walls[0][i][j]:
                        line += "__"
                    else:
                        line += "  "
                print(line)

        def get_path(self):
            n = self.size[0] * self.size[1]
            D = [None] * (n + 1) 
            D[self.start] = 0  
            Q = [self.start]
            Qstart = 0  
            Prev = [None] * (n + 1)
            while Qstart < len(Q):
                u = Q[Qstart]  
                Qstart += 1  
                for v in self.graphs[u - 1]:
                    if D[v] is None:
                        D[v] = D[u] + 1
                        Q.append(v)
                        Prev[v] = u

            self.amt_points = 0  
            self.test_solution_length = 0
            self.test_solution_path = []

            for i in range(n + 1):
                Ans = []  
                curr = i
                while curr is not None:
                    Ans.append(curr)  
                    curr = Prev[curr] 
                if D[i]:
                    self.amt_points += 1 
                    if self.test_solution_length < D[i]:
                        self.test_solution_length = D[i]
                        self.test_solution_path = Ans[::-1]  
                        self.finish = i  

        def try_to_create(self):
            self.create_flag = False
            self.graphs = ( [] ) 
            self.get_random_walls()
            for i in range(self.size[0] * self.size[1]):  
                self.num_vertex = i + 1
                self.get_edge_list()
                self.graphs.append(self.edge_list)  
            self.get_path()  
            if  (self.test_solution_length > self.length):  
                self.walls = self.test_walls.copy()
                self.solution_length = self.test_solution_length
                self.solution_path = self.test_solution_path.copy()
                self.create_flag = True

        def draw(self, color, coord, size, width_wall): 
            size_x = size[0] / self.size[0]  
            size_y = size[1] / self.size[1]  
            for i in range(self.size[1] + 1):
                for j in range(self.size[0] + 1):
                    if j + 1 < len(self.walls[0][i]):
                        if self.walls[0][i][j]:
                            pygame.draw.line(
                                screen,
                                color,
                                (
                                    int(j * size_x + coord[0]),
                                    int(i * size_y + coord[1]),
                                ),
                                (
                                    int((j + 1) * size_x + coord[0]),
                                    int(i * size_y + coord[1]),
                                ),
                                width_wall,
                            )
                    if i + 1 < len(self.walls[1]):
                        if self.walls[1][i + 1][j]:
                            pygame.draw.line(
                                screen,
                                color,
                                (
                                    int(j * size_x + coord[0]),
                                    int(i * size_y + coord[1]),
                                ),
                                (
                                    int(j * size_x + coord[0]),
                                    int((i + 1) * size_y + coord[1]),
                                ),
                                width_wall,
                            )

            crd = self.cell2coord(self.start)
            crd[0], crd[1] = crd[1], crd[0]
            crd[0] *= size_x
            crd[1] *= size_y
            pygame.draw.rect(
                screen,
                (0, 230, 0),
                (crd[0] + 10, crd[1] + 10, size_x - 15, size_y - 15),
            )
            pygame.draw.rect(
                screen,
                (0, 0, 0),
                (crd[0] + 10, crd[1] + 10, size_x - 15, size_y - 15),
                5,
            )

            crd = self.cell2coord(self.finish)
            crd[0], crd[1] = crd[1], crd[0]
            crd[0] *= size_x
            crd[1] *= size_y
            pygame.draw.rect(
                screen,
                (230, 0, 0),
                (crd[0] + 10, crd[1] + 10, size_x - 15, size_y - 15),
            )
            pygame.draw.rect(
                screen,
                (0, 0, 0),
                (crd[0] + 10, crd[1] + 10, size_x - 15, size_y - 15),
                5,
            )

        def if_wall_at_right(self):
            current_coords = self.player_coord
            vert_walls = self.walls[1][current_coords[1]]
            if vert_walls[current_coords[0]]:
                return True
            return False

        def if_wall_at_left(self):
            current_coords = self.player_coord
            vert_walls = self.walls[1][current_coords[1]]
            if vert_walls[current_coords[0] - 1]:
                return True
            return False

        def if_wall_at_up(self):
            current_coords = self.player_coord
            goriz_walls = self.walls[0][current_coords[1] - 1]
            if goriz_walls[current_coords[0] - 1]:
                return True
            return False

        def if_wall_at_down(self):
            current_coords = self.player_coord
            vert_walls = self.walls[0][current_coords[1]]
            if vert_walls[current_coords[0] - 1]:
                return True
            return False

        def draw_player(self, size):
            self.player_cell = self.coord2cell(self.player_coord) - 9

            size_x = size[0] / self.size[0]
            size_y = size[1] / self.size[1]

            crd = self.cell2coord(self.player_cell)
            crd[0], crd[1] = crd[1], crd[0]
            crd[0] *= size_x
            crd[1] *= size_y

            pygame.draw.rect(
                screen,
                (199, 21, 133),
                (
                    crd[0] + 10,
                    crd[1] + 10,
                    size_x - 15,
                    size_y - 15,
                ),
            )
            pygame.draw.rect(
                screen,
                (0, 0, 0),
                (
                    crd[0] + 10,
                    crd[1] + 10,
                    size_x - 15,
                    size_y - 15,
                ),
                5,
            )

    pygame.init()
    pygame.font.init()
    size_screen = [325, 645]
    color_screen = (224, 255, 255)
    screen = pygame.display.set_mode(size_screen)

    clock = pygame.time.Clock()
    FPS = 50

    keydown = []

    maze = Maze(20, [10, 1], [8, 16], 1, [1, 1])  #

    step = 1
    TMP_i = 0
    games_count = 0
    steps_player_count = 0
    default_time_per_step = 1.5
    time_elapsed = 0
    final_points = 0
    while step and games_count <= 5:
        keydown = pygame.key.get_pressed()
        if step == 1:
            maze.try_to_create()
            if maze.create_flag:
                #maze.print()
                #print("attempts to generate this maze:", TMP_i)
                TMP_i = 0
                step = 2
                points_for_the_round = 0
                if steps_player_count != 0:
                    points_for_the_round = (
                        (maze.length * default_time_per_step)
                        / max(
                            time_elapsed,
                            (maze.length * default_time_per_step),
                        )
                        + maze.length / steps_player_count
                    ) * 50
                    if points_for_the_round >= 94:
                        points_for_the_round = 100
                    final_points += points_for_the_round

                #print("points for that game:", points_for_the_round)

                games_count += 1
                steps_player_count = 0
                start_time = time.time()
            else:
                TMP_i += 1

        if step == 2:
            screen.fill(color_screen)
            maze.draw((0, 0, 0), [2, 2], [320, 640], 5)
            maze.draw_player([320, 640])

            if keydown[pygame.K_r]:
                maze.player_coord = list(
                    map(lambda x: x + 1, maze.cell2coord(maze.start))
                )[::-1]

            if keydown[pygame.K_d]:
                moving = False
                while not maze.if_wall_at_right():
                    moving = True
                    maze.player_coord[0] += 1
                    screen.fill(color_screen)
                    maze.draw((0, 0, 0), [2, 2], [320, 640], 5)
                    maze.draw_player([320, 640])
                    pygame.display.flip()
                    time.sleep(FPS * 0.001)
                if moving:
                    steps_player_count += 1
                if (
                    maze.player_coord
                    == list(map(lambda x: x + 1, maze.cell2coord(maze.finish)))[::-1]
                ):
                    maze.start = maze.finish
                    step = 1
                    end_time = time.time()
                    time_elapsed = end_time - start_time

            if keydown[pygame.K_a]:
                moving = False
                while not maze.if_wall_at_left():
                    moving = True
                    maze.player_coord[0] -= 1
                    screen.fill(color_screen)
                    maze.draw((0, 0, 0), [2, 2], [320, 640], 5)
                    maze.draw_player([320, 640])
                    pygame.display.flip()
                    time.sleep(FPS * 0.001)
                if moving:
                    steps_player_count += 1
                if (
                    maze.player_coord
                    == list(map(lambda x: x + 1, maze.cell2coord(maze.finish)))[::-1]
                ):
                    maze.start = maze.finish
                    step = 1
                    end_time = time.time()
                    time_elapsed = end_time - start_time

            if keydown[pygame.K_w]:
                moving = False
                while not maze.if_wall_at_up():
                    moving = True
                    maze.player_coord[1] -= 1
                    screen.fill(color_screen)
                    maze.draw((0, 0, 0), [2, 2], [320, 640], 5)
                    maze.draw_player([320, 640])
                    pygame.display.flip()
                    time.sleep(FPS * 0.001)
                if moving:
                    steps_player_count += 1
                if (
                    maze.player_coord
                    == list(map(lambda x: x + 1, maze.cell2coord(maze.finish)))[::-1]
                ):
                    maze.start = maze.finish
                    step = 1
                    end_time = time.time()
                    time_elapsed = end_time - start_time

            if keydown[pygame.K_s]:
                moving = False
                while not maze.if_wall_at_down():
                    moving = True
                    maze.player_coord[1] += 1
                    screen.fill(color_screen)
                    maze.draw((0, 0, 0), [2, 2], [320, 640], 5)
                    maze.draw_player([320, 640])
                    pygame.display.flip()
                    time.sleep(FPS * 0.001)
                if moving:
                    steps_player_count += 1
                if (
                    maze.player_coord
                    == list(map(lambda x: x + 1, maze.cell2coord(maze.finish)))[::-1]
                ):
                    maze.start = maze.finish
                    step = 1
                    end_time = time.time()
                    time_elapsed = end_time - start_time

            pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                step = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    step = 0

        clock.tick()

    #print(round(final_points), "/ 500")

    with open("data/info/record.txt", "r") as f:
        record_score = int(f.readlines()[0].strip())

    if round(final_points) > record_score:
        with open("data/info/record.txt", "w") as f:
            f.write(str(round(final_points)))

    return start_final_window(round(final_points))
