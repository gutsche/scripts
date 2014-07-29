#!/usr/bin/env python
"""

Add json files

"""

import sys,datetime,json,re,urllib2,httplib,time
import pytz
from optparse import OptionParser

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

def addJSONFiles(json_file_names):
    
    files = []
    for json_file_name in json_file_names:
        files.append(json.load(open(json_file_name)))

    keys = []
    for file in files:
        for key in file.keys():
            if key not in keys: keys.append(key)
            
    results = {}
    for key in keys:
        if key not in results.keys(): results[key] = { 'VALID':0, 'PRODUCTION':0, 'REQUESTED':0, 'INVALID':0, 'DEPRECATED':0}
        for file in files:
            if key in file.keys():
                results[key]['VALID'] += file[key]['VALID']
                results[key]['PRODUCTION'] += file[key]['PRODUCTION']
                results[key]['REQUESTED'] += file[key]['REQUESTED']
                results[key]['INVALID'] += file[key]['INVALID']
                results[key]['DEPRECATED'] += file[key]['DEPRECATED']
    return results
    

def main():
    usage="%prog <options>\n\nAdds json files\n"

    parser = OptionParser(usage=usage)
    parser.add_option("-d", "--data", dest="data", help="Comma separated list of input data in JSON format", metavar="<data>")
    parser.add_option("-n", "--name", dest="name", help="Base name of output json file", metavar="<data>")
   
    (opts, args) = parser.parse_args()
    if not (opts.data and opts.name):
        parser.print_help()
        parser.error('Please specify input data in JSON format using -d or --data; and the base output file name with -n or --name')        
    data = opts.data.split(',')
    result = addJSONFiles(data)

    # write output to files
    csv_output = open(opts.name + '.csv','w')
    json_output = open(opts.name + '.json','w')
    
    for day in sorted(result.keys()):
        csv_line = "%s,%i,%i,%i,%i,%i\n" % (utcTimeStringFromUtcTimestamp(int(day)),result[day]['VALID'],result[day]['PRODUCTION'],result[day]['REQUESTED'],result[day]['INVALID'],result[day]['DEPRECATED'])
        csv_output.write(csv_line)
    csv_output.close()
    
    json.dump(result,json_output)
    json_output.close
    
    sys.exit(0);

if __name__ == "__main__":
    main()
    sys.exit(0);
