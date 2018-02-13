# !/usr/bin/python3

import json

from math import radians, cos, sin, asin, sqrt
from traffic.GEO import GEO

class Vertice(object):

    def __init__(self, longitude=0, latitude=0):
        self.__longitude = longitude
        self.__latitude = latitude

    def __str__(self):
        return "Point " + self.__longitude + ", " + self.__latitude

    def get_location(self):
        return [self.__longitude, self.__latitude]

class Edge(object):

    def __init__(self, from_vertice=None, to_vertice=None, speed=0, name='', dis=0):
        if from_vertice == None:
            self.__from_vertice = -1
        else:
            self.__from_vertice = from_vertice
        if to_vertice == None:
            self.__to_vertice = -1
        else:
            self.__to_vertice = to_vertice
        self.__speed = speed
        self.__name = name
        self.__dis = dis

    def __str__(self):
        return "from " + str(self.__from_vertice) + " to " . str(self.__to_vertice) + ", the speed is " + str(self.__speed)

    def get_edge(self):
        return {'name': self.__name, 'from_vertice': self.__from_vertice, 'to_vertice': self.__to_vertice,
                'speed': self.__speed, 'dis': self.__dis}

class Graph(object):

    def __init__(self, graph_dict=None):
        if graph_dict == None:
            graph_dict = {}
            self.__vertices = []
            self.__edges = []
            self.__points = 0
            self.__vertex_dict = {}
        else:
            graph_dict = json.loads(graph_dict)
            self.__vertices = graph_dict['vertices']
            self.__edges = graph_dict['edges']

    def add_vertex(self, vertice=None):
        if not vertice == None and vertice.get_location() not in self.__vertices:
            for vex in self.__vertices:
                if self.same_point(vertice.get_location()[1], vertice.get_location()[0], vex[1], vex[0]):
                    return
            self.__vertices.append(vertice.get_location())
            self.__vertex_dict[self.__points] = vertice.get_location()
            self.__points += 1

    def add_vertices(self, from_vertice ,to_vertice):
        same1 = False
        same2 = False
        if not from_vertice == None and from_vertice.get_location() not in self.__vertices and not to_vertice == None \
            and to_vertice.get_location() not in self.__vertices:
            for vex in self.__vertices:
                if self.same_point(from_vertice.get_location()[1], from_vertice.get_location()[0], vex[1], vex[0]):
                    same1 = True
                    break
            for vex in self.__vertices:
                if self.same_point(to_vertice.get_location()[1], to_vertice.get_location()[0], vex[1], vex[0]):
                    same2 = True
                    break
            if same1 and same2:
                self.__vertices.append(to_vertice.get_location())
                self.__vertex_dict[self.__points] = to_vertice.get_location()
                self.__points += 1
                return
            if not same1:
                self.__vertices.append(from_vertice.get_location())
                self.__vertex_dict[self.__points] = from_vertice.get_location()
                self.__points += 1
            if not same2:
                self.__vertices.append(to_vertice.get_location())
                self.__vertex_dict[self.__points] = to_vertice.get_location()
                self.__points += 1
            return

    def add_edge(self, from_vertice, to_vertice, speed=0, name="", dis=0):
        self.add_vertices(from_vertice, to_vertice)
        fv = self.point_in_graph(from_vertice.get_location()[1], from_vertice.get_location()[0])
        fvc = self.coor_from_num(fv)
        tv = self.point_in_graph(to_vertice.get_location()[1], to_vertice.get_location()[0])
        tvc = self.coor_from_num(tv)

        lat1A = float(fvc[1])
        lon1A = float(fvc[0])

        lat1B = float(tvc[1])
        lon1B = float(tvc[0])

        geo = GEO()

        lat = 0
        lon = 0

        # For each edge in this graph, try to identify if they have intersections with other edge
        for edge in self.__edges[:]:
            print(edge)
            from_verticeA = self.coor_from_num(edge['from_vertice'])
            lat2A = float(from_verticeA[1])
            lon2A = float(from_verticeA[0])

            to_verticeA = self.coor_from_num(edge['to_vertice'])
            lat2B = float(to_verticeA[1])
            lon2B = float(to_verticeA[0])

            lat, lon = geo.gc_intersec_segement(lat1A, lon1A, lat1B, lon1B, lat2A, lon2A, lat2B, lon2B)
            if not lat == None and not lon == None and not self.same_point(lat, lon, lat1A, lon1A) \
                    and not self.same_point(lat, lon, lat1B, lon1B) and not self.same_point(lat, lon, lat2A, lon2A) \
                    and not self.same_point(lat, lon, lat2B, lon2B):
                self.__edges.remove(edge)
                if self.haversine(lat1A, lon1A, lat, lon) == 0: 
                    print("lat1A is %f, lng1A is %f, lat is %f, lng is %f" % (lat1A, lon1A, lat, lon))
                if self.haversine(lat, lon, lat1B, lon1B) == 0:
                    print("lat is %f, lng is %f, lat1B is %f, lng1B is %f" % (lat, lon, lat1B, lon1B))
                if self.haversine(lat2A, lon2A, lat, lon) == 0:
                    print("lat2A is %f, lng2A is %f, lat is %f, lng is %f" % (lat2A, lon2A, lat, lon))
                if self.haversine(lat, lon, lat2B, lon2B) == 0:
                    print("lat is %f, lng is %f, lat2B is %f, lng2B is %f" % (lat, lon, lat2B, lon2B))
                self.add_edge(Vertice(lon2A, lat2A), Vertice(lon, lat), speed, name, self.haversine(lat1A, lon1A, lat, lon))
                self.add_edge(Vertice(lon, lat), Vertice(lon2B, lat2B), speed, name, self.haversine(lat, lon, lat1B, lon1B))
                self.add_edge(Vertice(lon1A, lat1A), Vertice(lon, lat), edge['speed'], edge['name'], self.haversine(lat2A, lon2A, lat, lon))
                self.add_edge(Vertice(lon, lat), Vertice(lon1B, lat1B), edge['speed'], edge['name'], self.haversine(lat, lon, lat2B, lon2B))
                return
        if self.haversine(lat1A, lon1A, lat1B, lon1B) == 0:
            return
        self.__edges.append(Edge(fv, tv, speed, name, dis).get_edge())


    def get_vertex(self):
        return self.__vertex_dict

    def get_edges(self):
        return self.__edges

    def get_detailed_edges(self):
        return_edges = []
        for edge in self.__edges:
            new_edge = {}
            new_edge['name'] = edge['name']
            new_edge['speed'] = edge['speed']
            new_edge['dis'] = edge['dis']
            new_edge['from_vertice'] = self.coor_from_num(int(edge['from_vertice']))
            new_edge['to_vertice'] = self.coor_from_num(int(edge['to_vertice']))
            return_edges.append(new_edge)
        return return_edges

    def get_edges_from_point(self, from_vertice):
        lng = self.__vertex_dict[from_vertice][0]
        lat = self.__vertex_dict[from_vertice][1]
        edges = []
        for edge in self.__edges:
            from_vertice = self.__vertex_dict[edge["from_vertice"]]
            if (from_vertice[0] == lng and from_vertice[1] == lat):
                edges.append(edge)

        return edges

    def point_in_graph(self, lat1, lon1):
        for num, vex in self.__vertex_dict.items():
            dis = self.haversine(lat1, lon1, vex[1], vex[0])
            if dis < 45:
                return num

    def coor_from_num(self, num):
        for key, coor in self.__vertex_dict.items():
            if key == num:
                return coor

    def same_point(self, lat1, lon1, lat2, lon2):
        dis = self.haversine(lat1, lon1, lat2, lon2)
        return True if not dis == 0 and dis < 45 else False

    def haversine(self, lat1, lng1, lat2, lng2):
        geo = GEO()
        return geo.approx_distance(float(lat1), float(lng1), float(lat2), float(lng2))

    def get_point_num(self):
        return len(self.__vertex_dict)