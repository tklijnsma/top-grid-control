#!/usr/bin/env python
"""
Thomas:

"""

########################################
# Imports
########################################

import os
import shutil
import re

########################################
# Main
########################################

def main():

    workdir = 'work.gctop'

    jobdirs = os.listdir( '{0}/output/'.format(workdir) )

    outdir = 'sigma-result'
    if not os.path.isdir(outdir): os.makedirs(outdir)

    for jobdir in jobdirs:

        jobdir = workdir + '/output/' + jobdir

        with open('{0}/top++.cfg'.format(jobdir), 'r') as f:
            raw_cfg = f.read()

        match = re.search( r'PDFset\s(.*)\s', raw_cfg )
        PDFset = match.group(1).strip()

        match = re.search( r'Collider\s(.*)\s', raw_cfg )
        Collider = match.group(1).strip()

        match = re.search( r'ECMLHC\s(.*)\s', raw_cfg )
        ECMLHC = match.group(1).strip()

        match = re.search( r'OrderFO\s(.*)\s', raw_cfg )
        OrderFO = match.group(1).strip()
        
        match = re.search( r'OrderRES\s(.*)\s', raw_cfg )
        OrderRES = match.group(1).strip()

        outname = '{0}{1}-{2}+{3}-{4}'.format(
            Collider, ECMLHC, OrderFO, OrderRES, PDFset )

        shutil.copy2( '{0}/top++.log'.format(jobdir),
                      '{0}/{1}.log'.format(outdir, outname) )

        shutil.copy2( '{0}/top++.res'.format(jobdir),
                      '{0}/{1}.res'.format(outdir, outname) )

        shutil.copy2( '{0}/top++.cfg'.format(jobdir),
                      '{0}/{1}.cfg'.format(outdir, outname) )



########################################
# End of Main
########################################
if __name__ == "__main__":
    main()
