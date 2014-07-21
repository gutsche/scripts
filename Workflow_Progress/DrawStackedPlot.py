#!/usr/bin/env python
"""

Draw stacked plot using ROOT

"""

import  sys,datetime,json,re,urllib2,httplib,time
import pytz
from optparse import OptionParser

from ROOT import TCanvas, TPad, TFile, TPaveLabel, TPaveText, TH1F, THStack
from ROOT import gROOT,kRed,kBlue,kWhite

gROOT.Reset()
gROOT.SetBatch(True)

def PositiveIntegerWithCommas(number):
    if number > 0:
        return ''.join(reversed([x + (',' if i and not i % 3 else '') for i, x in enumerate(reversed(str(number)))]))

    return str(number)
    
def drawStackedPlot(json_file_name, lastDays = -1):

    # open json
    inputdata = json.load(open(json_file_name))
    identifier = json_file_name.split('.')[0]
    identifier = identifier.replace('STAR_','*/')
    identifier = '/' + identifier
    if lastDays == -1:
        print 'Creating VALID and PRODUCTION stack plot for',identifier,'reading in file',json_file_name
    else:
        print 'Creating VALID and PRODUCTION stack plot for',identifier,'reading in file',json_file_name,'for the last',lastDays,'days'
    
    # calculate bins and label offset so that 20 labels are drawn
    bins = sorted(inputdata.keys())
    if lastDays != -1:
        bins = sorted(inputdata.keys())[-lastDays:]
    nBins = len(bins)
    labelOffset = int(nBins/20)
    
    # create canvas
    c1 = TCanvas( 'c1', 'Histogram Drawing Options', 1024, 768 )
    c1.SetBottomMargin(0.15)
    c1.SetRightMargin(0.01)
    c1.SetGridx(True)
    c1.SetGridy(True)
    
    # create histogram(s)
    valid_name = "valid"
    if lastDays != -1:
        valid_name = valid_name + '_' + str(lastDays)
    production_name = "production"
    if lastDays != -1:
        production_name = production_name + '_' + str(lastDays)
    valid = TH1F(valid_name,valid_name,nBins,0,nBins)
    production = TH1F(production_name,production_name,nBins,0,nBins)

    # fill histogram(s)
    total_valid = 0;
    total_production = 0;
    for bin in range(nBins):
        valid.SetBinContent(bin+1,inputdata[bins[bin]]['VALID']+valid.GetBinContent(bin))
        total_valid += inputdata[bins[bin]]['VALID']
        production.SetBinContent(bin+1,inputdata[bins[bin]]['PRODUCTION']+production.GetBinContent(bin))
        total_production += inputdata[bins[bin]]['PRODUCTION']
        if nBins < 40:
            valid.GetXaxis().SetBinLabel(bin+1,datetime.datetime.fromtimestamp(int(bins[bin])).strftime("%d %b %Y"))
            production.GetXaxis().SetBinLabel(bin+1,datetime.datetime.fromtimestamp(int(bins[bin])).strftime("%d %b %Y"))
        else:
            if (bin) == 0:
                # first bin
                valid.GetXaxis().SetBinLabel(bin+1,datetime.datetime.fromtimestamp(int(bins[bin])).strftime("%d %b %Y"))
                production.GetXaxis().SetBinLabel(bin+1,datetime.datetime.fromtimestamp(int(bins[bin])).strftime("%d %b %Y"))
            elif (bin+1) % labelOffset == 0 and (bin+1) < nBins-labelOffset :
                # only 20 axis labels are drawn
                valid.GetXaxis().SetBinLabel(bin+1,datetime.datetime.fromtimestamp(int(bins[bin])).strftime("%d %b %Y"))
                production.GetXaxis().SetBinLabel(bin+1,datetime.datetime.fromtimestamp(int(bins[bin])).strftime("%d %b %Y"))
            elif (bin+1) == nBins:
                # last bin
                valid.GetXaxis().SetBinLabel(bin+1,datetime.datetime.fromtimestamp(int(bins[bin])).strftime("%d %b %Y"))
                production.GetXaxis().SetBinLabel(bin+1,datetime.datetime.fromtimestamp(int(bins[bin])).strftime("%d %b %Y"))
            else:
                valid.GetXaxis().SetBinLabel(bin+1,'')
                production.GetXaxis().SetBinLabel(bin+1,'')

    # set histogram options
    valid.SetTitle('Events with DBS-status VALID, total: ' + PositiveIntegerWithCommas(total_valid))
    valid.SetStats(False)
    valid.GetXaxis().CenterLabels()
    valid.GetXaxis().LabelsOption('v')
    valid.SetLineWidth(2)
    valid.SetLineColor(kBlue)
    valid.SetFillColor(kBlue)
    valid.SetFillStyle(1000)
    production.SetTitle('Events with DBS-status PRODUCTION, total: ' + PositiveIntegerWithCommas(total_production))
    production.SetStats(False)
    production.GetXaxis().CenterLabels()
    production.GetXaxis().LabelsOption('v')
    production.SetLineWidth(2)
    production.SetLineColor(kRed)
    production.SetFillColor(kRed)
    production.SetFillStyle(1000)
    
    # draw and save in pdf
    stack = THStack('stack',identifier)
    stack.Add(valid)
    stack.Add(production)
    stack.Draw("C")
    stack.GetXaxis().LabelsOption('v')
    legend = c1.BuildLegend(0.14,0.8,0.54,0.89)
    legend.SetFillColor(kWhite)
    if lastDays == -1:
        c1.SaveAs(json_file_name.replace('.json','.pdf'))
        c1.SaveAs(json_file_name.replace('.json','.gif'))
    else:
        c1.SaveAs(json_file_name.replace('.json','_' + str(lastDays) + '.pdf'))
        c1.SaveAs(json_file_name.replace('.json','_' + str(lastDays) + '.gif'))
    return

def main():
    usage="%prog <options>\n\nPrepares stacked plots of PRODUCTION and VALID events produced per day, for all days in the input data file and for the last specified days\n"

    parser = OptionParser(usage=usage)
    parser.add_option("-d", "--data", dest="data", help="Input data in JSON format", metavar="<data>")
    parser.add_option("-l", "--last", dest="last", help="restrict to last X days of the input JSON, default is 7 days.", metavar="<last>")
    parser.set_defaults(last=7)
   
    (opts, args) = parser.parse_args()
    if not (opts.data):
        parser.print_help()
        parser.error('Please specify input data in JSON format using -d or --data')
        
    drawStackedPlot(opts.data,-1)
    drawStackedPlot(opts.data,opts.last)
    
    sys.exit(0);

if __name__ == "__main__":
    main()
    sys.exit(0);
