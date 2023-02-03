import argparse
import json
import os
import sys

def main():

    agrparse = list()
    desc = "SISTER Algorithm router"

    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('--files', nargs='+',
                        help='Input files')

    parser.add_argument('--metadata', nargs='+',
                        help='Input metadata')

    parser.add_argument('--soil_cover', type=float, default = 0.5,
                        help='Soil cover minimum',)

    parser.add_argument('--veg_cover', type=float,  default = 0.5,
                        help='Vegetation cover minimum',)

    parser.add_argument('--water_cover', type=float,  default = 0.5,
                        help='Water cover minimum',)

    parser.add_argument('--snow_cover', type=float,  default = 0.5,
                        help='Snow cover minimum')

    parser.add_argument('--min_pixels', type=float, default = 100,
                        help='Soil cover minimum')

    args = parser.parse_args()

    for meta_file_path in args.metadata:
        if "FRCOV" in meta_file_path:
            break

    with open(meta_file_path, 'r') as meta_file:
        metadata =json.load(meta_file)

    snow_run = metadata['cover_percentile_counts']['soil'][str(args.snow_cover)] >= args.min_pixels

    veg_run = metadata['cover_percentile_counts']['vegetation'][str(args.veg_cover)] >= args.min_pixels


    # # Vegetation biochemistry PGE
    if veg_run:

        vegbiochem_algo ={'algo_id':"sister-trait_estimate",
                    'l2a_rfl': '',
                    'l2a_frcover': '',
                    'veg_cover' : args.veg_cover,
                    'CRID': '000',
                    'publish_to_cmr':False,
                    'cmr_metadata':{},
                    'queue':"sister-job_worker-16gb",
                    'identifier':""}
        print(vegbiochem_algo)

    # # Snow grain size PGE
    if snow_run  & ("DESIS" not in meta_file_path):

        grainsize_algo = {'algo_id':"sister-grainsize",
                    'version':"sister-dev",
                    'l2a_rfl': '',
                    'l2a_frcover': '',
                    'snow_cover ': args.snow_cover,
                    'CRID': '000',
                    'publish_to_cmr':False,
                    'cmr_metadata':{},
                    'queue':"sister-job_worker-16gb",
                    'identifier':""}
        print(grainsize_algo)



if __name__== "__main__":
    main()
