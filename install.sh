# Need to do custom install to prevent dependency errors
conda create -y --name sister python=3.8
source activate sister

conda install gdal -y

git clone https://gitlab.com/geospec/maap-py.git
cd maap-py
pip install .
