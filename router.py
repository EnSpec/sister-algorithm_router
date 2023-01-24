import json
import os
import sys
from osgeo import gdal


def main():

    run_config_json = sys.argv[1]

    with open(run_config_json, 'r') as in_file:
        run_config =json.load(in_file)

    fc_base_name = os.path.basename(run_config['inputs']['frcover_granule'])
    fc_file = f'input/{fc_base_name}/{fc_base_name}.tif'

    # Open fractional cover image
    fc_obj = gdal.Open(fc_file).ReadAsArray()

    algorithms = {'soil':0,
                  'veg':1,
                  'water':2,
                  'snow':3,}

    for alg_type in ['veg','snow']:
        if (alg_type == 'snow') and ("DESIS" in fc_base_name):
            continue

        cover_mask = fc_obj[algorithms[alg_type]] >= run_config['inputs'][f'{alg_type}_cover']

        if cover_mask.sum() >= run_config['inputs']['min_pixels']:
            print(alg_type)


if __name__== "__main__":
    main()
