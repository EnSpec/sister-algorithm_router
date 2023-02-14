#!/bin/bash


basedir=$( cd "$(dirname "$0")" ; pwd -P )
export MAAP_CONF=${basedir}/maap-py
python ${basedir}/router.py --inputs_json inputs.json
