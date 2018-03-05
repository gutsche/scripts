#! /bin/bash
#
# script that scans the tv shows directory for *.ts files from PLEX DVR
# runs handbrake and renames to *.m4v, then refreshes the TV Shows PLEX library

lockFile='/tmp/plexPostProcessing.lock'
updateFile='/tmp/plexPostProcessingUpdate.lock'
plexPostLog='/tmp/plexPostProcessing.log'
tvShowsDirectory="/Volumes/Media/TV Shows"
time=`date '+%Y-%m-%d %H:%M:%S'`
handbrake=/Volumes/Home/gutsche/.bin/HandBrakeCLI/HandBrakeCLI

echo "'$time' Plex DVR Postprocessing script started" | tee -a $plexPostLog

# check if post processing script is already running
if [ -f $lockFile ]
then
	echo "'$time' $lockFile exists, terminating process" | tee -a $plexPostLog
	exit 0
else
    # Create lock file to prevent other post-processing from running simultaneously
    echo "'$time' Creating lock file" | tee -a $plexPostLog
    touch $lockFile
	
	# loop over all *.ts files in tvShowsDirectory
	FilesFound=$(find  "$tvShowsDirectory" -type f -name "*.ts" -print)
	IFSbkp="$IFS"
	IFS=$'\n'
	for file in $FilesFound; do
		echo "'$time' Processing $file" | tee -a $plexPostLog
		outFile="${file%.ts}.m4v"
		$handbrake -i "$file" -o "$outFile" --preset="HQ 1080p30 Surround" -O | tee -a $plexPostLog
		# remove input file if handrake is successful and output file exists
		if [ $? -eq 0 ]; then
			if [ -f "$outFile" ]; then
				echo "'$time' removing input file $file" | tee -a $plexPostLog
				rm "$file"
			    echo "'$time' Creating PLEX library update lock file" | tee -a $plexPostLog
			    touch $updateFile
			fi
		fi
	done
	IFS="$IFSbkp"
	
	# update plex TV shows library if updateFile exists
	if [ -f $updateFile ]
	then
		echo "'$time' updating TV Shows library in PLEX" | tee -a $plexPostLog
		curl http://127.0.0.1:32400/library/sections/7/refresh?X-Plex-Token=<token>
	    echo "'$time' Removing PLEX library update lock file" | tee -a $plexPostLog
		rm $updateFile
	fi
	
    #Remove lock file
    echo "'$time' All done! Removing lock" | tee -a $plexPostLog
    rm $lockFile
fi


		
