#!/bin/bash

lockFile='/tmp/teslaPostProcessing.lock'
teslaPostLog='/tmp/teslaPostProcessing.log'
inputDir='/home/gutsche/TeslaCamInput'
outputDir='/Media/TeslaCamClips'
time=`date '+%Y-%m-%d %H:%M:%S'`

echo "'$time' tesla Postprocessing script started" | tee -a $teslaPostLog

# check if post processing script is already running
if [ -f $lockFile ]
then
    time=`date '+%Y-%m-%d %H:%M:%S'`
	echo "'$time' $lockFile exists, terminating process" | tee -a $teslaPostLog
	exit 0
else
    # Create lock file to prevent other post-processing from running simultaneously
    time=`date '+%Y-%m-%d %H:%M:%S'`
    echo "'$time' Creating lock file" | tee -a $teslaPostLog
    touch $lockFile

    # count subdirectories in $inputDir and only if ge 1 then proceed
    subdircount=`find $inputDir -mindepth 1 -type d | wc -l`
    if [ $subdircount -ge 1 ]
    then

        # post processing of all sub directories in inputDir
        time=`date '+%Y-%m-%d %H:%M:%S'`
        echo "'$time' Starting post processing of all Tesla Cam sub directories in $inputDir" | tee -a $teslaPostLog

        docker run --user 1000:1000 -v $inputDir:/input -v $outputDir:/output oguatworld/tesla_dashcam --output /output  --encoding x264 --speedup 2 --mirror --no-notification --delete_source /input | tee -a $teslaPostLog

        time=`date '+%Y-%m-%d %H:%M:%S'`
        echo "'$time' Finished post processing of all Tesla Cam sub directories in $inputDir" | tee -a $teslaPostLog

        time=`date '+%Y-%m-%d %H:%M:%S'`
        curl http://<FILLME>:32400/library/sections/<FILLME>/refresh?X-Plex-Token=<FILLME>
        echo "'$time' updated TeslaCamClips library in PLEX" | tee -a $teslaPostLog
    else
        time=`date '+%Y-%m-%d %H:%M:%S'`
        echo "'$time' no sub directories in $inputDir, nothing to process" | tee -a $teslaPostLog
    fi

    #Remove lock file
    time=`date '+%Y-%m-%d %H:%M:%S'`
    echo "'$time' All done! Removing lock" | tee -a $teslaPostLog
    rm $lockFile
fi
