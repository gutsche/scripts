#!/usr/bin/env bash

backupdir='/mnt/Homelab-PM-Storage-gutsche/shortterm_backups/Homelab-PM-Teslamate'
teslamatedest="${backupdir}/Teslamate"
teslamatesource='/home/gutsche/backup'
now=$(date)

### Check if a directory does not exist ###
if [ ! -d ${backupdir} ] 
then
    echo "${now}: Directory ${backupdir} cannot be mounted. Server down?" 
    exit 9999 # die with error code 9999
fi

echo "${now} making backup of teslamate"

# copy all teslamate backups 
cp -au ${teslamatesource}/* ${teslamatedest}

# only keep latest 4 files
find ${teslamatedest} -maxdepth 1 -type f -name "*" | sort -r | awk 'NR>4' | xargs --no-run-if-empty rm
