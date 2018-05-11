import math

class GEO(object):

    def __init__(self):
        self.__PI = 3.14159265359
        self.__TWOPI = 6.28318530718
        self.__DE2RA = 0.01745329252
        self.__RA2DE = 57.2957795129
        self.__ERAD = 6378.135
        self.__ERADM = 6378135.0
        self.__AVG_ERAD = 6371.0
        self.__flattening = 1.0 / 298.257223563
        self.__eps = 0.000000000005
        self.__km2mi = 0.621371
        self.__geistatuibart_alt = 35786.0

    def gc_intersec_segement(self, lat1A, lon1A, lat1B, lon1B, lat2A, lon2A, lat2B, lon2B):
        radlat1A = lat1A * self.__DE2RA
        radlon1A = lon1A * self.__DE2RA
        radlat1B = lat1B * self.__DE2RA
        radlon1B = lon1B * self.__DE2RA
        radlat2A = lat2A * self.__DE2RA
        radlon2A = lon2A * self.__DE2RA
        radlat2B = lat2B * self.__DE2RA
        radlon2B = lon2B * self.__DE2RA

        d1 = self.approx_distance(lat1A, lon1A, lat1B, lon1B)
        d2 = self.approx_distance(lat2A, lon2A, lat2B, lon2B)

        P1 = (math.cos(radlat1A) * math.cos(radlon1A), math.cos(radlat1A) * math.sin(radlon1A), math.sin(radlat1A))
        P2 = (math.cos(radlat1B) * math.cos(radlon1B), math.cos(radlat1B) * math.sin(radlon1A), math.sin(radlat1B))
        P3 = (math.cos(radlat2A) * math.cos(radlon2A), math.cos(radlat2A) * math.sin(radlon2A), math.sin(radlat2A))
        P4 = (math.cos(radlat2B) * math.cos(radlon2B), math.cos(radlat2B) * math.sin(radlon2B), math.sin(radlat2B))

        V1 = (P1[1] * P2[2] - P2[1] * P1[2], P2[0] * P1[2] - P1[0] * P2[2], P1[0] * P2[1] - P2[0] * P1[1])
        V2 = (P3[1] * P4[2] - P4[1] * P3[2], P4[0] * P3[2] - P3[0] * P4[2], P3[0] * P4[1] - P4[0] * P3[1])

        length1 = math.sqrt(V1[0] * V1[0] + V1[1] * V1[1] + V1[2] * V1[2])
        length2 = math.sqrt(V2[0] * V2[0] + V2[1] * V2[1] + V2[2] * V2[2])

        U1 = (V1[0] / length1, V1[1] / length1, V1[2] / length1)
        U2 = (V2[0] / length2, V2[1] / length2, V2[2] / length2)

        if math.fabs(U1[0] - U2[0]) < self.__eps or math.fabs(U1[1] - U2[1]) < self.__eps or math.fabs(U1[2] - U2[2]) < self.__eps:
            return None, None

        D = (U1[1] * U2[2] - U2[1] * U1[2], U2[0] * U1[2] - U1[0] * U2[2], U1[0] * U2[1] - U2[0] * U1[1])
        lengthd = math.sqrt(D[0] * D[0] + D[1] * D[1] + D[2] * D[2])

        S1 = (D[0] / lengthd, D[1] / lengthd, D[2] / lengthd)
        S2 = (-S1[0], -S1[1], -S1[2])

        lat1 = math.asin(S1[2])

        tmp = math.cos(lat1)
        sign = math.asin(S1[1] / tmp)
        if sign > 0:
            sign = 1
        else:
            sign = -1
        lon1 = math.acos(S1[0] / tmp) * sign

        lat2 = math.asin(S2[2])
        tmp = math.cos(lat2)
        sign = math.asin(S2[1] / tmp)
        if sign > 0:
            sign = 1
        else:
            sign = -1
        lon2 = math.acos(S2[0] / tmp) * sign

        lat1 = lat1 * self.__RA2DE
        lon1 = lon1 * self.__RA2DE
        lat2 = lat2 * self.__RA2DE
        lon2 = lon2 * self.__RA2DE

        d1a1 = self.approx_distance(lat1A, lon1A, lat1, lon1)
        d1b1 = self.approx_distance(lat1, lon1, lat1B, lon1B)
        d2a1 = self.approx_distance(lat2A, lon2A, lat1, lon1)
        d2b1 = self.approx_distance(lat1, lon1, lat2B, lon2B)

        d1a2 = self.approx_distance(lat1A, lon1A, lat2, lon2)
        d1b2 = self.approx_distance(lat2, lon2, lat1B, lon1B)
        d2a2 = self.approx_distance(lat2A, lon2A, lat2, lon2)
        d2b2 = self.approx_distance(lat2, lon2, lat2B, lon2B)

        if d1a1 < d1 and d1b1 < d1 and d2a1 < d2 and d2b1 < d2:
            return lat1, lon1
        elif d1a2 < d1 and d1b2 < d1 and d2a2 < d2 and d2b2 < d2:
            return lat2, lon2
        else:
            return None, None

    def approx_distance(self, lat1, lon1, lat2, lon2):
        lat1 = math.radians(lat1)
        lon1 = math.radians(lon1)
        lat2 = math.radians(lat2)
        lon2 = math.radians(lon2)
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = math.pow(math.sin(dlat / 2), 2) + math.cos(lat1) * math.cos(lat2) * \
                                                             math.pow(math.sin(dlon / 2), 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        if c == 0:
            print("lat1 is %f, lng1 is %f, lat2 is %f, lng2 is %f" % (lat1, lon1, lat2, lon2))
        return self.__ERAD* c