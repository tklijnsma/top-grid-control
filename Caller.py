#!/usr/bin/env python
"""
Thomas:

"""

########################################
# Imports
########################################

import subprocess
import os
import shutil
import re
import gzip
#from CreateStatisticsReport import Create_Single_sig_Report
from time import sleep
import time
import datetime


########################################
# Functions
########################################

def Create_Error_Report( workdir ):

    n_specific_prints = 0

    dirs = os.listdir( '{0}/output/'.format(workdir) )

    out_f = open( 'Errors.txt' , 'w' )

    for jobdir in dirs:

        stdout_filename = 'work.{0}/output/{1}/job.stderr.gz'.format(workdir,jobdir)

        if not os.path.isfile( stdout_filename ):
            continue

        out_f.write( '\nERROR IN {0}\n=================\n'.format(jobdir) )

        f = gzip.open(stdout_filename, 'rb')
        out_f.write( f.read() )
        f.close()

    out_f.close()


########################################
# Main
########################################

def main():

    start_time = time.time()

    gopy = 'grid-control/go.py'
    conf = 'gctop.conf'
    workdir = 'work.gctop'

    submitcmd   = [ gopy , conf, '-q' ]
    statuscmd   = [ gopy , conf, '-qs' ]
    retrievecmd   = [ gopy , conf, '-r' ]


    # Delete currently existing jobs
    subprocess.call( [ 'qdel', '-u', 'tklijnsm' ] )

    # Remove work.*
    if os.path.isdir(workdir):
        print 'Removing {0}'.format(workdir)
        shutil.rmtree(workdir)

    # Submit jobs
    print 'Submitting jobs'
    #subprocess.call( submitcmd , stdout=open(os.devnull, 'wb') )
    subprocess.call( submitcmd )


    # Check status repeatedly - detect 100% success rate to stop repeating
    n_limit_checks = 450

    for i_check in range(n_limit_checks):

        print 'Checking status (call {0})'.format( i_check )

        subprocess.call( statuscmd, stdout=open(os.devnull, 'wb'))

        output = subprocess.Popen(
            retrievecmd, stdout=subprocess.PIPE ).communicate()[0]

        match = re.search( r'FAILED:\s*\d+\s*(\d+)', output )
        if int(match.group(1)) > 0:
            print 'There was a failed job. '\
                'See error report in Errors.txt'
            Create_Error_Report(workdir)
            return 0
        
        match = re.search( r'SUCCESS:\s*(\d+)\s*(\d+)', output )
        n_success = match.group(1)
        p_success = int(match.group(2))

        match = re.search( r'RUNNING:\s*(\d+)\s*(\d+)', output )
        n_running = match.group(1)

        match = re.search( r'QUEUED:\s*(\d+)\s*(\d+)', output )
        n_queued = match.group(1)

        print '    Running: {0:4s} , Queued: {1:4s} , Finished: {2:4s}'.format(
            n_running, n_queued, n_success )

        if p_success == 100: break
        else: sleep(30)



    end_time = time.time()
    start_time_str = datetime.datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')
    end_time_str = datetime.datetime.fromtimestamp(end_time).strftime('%Y-%m-%d %H:%M:%S')
    print 'Started run on: {0}'.format( start_time_str )
    print 'Ended run on:   {0}'.format( end_time_str )
    print 'Duration:       {0} seconds'.format( end_time - start_time )


########################################
# End of Main
########################################
if __name__ == "__main__":
    main()
