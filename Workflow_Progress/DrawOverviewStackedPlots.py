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

# seconds per day	
sdays = 86400

def local_time_offset(t=None):
    """Return offset of local zone from GMT, either at present or at time t."""
    # python2.3 localtime() can't take None
    if t is None:
        t = time.time()

    if time.localtime(t).tm_isdst and time.daylight:
        return -time.altzone
    else:
        return -time.timezone
        
def utcTimestampFromDate(year,month,day):
    local = datetime.datetime(year,month,day)
    return int(local.strftime('%s')) + local_time_offset()
    
def utcTimeStringFromUtcTimestamp(timestamp):
    return datetime.datetime.fromtimestamp(int(timestamp), tz=pytz.timezone('UTC')).strftime("%d %b %Y")

def PositiveIntegerWithCommas(number):
    if number > 0:
        return ''.join(reversed([x + (',' if i and not i % 3 else '') for i, x in enumerate(reversed(str(number)))]))

    return str(number)
    
def drawStackedPlot(all_json_file_name, json_file_names, status, lastDays = -1):
    # open json files
    # use all json file and subtract all specific json files in the end, therefore call it other although 'inputdata' points to the all_json_file_name
    other = {}
    identifier = all_json_file_name.split('.')[0]
    identifier = identifier.replace('STAR_','*/')
    identifier = '/' + identifier
    other[identifier] = {}
    other[identifier]['inputdata'] = json.load(open(all_json_file_name))
    other[identifier]['total'] = 0
    other[identifier]['table'] = {}
    other_identifier = identifier
    
    data = {}
    for json_file_name in json_file_names:
        identifier = json_file_name.split('.')[0]
        identifier = identifier.replace('STAR_','*/')
        identifier = '/' + identifier
        data[identifier] = {}
        data[identifier]['inputdata'] = json.load(open(json_file_name))
        data[identifier]['total'] = 0
        data[identifier]['table'] = {}
        
        
    printout = 'Creating stack plot for DBS-status '
    if status == 'production':
        printout = printout + 'PRODUCTION+VALID'
    elif status == 'valid':
        printout = printout + 'VALID'
    printout = printout + ' for identifier ' + identifier + ' reading in the file for the complete production ' + json_file_name + ' and the specific production files ' + ','.join(json_file_names)
    if lastDays != -1:
        printout = printout + 'for the last ' + str(lastDays) + ' days'
    print printout
    
    # calculate bins and label offset so that 20 labels are drawn
    # use all as reference
    bins = sorted(other[other_identifier]['inputdata'].keys())
    if lastDays != -1:
        bins = sorted(other[other_identifier]['inputdata'].keys())[-lastDays:]
    nBins = len(bins)
    labelOffset = int(nBins/20)
    
    # create canvas
    c1 = TCanvas( 'c1', 'Histogram Drawing Options', 1024, 768 )
    c1.SetBottomMargin(0.15)
    c1.SetRightMargin(0.01)
    c1.SetGridx(True)
    c1.SetGridy(True)
    
    # create histogram(s)
    other_name = "other"
    if lastDays != -1:
        other_name = other_name + '_' + str(lastDays)
    other[other_identifier]['hist'] = TH1F(other_name,other_name,nBins,0,nBins)
    counter = 0
    for entry in data.keys():
        counter += 1
        hist_name = "hist " + str(counter)
        if lastDays != -1:
            hist_name = hist_name + '_' + str(lastDays)
        data[entry]['hist'] = TH1F(hist_name,hist_name,nBins,0,nBins)


    # fill histogram(s)
    for bin in range(nBins):
        total_bin_value_to_calculate_other = 0
        for entry in data.keys():
            bin_value = 0
            if bins[bin] in data[entry]['inputdata'].keys():
                bin_value = data[entry]['inputdata'][bins[bin]]['VALID']
                if status == 'production':
                    bin_value += data[entry]['inputdata'][bins[bin]]['PRODUCTION']
            data[entry]['total'] += bin_value
            total_bin_value_to_calculate_other += bin_value
            data[entry]['hist'].SetBinContent(bin+1,bin_value+data[entry]['hist'].GetBinContent(bin))
            data[entry]['table'][bins[bin]] = bin_value
            if nBins < 40:
                data[entry]['hist'].GetXaxis().SetBinLabel(bin+1,utcTimeStringFromUtcTimestamp(int(bins[bin])))
            else:
                if (bin) == 0:
                    # first bin
                    data[entry]['hist'].GetXaxis().SetBinLabel(bin+1,utcTimeStringFromUtcTimestamp(int(bins[bin])))
                elif (bin+1) % labelOffset == 0 and (bin+1) < nBins-labelOffset :
                    # only 20 axis labels are drawn
                    data[entry]['hist'].GetXaxis().SetBinLabel(bin+1,utcTimeStringFromUtcTimestamp(int(bins[bin])))
                elif (bin+1) == nBins:
                    # last bin
                    data[entry]['hist'].GetXaxis().SetBinLabel(bin+1,utcTimeStringFromUtcTimestamp(int(bins[bin])))
                else:
                    data[entry]['hist'].GetXaxis().SetBinLabel(bin+1,'')
                    
        other_bin_value = other[other_identifier]['inputdata'][bins[bin]]['VALID']
        if status == 'production':
            other_bin_value += other[other_identifier]['inputdata'][bins[bin]]['PRODUCTION']
        # subtract all other campaigns
        other_bin_value -= total_bin_value_to_calculate_other
        other[other_identifier]['total'] += other_bin_value
        other[other_identifier]['hist'].SetBinContent(bin+1,other_bin_value+other[other_identifier]['hist'].GetBinContent(bin))
        other[other_identifier]['table'][bins[bin]] = other_bin_value
        if nBins < 40:
            other[other_identifier]['hist'].GetXaxis().SetBinLabel(bin+1,utcTimeStringFromUtcTimestamp(int(bins[bin])))
        else:
            if (bin) == 0:
                # first bin
                other[other_identifier]['hist'].GetXaxis().SetBinLabel(bin+1,utcTimeStringFromUtcTimestamp(int(bins[bin])))
            elif (bin+1) % labelOffset == 0 and (bin+1) < nBins-labelOffset :
                # only 20 axis labels are drawn
                other[other_identifier]['hist'].GetXaxis().SetBinLabel(bin+1,utcTimeStringFromUtcTimestamp(int(bins[bin])))
            elif (bin+1) == nBins:
                # last bin
                other[other_identifier]['hist'].GetXaxis().SetBinLabel(bin+1,utcTimeStringFromUtcTimestamp(int(bins[bin])))
            else:
                other[other_identifier]['hist'].GetXaxis().SetBinLabel(bin+1,'')

    # set histogram options
    other_title = 'Events for all other campaigns, total: ' + PositiveIntegerWithCommas(other[other_identifier]['total'])
    if lastDays == -1:
        other_title += ', avg/day: ' + PositiveIntegerWithCommas(int(float(other[other_identifier]['total'])/float(nBins)))
    else:
        other_title += ', avg/day: ' + PositiveIntegerWithCommas(int(float(other[other_identifier]['total'])/float(lastDays)))
    other[other_identifier]['hist'].SetTitle(other_title)
    other[other_identifier]['hist'].SetStats(False)
    other[other_identifier]['hist'].GetXaxis().CenterLabels()
    other[other_identifier]['hist'].GetXaxis().LabelsOption('v')
    other[other_identifier]['hist'].SetLineWidth(2)
    other[other_identifier]['hist'].SetLineColor(9)
    other[other_identifier]['hist'].SetFillColor(9)
    other[other_identifier]['hist'].SetFillStyle(1000)
    if nBins < 40:
        other[other_identifier]['hist'].SetBarWidth(0.8)
        other[other_identifier]['hist'].SetBarOffset(0.1)
    counter = 1
    for entry in data.keys():
        counter += 1
        entry_title = 'Events for ' + entry + ' , total: ' + PositiveIntegerWithCommas(data[entry]['total'])
        if lastDays == -1:
            entry_title += ', avg/day: ' + PositiveIntegerWithCommas(int(float(data[entry]['total'])/float(nBins)))
        else:
            entry_title += ', avg/day: ' + PositiveIntegerWithCommas(int(float(data[entry]['total'])/float(lastDays)))
        data[entry]['hist'].SetTitle(entry_title)
        data[entry]['hist'].SetStats(False)
        data[entry]['hist'].GetXaxis().CenterLabels()
        data[entry]['hist'].GetXaxis().LabelsOption('v')
        data[entry]['hist'].SetLineWidth(2)
        data[entry]['hist'].SetLineColor(counter)
        data[entry]['hist'].SetFillColor(counter)
        data[entry]['hist'].SetFillStyle(1000)
        if nBins < 40:
            data[entry]['hist'].SetBarWidth(0.8)
            data[entry]['hist'].SetBarOffset(0.1)
    
    # draw and save in pdf
    title = 'Overview for DBS-status VALID'
    total = 0
    if status == 'production':
        title = title + '+PRODUCTION'
    stack = THStack('stack',title)
    stack.Add(other[other_identifier]['hist'])
    total += other[other_identifier]['total']
    for entry in data.keys():
        stack.Add(data[entry]['hist'])
        total += data[entry]['total']
    title = title + ', total: ' + PositiveIntegerWithCommas(total)
    if lastDays == -1:
        title += ', avg/day: ' + PositiveIntegerWithCommas(int(float(total)/float(nBins)))
    else:
        title += ', avg/day: ' + PositiveIntegerWithCommas(int(float(total)/float(lastDays)))
    stack.SetTitle(title)
    stack.Draw("bar0")
    stack.GetXaxis().LabelsOption('v')
    legend = c1.BuildLegend(0.14,0.8,0.64,0.89)
    legend.SetFillColor(kWhite)
    base_output_filename = all_json_file_name.replace('.json','_valid')
    if status == 'production':
        base_output_filename = base_output_filename + '_plus_production'
    if lastDays != -1:
        base_output_filename = base_output_filename + '_' + str(lastDays)
    c1.SaveAs('total_' + base_output_filename + '.pdf')
    c1.SaveAs('total_' + base_output_filename + '.gif')

    # print table
    table = ''
    total = 0
    # header
    if status == 'production':
        table += '| *PRODUCTION+VALID* |'
    else:
        table += '| *VALID* |'
    for entry in data.keys():
        table += ' *' + entry + '* |'
    table += ' *Other* | *Total* |\n'
    for day in sorted(other[other_identifier]['table'].keys()):
        total_per_day = 0
        table += '| *' + datetime.datetime.fromtimestamp(int(day)).strftime("%d %b %Y") + '* |'
        for entry in data.keys():
            table += '  ' + PositiveIntegerWithCommas(data[entry]['table'][day]) + ' |'
            total_per_day += data[entry]['table'][day]
        table += '  ' + PositiveIntegerWithCommas(other[other_identifier]['table'][day]) + ' |'
        total_per_day += other[other_identifier]['table'][day]
        table += '  ' + PositiveIntegerWithCommas(total_per_day) + ' |\n'
        total += total_per_day
    table += '| *Total* |'
    denominator = nBins
    if lastDays != -1:
        denominator = lastDays
    for entry in data.keys():
        table += '  ' + PositiveIntegerWithCommas(data[entry]['total']) + ' |'
    table += '  ' + PositiveIntegerWithCommas(other[other_identifier]['total']) + ' |'
    table += '  ' + PositiveIntegerWithCommas(total) + ' |\n'
    table += '| *Average* |'
    denominator = nBins
    if lastDays != -1:
        denominator = lastDays
    for entry in data.keys():
        table += '  ' + PositiveIntegerWithCommas(int(float(data[entry]['total'])/float(denominator))) + ' |'
    table += '  ' + PositiveIntegerWithCommas(int(float(other[other_identifier]['total'])/float(denominator))) + ' |'
    table += '  ' + PositiveIntegerWithCommas(int(float(total)/float(denominator))) + ' |\n'
    
    table_output_file = open('total_' + base_output_filename + '_twiki.txt','w')
    table_output_file.write(table)
    table_output_file.close()
    printout = "Wrote TWiki table of daily production values and averages to " + 'total_' + base_output_filename + '_twiki.txt'

    return

