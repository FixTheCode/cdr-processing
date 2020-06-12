import os
import json
import itertools as it


def main():
    # count the coordinates in the GeoJSON files in the current
    # directory

    for filename in os.listdir('.'):
        if filename.endswith('.geojson'):
            try:
                file = open(filename, 'r')
                data = json.load(file)
                name = [f['properties']['COUNTRY']
                        for f in data['features']][0]
                code = [f['properties']['CODE']
                        for f in data['features']][0]
                coords = 0
                for t in data['features']:
                    all_coords = list(
                        it.chain.from_iterable(
                            t['geometry']['coordinates']))
                    for c in all_coords:
                        coords += len(c)

                print(code + ' ' + name + ' ' +
                      str(coords) + ' coordinates in ' + filename)

            except (ValueError):
                print(filename + ' is not a valid JSON document.')
            except (KeyError):
                print(filename + ' invalid key.')


if __name__ == '__main__':
    main()
