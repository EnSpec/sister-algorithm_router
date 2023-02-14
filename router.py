import argparse
import json
import os
import sys
import logging


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)
if LOGGER.hasHandlers():
    LOGGER.handlers.clear()


def evaluate(metadata: list, snow_cover, veg_cover, min_pixels, soil_cover, water_cover, **kwargs):
    LOGGER.info("Evaluating router config")
    algorithms = []
    for meta_file_path in metadata:
        if "FRCOV" not in meta_file_path:
            LOGGER.warning(f"FRCOV not in {meta_file_path} doing nothing")
            continue

        LOGGER.info(f"Processing {meta_file_path}")
        with open(meta_file_path, 'r') as meta_file:
            metadata = json.load(meta_file)

        snow_run = metadata['cover_percentile_counts']['soil'][str(snow_cover)] >= min_pixels
        veg_run = metadata['cover_percentile_counts']['vegetation'][str(veg_cover)] >= min_pixels
        identifier = kwargs.get("routed_pge_identifier")
        kwargs.pop("routed_pge_identifier")
        queue = kwargs.get("routed_pge_queue")
        kwargs.pop("routed_pge_queue")

        # # Vegetation biochemistry PGE
        if veg_run:
            vegbiochem_algo = {'algo_id': "sister-trait_estimate",
                               'version': "1.0.0",
                               "identifier": f"{identifier.replace('ROUTER', 'VEGBIOCHEM')}",
                               "queue": queue,
                               **kwargs
                               }

            LOGGER.info("Appending config for vegbiochem_algo")
            algorithms.append(vegbiochem_algo)
            LOGGER.debug(f"{json.dumps(vegbiochem_algo)}")

        # # Snow grain size PGE
        if snow_run & ("DESIS" not in meta_file_path):
            grainsize_algo = {'algo_id': "sister-grainsize",
                              'version': "1.0.0",
                              "identifier": f"{identifier.replace('ROUTER', 'GRAINSIZE')}",
                              "queue": queue,
                              'snow_cover ': snow_cover,
                              **kwargs
                              }
            LOGGER.info("Appending config for grainsize_algo")
            algorithms.append(grainsize_algo)
            LOGGER.debug(f"{json.dumps(grainsize_algo)}")

    return algorithms


def get_input_metadata(filename):
    metadata_file = os.path.join('input', filename, f"{filename}.met.json")
    if os.path.exists(metadata_file):
        return metadata_file


def route_pge_with_inputs_json(inputs_json):
    config = inputs_json.get("config")
    files = inputs_json.get("file")
    input_metadata_filepaths = []
    input_files = {}
    for file_obj in files:
        for key, filepath in file_obj.items():
            input_metadata_filepaths.append(get_input_metadata(os.path.basename(filepath)))
            input_files.update({key: filepath})
    algorithms = evaluate(metadata=input_metadata_filepaths, **config, **input_files)
    return algorithms, config.get("maap_api_host")


def run_pges(pges_to_run, maap_host):
    LOGGER.info(f"Processing {len(pges_to_run)} PGEs to run")
    from maap.maap import MAAP
    maap = MAAP(maap_host=maap_host)
    for pge_config in pges_to_run:
        LOGGER.info(f"Submitting PGE with config {json.dumps(pge_config)}")
        job = maap.submitJob(dedup=True, **pge_config)
        LOGGER.info(f"Submitted job result {job}")


def main():

    agrparse = list()
    desc = "SISTER Algorithm router"

    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('--inputs_json',
                        help='Inputs.json file for running in dps',
                        required=False)
    parser.add_argument('--files', nargs='+',
                        help='Input files',
                        required='--inputs_json' not in sys.argv)
    parser.add_argument('--metadata', nargs='+',
                        help='Input metadata',
                        required='--inputs_json' not in sys.argv)
    parser.add_argument('--soil_cover', type=float, default = 0.5,
                        help='Soil cover minimum',
                        required='--inputs_json' not in sys.argv)
    parser.add_argument('--veg_cover', type=float,  default = 0.5,
                        help='Vegetation cover minimum',
                        required='--inputs_json' not in sys.argv)
    parser.add_argument('--water_cover', type=float,  default = 0.5,
                        help='Water cover minimum',
                        required='--inputs_json' not in sys.argv)
    parser.add_argument('--snow_cover', type=float,  default = 0.5,
                        help='Snow cover minimum',
                        required='--inputs_json' not in sys.argv)
    parser.add_argument('--min_pixels', type=float, default = 100,
                        help='Soil cover minimum',
                        required='--inputs_json' not in sys.argv)
    parser.add_argument('--crid', type=str, default='000',
                        help='Composite Release ID',
                        required='--inputs_json' not in sys.argv)
    parser.add_argument('--maap_api_host', type=str, default='sister-api.imgspec.org',
                        help='MAAP API HOSTNAME',
                        required='--inputs_json' not in sys.argv)

    args = parser.parse_args()
    if args.inputs_json:
        with open(args.inputs_json, 'r') as fr:
            LOGGER.info("Using inputs.json")
            inputs_config = json.load(fr)
            pge_to_run, maap_host = route_pge_with_inputs_json(inputs_config)
            run_pges(pge_to_run, maap_host=maap_host)
    else:
        pge_to_run = evaluate(metadata=args.metadata, snow_cover=args.snow_cover, veg_cover=args.veg_cover,
                              soil_cover=args.snow_cover, water_cover=args.water_cover,
                              min_pixels=args.min_pixels, crid=args.crid)
        run_pges(pge_to_run, maap_host=args.maap_api_host)


if __name__ == "__main__":
    main()
