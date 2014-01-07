# dbs search --noheader --production --query="find block,block.size,block.numevents,block.createdate where tier = GEN and block.createdate >= 2013-01-01 and block.createdate < 2013-02-01" > mc_2013_jan_gen.blocks
# dbs search --noheader --production --query="find block,block.size,block.numevents,block.createdate where tier = GEN-RAW* and block.createdate >= 2013-01-01 and block.createdate < 2013-02-01" > mc_2013_jan_raw.blocks
# dbs search --noheader --production --query="find block,block.size,block.numevents,block.createdate where tier = GEN-SIM* and block.createdate >= 2013-01-01 and block.createdate < 2013-02-01" | grep -v RECO > mc_2013_jan_sim.blocks
# dbs search --noheader --production --query="find block,block.size,block.numevents,block.createdate where tier = GEN-SIM* and block.createdate >= 2013-01-01 and block.createdate < 2013-02-01" | grep RECO > mc_2013_jan_reco.blocks
# dbs search --noheader --production --query="find block,block.size,block.numevents,block.createdate where tier = AODSIM and block.createdate >= 2013-01-01 and block.createdate < 2013-02-01" > mc_2013_jan_aod.blocks

# dbs search --noheader --production --query="find block,block.size,block.numevents,block.createdate where tier = GEN and block.createdate >= 2013-02-01 and block.createdate < 2013-03-01" > mc_2013_feb_gen.blocks
# dbs search --noheader --production --query="find block,block.size,block.numevents,block.createdate where tier = GEN-RAW* and block.createdate >= 2013-02-01 and block.createdate < 2013-03-01" > mc_2013_feb_raw.blocks
# dbs search --noheader --production --query="find block,block.size,block.numevents,block.createdate where tier = GEN-SIM* and block.createdate >= 2013-02-01 and block.createdate < 2013-03-01" | grep -v RECO > mc_2013_feb_sim.blocks
# dbs search --noheader --production --query="find block,block.size,block.numevents,block.createdate where tier = GEN-SIM* and block.createdate >= 2013-02-01 and block.createdate < 2013-03-01" | grep RECO > mc_2013_feb_reco.blocks
# dbs search --noheader --production --query="find block,block.size,block.numevents,block.createdate where tier = AODSIM and block.createdate >= 2013-02-01 and block.createdate < 2013-03-01" > mc_2013_feb_aod.blocks
 
# dbs search --noheader --production --query="find block,block.size,block.numevents,block.createdate where tier = GEN and block.createdate >= 2013-03-01 and block.createdate < 2013-04-01" > mc_2013_mar_gen.blocks
# dbs search --noheader --production --query="find block,block.size,block.numevents,block.createdate where tier = GEN-RAW* and block.createdate >= 2013-03-01 and block.createdate < 2013-04-01" > mc_2013_mar_raw.blocks
# dbs search --noheader --production --query="find block,block.size,block.numevents,block.createdate where tier = GEN-SIM* and block.createdate >= 2013-03-01 and block.createdate < 2013-04-01" | grep -v RECO > mc_2013_mar_sim.blocks
# dbs search --noheader --production --query="find block,block.size,block.numevents,block.createdate where tier = GEN-SIM* and block.createdate >= 2013-03-01 and block.createdate < 2013-04-01" | grep RECO > mc_2013_mar_reco.blocks
# dbs search --noheader --production --query="find block,block.size,block.numevents,block.createdate where tier = AODSIM and block.createdate >= 2013-03-01 and block.createdate < 2013-04-01" > mc_2013_mar_aod.blocks

