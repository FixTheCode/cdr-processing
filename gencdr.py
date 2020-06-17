# -----------------------------------------------------------
# create random call detail record test data
#
# https://github.com/FixTheCode CC0 1.0 Universal
# -----------------------------------------------------------
import random
import sys
import argparse
import uuid
from datetime import datetime, timedelta
from random import randint

import data
import geo


def main():

    def get_checkdigit(number) -> int:
        """ Generate the Luhn algorithm check digit to append to the number provided. """
        digit = checksum(number + '0')
        return (10 - digit) % 10

    def checksum(number) -> int:
        """ Compute the Luhn algorithm checksum to validate the number provided. """
        digits = list(map(int, number))
        odd_sum = sum(digits[-1::-2])
        even_sum = sum([sum(divmod(2 * d, 10))
                        for d in digits[-2::-2]])
        return (odd_sum + even_sum) % 10

    def get_random_phone_number() -> str:
        """ generate a random UK mobile number """
        mobile = random.choice(
            data.mobile_numbers) + str(random.randrange(100, 10000000000))
        return str(mobile[:13])

    def get_random_IMEI_number() -> str:
        """
        generate a random International Mobile Station Equipment Identity
        IMEI number of 14 digits and check digit calculated using the Luhn
        formula. Format is 8-digit TAC code + 6-digit serial number + check
        digit

        """
        imie = str(random.choice(data.imie_type_identifier))
        imie += str(random.randrange(1, 999999))
        imie += str(get_checkdigit(imie))
        return (imie)

    def get_random_date(start_date, end_date):
        """ generate a random date between two dates """
        time_between = end_date - start_date
        days_between = time_between.days
        random_date = start_date + timedelta(
            days=random.randrange(days_between),
            hours=random.randrange(24),
            minutes=random.randrange(60),
            seconds=random.randrange(60))
        return (random_date)

    def get_random_location_tracking(x0, y0, miles, records, geojson):
        """
        generate a small CDR data set for mobile phone movement within an
        approximate specified radius of miles. this data simulates mobile
        phone location by connection to cell towers or GPS data. results
        can be plotted on a map.  locations can be constrained to be within
        a geographic boundary for a provided GeoJSON file. if a location
        is outside of the boundary we recalculate it

        """
        orig_x = x0
        orig_y = y0

        meters = int(miles) * 1610
        if (geojson):
            boundary_coords = geo.extract_geojson_coordinates(geojson)

        phone_to_track = get_random_phone_number()
        network = random.choice(data.operators)
        for i in range(int(records)):
            x0, y0 = geo.get_random_location(
                float(x0), float(y0), meters)
            if (geojson):
                while not geo.is_within_boundary(
                        float(x0), float(y0), boundary_coords):
                    x0, y0 = geo.get_random_location(
                        orig_x, orig_y, meters)

            random_date = get_random_date(
                datetime.now() - timedelta(30),
                datetime.now() +
                timedelta(days=30))

            print(
                '"M",' +
                '"' + str(phone_to_track) + '",' +
                '"' + str(get_random_phone_number()) + '",' +
                '"' + random_date.strftime("%d/%m/%Y") + '",' +
                '"' + random_date.strftime("%H:%M:%S") + '",' +
                '"' + str(random.randrange(1, 600)) + '",' +
                '"GBR",' +
                '"' + str(network) + '",' +
                '"' + str(random.randrange(1, 10)) + '",' +
                '"' + str(uuid.uuid4()) + '",' +
                '"' + str(i) + '",' +
                '"' + str(x0) + '",' +
                '"' + str(y0) + '"'
            )

    def get_random_cdr_data(records, x0, y0, geojson):
        """
        generate random CDR records. locations can be constrained to be within
        a geographic boundary for a provided GeoJSON file. if a location
        is outside of the boundary we recalculate it

        """

        orig_x = x0
        orig_y = y0
        if (geojson):
            boundary_coords = geo.extract_geojson_coordinates(geojson)

        for i in range(int(records)):
            x0, y0 = geo.get_random_location(
                float(x0), float(y0), 8000)
            if (geojson):
                while not geo.is_within_boundary(
                        float(x0), float(y0), boundary_coords):
                    x0, y0 = geo.get_random_location(
                        orig_x, orig_y, 8000)

            random_date = get_random_date(
                datetime.now() - timedelta(30),
                datetime.now() +
                timedelta(days=30))
            print(
                '"M",' +
                '"' + str(get_random_phone_number()) + '",' +
                '"' + str(get_random_phone_number()) + '",' +
                '"' + random_date.strftime("%d/%m/%Y") + '",' +
                '"' + random_date.strftime("%H:%M:%S") + '",' +
                '"' + str(random.randrange(1, 600)) + '",' +
                '"GBR",' +
                '"' + str(random.choice(data.operators)) + '",' +
                '"' + str(random.randrange(1, 10)) + '",' +
                '"' + str(uuid.uuid4()) + '",' +
                '"' + str(i) + '",' +
                '"' + str(x0) + '",' +
                '"' + str(y0) + '"'
            )

    def print_header():
        print(
            '"Call Type",' +
            '"Customer Identifier",' +
            '"Telephone Number Dialed",' +
            '"Call Date",' +
            '"Call Time",' +
            '"Duration",' +
            '"Country of Origin",' +
            '"Network",' +
            '"Ring Time",' +
            '"RecordID",' +
            '"Cell ID",' +
            '"Cell Lat",' +
            '"Cell Long"')

    if (args.c):
        x0, y0, *remaining = str(args.c).split(',')

        ''' ensure the specified coordinate are within the specified boundary '''
        if (args.b):
            boundary_coords = geo.extract_geojson_coordinates(args.b)
            print(str(x0) + ',' + str(y0))
            if not geo.is_within_boundary(
                    float(x0),
                    float(y0),
                    boundary_coords):
                print(
                    'Specified coordinate must be within boundary of ' + str(args.b))
                sys.exit(-1)
    else:
        x0, y0 = geo.get_random_location(
            data.places['London']['lat'],
            data.places['London']['lng'],
            8000)

    try:
        print_header()
        if (args.t):
            get_random_location_tracking(
                x0, y0, args.m, args.t, args.b)

        get_random_cdr_data(args.n, x0, y0, args.b)
    except (ValueError):
        raise SystemExit(
            'Incorrect usage. Check command line options.')


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-n',
        required=True,
        metavar='INT',
        help='number of records to create')
    parser.add_argument(
        '-t',
        metavar='INT',
        help='number of tracking records to create')
    parser.add_argument(
        '-m',
        metavar='INT',
        help='number of miles for radius')
    parser.add_argument(
        '-c',
        required=False,
        metavar='FLOAT',
        help='custom coordinated specified as latitude,longitude')
    parser.add_argument(
        '-b',
        required=False,
        metavar='STR',
        help='GeoJSON boundary/polygon for coordinate')
    args = parser.parse_args()

    main()
