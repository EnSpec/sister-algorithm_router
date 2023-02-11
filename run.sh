#!/bin/bash

source ~/.bashrc
basedir=$( cd "$(dirname "$0")" ; pwd -P )
python ${basedir}/router.py --inputs_json inputs.json
