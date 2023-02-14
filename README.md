# SISTER Algorithm Router PGE Documentation

## Description
The algorithm router PGE initializes L2B algorithm PGEs based on fractional cover and pixel count thresholds. The router currently supports initializing two algorithms:

1. Vegetation biochemistry: [sister-trait_estimate](https://github.com/EnSpec/sister-trait_estimate)
2. Snow grain size: [sister-grainsize](https://github.com/EnSpec/sister-grainsize)

The algorithm reads metadata from the input fractional cover dataset to determine the number of pixels exceeding the input cover thresholds, if the number of pixels is greater than or equal the user-specified minimum number of pixels the corresponding algorithm will be submitted for execution.

## PGE Arguments

In addition to required MAAP job submission arguments the algorithm router PGE also takes the following argument(s):|Argument| Type |  Description | Default||---|---|---|---|| frcov_dataset| file |L1B observation dataset | -|| reflectance_dataset| config |L2A reflectance dataset| -|
| snow_cover| config | Snow cover threshold| 0.5|| veg_cover| config |Vegetation cover threshold| 0.5|| soil_cover| config |Soil cover threshold| 0.5|| water_cover| config |Water cover threshold| 0.5|| min_pixels| config |Minimum number of pixels to execute algorithm| 100|| crid| config | Composite release identifier| '000'|
| routed\_pge\_queue| config |Queue to run the routed PGE in| sister-job_worker-16gb|| routed\_pge\_identifier| config | ID tag for the routed PGE| sister-routed-pge|| maap\_api\_host| config |API Host name| smap-api-int.imgspec.org|
## Outputs
The algorithm router PGE does not produce any outputs.

## Algorithm registration

This algorithm can be registered using the algorithm_config.yml file found in this repository:

	from maap.maap import MAAP
	import IPython
	
	maap = MAAP(maap_host="sister-api.imgspec.org")

	router_alg_yaml = './sister-algorithm_router/algorithm_config.yaml'
	maap.register_algorithm_from_yaml_file(file_path= router_alg_yaml)


## Example	router_job_response = maap.submitJob(	    algo_id="sister-algorithm-router",	    version="1.0.0",	    frcov_dataset ='SISTER_AVNG_L2B_FRCOVER_20220502T180901_001_OBS',	    reflectance_dataset ='SISTER_AVNG_L2A_CORFL_20220502T180901_001',
	    crid = '000',
	    snow_cover = 0.9,	    queue="sister-job_worker-8gb",	    identifier='SISTER_AVNG_L2B_ROUTER_20220502T180901_001')