# dbs search --noheader --production --query="find block,block.size,block.numevents,block.createdate where tier = GEN and block.createdate >= 2013-04-01 and block.createdate < 2013-05-01" > mc_2013_apr_gen.blocks
# dbs search --noheader --production --query="find block,block.size,block.numevents,block.createdate where tier = GEN-RAW* and block.createdate >= 2013-04-01 and block.createdate < 2013-05-01" > mc_2013_apr_raw.blocks
# dbs search --noheader --production --query="find block,block.size,block.numevents,block.createdate where tier = GEN-SIM* and block.createdate >= 2013-04-01 and block.createdate < 2013-05-01" | grep -v RECO > mc_2013_apr_sim.blocks
# dbs search --noheader --production --query="find block,block.size,block.numevents,block.createdate where tier = GEN-SIM* and block.createdate >= 2013-04-01 and block.createdate < 2013-05-01" | grep RECO > mc_2013_apr_reco.blocks
# dbs search --noheader --production --query="find block,block.size,block.numevents,block.createdate where tier = AODSIM and block.createdate >= 2013-04-01 and block.createdate < 2013-05-01" > mc_2013_apr_aod.blocks

# dbs search --noheader --production --query="find block,block.size,block.numevents,block.createdate where tier = GEN and block.createdate >= 2013-05-01 and block.createdate < 2013-06-01" > mc_2013_may_gen.blocks
# dbs search --noheader --production --query="find block,block.size,block.numevents,block.createdate where tier = GEN-RAW* and block.createdate >= 2013-05-01 and block.createdate < 2013-06-01" > mc_2013_may_raw.blocks
# dbs search --noheader --production --query="find block,block.size,block.numevents,block.createdate where tier = GEN-SIM* and block.createdate >= 2013-05-01 and block.createdate < 2013-06-01" | grep -v RECO > mc_2013_may_sim.blocks
# dbs search --noheader --production --query="find block,block.size,block.numevents,block.createdate where tier = GEN-SIM* and block.createdate >= 2013-05-01 and block.createdate < 2013-06-01" | grep RECO > mc_2013_may_reco.blocks
# dbs search --noheader --production --query="find block,block.size,block.numevents,block.createdate where tier = AODSIM and block.createdate >= 2013-05-01 and block.createdate < 2013-06-01" > mc_2013_may_aod.blocks
#
# dbs search --noheader --production --query="find block,block.size,block.numevents,block.createdate where tier = GEN and block.createdate >= 2013-06-01 and block.createdate < 2013-07-01" > mc_2013_jun_gen.blocks
# dbs search --noheader --production --query="find block,block.size,block.numevents,block.createdate where tier = GEN-RAW* and block.createdate >= 2013-06-01 and block.createdate < 2013-07-01" > mc_2013_jun_raw.blocks
# dbs search --noheader --production --query="find block,block.size,block.numevents,block.createdate where tier = GEN-SIM* and block.createdate >= 2013-06-01 and block.createdate < 2013-07-01" | grep -v RECO > mc_2013_jun_sim.blocks
# dbs search --noheader --production --query="find block,block.size,block.numevents,block.createdate where tier = GEN-SIM* and block.createdate >= 2013-06-01 and block.createdate < 2013-07-01" | grep RECO > mc_2013_jun_reco.blocks
# dbs search --noheader --production --query="find block,block.size,block.numevents,block.createdate where tier = AODSIM and block.createdate >= 2013-06-01 and block.createdate < 2013-07-01" > mc_2013_jun_aod.blocks
# 
# dbs search --noheader --production --query="find block,block.size,block.numevents,block.createdate where tier = GEN and block.createdate >= 2013-07-01 and block.createdate < 2013-08-01" > mc_2013_jul_gen.blocks
# dbs search --noheader --production --query="find block,block.size,block.numevents,block.createdate where tier = GEN-RAW* and block.createdate >= 2013-07-01 and block.createdate < 2013-08-01" > mc_2013_jul_raw.blocks
# dbs search --noheader --production --query="find block,block.size,block.numevents,block.createdate where tier = GEN-SIM* and block.createdate >= 2013-07-01 and block.createdate < 2013-08-01" | grep -v RECO > mc_2013_jul_sim.blocks
# dbs search --noheader --production --query="find block,block.size,block.numevents,block.createdate where tier = GEN-SIM* and block.createdate >= 2013-07-01 and block.createdate < 2013-08-01" | grep RECO > mc_2013_jul_reco.blocks
# dbs search --noheader --production --query="find block,block.size,block.numevents,block.createdate where tier = AODSIM and block.createdate >= 2013-07-01 and block.createdate < 2013-08-01" > mc_2013_jul_aod.blocks
# 
# dbs search --noheader --production --query="find block,block.size,block.numevents,block.createdate where tier = GEN and block.createdate >= 2013-08-01 and block.createdate < 2013-09-01" > mc_2013_aug_gen.blocks
# dbs search --noheader --production --query="find block,block.size,block.numevents,block.createdate where tier = GEN-RAW* and block.createdate >= 2013-08-01 and block.createdate < 2013-09-01" > mc_2013_aug_raw.blocks
# dbs search --noheader --production --query="find block,block.size,block.numevents,block.createdate where tier = GEN-SIM* and block.createdate >= 2013-08-01 and block.createdate < 2013-09-01" | grep -v RECO > mc_2013_aug_sim.blocks
# dbs search --noheader --production --query="find block,block.size,block.numevents,block.createdate where tier = GEN-SIM* and block.createdate >= 2013-08-01 and block.createdate < 2013-09-01" | grep RECO > mc_2013_aug_reco.blocks
# dbs search --noheader --production --query="find block,block.size,block.numevents,block.createdate where tier = AODSIM and block.createdate >= 2013-08-01 and block.createdate < 2013-09-01" > mc_2013_aug_aod.blocks
# 
# dbs search --noheader --production --query="find block,block.size,block.numevents,block.createdate where tier = GEN and block.createdate >= 2013-09-01 and block.createdate < 2013-10-01" > mc_2013_sep_gen.blocks
# dbs search --noheader --production --query="find block,block.size,block.numevents,block.createdate where tier = GEN-RAW* and block.createdate >= 2013-09-01 and block.createdate < 2013-10-01" > mc_2013_sep_raw.blocks
# dbs search --noheader --production --query="find block,block.size,block.numevents,block.createdate where tier = GEN-SIM* and block.createdate >= 2013-09-01 and block.createdate < 2013-10-01" | grep -v RECO > mc_2013_sep_sim.blocks
# dbs search --noheader --production --query="find block,block.size,block.numevents,block.createdate where tier = GEN-SIM* and block.createdate >= 2013-09-01 and block.createdate < 2013-10-01" | grep RECO > mc_2013_sep_reco.blocks
# dbs search --noheader --production --query="find block,block.size,block.numevents,block.createdate where tier = AODSIM and block.createdate >= 2013-09-01 and block.createdate < 2013-10-01" > mc_2013_sep_aod.blocks
# 
# dbs search --noheader --production --query="find block,block.size,block.numevents,block.createdate where tier = GEN and block.createdate >= 2013-10-01 and block.createdate < 2013-11-01" > mc_2013_oct_gen.blocks
# dbs search --noheader --production --query="find block,block.size,block.numevents,block.createdate where tier = GEN-RAW* and block.createdate >= 2013-10-01 and block.createdate < 2013-11-01" > mc_2013_oct_raw.blocks
# dbs search --noheader --production --query="find block,block.size,block.numevents,block.createdate where tier = GEN-SIM* and block.createdate >= 2013-10-01 and block.createdate < 2013-11-01" | grep -v RECO > mc_2013_oct_sim.blocks
# dbs search --noheader --production --query="find block,block.size,block.numevents,block.createdate where tier = GEN-SIM* and block.createdate >= 2013-10-01 and block.createdate < 2013-11-01" | grep RECO > mc_2013_oct_reco.blocks
# dbs search --noheader --production --query="find block,block.size,block.numevents,block.createdate where tier = AODSIM and block.createdate >= 2013-10-01 and block.createdate < 2013-11-01" > mc_2013_oct_aod.blocks
# 
dbs search --noheader --production --query="find block,block.size,block.numevents,block.createdate where tier = GEN and block.createdate >= 2013-11-01 and block.createdate < 2013-12-01" > mc_2013_nov_gen.blocks
dbs search --noheader --production --query="find block,block.size,block.numevents,block.createdate where tier = GEN-RAW* and block.createdate >= 2013-11-01 and block.createdate < 2013-12-01" > mc_2013_nov_raw.blocks
dbs search --noheader --production --query="find block,block.size,block.numevents,block.createdate where tier = GEN-SIM* and block.createdate >= 2013-11-01 and block.createdate < 2013-12-01" | grep -v RECO > mc_2013_nov_sim.blocks
dbs search --noheader --production --query="find block,block.size,block.numevents,block.createdate where tier = GEN-SIM* and block.createdate >= 2013-11-01 and block.createdate < 2013-12-01" | grep RECO > mc_2013_nov_reco.blocks
dbs search --noheader --production --query="find block,block.size,block.numevents,block.createdate where tier = AODSIM and block.createdate >= 2013-11-01 and block.createdate < 2013-12-01" > mc_2013_nov_aod.blocks
# # 
dbs search --noheader --production --query="find block,block.size,block.numevents,block.createdate where tier = GEN and block.createdate >= 2013-12-01 and block.createdate < 2014-01-01" > mc_2013_dec_gen.blocks
dbs search --noheader --production --query="find block,block.size,block.numevents,block.createdate where tier = GEN-RAW* and block.createdate >= 2013-12-01 and block.createdate < 2014-01-01" > mc_2013_dec_raw.blocks
dbs search --noheader --production --query="find block,block.size,block.numevents,block.createdate where tier = GEN-SIM* and block.createdate >= 2013-12-01 and block.createdate < 2014-01-01" | grep -v RECO > mc_2013_dec_sim.blocks
dbs search --noheader --production --query="find block,block.size,block.numevents,block.createdate where tier = GEN-SIM* and block.createdate >= 2013-12-01 and block.createdate < 2014-01-01" | grep RECO > mc_2013_dec_reco.blocks
dbs search --noheader --production --query="find block,block.size,block.numevents,block.createdate where tier = AODSIM and block.createdate >= 2013-12-01 and block.createdate < 2014-01-01" > mc_2013_dec_aod.blocks

