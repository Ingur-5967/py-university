import time
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import math
import heapq
import osmnx as ox

# Скачиваем граф по названию города
G = ox.graph_from_place('Любляна, Словения', network_type='drive')
# Сохраняем в файл для последующего использования
ox.save_graphml(G, 'slowenia_road_network.graphml')

def haversine(coord1: tuple[float, float], coord2: tuple[float, float]) -> float:
    lon1, lat1 = coord1
    lon2, lat2 = coord2
    R = 6371

    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))



def dijkstra(graph: dict[tuple[float, float], list[tuple[tuple[float, float], float]]], start: tuple[float, float], end: tuple[float, float]) -> tuple[list[tuple[float, float]], float]:

    start_execute_time = time.time()

    queue = []
    heapq.heappush(queue, (0.0, start))

    paths = {start: (None, 0.0)}
    visited = set()

    while queue:
        current_distance, c_node = heapq.heappop(queue)

        if c_node == end:
            break

        if c_node in visited:
            continue

        visited.add(c_node)

        for neighbor, distance in graph.get(c_node, []):
            new_distance = current_distance + distance
            if neighbor not in paths or new_distance < paths[neighbor][1]:
                paths[neighbor] = (c_node, new_distance)
                heapq.heappush(queue, (new_distance, neighbor))

    path = []
    current = end
    total_distance = 0.0
    if end not in paths:
        return [], math.inf, []

    while current is not None:
        path.append(current)
        next_node = paths[current][0]
        if next_node is not None:
            total_distance += haversine(current, next_node)
        current = next_node

    path.reverse()

    end_execute_time = (time.time() - start_execute_time) * 1000

    print(f"Алгоритм Дейкстры закончил за {end_execute_time}ms")

    return path, total_distance


def build_graph(edges: list[tuple[tuple[float, float], tuple[float, float], str]]) -> dict[tuple[float, float], list[tuple[tuple[float, float], float]]]:
    graph = {}
    for start, end, _ in edges:
        dist = haversine(start, end)
        graph.setdefault(start, []).append((end, dist))
        graph.setdefault(end, []).append((start, dist))
    return graph


def read_graphml(file_path: str) -> tuple[dict[str, tuple[float, float]], list[tuple[tuple[float, float], tuple[float, float], str]]]:
    tree = ET.parse(file_path)
    root = tree.getroot()

    namespaces = {'g': 'http://graphml.graphdrawing.org/xmlns'}

    nodes = {}

    for node in root.findall('.//g:node', namespaces):
        node_id = node.get('id')
        x, y = 0.0, 0.0
        for data in node.findall('g:data', namespaces):
            key = data.get('key')
            if key == 'd5':
                x = float(data.text)
            elif key == 'd4':
                y = float(data.text)
        nodes[node_id] = (x, y)

    edges = []
    for edge in root.findall('.//g:edge', namespaces):
        source = edge.get('source')
        target = edge.get('target')
        street_name = ''
        for data in edge.findall('g:data', namespaces):
            if data.get('key') == 'd13':
                street_name = data.text
        if source in nodes and target in nodes:
            edges.append((nodes[source], nodes[target], street_name))

    return nodes, edges


def find_street_index(edges: list[tuple[tuple[float, float], tuple[float, float], str]], street_name_query: str) -> tuple[int, str]:
    for i, (_, _, name) in enumerate(edges):
        if name.lower() == street_name_query.lower():
            return i, name

    return -1, None


def visualize_path_with_network(edges, path, street_names=None, figsize=(20, 20)):
    """
    Визуализация всей дорожной сети + маршрута красным.
    Если передан список street_names, то названия улиц выводятся вдоль маршрута.
    """
    plt.figure(figsize=figsize)
    ax = plt.gca()

    # Все рёбра — серые
    all_lines = [(start, end) for start, end, _ in edges]
    lc = LineCollection(all_lines, linewidths=0.3, colors='gray', alpha=0.4)
    ax.add_collection(lc)

    # Путь — красный
    if path and len(path) > 1:
        path_lines = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
        lc_path = LineCollection(path_lines, linewidths=2.0, colors='red', alpha=0.9)
        ax.add_collection(lc_path)

        # Отображаем названия улиц, если они заданы
        if street_names:
            for i in range(len(path) - 1):
                mid_point = ((path[i][0] + path[i + 1][0]) / 2, (path[i][1] + path[i + 1][1]) / 2)
                if i < len(street_names) and street_names[i]:
                    plt.text(mid_point[0], mid_point[1], street_names[i],
                             fontsize=8, color='blue', ha='center')

    ax.autoscale()
    plt.axis('equal')
    plt.title('Кратчайший маршрут')
    plt.xlabel('Долгота')
    plt.ylabel('Широта')
    plt.grid(False)
    plt.tight_layout()
    plt.show()


def visualize_only_path(path, figsize=(10, 10)):
    """
    Визуализирует только маршрут (без остального графа)
    """
    if not path or len(path) < 2:
        print("Маршрут слишком короткий или отсутствует.")
        return

    plt.figure(figsize=figsize)
    ax = plt.gca()

    path_lines = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
    lc_path = LineCollection(path_lines, linewidths=2.5, colors='red', alpha=0.9)
    ax.add_collection(lc_path)

    ax.autoscale()
    plt.axis('equal')
    plt.title("Кратчайший маршрут")
    plt.xlabel("Долгота")
    plt.ylabel("Широта")
    plt.grid(True)
    plt.tight_layout()
    plt.show()



if __name__ == "__main__":
    # 1. Загрузка данных
    nodes, edges = read_graphml("slowenia_road_network.graphml")

    # 2. Задаём названия улиц для начала и конца маршрута
    #start_street_query = "Cesta 24. junija"
    #start_street_query = "Šmartinska cesta"

    start_street_query = "Brdnikova ulica"
    end_street_query = "Ulica Rezke Dragarjeve"

    #end_street_query = "Smrekarjeva ulica"
    #end_street_query = "Smrekarjeva ulica"

    # 3. Используем find_street_index для определения нужных рёбер
    start_index, start_street = find_street_index(edges, start_street_query)
    end_index, end_street = find_street_index(edges, end_street_query)

    if start_index == -1 or end_index == -1:
        print("Не удалось найти заданную улицу для начала или конца маршрута")
    else:
        # 4. Определяем стартовый и конечный узлы:
        # Используем первую точку ребра для старта и вторую точку ребра для финиша.
        start_node = edges[start_index][0]
        end_node = edges[end_index][1]

        # 5. Строим граф и ищем кратчайший путь
        graph = build_graph(edges)
        path, distance = dijkstra(graph, start_node, end_node)

        if not path:
            print("Путь не найден")
        else:
            print(f"Найден путь длиной {distance:.2f} км")
            print(f"Вершин/Ребер {len(nodes)}/{len(edges)}")

            # 6. Визуализация маршрута
            visualize_path_with_network(edges, path)
