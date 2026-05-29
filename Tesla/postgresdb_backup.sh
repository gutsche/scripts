#!/usr/bin/env bash
date=`date +%y%m%d_%H%M%S`
composedir='/etc/docker-compose/teslamate'
backupfilenamestart='teslamate_db_backup'
backupfilename="${backupfilenamestart}_$date.bck"
backupdir="/home/gutsche/backup"
rm -f /tmp/${backupfilename}
cd $composedir
/usr/bin/docker-compose exec -T database pg_dump -U teslamate teslamate > ${backupdir}/${backupfilename}
gzip -9 ${backupdir}/${backupfilename}
cd $HOME

# only keep latest 4 files
find $backupdir -maxdepth 1 -type f -name "${backupfilenamestart}*" | sort -r | awk 'NR>4' | xargs --no-run-if-empty rm
