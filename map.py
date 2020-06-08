# -----------------------------------------------------------
# create a simple GeoJSON for the Call Detail Record (CDR)
# data so that locations can be visualised on a map. this
# creates single point geometry format based on latitude and
# longitude data, specified in WGS 84 decimal degrees, for
# each record in the CDR input file.
#
# GeoJSON format: https://tools.ietf.org/html/rfc7946
# GeoJSONLint:    http://geojsonlint.com/
# Visualisation:  http://geojson.io/
#
# https://github.com/FixTheCode CC0 1.0 Universal
# -----------------------------------------------------------
import csv
import sys
import json
import argparse

import geo


def main():

    def get_property(name: str, value: str, last=False) -> str:
        # returns a GeoJSON property field. apply a different format if the
        # field is the last one
        response = '"' + name + '":"' + value + '"'
        if last:
            response += '},'
        else:
            response += ','
        return (response)

    def get_geometry(x0: float, y0: float, last=False) -> str:
        # returns a GeoJSON geometry field. apply a different format if the
        # field is the last one
        response = '"geometry": {"type":"Point","coordinates": [' + \
            y0 + ',' + x0 + ']}}'
        if not last:
            response += ','
        return (response)

    def validate_file(file_name: str, x: int, y: int):
        # validate that the field positions specified on the command line are
        # valid and that each coordinate at the specified positions are valid
        # WGS 84 format
        invalid_rows = ''
        f = open(file_name, 'r')
        reader = csv.DictReader(f)
        fields = reader.fieldnames
        for row in reader:
            try:
                a = int(x, 10)
                b = int(y, 10)
            except ValueError:
                print('error: -x and -y must be integers.')
                sys.exit(-1)
            try:
                x0 = row[fields[a]]
                y0 = row[fields[b]]
                float(x0)
                float(y0)
                if not geo.is_valid_coordinate(float(x0), float(y0)):
                    invalid_rows += 'Row ' + str(reader.line_num) + \
                        ' invalid WGS 84 coordinate ' + \
                        str(x0) + ', ' + str(y0) + '\n'
            except ValueError:
                print(
                    'error: check values for -x and -y are correct. field ' +
                    str(x) +
                    ' = ' +
                    str(x0) +
                    ' field ' +
                    str(y) +
                    ' = ' +
                    str(y0))
                sys.exit(-1)

        if len(invalid_rows) > 0:
            print(invalid_rows)
            sys.exit(-1)

    # open specified csv file to process and scan to check that all the geo
    # coordinates are valid. if validation passes we have a file with valid
    # WGS 84 format coordinates and we will be able to output a GeoJSON
    # representation
    validate_file(args.i, args.x, args.y)
    try:
        f = open(args.i, 'r')
        total_rows = sum(1 for row in f)
        f.seek(0)
        rawData = csv.DictReader(f)
        current_field = 0
    except (FileNotFoundError):
        raise SystemExit(
            f'File ' + args.i + ' not found.')

    # create GeoJSON from the input file.  coordinate fields are skipped when
    # creating the properties for a row and used to create the geometry section
    # once all other fields  have been processed
    output = '{"type": "FeatureCollection","features": ['
    header = rawData.fieldnames
    x = (int(args.x, 10))
    y = (int(args.y, 10))
    for row in rawData:
        x0 = row[header[x]]
        y0 = row[header[y]]
        output += '{"type":"Feature","properties":{'
        while current_field <= len(header):
            if current_field == x or current_field == y:
                current_field += 1
            elif current_field == len(header) - 3:
                output += get_property(header[current_field],
                                       row[header[current_field]], True)
            elif current_field == len(header):
                if rawData.line_num != total_rows:
                    output += get_geometry(x0, y0)
                else:
                    output += get_geometry(x0, y0, True)
            else:
                output += get_property(header[current_field],
                                       row[header[current_field]])
            current_field += 1
        current_field = 0
    output += ']}'

    # output a formatted or minimised geoJSON file. it is possible that the
    # incorrect specified field positions for coordinates return a valid type
    # that results in a malfored string.
    if not args.m:
        try:
            parsed = json.loads(output)
            output = json.dumps(parsed, indent=4)
        except BaseException:
            print(
                'invalid JSON. check that -x and -y were correct. run with -m to see output.')
            sys.exit(-1)
    print(output)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-m',
        action='store_true',
        help='minimise the GeoJSON output')
    parser.add_argument(
        '-i',
        required=True,
        metavar="FILE",
        help='input file')
    parser.add_argument(
        '-x',
        required=True,
        metavar="INT",
        help='position of latituide field in file')
    parser.add_argument(
        '-y',
        required=True,
        metavar="INT",
        help='position of longitude field in file')
    args = parser.parse_args()
    main()
