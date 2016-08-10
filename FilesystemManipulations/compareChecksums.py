#!/usr/bin/env python
import os,sys
from optparse import OptionParser
import json


def main():
    # initialization
    usage  = "Usage: %prog [options]"
    parser = OptionParser(usage=usage)
    parser.add_option("-v", "--verbose", action="store_true", default=False, dest="verbose", help="verbose output")
    parser.add_option("-o", "--one", action="store", type="string", default=None, dest="one", help="First filename with chksums in JSON format")
    parser.add_option("-t", "--two", action="store", type="string", default=None, dest="two", help="Second filename with chksums in JSON format")
    (opts, args) = parser.parse_args()
    verbose=opts.verbose
    one = opts.one
    two = opts.two

    if one == None or two == None:
        parser.print_help()
        parser.error('Please specify two input filenames.')

    one_dict = json.load(open(one))
    two_dict = json.load(open(two))

    print ''
    print 'Number of entries in file:',one,':',len(one_dict.keys())
    print 'Number of entries in file:',two,':',len(two_dict.keys())

    files_in_one_but_not_in_two = []
    files_in_two_but_not_in_one = []
    checksum_mismatch = []
    
    for file in one_dict.keys():
        if file not in two_dict.keys(): 
            files_in_one_but_not_in_two.append(file)
        else:
            if one_dict[file]['chksum'] != two_dict[file]['chksum']: checksum_mismatch.append(file)
            if verbose:
                print 'file:',one,':',file,one_dict[file]['chksum'],'file:',two,':',file,two_dict[file]['chksum']
    for file in two_dict.keys():
        if file not in one_dict.keys(): 
            files_in_two_but_not_in_one.append(file)
            
            
    print ''
    print 'Number of entries in file:',one,'but not in file:',two,':',len(files_in_one_but_not_in_two)
    for missing_two in files_in_one_but_not_in_two:
        print 'entry:',os.path.join(one_dict[missing_two]['root'],missing_two)

    print ''
    print 'Number of entries in file:',two,'but not in file:',one,':',len(files_in_two_but_not_in_one)
    for missing_one in files_in_two_but_not_in_one:
        print 'entry:',missing_one
        
    print ''
    print 'Checksum mismatches:',len(checksum_mismatch)
    for mismatch in checksum_mismatch:
        print ''
        print 'mismatch from file:',one,':',mismatch,one_dict[mismatch]['chksum']
        print 'mismatch from file:',two,':',mismatch,two_dict[mismatch]['chksum']


if __name__ == "__main__":
    main()
    sys.exit(0);
