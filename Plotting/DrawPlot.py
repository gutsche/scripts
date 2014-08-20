#!/usr/bin/env python
"""

Draw plot using ROOT

"""

import sys,json
from optparse import OptionParser

from ROOT import TCanvas, TPad, TFile, TPaveLabel, TPaveText, TH1F, THStack
from ROOT import gROOT,kRed,kBlue,kWhite,gStyle

gROOT.Reset()
# gROOT.SetBatch(True)
# statistics display
gStyle.SetOptStat(1111)

# seconds per day	
sdays = 86400

def drawPlot(json_file_name,property):

    # open json
    inputdata = json.load(open(json_file_name))

    # property check
    if property not in inputdata.keys():
        print 'Property:',property,'is not included in input file, possible properties to plot are:'
        for category in inputdata.keys():
            print category
        return
        
    # create canvas
    c1 = TCanvas( 'c1', 'Histogram Drawing Options', 1024, 768 )
    
    # c1.SetBottomMargin(0.15)
    # c1.SetRightMargin(0.01)
    # c1.SetGridx(True)
    # c1.SetGridy(True)

    # create histogram(s)
    nbins = int(sorted(inputdata[property])[-1]*1.1)
    maxbin = nbins
    if nbins < 1000: nbins = 1000
    histogram = TH1F(property,property,nbins,0,maxbin)
    
    # fill histogram(s)
    for number in inputdata[property]:
        histogram.Fill(number)

    # # set histogram options
    # histogram.SetOptStats(11111)
    # valid.SetTitle('Events with DBS-status VALID, total: ' + PositiveIntegerWithCommas(total_valid))
    # valid.SetStats(False)
    # valid.GetXaxis().CenterLabels()
    # valid.GetXaxis().LabelsOption('v')
    # valid.SetLineWidth(2)
    # valid.SetLineColor(kBlue)
    # valid.SetFillColor(kBlue)
    # valid.SetFillStyle(1000)
    # if nBins < 40:
    #     valid.SetBarWidth(0.8)
    #     valid.SetBarOffset(0.1)

    # draw
    histogram.Draw()
    
    raw_input('Press <ret> to end -> ')
    
    # safe as pdf and gif
    c1.SaveAs(json_file_name.replace('.json','') + '_' + property + '.pdf')
    c1.SaveAs(json_file_name.replace('.json','') + '_' + property + '.gif')
    return

def main():
    usage="%prog <options>\n\nPrepares plot from input JSON file\n"

    parser = OptionParser(usage=usage)
    parser.add_option("-d", "--data", dest="data", help="Input data in JSON format", metavar="<data>")
    parser.add_option("-p", "--property", dest="property", help="property to plot from JSON input file", metavar="<property>")
   
    (opts, args) = parser.parse_args()
    if not (opts.data):
        parser.print_help()
        parser.error('Please specify input data in JSON format using -d or --data')
    if not (opts.property):
        parser.print_help()
        parser.error('Please specify property to plot from JSON input file using -p or --property')
        
    drawPlot(opts.data,opts.property)
    
    sys.exit(0);

if __name__ == "__main__":
    main()
    sys.exit(0);
