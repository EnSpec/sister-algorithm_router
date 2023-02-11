#!/bin/bash

git clone --single-branch --branch sister-dev https://gitlab.com/geospec/maap-py.git
pushd maap-py
pip install -e .
echo MAAP_CONF=${PWD} >> ~/.bashrc
popd
