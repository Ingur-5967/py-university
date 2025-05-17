import pygame
import random
import math
from queue import PriorityQueue

from pygame import Surface, Rect
from pygame.sprite import Sprite

# Инициализация Pygame
pygame.init()

# Константы
WIDTH = 600
GRID_SIZE = 30  # Размер поля NxN
CELL_SIZE = WIDTH // GRID_SIZE
WINDOW = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A*")

# Цвета
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

# Типы ячеек
EMPTY = 0
OBSTACLE = 1
START = 2
END = 3
PATH = 4
VISITED = 5

types = {
    0: EMPTY,
    1: OBSTACLE,
    2: START,
    3: END,
    4: PATH,
    5: VISITED
}

colors = {
    START: ORANGE,
    END: TURQUOISE,
    OBSTACLE: BLACK,
    PATH: PURPLE,
    VISITED: RED,
    EMPTY: WHITE
}

class Cell(Sprite):
    def __init__(self, x, y, type: int, color=WHITE):
        super().__init__()
        self.x = x
        self.y = y
        self.type = type
        self.color = color
        self.neighbors = []
        self.g = float('inf')
        self.h = 0
        self.f = float('inf')
        self.parent = None

    def draw(self, window: Surface):
        pygame.draw.rect(window, self.color, (self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def update_color(self):
        self.color = colors.get(self.type, WHITE)

    def update_neighbors(self, grid):
        self.neighbors = []
        directions = [(-1,0), (1,0), (0,-1), (0,1)]
        for dx, dy in directions:
            x = self.x + dx
            y = self.y + dy
            if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
                try:
                    cell = grid[x][y]
                    if cell.type != OBSTACLE:
                        self.neighbors.append(cell)
                except IndexError as e:
                    continue

    def make_start(self):
        self.type = START
        self.update_color()

    def make_end(self):
        self.type = END
        self.update_color()

    def make_barrier(self):
        self.type = OBSTACLE
        self.update_color()

    def reset(self):
        self.type = EMPTY
        self.update_color()
        self.g = float('inf')
        self.h = 0
        self.f = float('inf')
        self.parent = None
        self.neighbors.clear()

    def is_start(self, start):
        return self.x == start.x and self.y == start.y

    def is_end(self, end):
        return self.x == end.x and self.y == end.y

    def get_neighbors(self):
        return self.neighbors

    def update_type(self, type):
        self.type = type

    def get_type(self):
        return self.type

    def __lt__(self, other):
        return (self.x, self.y) < (other.x, other.y)

def make_grid():
    grid = []
    for i in range(GRID_SIZE):
        grid.append([])
        for j in range(GRID_SIZE):
            cell = Cell(i, j, EMPTY)
            grid[i].append(cell)
    return grid

def draw_grid(window, grid):
    for row in grid:
        for cell in row:
            cell.draw(window)

    # Рисуем сетку
    for i in range(GRID_SIZE):
        pygame.draw.line(window, GREY, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE))
        pygame.draw.line(window, GREY, (i * CELL_SIZE, 0), (i * CELL_SIZE, WIDTH))

    pygame.display.update()


def generate_random_grid(grid):
    # Очищаем сетку
    for row in grid:
        for cell in row:
            cell.reset()

    # Выбираем случайные начальную и конечную точки
    start_row, start_col = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
    end_row, end_col = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)

    # Убедимся, что начальная и конечная точки разные
    while (start_row, start_col) == (end_row, end_col):
        end_row, end_col = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)

    start = grid[start_row][start_col]
    end = grid[end_row][end_col]

    start.make_start()
    end.make_end()

    # Добавляем случайные препятствия (20% ячеек)
    obstacle_count = int(GRID_SIZE * GRID_SIZE * 0.2)
    for _ in range(obstacle_count):
        row, col = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        cell = grid[row][col]
        if not cell.is_start(start) and not cell.is_end(end):
            cell.make_barrier()

    return start, end

def heuristic(loc_from, loc_to):
    return abs(loc_from.x - loc_to.x) + abs(loc_from.y - loc_to.y)