rm -f statistics.txt
cat mc_2013_jan_gen.blocks | grep -v Backfill | grep -vi jobrobot | grep -vi sam | awk '{SUM1+=$2} {SUM2+=$3} END {print "January 2013 GEN: Size [TB]: "SUM1/1000000000000" Events: "SUM2}' >> statistics.txt
cat mc_2013_jan_sim.blocks | grep -v Backfill | grep -vi jobrobot | grep -vi sam | awk '{SUM1+=$2} {SUM2+=$3} END {print "January 2013 GEN-SIM: Size [TB]: "SUM1/1000000000000" Events: "SUM2}' >> statistics.txt
cat mc_2013_jan_raw.blocks | grep -v Backfill | grep -vi jobrobot | grep -vi sam | awk '{SUM1+=$2} {SUM2+=$3} END {print "January 2013 GEN-RAW: Size [TB]: "SUM1/1000000000000" Events: "SUM2}' >> statistics.txt
cat mc_2013_jan_reco.blocks | grep -v Backfill | grep -vi jobrobot | grep -vi sam | awk '{SUM1+=$2} {SUM2+=$3} END {print "January 2013 GEN-SIM-RECO: Size [TB]: "SUM1/1000000000000" Events: "SUM2}' >> statistics.txt
cat mc_2013_jan_aod.blocks | grep -v Backfill | grep -vi jobrobot | grep -vi sam | awk '{SUM1+=$2} {SUM2+=$3} END {print "January 2013 AODSIM: Size [TB]: "SUM1/1000000000000" Events: "SUM2}' >> statistics.txt

