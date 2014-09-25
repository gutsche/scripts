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

# cpu model mapping
cpu_mapping = {}
cpu_mapping['Intel(R) Xeon(R) CPU E5520 @ 2.27GHz'] = {'hs06' : 5.76 , 'speed' : 2270}
cpu_mapping['Intel(R) Xeon(R) CPU E5645 @ 2.40GHz'] = {'hs06' : 5.57 , 'speed' : 2400}
cpu_mapping['AMD Opteron(tm) Processor 6320'] = {'hs06' : 5.96 , 'speed' : 2800}
cpu_mapping['AMD Opteron(TM) Processor 6238'] = {'hs06' : 4.92 , 'speed' : 2600}
cpu_mapping['Intel(R) Xeon(R) CPU E5620 @ 2.40GHz'] = {'hs06' : 6.88 , 'speed' : 2400}

def drawPlot(json_file_name,property,step,normalization):

    # open json
    inputdata = json.load(open(json_file_name))
    
    # extract steps
    steps = inputdata[0].keys()

    # step check
    if step not in steps:
        print 'Step:',step,'is not included in input file, possible steps to plot are:'
        for category in steps:
            print category
        return

    # extract properties
    properties = inputdata[0][step].keys()

    # property check
    if property not in properties:
        print 'Property:',property,'is not included in input file, possible properties to plot are:'
        for category in properties:
            print category
        return
    
    for prop in properties:
        print prop
    
    # prepare array to plot
    plotarray = []
    cpus = []
    for entry in inputdata:
        
        data = entry[step][property]
        
        # divide by total job time for Timing-tstoragefile-read-totalMegabytes
        if property == 'Timing-tstoragefile-read-totalMegabytes':
            data /= entry[step]['TotalJobTime']
        
        norm = 1.
        if normalization == 2:
            norm = cpu_mapping[entry[step]['CPUModels']]['hs06']
        elif normalization == 3:
            norm = cpu_mapping[entry[step]['CPUModels']]['hs06']*entry[step]['averageCoreSpeed']/cpu_mapping[entry[step]['CPUModels']]['speed']

        plotarray.append(data * norm)

        tmp_cpu = {'CPUModels':entry[step]['CPUModels'],'totalCPUs':entry[step]['totalCPUs']}
        if tmp_cpu not in cpus: cpus.append(tmp_cpu)
        
    for cpu in cpus:
        print "Model: %40s, totalCPUs: %3i" % (cpu['CPUModels'],cpu['totalCPUs'])

        
    # create canvas
    c1 = TCanvas( 'c1', 'Histogram Drawing Options', 1024, 768 )
    
    # c1.SetBottomMargin(0.15)
    # c1.SetRightMargin(0.01)
    # c1.SetGridx(True)
    # c1.SetGridy(True)

    # create histogram(s)
    maxbin = sorted(plotarray)[-1]*1.1
    nbins = 100
    histogram = TH1F(property,property,nbins,0,maxbin)
    
    # fill histogram(s)
    for number in plotarray:
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
    
    filename = json_file_name.replace('.json','') + '_' + property
    if normalization == 2:
        filename += '_HS06_normalization'
    elif normalization == 3:
        filename += '_HS06_and_clock_speed_normalization'

    # safe as pdf and gif
    c1.SaveAs(filename + '.pdf')
    c1.SaveAs(filename + '.gif')
    return

def main():
    usage="%prog <options>\n\nPrepares plot from input JSON file\n"

    parser = OptionParser(usage=usage)
    parser.add_option("-d", "--data", dest="data", help="Input data in JSON format", metavar="<data>")
    parser.add_option("-s", "--step", dest="step", help="TaskChain step", metavar="<step>")
    parser.add_option("-p", "--property", dest="property", help="property to plot from JSON input file", metavar="<property>")
    parser.add_option("-n", "--normalization", dest="normalization", help="normalization: 1: no normalization, 2: normalize on HS06, 3: normalize on HS06 and average clock speed", metavar="<normalization>")
   
    (opts, args) = parser.parse_args()
    if not (opts.data):
        parser.print_help()
        parser.error('Please specify input data in JSON format using -d or --data')
    if not (opts.property):
        parser.print_help()
        parser.error('Please specify property to plot from JSON input file using -p or --property')
    if not (opts.step):
        parser.print_help()
        parser.error('Please specify TaskChain step to plot from JSON input file using -s or --step')

    if not (opts.normalization):
        parser.print_help()
        parser.error('Please specifu normalization with -n or --normalization')
        
    if int(opts.normalization) == 1:
        print "No normalization"
    elif int(opts.normalization) == 2:
        print "Normalize on HS06"
    elif int(opts.normalization) == 3:
        print "Normalize on HS06 and average clock speed"            
    else:
        print "Unknown normalization"
        sys.exit(1)

    drawPlot(opts.data,opts.property, opts.step, int(opts.normalization))
    
    sys.exit(0);

if __name__ == "__main__":
    main()
    sys.exit(0);
