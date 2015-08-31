#!/bin/bash

# make temp directory
mkdir .pa_temp/
# copy all files
rsync -R *.sh *.py .train_api_key templates/* static/* .pa_temp/
# change directory
cd .pa_temp
# patch the files
sed -e 's/\.train_api_key/\/home\/dubki\/app\/\.train_api_key/' route_train.py | tee route_train_PA.py
sed -e 's/\.bus_schedule/\/home\/dubki\/app\/\.bus_schedule/' route_bus.py  | tee route_bus_PA.py
mv route_train_PA.py route_train.py
mv route_bus_PA.py route_bus.py


LAST_COMMIT_HASH="$(git rev-parse HEAD)"

# archive files
tar -cjf ../dubki-${LAST_COMMIT_HASH}.tbz2 .
# change directory back
cd ..
# delete temp files
rm -rf .pa_temp
