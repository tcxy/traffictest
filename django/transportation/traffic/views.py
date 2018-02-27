from django.shortcuts import render
import json
import queue
import os
from math import *
from django.http import HttpResponse
from traffic.Graph import Graph, Edge, Vertice
from traffic.GEO import GEO
from geopy.distance import vincenty
from collections import defaultdict, deque
from django.conf import settings

# Create your views here.
# Get to the index page
def index(request):
    filepath = os.path.abspath('./traffic/Data/new_model.json')
    with open(filepath, 'r') as model:
        json_data = json.loads(model.read())
        print(json_data['vertices']['1'])
        graph = Graph(json_data)
        settings.graph = graph
    return render(request, 'map.html')

def get_edges(request):
    edges = []  # stores all the edges
    for edge in settings.graph.get_edges():
        # transfer the from vertex and to vertex from numbers into coordinates
        from_vertex = settings.graph.coor_from_num(edge['from_vertice'])
        to_vertex = settings.graph.coor_from_num(edge['to_vertice'])
        # each edge will return several information
        edges.append(Edge(from_vertex, to_vertex, edge['speed'], edge['name'], edge['dis'], edge['id']).get_edge())
    return HttpResponse(json.dumps(edges))


def get_points(request):
    filepath = os.path.abspath('./traffic/Data/inter_model.json')
    with open(filepath, 'r') as inter_model:
        json_data = json.loads(inter_model.read())
        points = set()
        for key in json_data:
            for edge in json_data[key]:
                for point in edge:
                    points.add(tuple(point))
        list_points = [list(x) for x in points]
    return HttpResponse(json.dumps(list_points))

# Get all the red path in the map
def red(request):
    red = []
    for edge in settings.graph.get_edges():
        if float(edge['speed']) < 0.4:
            from_vertex = settings.graph.coor_from_num(edge['from_vertice'])
            to_vertex = settings.graph.coor_from_num(edge['to_vertice'])
            red.append(Edge(from_vertex, to_vertex, edge['speed'], edge['name'], edge['dis'], edge['id']).get_edge())
    return HttpResponse(json.dumps(red));

# Get all the green path in the map
def green(request):
    green = []
    for edge in settings.graph.get_edges():
        if float(edge['speed']) > 0.8:
            from_vertex = settings.graph.coor_from_num(edge['from_vertice'])
            to_vertex = settings.graph.coor_from_num(edge['to_vertice'])
            green.append(Edge(from_vertex, to_vertex, edge['speed'], edge['name'], edge['dis'], edge['id']).get_edge())
    return HttpResponse(json.dumps(green));

# Get all the yellow path in the map
def yellow(request):
    yellow = []
    for edge in settings.graph.get_edges():
        if float(edge['speed']) > 0.4 and float(edge['speed']) < 0.8:
            from_vertex = settings.graph.coor_from_num(edge['from_vertice'])
            to_vertex = settings.graph.coor_from_num(edge['to_vertice'])
            yellow.append(Edge(from_vertex, to_vertex, edge['speed'], edge['name'], edge['dis'], edge['id']).get_edge())
    return HttpResponse(json.dumps(yellow));

# Retrieve graph from local file
def getGraph():
    with open('C:/Users/new user/Dropbox/La Crosse/Traffic/Project/Data Module/model.json', 'r') as f:
        json_data = json.loads(f.read())
        edges = json_data['edges']
        graph = Graph()
        for edge in edges:
            from_vertice = Vertice(edge['from_vertice'][0], edge['from_vertice'][1])
            to_vertice = Vertice(edge['to_vertice'][0], edge['to_vertice'][1])
            graph.add_edge(from_vertice, to_vertice, edge['speed'], edge['name'], edge['dis'])
    return graph


def getNearestStreet(graph, vertice):
    vertices = graph.get_vertex()
    shortestpath = 65535
    shortestpoint = Vertice()
    point1 = (vertice.getLat(), vertice.getLng())
    for vertice in vertices:
        point2 = (vertice[1], vertice[0])
        path = vincenty(point1, point2).kilometers
        if path < shortestpath:
            shortestpath = path
            shortestpoint = vertice

    return shortestpoint

# Get the distance between two coordinates
def getDistance(PAx, PAy, PBx, PBy, PCx, PCy):
    A = (PAy, PAx)
    B = (PBy, PBx)
    C = (PCy, PCx)
    ab = vincenty(A, B).kilometers
    bc = vincenty(B, C).kilometers
    ac = vincenty(A, C).kilometers

    l = (ab + bc + ac) / 2
    s = sqrt(l * (l - ab) * (l - bc) * (l - ac))
    return 2 * s / ab

# Shortest path dijkstra algorithm
def dijkstra(graph, departure, destination):
    q = queue.PriorityQueue()
    parents = {}
    distances = {}
    start_weight = float("inf")

    for num in graph.get_vertex():
        weight = start_weight
        num = int(num)
        if departure == num:
            weight = 0.0
        distances[num] = weight
        parents[num] = None

    q.put(([0,departure]))

    while not q.empty():
        v_tuple = q.get()
        v = int(v_tuple[1])
        print("v is ")
        print(v)

        for edge in graph.get_edges_from_point(v):
            # for each edge, the first element to to vertice, the second element is weight
            print(edge)
            to_vertice = int(edge[0])
            weight = edge[1]
            candidate_weight = distances[v] + float(weight)
            to_vertice = int(to_vertice)
            if distances[to_vertice] > candidate_weight:
                distances[to_vertice] = candidate_weight
                parents[to_vertice] = v

                if candidate_weight < - 1000:
                    raise Exception("Negative cycle detected")
                q.put(([distances[to_vertice], to_vertice]))


    s_path = []
    end = destination
    print('parents are')
    print(parents)
    print('distances are')
    print(distances)
    while end is not None:
        s_path.append(end)
        end = parents[end]

    s_path.reverse()

    return s_path


# Return the list of path which from depart to dest
def navigate(request):
    if request.method == 'POST':
        filepath = os.path.abspath('./traffic/Data/model.json')
        with open(filepath, 'r') as model:
            graph = settings.graph
            print('navigate function start')
            depart_lat = request.POST.get('depart_lat')
            depart_lng = request.POST.get('depart_lng')
            dest_lat = request.POST.get('dest_lat')
            dest_lng = request.POST.get('dest_lng')
            print('tries to build graph')
            depart = graph.nearest_point(depart_lat, depart_lng)
            print('depart is : ' + str(depart))
            dest = graph.nearest_point(dest_lat, dest_lng)
            print('dest is: ' + str(dest))
            print('find shortest path')
            path = dijkstra(graph, depart, dest)
            print('path: ' + str(path))
            # coordinate_path = []
            # for point in path:
            #     coordinate = graph.coor_from_num(point)
            #     coordinate_path.append(coordinate)
            edges = []
            for i in range(len(path) - 1):
                edges.append(graph.get_edge_by_coor(path[i], path[i+1]))

            return HttpResponse(json.dumps({
                "path": edges
            }))