import json
import os
import sys
from osgeo import gdal
import maap

def main():

    run_config_json = sys.argv[1]

    with open(run_config_json, 'r') as in_file:
        run_config =json.load(in_file)

    fc_base_name = os.path.basename(run_config['inputs']['l2a_frcover'])
    fc_file = f'input/{fc_base_name}/{fc_base_name}.tif'

    # Open fractional cover image
    fc_obj = gdal.Open(fc_file).ReadAsArray()

    snow_mask = fc_obj[3] >= run_config['inputs']['snow_cover']
    veg_mask = fc_obj[1] >= run_config['inputs']['veg_cover']


    # Vegetation biochemistry PGE
    if (veg_mask.sum() >= run_config['inputs']['min_pixels']):

        veg_traits = maap.submitJob(
            algo_id="sister-trait_estimate",
            version="sister-dev",
            l2a_rfl= run_config['inputs']['l2a_rfl'],
            l2a_frcover= run_config['inputs']['l2a_frcover'],
            veg_cover = run_config['inputs']['veg_cover'],
            CRID= run_config['inputs']['CRID'],
            publish_to_cmr=False,
            cmr_metadata={},
            queue="sister-job_worker-16gb",
            identifier="")


    # Snow grain size PGE
    if (snow_mask.sum() >= run_config['inputs']['min_pixels']) & ("DESIS" in fc_base_name):

        grainsize = maap.submitJob(
            algo_id="sister-grainsize",
            version="sister-dev",
            l2a_rfl= run_config['inputs']['l2a_rfl'],
            l2a_frcover= run_config['inputs']['l2a_frcover'],
            snow_cover = run_config['inputs']['snow_cover'],
            CRID= run_config['inputs']['CRID'],
            publish_to_cmr=False,
            cmr_metadata={},
            queue="sister-job_worker-16gb",
            identifier="")



if __name__== "__main__":
    main()
