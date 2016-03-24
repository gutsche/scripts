#!/usr/bin/env python
import sys,os,tempfile,tarfile,json,shutil
from optparse import OptionParser
import WMCore.FwkJobReport.Report as Report

def extractFJR(inputLogArchive, outputDirectory, baseTempDirectory, verbose):
    # make temporary directory
    if baseTempDirectory == None:
        tempDirectory = tempfile.mkdtemp()
    else:
        tempDirectory = tempfile.mkdtemp('',baseTempDirectory)
    if verbose == True: print 'tempDirectory',tempDirectory
    
    # untar logArchive into tempDirectory
    logArchiveTarFile = tarfile.open(inputLogArchive)
    logArchiveTarFile.extractall(path=tempDirectory)

    # list directories
    relativeSubDirectories = [ d for d in os.listdir(tempDirectory) if os.path.isdir(os.path.join(tempDirectory,d))]

    report_components = {}

    # find FrameworkJobReport.xml and Report.pkl in each directory
    for dir in relativeSubDirectories:
        if os.path.isfile(os.path.join(tempDirectory,dir)+'/FrameworkJobReport.xml'):
            if dir not in report_components.keys(): report_components[dir] = {}
            if 'fjr' not in report_components[dir].keys(): report_components[dir]['fjr'] = None
            if report_components[dir]['fjr'] != None:
                print "Found additional FrameworkJobReport.xml for",dir
            report_components[dir]['fjr'] = os.path.join(tempDirectory,dir)+'/FrameworkJobReport.xml'
        if os.path.isfile(os.path.join(tempDirectory,dir)+'/Report.pkl'):
            if dir not in report_components.keys(): report_components[dir] = {}
            if 'report' not in report_components[dir].keys(): report_components[dir]['report'] = None
            if report_components[dir]['report'] != None:
                print "Found additional Report.pkl for",dir
            report_components[dir]['report'] = os.path.join(tempDirectory,dir)+'/Report.pkl'
            
    # create final report object
    finalReport = Report.Report()

    workload = None

    # loop through reports
    for report in report_components.keys():
        # check that at least we have a Report.pkl, if not, return
        reportReport = None
        if 'report' in report_components[report].keys() and report_components[report]['report'] != None:
            reportReport = Report.Report()
            reportReport.addStep(report)
            reportReport.unpersist(report_components[report]['report'],report)
        else:
            print "report",report,'does not have a Report.pkl, skipping report'
            continue
        tmp_workload = reportReport.data.workload
        if workload == None: workload = tmp_workload
        if workload != tmp_workload:
            print 'reports have inconsistent workloads, exiting'
            sys.exit(1)

        # try to load FrameworkJobReport.xml if it exists
        fjrReport = None
        if 'fjr' in report_components[report].keys() and report_components[report]['fjr'] != None:
            fjrReport = Report.Report()
            fjrReport.addStep(report)
            fjrReport.parse(report_components[report]['fjr'],report)
        
        # prefer FrameworkJobReport.xml, otherwise use Report.pkl
        if fjrReport != None:
            finalReport.setStep(report,fjrReport.retrieveStep(report))
        elif reportReport != None:
            finalReport.setStep(report,reportReport.retrieveStep(report))
        else:
            print "something wrong, nothing added to finalReport"
            sys.exit(1)
        
    finalReport.data.workload = workload
    finalReportDictionary = finalReport.data.dictionary_whole_tree_()
    outputFileName = workload + '-' + os.path.basename(inputLogArchive).replace('.tar.gz','') + '.json'
    if outputDirectory == None:
        absoluteOutputFileName = outputFileName
    else:
        absoluteOutputFileName = os.path.join(outputDirectory,outputFileName)
    if verbose == True: print 'Output filename for FrameworkJobReport dictionary:',absoluteOutputFileName
    # safet check for file exists
    if os.path.isfile(absoluteOutputFileName) == True:
        print 'Output filename for FrameworkJobReport dictionary:',absoluteOutputFileName,'already exists, adding _01 to the name.'
        outputFileName = workload + '-' + os.path.basename(inputLogArchive).replace('.tar.gz','') + '_01.json'
        if outputDirectory == None:
            absoluteOutputFileName = outputFileName
        else:
            absoluteOutputFileName = os.path.join(outputDirectory,outputFileName)
        
    outputFile = open(absoluteOutputFileName,'w')
    json.dump(finalReportDictionary,outputFile)
    outputFile.close()
    
    # delete temporary directory
    if verbose == True: print 'Deleting temporary directory:',tempDirectory
    shutil.rmtree(tempDirectory)
    
    return 1

