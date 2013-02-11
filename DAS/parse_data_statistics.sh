echo ""
echo "RAW Size"
echo ""
cat statistics.txt | grep 'RAW:' | awk '{print $6}'
echo ""
echo "RAW Events"
echo ""
cat statistics.txt | grep 'RAW:' | awk '{print $8}'

echo ""
echo "PromptReco RECO Size"
echo ""
cat statistics.txt | grep 'PromptReco RECO' | awk '{print $7}'
echo ""
echo "PromptReco RECO Events"
echo ""
cat statistics.txt | grep 'PromptReco RECO' | awk '{print $9}'
echo ""
echo "PromptSkim RECO Size"
echo ""
cat statistics.txt | grep 'PromptSkim RECO' | awk '{print $7}'
echo ""
echo "PromptSkim RECO Events"
echo ""
cat statistics.txt | grep 'PromptSkim RECO' | awk '{print $9}'
echo ""
echo "NonPrompt RECO Size"
echo ""
cat statistics.txt | grep 'NonPrompt RECO' | awk '{print $7}'
echo ""
echo "NonPrompt RECO Events"
echo ""
cat statistics.txt | grep 'NonPrompt RECO' | awk '{print $9}'

echo ""
echo "PromptReco AOD Size"
echo ""
cat statistics.txt | grep 'PromptReco AOD' | awk '{print $7}'
echo ""
echo "PromptReco AOD Events"
echo ""
cat statistics.txt | grep 'PromptReco AOD' | awk '{print $9}'
echo ""
echo "PromptSkim AOD Size"
echo ""
cat statistics.txt | grep 'PromptSkim AOD' | awk '{print $7}'
echo ""
echo "PromptSkim AOD Events"
echo ""
cat statistics.txt | grep 'PromptSkim AOD' | awk '{print $9}'
echo ""
echo "NonPrompt AOD Size"
echo ""
cat statistics.txt | grep 'NonPrompt AOD' | awk '{print $7}'
echo ""
echo "NonPrompt AOD Events"
echo ""
cat statistics.txt | grep 'NonPrompt AOD' | awk '{print $9}'

echo ""
echo "PromptSkim RAW-RECO Size"
echo ""
cat statistics.txt | grep 'PromptSkim RAW-RECO' | awk '{print $7}'
echo ""
echo "PromptSkim RAW-RECO Events"
echo ""
cat statistics.txt | grep 'PromptSkim RAW-RECO' | awk '{print $9}'
echo ""
echo "NonPrompt RAW-RECO Size"
echo ""
cat statistics.txt | grep 'NonPrompt RAW-RECO' | awk '{print $7}'
echo ""
echo "NonPrompt RAW-RECO Events"
echo ""
cat statistics.txt | grep 'NonPrompt RAW-RECO' | awk '{print $9}'

echo ""
echo "PromptSkim USER Size"
echo ""
cat statistics.txt | grep 'PromptSkim USER' | awk '{print $7}'
echo ""
echo "PromptSkim USER Events"
echo ""
cat statistics.txt | grep 'PromptSkim USER' | awk '{print $9}'
echo ""
echo "NonPrompt USER Size"
echo ""
cat statistics.txt | grep 'NonPrompt USER' | awk '{print $7}'
echo ""
echo "NonPrompt USER Events"
echo ""
cat statistics.txt | grep 'NonPrompt USER' | awk '{print $9}'
