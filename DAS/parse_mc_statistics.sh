echo ""
echo "GEN Size:"
echo ""
cat statistics.txt | grep GEN | grep -v SIM | grep -v RAW | awk '{print $6}'
echo ""
echo "GEN Events:"
echo ""
cat statistics.txt | grep GEN | grep -v SIM | grep -v RAW | awk '{print $8}'
echo ""
echo "GEN-SIM Size:"
echo ""
cat statistics.txt | grep GEN-SIM | grep -v RECO | awk '{print $6}'
echo ""
echo "GEN-SIM Events:"
echo ""
cat statistics.txt | grep GEN-SIM | grep -v RECO | awk '{print $8}'
echo ""
echo "GEN-RAW Size:"
echo ""
cat statistics.txt | grep GEN-RAW | awk '{print $6}'
echo ""
echo "GEN-RAW Events:"
echo ""
cat statistics.txt | grep GEN-RAW | awk '{print $8}'
echo ""
echo "GEN-SIM-RECO Size:"
echo ""
cat statistics.txt | grep GEN-SIM-RECO | awk '{print $6}'
echo ""
echo "GEN-SIM-RECO Events:"
echo ""
cat statistics.txt | grep GEN-SIM-RECO | awk '{print $8}'
echo ""
echo "AODSIM Size:"
echo ""
cat statistics.txt | grep AODSIM | awk '{print $6}'
echo ""
echo "AODSIM Events:"
echo ""
cat statistics.txt | grep AODSIM | awk '{print $8}'