def build_path(end):
    path = []
    current = end
    while current.parent:
        path.append(current)
        current = current.parent
    return path[::-1]

def a_star(grid, start, end):
    open_set = PriorityQueue() # Очередь с приоритетом
    open_set.put((0, start)) # Инициализация начальной точки
    start.g = 0 # Начальная стоимость пути
    start.f = heuristic(start, end) # Полная оценка стоимости пути, расстояние (манхэттенское расстояние)


    start.update_neighbors(grid) # Определяем соседей для начальной точки

    open_set_hash = {start} # Все узлы (Поиск)

    while not open_set.empty():
        current = open_set.get()[1] # Получаем узел с минимальной ценой
        open_set_hash.remove(current) # Удаляем узел из множества

        if current == end: # Если мы пришли в конечную точку, то завершаем работу и возвращаем построенный маршрут
            path = build_path(end) # Выстраиваем путь
            return path

        for neighbor in current.neighbors:
            temp_g = current.g + 1 # Повышаем стоимость пути
            if temp_g < neighbor.g: # В случае получения более короткого пути - запоминаем узел, чтобы в дальнейшем через него проводить маршрут
                neighbor.parent = current # Устанавливаем более оптимального родителя по стоимости
                neighbor.g = temp_g # Обновляем стоимость
                neighbor.h = heuristic(neighbor, end) # Вычисляем расстояние
                neighbor.f = neighbor.g + neighbor.h # Вычисляем полную стоимость

                if neighbor not in open_set_hash: # Если узел еще не обработан
                    open_set.put((neighbor.f, neighbor)) # Добавляем в поток на обработку узла
                    open_set_hash.add(neighbor)
                    if neighbor != end and neighbor != start: # Если мы не дошли до конца и сосед не является стартовой позицией, мы изменяем тип точки на посещенную и меняем цвет
                        neighbor.type = VISITED
                        neighbor.update_color()

        draw_grid(WINDOW, grid)
        pygame.time.wait(50)

    return None

def variant_work(window):
    map = [
        [0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
        [2, 0, 1, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 1, 1, 0],
        [0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
        [1, 0, 1, 1, 0, 1, 1, 0, 1, 0],
        [1, 1, 0, 1, 0, 1, 0, 0, 0, 0],
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 0, 0, 0, 0, 0, 1],
        [0, 0, 1, 0, 0, 1, 0, 1, 0, 3]
    ]

    window.fill((0,0,0))
    grid = []
    start, end = None, None
    for i in range(len(map)):
        grid.append([])
        for j in range(len(map)):
            cell = Cell(i, j, types[map[i][j]], colors[map[i][j]])

            if cell.type == START: start = cell
            if cell.type == END: end = cell

            grid[i].append(cell)

    draw_grid(WINDOW, grid)

    for row in grid:
        for cell in row:
            print(cell.x, cell.y)
            cell.update_neighbors(grid)

    path = a_star(grid, start, end)
    print(f"Восстановленный путь: {[(point.x, point.y) for point in path]}")

    if path:
        for cell in path[0:-1]:
            cell.type = PATH
            cell.update_color()
        draw_grid(WINDOW, grid)

def main():

    running = True
    grid = make_grid()
    start, end = generate_random_grid(grid)
    draw_grid(WINDOW, grid)
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.display.flip()
                    variant_work(WINDOW)
                if event.key == pygame.K_r:
                    grid = make_grid()
                    start, end = generate_random_grid(grid)
                    draw_grid(WINDOW, grid)
                elif event.key == pygame.K_SPACE:
                    for row in grid:
                        for cell in row:
                            cell.update_neighbors(grid)

                    path = a_star(grid, start, end)

                    print(f"Восстановленный путь: {[(point.x, point.y) for point in path]}")

                    if path:
                        for cell in path[0:-1]:
                            cell.type = PATH
                            cell.update_color()

                        draw_grid(WINDOW, grid)

        pygame.display.update()

    pygame.quit()

main()