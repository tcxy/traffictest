from django.shortcuts import render
import json
import queue
import math
from django.http import HttpResponse
from traffic.Graph import Graph, Vertice, Edge

def navigate(request):
    if request.method == 'POST':
        depart_lat = request.POST.get('depart_lat')
        depart_lng = request.POST.get('depart_lng')
        dest_lat = request.POST.get('dest_lat')
        dest_lng = request.POST.get('dest_lng')
        graph = getGraph()
        street = getNearestStreet(graph, Vertice(depart_lng, depart_lat).getLocation(), Vertice(dest_lng, dest_lat).getLocation)
        return HttpResponse(json.dumps({
            "edge": street
        }))


def getGraph():
    with open('/Users/duwei/development/workspace/python/Web/Transportation/model.json', 'r') as f:
        json_data = json.load(f.read());
        edges = json_data['edges'];
        graph = Graph();
        for edge in edges:
            from_vertice = Vertice(edge['from_vertice'][0], edge['from_vertice'][1])
            to_vertice = Vertice(edge['to_vertice'][0], edge['to_vertice'][1])
            graph.add_edge(from_vertice, to_vertice, edge['speed'], edge['name'], edge['dis']);
    return graph

def getNearestStreet(graph, departure, destination):
    q = queue.PriorityQueue()
    parents = []
    distances = []
    start_weight = float("inf")

    for vertex in graph.get_vertex():
        weight = start_weight
        if departure == vertex:
            weight = 0
        distances.append(weight)
        parents.append(None)

    return None

def distanceBtwP(lonA, latA, lonB, latB):
    radLng = latA * math.pi / 180.0
    radLn2 = latB * math.pi / 180.0
    a = radLng - radLn2
    b = (lonA - lonB) * math.pi / 180.0
    s = 22 * math.asin(math.sqrt(math.pow(math.sin(a / 2), 2) + math.cos(radLng) * math.cos(radLn2) * math.pow(math.sin(b / 2), 2))) * 6378.137;
    return s

def getDistance(PAx, PAy, PBx, PBy, PCx, PCy):
    a = distanceBtwP(PAy, PAx, PBy, PBx);
    b = distanceBtwP(PBy, PBx, PCy, PCx);
    c = distanceBtwP(PAy, PAx, PCy, PCx);

    if (b * b >= c * c + a * a):
        return c
    if (c * c >= b * b + a * a):
        return b
    l = (a + b + c) / 2
    s = math.sqrt(l * (l - a) * (l - b) * (l - c))
    return 2 * s / a