cat mc_2013_feb_gen.blocks | grep -v Backfill | grep -vi jobrobot | grep -vi sam | awk '{SUM1+=$2} {SUM2+=$3} END {print "February 2013 GEN: Size [TB]: "SUM1/1000000000000" Events: "SUM2}' >> statistics.txt
cat mc_2013_feb_sim.blocks | grep -v Backfill | grep -vi jobrobot | grep -vi sam | awk '{SUM1+=$2} {SUM2+=$3} END {print "February 2013 GEN-SIM: Size [TB]: "SUM1/1000000000000" Events: "SUM2}' >> statistics.txt
cat mc_2013_feb_raw.blocks | grep -v Backfill | grep -vi jobrobot | grep -vi sam | awk '{SUM1+=$2} {SUM2+=$3} END {print "February 2013 GEN-RAW: Size [TB]: "SUM1/1000000000000" Events: "SUM2}' >> statistics.txt
cat mc_2013_feb_reco.blocks | grep -v Backfill | grep -vi jobrobot | grep -vi sam | awk '{SUM1+=$2} {SUM2+=$3} END {print "February 2013 GEN-SIM-RECO: Size [TB]: "SUM1/1000000000000" Events: "SUM2}' >> statistics.txt
cat mc_2013_feb_aod.blocks | grep -v Backfill | grep -vi jobrobot | grep -vi sam | awk '{SUM1+=$2} {SUM2+=$3} END {print "February 2013 AODSIM: Size [TB]: "SUM1/1000000000000" Events: "SUM2}' >> statistics.txt
# 
cat mc_2013_mar_gen.blocks | grep -v Backfill | grep -vi jobrobot | grep -vi sam | awk '{SUM1+=$2} {SUM2+=$3} END {print "March 2013 GEN: Size [TB]: "SUM1/1000000000000" Events: "SUM2}' >> statistics.txt
cat mc_2013_mar_sim.blocks | grep -v Backfill | grep -vi jobrobot | grep -vi sam | awk '{SUM1+=$2} {SUM2+=$3} END {print "March 2013 GEN-SIM: Size [TB]: "SUM1/1000000000000" Events: "SUM2}' >> statistics.txt
cat mc_2013_mar_raw.blocks | grep -v Backfill | grep -vi jobrobot | grep -vi sam | awk '{SUM1+=$2} {SUM2+=$3} END {print "March 2013 GEN-RAW: Size [TB]: "SUM1/1000000000000" Events: "SUM2}' >> statistics.txt
cat mc_2013_mar_reco.blocks | grep -v Backfill | grep -vi jobrobot | grep -vi sam | awk '{SUM1+=$2} {SUM2+=$3} END {print "March 2013 GEN-SIM-RECO: Size [TB]: "SUM1/1000000000000" Events: "SUM2}' >> statistics.txt
cat mc_2013_mar_aod.blocks | grep -v Backfill | grep -vi jobrobot | grep -vi sam | awk '{SUM1+=$2} {SUM2+=$3} END {print "March 2013 AODSIM: Size [TB]: "SUM1/1000000000000" Events: "SUM2}' >> statistics.txt
# 
cat mc_2013_apr_gen.blocks | grep -v Backfill | grep -vi jobrobot | grep -vi sam | awk '{SUM1+=$2} {SUM2+=$3} END {print "April 2013 GEN: Size [TB]: "SUM1/1000000000000" Events: "SUM2}' >> statistics.txt
cat mc_2013_apr_sim.blocks | grep -v Backfill | grep -vi jobrobot | grep -vi sam | awk '{SUM1+=$2} {SUM2+=$3} END {print "April 2013 GEN-SIM: Size [TB]: "SUM1/1000000000000" Events: "SUM2}' >> statistics.txt
cat mc_2013_apr_raw.blocks | grep -v Backfill | grep -vi jobrobot | grep -vi sam | awk '{SUM1+=$2} {SUM2+=$3} END {print "April 2013 GEN-RAW: Size [TB]: "SUM1/1000000000000" Events: "SUM2}' >> statistics.txt
cat mc_2013_apr_reco.blocks | grep -v Backfill | grep -vi jobrobot | grep -vi sam | awk '{SUM1+=$2} {SUM2+=$3} END {print "April 2013 GEN-SIM-RECO: Size [TB]: "SUM1/1000000000000" Events: "SUM2}' >> statistics.txt
cat mc_2013_apr_aod.blocks | grep -v Backfill | grep -vi jobrobot | grep -vi sam | awk '{SUM1+=$2} {SUM2+=$3} END {print "April 2013 AODSIM: Size [TB]: "SUM1/1000000000000" Events: "SUM2}' >> statistics.txt
# 
cat mc_2013_may_gen.blocks | grep -v Backfill | grep -vi jobrobot | grep -vi sam | awk '{SUM1+=$2} {SUM2+=$3} END {print "May 2013 GEN: Size [TB]: "SUM1/1000000000000" Events: "SUM2}' >> statistics.txt
cat mc_2013_may_sim.blocks | grep -v Backfill | grep -vi jobrobot | grep -vi sam | awk '{SUM1+=$2} {SUM2+=$3} END {print "May 2013 GEN-SIM: Size [TB]: "SUM1/1000000000000" Events: "SUM2}' >> statistics.txt
cat mc_2013_may_raw.blocks | grep -v Backfill | grep -vi jobrobot | grep -vi sam | awk '{SUM1+=$2} {SUM2+=$3} END {print "May 2013 GEN-RAW: Size [TB]: "SUM1/1000000000000" Events: "SUM2}' >> statistics.txt
cat mc_2013_may_reco.blocks | grep -v Backfill | grep -vi jobrobot | grep -vi sam | awk '{SUM1+=$2} {SUM2+=$3} END {print "May 2013 GEN-SIM-RECO: Size [TB]: "SUM1/1000000000000" Events: "SUM2}' >> statistics.txt
cat mc_2013_may_aod.blocks | grep -v Backfill | grep -vi jobrobot | grep -vi sam | awk '{SUM1+=$2} {SUM2+=$3} END {print "May 2013 AODSIM: Size [TB]: "SUM1/1000000000000" Events: "SUM2}' >> statistics.txt
# 
cat mc_2013_jun_gen.blocks | grep -v Backfill | grep -vi jobrobot | grep -vi sam | awk '{SUM1+=$2} {SUM2+=$3} END {print "June 2013 GEN: Size [TB]: "SUM1/1000000000000" Events: "SUM2}' >> statistics.txt
cat mc_2013_jun_sim.blocks | grep -v Backfill | grep -vi jobrobot | grep -vi sam | awk '{SUM1+=$2} {SUM2+=$3} END {print "June 2013 GEN-SIM: Size [TB]: "SUM1/1000000000000" Events: "SUM2}' >> statistics.txt
cat mc_2013_jun_raw.blocks | grep -v Backfill | grep -vi jobrobot | grep -vi sam | awk '{SUM1+=$2} {SUM2+=$3} END {print "June 2013 GEN-RAW: Size [TB]: "SUM1/1000000000000" Events: "SUM2}' >> statistics.txt
cat mc_2013_jun_reco.blocks | grep -v Backfill | grep -vi jobrobot | grep -vi sam | awk '{SUM1+=$2} {SUM2+=$3} END {print "June 2013 GEN-SIM-RECO: Size [TB]: "SUM1/1000000000000" Events: "SUM2}' >> statistics.txt
cat mc_2013_jun_aod.blocks | grep -v Backfill | grep -vi jobrobot | grep -vi sam | awk '{SUM1+=$2} {SUM2+=$3} END {print "June 2013 AODSIM: Size [TB]: "SUM1/1000000000000" Events: "SUM2}' >> statistics.txt
# 
cat mc_2013_jul_gen.blocks | grep -v Backfill | grep -vi jobrobot | grep -vi sam | awk '{SUM1+=$2} {SUM2+=$3} END {print "July 2013 GEN: Size [TB]: "SUM1/1000000000000" Events: "SUM2}' >> statistics.txt
cat mc_2013_jul_sim.blocks | grep -v Backfill | grep -vi jobrobot | grep -vi sam | awk '{SUM1+=$2} {SUM2+=$3} END {print "July 2013 GEN-SIM: Size [TB]: "SUM1/1000000000000" Events: "SUM2}' >> statistics.txt
cat mc_2013_jul_raw.blocks | grep -v Backfill | grep -vi jobrobot | grep -vi sam | awk '{SUM1+=$2} {SUM2+=$3} END {print "July 2013 GEN-RAW: Size [TB]: "SUM1/1000000000000" Events: "SUM2}' >> statistics.txt
cat mc_2013_jul_reco.blocks | grep -v Backfill | grep -vi jobrobot | grep -vi sam | awk '{SUM1+=$2} {SUM2+=$3} END {print "July 2013 GEN-SIM-RECO: Size [TB]: "SUM1/1000000000000" Events: "SUM2}' >> statistics.txt
cat mc_2013_jul_aod.blocks | grep -v Backfill | grep -vi jobrobot | grep -vi sam | awk '{SUM1+=$2} {SUM2+=$3} END {print "July 2013 AODSIM: Size [TB]: "SUM1/1000000000000" Events: "SUM2}' >> statistics.txt
# 
cat mc_2013_aug_gen.blocks | grep -v Backfill | grep -vi jobrobot | grep -vi sam | awk '{SUM1+=$2} {SUM2+=$3} END {print "August 2013 GEN: Size [TB]: "SUM1/1000000000000" Events: "SUM2}' >> statistics.txt
cat mc_2013_aug_sim.blocks | grep -v Backfill | grep -vi jobrobot | grep -vi sam | awk '{SUM1+=$2} {SUM2+=$3} END {print "August 2013 GEN-SIM: Size [TB]: "SUM1/1000000000000" Events: "SUM2}' >> statistics.txt
cat mc_2013_aug_raw.blocks | grep -v Backfill | grep -vi jobrobot | grep -vi sam | awk '{SUM1+=$2} {SUM2+=$3} END {print "August 2013 GEN-RAW: Size [TB]: "SUM1/1000000000000" Events: "SUM2}' >> statistics.txt
cat mc_2013_aug_reco.blocks | grep -v Backfill | grep -vi jobrobot | grep -vi sam | awk '{SUM1+=$2} {SUM2+=$3} END {print "August 2013 GEN-SIM-RECO: Size [TB]: "SUM1/1000000000000" Events: "SUM2}' >> statistics.txt
cat mc_2013_aug_aod.blocks | grep -v Backfill | grep -vi jobrobot | grep -vi sam | awk '{SUM1+=$2} {SUM2+=$3} END {print "August 2013 AODSIM: Size [TB]: "SUM1/1000000000000" Events: "SUM2}' >> statistics.txt
# 
cat mc_2013_sep_gen.blocks | grep -v Backfill | grep -vi jobrobot | grep -vi sam | awk '{SUM1+=$2} {SUM2+=$3} END {print "September 2013 GEN: Size [TB]: "SUM1/1000000000000" Events: "SUM2}' >> statistics.txt
cat mc_2013_sep_sim.blocks | grep -v Backfill | grep -vi jobrobot | grep -vi sam | awk '{SUM1+=$2} {SUM2+=$3} END {print "September 2013 GEN-SIM: Size [TB]: "SUM1/1000000000000" Events: "SUM2}' >> statistics.txt
cat mc_2013_sep_raw.blocks | grep -v Backfill | grep -vi jobrobot | grep -vi sam | awk '{SUM1+=$2} {SUM2+=$3} END {print "September 2013 GEN-RAW: Size [TB]: "SUM1/1000000000000" Events: "SUM2}' >> statistics.txt
cat mc_2013_sep_reco.blocks | grep -v Backfill | grep -vi jobrobot | grep -vi sam | awk '{SUM1+=$2} {SUM2+=$3} END {print "September 2013 GEN-SIM-RECO: Size [TB]: "SUM1/1000000000000" Events: "SUM2}' >> statistics.txt
cat mc_2013_sep_aod.blocks | grep -v Backfill | grep -vi jobrobot | grep -vi sam | awk '{SUM1+=$2} {SUM2+=$3} END {print "September 2013 AODSIM: Size [TB]: "SUM1/1000000000000" Events: "SUM2}' >> statistics.txt
# 
cat mc_2013_oct_gen.blocks | grep -v Backfill | grep -vi jobrobot | grep -vi sam | awk '{SUM1+=$2} {SUM2+=$3} END {print "October 2013 GEN: Size [TB]: "SUM1/1000000000000" Events: "SUM2}' >> statistics.txt
cat mc_2013_oct_sim.blocks | grep -v Backfill | grep -vi jobrobot | grep -vi sam | awk '{SUM1+=$2} {SUM2+=$3} END {print "October 2013 GEN-SIM: Size [TB]: "SUM1/1000000000000" Events: "SUM2}' >> statistics.txt
cat mc_2013_oct_raw.blocks | grep -v Backfill | grep -vi jobrobot | grep -vi sam | awk '{SUM1+=$2} {SUM2+=$3} END {print "October 2013 GEN-RAW: Size [TB]: "SUM1/1000000000000" Events: "SUM2}' >> statistics.txt
cat mc_2013_oct_reco.blocks | grep -v Backfill | grep -vi jobrobot | grep -vi sam | awk '{SUM1+=$2} {SUM2+=$3} END {print "October 2013 GEN-SIM-RECO: Size [TB]: "SUM1/1000000000000" Events: "SUM2}' >> statistics.txt
cat mc_2013_oct_aod.blocks | grep -v Backfill | grep -vi jobrobot | grep -vi sam | awk '{SUM1+=$2} {SUM2+=$3} END {print "October 2013 AODSIM: Size [TB]: "SUM1/1000000000000" Events: "SUM2}' >> statistics.txt
# 
cat mc_2013_nov_gen.blocks | grep -v Backfill | grep -vi jobrobot | grep -vi sam | awk '{SUM1+=$2} {SUM2+=$3} END {print "November 2013 GEN: Size [TB]: "SUM1/1000000000000" Events: "SUM2}' >> statistics.txt
cat mc_2013_nov_sim.blocks | grep -v Backfill | grep -vi jobrobot | grep -vi sam | awk '{SUM1+=$2} {SUM2+=$3} END {print "November 2013 GEN-SIM: Size [TB]: "SUM1/1000000000000" Events: "SUM2}' >> statistics.txt
cat mc_2013_nov_raw.blocks | grep -v Backfill | grep -vi jobrobot | grep -vi sam | awk '{SUM1+=$2} {SUM2+=$3} END {print "November 2013 GEN-RAW: Size [TB]: "SUM1/1000000000000" Events: "SUM2}' >> statistics.txt
cat mc_2013_nov_reco.blocks | grep -v Backfill | grep -vi jobrobot | grep -vi sam | awk '{SUM1+=$2} {SUM2+=$3} END {print "November 2013 GEN-SIM-RECO: Size [TB]: "SUM1/1000000000000" Events: "SUM2}' >> statistics.txt
cat mc_2013_nov_aod.blocks | grep -v Backfill | grep -vi jobrobot | grep -vi sam | awk '{SUM1+=$2} {SUM2+=$3} END {print "November 2013 AODSIM: Size [TB]: "SUM1/1000000000000" Events: "SUM2}' >> statistics.txt
# 
cat mc_2013_dec_gen.blocks | grep -v Backfill | grep -vi jobrobot | grep -vi sam | awk '{SUM1+=$2} {SUM2+=$3} END {print "December 2013 GEN: Size [TB]: "SUM1/1000000000000" Events: "SUM2}' >> statistics.txt
cat mc_2013_dec_sim.blocks | grep -v Backfill | grep -vi jobrobot | grep -vi sam | awk '{SUM1+=$2} {SUM2+=$3} END {print "December 2013 GEN-SIM: Size [TB]: "SUM1/1000000000000" Events: "SUM2}' >> statistics.txt
cat mc_2013_dec_raw.blocks | grep -v Backfill | grep -vi jobrobot | grep -vi sam | awk '{SUM1+=$2} {SUM2+=$3} END {print "December 2013 GEN-RAW: Size [TB]: "SUM1/1000000000000" Events: "SUM2}' >> statistics.txt
cat mc_2013_dec_reco.blocks | grep -v Backfill | grep -vi jobrobot | grep -vi sam | awk '{SUM1+=$2} {SUM2+=$3} END {print "December 2013 GEN-SIM-RECO: Size [TB]: "SUM1/1000000000000" Events: "SUM2}' >> statistics.txt
cat mc_2013_dec_aod.blocks | grep -v Backfill | grep -vi jobrobot | grep -vi sam | awk '{SUM1+=$2} {SUM2+=$3} END {print "December 2013 AODSIM: Size [TB]: "SUM1/1000000000000" Events: "SUM2}' >> statistics.txt
