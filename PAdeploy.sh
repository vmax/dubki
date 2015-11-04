#!/bin/bash

# make temp directory
mkdir .pa_temp/
# copy all files
rsync -R *.sh *.py .train_api_key templates/* static/* .pa_temp/
# change directory
cd .pa_temp
# create needed directories
mkdir logs cache
# version
LAST_COMMIT_HASH="$(git rev-parse HEAD)"
# patch the files
sed -i '' "s|VERSION_PLACEHOLDER|${LAST_COMMIT_HASH}|" app.py
sed -i '' 's|#PYTHONANYWHERE|cd\ /home/dubki/app/|' update-schedules.sh
sed -i '' 's|#PYTHONANYWHERE|chdir("/home/dubki/app/")|' app.py

# archive files
tar -cjf ../dubki-${LAST_COMMIT_HASH}.tbz2 .
# change directory back
cd ..
# delete temp files
rm -rf .pa_temp
