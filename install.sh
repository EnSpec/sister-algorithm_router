#!/bin/bash

basedir=$( cd "$(dirname "$0")" ; pwd -P )
pushd $basedir
git clone --single-branch --branch sister-dev https://gitlab.com/geospec/maap-py.git
pushd maap-py
pip install -e .
