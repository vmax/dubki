#!/usr/bin/env bash

# make temp directory
mkdir .pa_temp/
# copy all files
rsync -R *.py .train_api_key templates/* static/* .pa_temp/
# change directory
cd .pa_temp
# patch the files

sed -e 's/.train_api_key/\/home\/dubki\/app\/.train_api_key/' -i route_train.py
sed -e 's/.bus_schedule/\/home\/app\/dubki\/.bus_schedule/' -i route_bus.py 

# archive files
tar -cjf ../dubki.tbz2 .
# change directory back
cd ..
# delete temp files
rm -rf .pa_temp