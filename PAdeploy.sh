#!/bin/bash

# make temp directory
mkdir .pa_temp/
# copy all files
rsync -R *.sh *.py .train_api_key templates/* static/* .pa_temp/
# change directory
cd .pa_temp
# patch the files
sed -i '' 's|\.bus_schedule|/home/dubki/app/\.bus_schedule|' route_bus.py
sed -i '' 's|\.train_api_key|/home/dubki/app/\.train_api_key|' route_train.py
sed -i '' 's|feedback.txt|/home/dubki/app/feedback.txt|' app.py

LAST_COMMIT_HASH="$(git rev-parse HEAD)"

# archive files
tar -cjf ../dubki-${LAST_COMMIT_HASH}.tbz2 .
# change directory back
cd ..
# delete temp files
rm -rf .pa_temp
