#!/bin/bash

source activate sister

pge_dir=$(cd "$(dirname "$0")" ; pwd -P)

echo "Creating runconfig"
python ${pge_dir}/generate_runconfig.py inputs.json

echo "Running Algorithm router"
python ${pge_dir}/router.py runconfig.json
