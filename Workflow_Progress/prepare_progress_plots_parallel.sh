# initialization
source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=slc6_amd64_gcc481

echo "CERN working environment"
cd /afs/cern.ch/user/c/cmst2/Software/CMSSW_7_3_X_2014-10-31-1000/src
eval `scram runtime -sh`
cd
echo "CERN CRAB configuration"
source /cvmfs/cms.cern.ch/crab/crab.sh

# queries
cd /afs/cern.ch/user/c/cmst2/progress_plots
python EventsPerDay.py -d '/*/Fall13-*/GEN-SIM' -s 2013-09-06 &
python EventsPerDay.py -d '/*/Spring14*/AODSIM' -s 2014-04-30 &
python EventsPerDay.py -d '/*/Spring14*S14_POSTLS170*/AODSIM' -s 2014-03-30 &
python EventsPerDay.py -d '/*/Spring14*PU20bx25_POSTLS170*/AODSIM' -s 2014-03-30 &
python EventsPerDay.py -d '/*/Spring14*PU40bx25_POSTLS170*/AODSIM' -s 2014-07-17
python EventsPerDay.py -d '/*/Spring14*/MINIAODSIM' -s 2014-06-20 &
python EventsPerDay.py -m -d '/*/*/USER' -u https://cmsweb.cern.ch/dbs/prod/phys03/DBSReader -s 2014-06-20 &

python EventsPerDay.py -d '/*/*Upg14*/AODSIM' -s 2014-04-27 &
python EventsPerDay.py -d '/*/*Upg14*PU50bx25*/AODSIM' -s 2014-04-27
python EventsPerDay.py -d '/*/*Upg14*PU140bx25*/AODSIM' -s 2014-04-27
python EventsPerDay.py -d '/*/*Upg14*/GEN-SIM-RECO' -s 2014-04-30 &
python EventsPerDay.py -d '/*/*Upg14*/GEN-SIM' -s 2014-04-20 &

python EventsPerDay.py -d '/*/Summer11*/AODSIM' -s 2013-07-04 &
python EventsPerDay.py -d '/*/Summer11*/GEN-SIM' -s 2013-02-24 & 

python EventsPerDay.py -d '/*/*/GEN-SIM' -s 2014-04-05 &
python EventsPerDay.py -d '/*/*/AODSIM' -s 2014-04-05 &

python EventsPerDay.py -d '/*/Summer12*/AODSIM' -s 2012-12-04
python EventsPerDay.py -d '/*/Summer12*/GEN-SIM' -s 2012-12-06

python addJSONFiles.py -n User-MINIAOD -d STAR_STAR_USER.json,STAR_Spring14STAR_MINIAODSIM.json

python DrawStackedPlot.py -d STAR_Fall13-STAR_GEN-SIM.json
python DrawStackedPlot.py -d STAR_STARUpg14STAR_AODSIM.json
python DrawStackedPlot.py -d STAR_STARUpg14STARPU50bx25STAR_AODSIM.json
python DrawStackedPlot.py -d STAR_STARUpg14STARPU140bx25STAR_AODSIM.json
python DrawStackedPlot.py -d STAR_STARUpg14STAR_GEN-SIM-RECO.json
python DrawStackedPlot.py -d STAR_STARUpg14STAR_GEN-SIM.json
python DrawStackedPlot.py -d STAR_STAR_AODSIM.json
python DrawStackedPlot.py -d STAR_STAR_GEN-SIM.json
python DrawStackedPlot.py -d STAR_Spring14STAR_MINIAODSIM.json
python DrawStackedPlot.py -d STAR_STAR_USER.json
python DrawStackedPlot.py -d STAR_Spring14STARPU20bx25_POSTLS170STAR_AODSIM.json
python DrawStackedPlot.py -d STAR_Spring14STARS14_POSTLS170STAR_AODSIM.json
python DrawStackedPlot.py -d STAR_Spring14STARPU40bx25_POSTLS170STAR_AODSIM.json
python DrawStackedPlot.py -d STAR_Spring14STAR_AODSIM.json
python DrawStackedPlot.py -d STAR_Summer11STAR_AODSIM.json
python DrawStackedPlot.py -d STAR_Summer11STAR_GEN-SIM.json
python DrawStackedPlot.py -d STAR_Summer12STAR_AODSIM.json
python DrawStackedPlot.py -d STAR_Summer12STAR_GEN-SIM.json

python DrawOverviewStackedPlots.py -a STAR_STAR_GEN-SIM.json -d STAR_Fall13-STAR_GEN-SIM.json,STAR_STARUpg14STAR_GEN-SIM.json,STAR_Summer12STAR_GEN-SIM.json,STAR_Summer11STAR_GEN-SIM.json
python DrawOverviewStackedPlots.py -a STAR_STAR_GEN-SIM.json -d STAR_Fall13-STAR_GEN-SIM.json,STAR_STARUpg14STAR_GEN-SIM.json,STAR_Summer12STAR_GEN-SIM.json,STAR_Summer11STAR_GEN-SIM.json -s valid

python DrawOverviewStackedPlots.py -a STAR_STAR_AODSIM.json -d STAR_Spring14STAR_AODSIM.json,STAR_STARUpg14STAR_AODSIM.json,STAR_Summer12STAR_AODSIM.json,STAR_Summer11STAR_AODSIM.json
python DrawOverviewStackedPlots.py -a STAR_STAR_AODSIM.json -d STAR_Spring14STAR_AODSIM.json,STAR_STARUpg14STAR_AODSIM.json,STAR_Summer12STAR_AODSIM.json,STAR_Summer11STAR_AODSIM.json -s valid

python DrawOverviewStackedPlots.py -a STAR_Spring14STAR_AODSIM.json -d STAR_Spring14STARPU40bx25_POSTLS170STAR_AODSIM.json,STAR_Spring14STARPU20bx25_POSTLS170STAR_AODSIM.json,STAR_Spring14STARS14_POSTLS170STAR_AODSIM.json

python DrawOverviewStackedPlots.py -a STAR_STARUpg14STAR_AODSIM.json -d STAR_STARUpg14STARPU50bx25STAR_AODSIM.json,STAR_STARUpg14STARPU140bx25STAR_AODSIM.json

python DrawOverviewStackedPlots.py -n -a User-MINIAOD.json -d STAR_STAR_USER.json,STAR_Spring14STAR_MINIAODSIM.json

curl "http://dashb-cms-prod.cern.ch/dashboard/request.py/condorjobnumbers_individual?sites=All%20T3210&sitesSort=7&jobTypes=&start=&end=&timeRange=lastWeek&granularity=Hourly&sortBy=3&series=All&type=r" > running.png
curl "http://dashb-cms-prod.cern.ch/dashboard/request.py/condorjobnumbers_individual?sites=All%20T3210&sitesSort=7&jobTypes=&start=&end=&timeRange=lastWeek&granularity=Hourly&sortBy=3&series=All&type=p" > pending.png

# copy to www
cp -f *.png *.txt *.gif *.pdf *.csv *.json /afs/cern.ch/user/c/cmst2/www/progress_plots/