def main():
    usage="%prog <options>\n\nPrepares stacked plots of PRODUCTION and VALID events produced per day, for all days in the input data file and for the last specified days, specifying the total production and specific selected campaigns or selected workflows\n"

    parser = OptionParser(usage=usage)
    parser.add_option("-d", "--data", dest="data", help="Comma separated list of input data in JSON format", metavar="<data>")
    parser.add_option("-a", "--all", dest="all", help="Input data of the complete production in JSON format", metavar="<all>")
    parser.add_option("-l", "--last", dest="last", help="restrict to last X days of the input JSON, default is 7 days.", metavar="<last>")
    parser.add_option("-s", "--status", dest="status", help="To prepare plots for events with DBS-status VALID+PRODUCTION, select -s production; to prepare plots for DBS-status VALID, selecte -s valid; default is production", metavar="<status>")
    parser.set_defaults(last=7)
    parser.set_defaults(status='production')
   
    (opts, args) = parser.parse_args()
    if not (opts.data or opts.all):
        parser.print_help()
        parser.error('Please specify input data in JSON format using -d or --data, and input JSON file for the complete production using -a or --all')        
    data = opts.data.split(',')
    drawStackedPlot(opts.all,data,opts.status,-1)
    drawStackedPlot(opts.all,data,opts.status,opts.last)
    
    sys.exit(0);

if __name__ == "__main__":
    main()
    sys.exit(0);
