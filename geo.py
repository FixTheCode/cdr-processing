# -----------------------------------------------------------
# geo utility functions
#
# https://github.com/FixTheCode CC0 1.0 Universal
# -----------------------------------------------------------
import random
import json
import itertools as it
from math import acos

import numpy as np


def get_random_location(x0: float, y0: float, meters: int):
    """
    generate a random location within an approximate number of meters from
    specified decimal degree coordinates. we restrict to 6 decimal places as
    this is sufficient precision to identify an object e.g. person
    or device

    """

    x0, y0 = float(x0), float(y0)
    if is_valid_coordinate(x0, y0):
        # approximate equivalent of meters to a degree is 111139
        r = meters / 111139
        u = np.random.uniform(0, 1)
        v = np.random.uniform(0, 1)
        # ensure points are created within a radius
        w = r * np.sqrt(u)
        t = 2 * np.pi * v
        x = w * np.cos(t)
        y = w * np.sin(t)
        # cater for lat longs being in degrees by shrinking the the east-west
        # distances
        x1 = x / np.cos(y0)
    return (float('%.6f' % (x0 + x1)), float('%.6f' % (y0 + y)))


def is_valid_coordinate(x0: float, y0: float) -> bool:
    """
    validates a latitude and longitude decimal degree coordinate pairs.

    """
    if isinstance(x0, float) and isinstance(y0, float):
        if -90 <= x0 <= 90:
            if -180 <= y0 <= 180:
                return True
    return False


def get_distance(x0: float, y0: float, x1: float, y1: float) -> int:
    """
    calculate the distance between two latitude and longitude decimal degress
    pairs. we use the haversine formula to calculate the straight line
    distance between two points in miles.

    """
    result = -1
    radius_miles = 3958.756
    if is_valid_coordinate(x0, y0) and is_valid_coordinate(x1, y1):
        y0, x0, y1, x1 = map(np.radians, [y0, x0, y1, x1])
        result = float(
            '%.1f' %
            (radius_miles *
             acos(
                 np.sin(x0) *
                 np.sin(x1) +
                 np.cos(x0) *
                 np.cos(x1) *
                 np.cos(
                     y0 -
                     y1))))
    return result


def is_within_boundary(lat: float, lng: float, poly: list) -> bool:
    """
    determines if a point is within a 2D polygon. the polygon shape is
    completed by the modulus operator. Given the coordinate list of A,B,C,D
    we process A,B,C,D,A. we use latitude and longitude coordinates to
    determine each point of our polygon.  we expect coordinates as a list
    of strings that we convert to floats e.g
    '60.6733322143556,-0.835000038146973'

    https://www.eecs.umich.edu/courses/eecs380/HANDOUTS/PROJ2/InsidePoly.html

    an alternative would be to use matplotlib Path class and contains_point
    function
    """
    n = len(poly)
    result = False

    x0, y0 = str(poly[0]).split(',')
    for i in range(n + 1):
        x1, y1 = str(poly[i % n]).split(',')
        if lng > min(float(y0), float(y1)):
            if lng <= max(float(y0), float(y1)):
                if lat <= max(float(x0), float(x1)):
                    if float(y0) != float(y1):
                        xinters = float(x0) + (float(lng) - float(y0)) * \
                            (float(x1) - float(x0)) / \
                            (float(y1) - float(y0))
                    if float(x0) == float(x1) or float(
                            lat) <= float(xinters):
                        result = not result
                        return result
        x0, y0 = x1, y1

    return result


def extract_geojson_coordinates(file_name: str) -> list:
    """
    note that GeoJSON orders coordinates as longitude, latitude. we need them
    in the normal convention of latitude, longitude.  it is normal for
    geographic boundaries to be represented using the MultiPolygon datatype in
    GeoJSON. we want each coordinate to be represented like this
    58.3177719116212,-6.23250007629395,
    """
    try:
        f = open(file_name, 'r')
        data = json.load(f)
    except (FileNotFoundError):
        raise SystemExit('File ' + file_name + ' not found.')
    except (ValueError):
        raise SystemExit('File is not a valid JSON document.')

    boundary = ''
    lst = []
    for t in data['features']:
        all_coords = list(
            it.chain.from_iterable(
                t['geometry']['coordinates']))
        for c in all_coords:
            x = str(
                str(c).replace(
                    '[', '').replace(
                    ']', '')).split(',')
            multipoint_length = len(x)
            for i in range(0, multipoint_length - 1, 2):
                if i == 0:
                    pair = x[i + 1] + ',' + x[i]
                elif i == int(multipoint_length - 2):
                    pair = ':'
                else:
                    pair = ':' + x[i + 1] + ',' + x[i]
                boundary += pair.replace('"', '')
            boundary = boundary.replace(' ', '')
            lst.append(boundary)
        boundary = boundary[:-1]
    boundary = boundary[:-1]
    lst = list(boundary.split(':'))
    return(lst)
