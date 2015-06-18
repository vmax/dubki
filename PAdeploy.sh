#!/usr/bin/env bash

# make temp directory
mkdir .pa_temp/
# copy all files
rsync -R *.py .train_api_key templates/* static/* .pa_temp/
# change directory
cd .pa_temp
# patch the files

sed -ie 's/.train_api_key/\/home\/dubki\/app\/.train_api_key/' route_train.py
sed -ie 's/.bus_schedule/\/home\/app\/dubki\/.bus_schedule/' route_bus.py 

# archive files
tar -cjf ../dubki.tbz2 .
# change directory back
cd ..
# delete temp files
rm -rf .pa_temp