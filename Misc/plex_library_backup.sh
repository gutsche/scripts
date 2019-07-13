#!/usr/bin/env bash
date=`date +%y%m%d_%H%M%S`
plexdir='/home/plexmediaserver'
plexbackupfilenamestart='plex_library_backup'
backupfilename="${plexbackupfilenamestart}_$date.tgz"
backupdir="/Media/Backups"
backupfile="$backupdir/$backupfilename"
tar czf $backupfile $plexdir

# only keep latest 4 files
find $backupdir -maxdepth 1 -type f -name "${plexbackupfilenamestart}*" | sort -r | awk 'NR>4' | xargs --no-run-if-empty rm