def extractLogArchives(inputLogCollect, outputDirectory, baseTempDirectory, verbose):
    # make temporary directory
    if baseTempDirectory == None:
        tempDirectory = tempfile.mkdtemp()
    else:
        tempDirectory = tempfile.mkdtemp('',baseTempDirectory)
    if verbose == True: print 'tempDirectory',tempDirectory
    
    # untar logCollect into tempDirectory
    logCollectTarFile = tarfile.open(inputLogCollect)
    logCollectTarFile.extractall(path=tempDirectory)
    
    counter = 0
    
    # find all logArchives
    for root, subFolders, files in os.walk(tempDirectory):
        for tmpfile in files:
            if os.path.splitext(tmpfile)[1] == '.gz':
                absoluteTmpFile = os.path.join(root,tmpfile)
                if verbose == True: print 'Found logArchive:',absoluteTmpFile
                counter += extractFJR(absoluteTmpFile, outputDirectory, baseTempDirectory, verbose)
                
    print "In the logCollectArchive:",inputLogCollect,'we extracted FrameworkJobReport dictionaries for',str(counter),'jobs.'
    
    # delete temporary directory
    if verbose == True: print 'Deleting temporary directory:',tempDirectory
    shutil.rmtree(tempDirectory)
    
    
def main():
    usage="%prog <options>"

    parser = OptionParser(usage=usage)
    parser.add_option("-c", "--logCollect", dest="logCollect", help="logCollect tarball filename containing many logArchive tarballs")
    parser.add_option("-a", "--logArchive", dest="logArchive", help="logArchive tarball")
    parser.add_option("-o", "--outputDirectory", dest="outputDirectory", help="output directory")
    parser.add_option("-v", "--verbose", dest="verbose", help="outut directory",action="store_true", default=False)
    parser.add_option("-t", "--baseTempDirectory", dest="baseTempDirectory", help="base directory for temporary files")

    (opts, args) = parser.parse_args()
    if not (opts.logArchive or opts.logCollect):
        parser.print_help()
        parser.error('Please specify logArchive or logCollect tarball filename!')
        
    if opts.logArchive != None: 
        logArchive = os.path.abspath(opts.logArchive)
    else :
        logArchive = opts.logArchive
    if opts.logCollect != None: 
        logCollect = os.path.abspath(opts.logCollect)
    else:
        logCollect = opts.logCollect
    if opts.outputDirectory != None: 
        outputDirectory = os.path.abspath(opts.outputDirectory)
    else:
        outputDirectory = os.getcwd()
    if opts.baseTempDirectory != None: 
        baseTempDirectory = os.path.abspath(opts.baseTempDirectory) + '/'
    else:
        baseTempDirectory = opts.baseTempDirectory
    verbose = opts.verbose
    
    if logArchive:
        if verbose == True: print 'handling logArchive:',logArchive, outputDirectory, baseTempDirectory, verbose
        extractFJR(logArchive, outputDirectory, baseTempDirectory, verbose)
    elif logCollect:
        if verbose == True: print 'handling logCollect:',logCollect, outputDirectory, baseTempDirectory, verbose
        extractLogArchives(logCollect, outputDirectory, baseTempDirectory, verbose)


    sys.exit(0);

if __name__ == "__main__":
    main()
    sys.exit(0);
