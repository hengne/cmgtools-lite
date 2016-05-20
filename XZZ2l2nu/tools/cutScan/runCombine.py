#!/bin/env python

#import optparse
import os
from Setup import *


#options = '-M Asymptotic --run blind '
options = '-M Asymptotic --run blind --rMax 100000'

#parser = optparse.OptionParser()
#parser.add_option("-m","--masses",dest="masses",default='limitPlot',help="Limit plot")


#tag='sig1pb'
tag='xzz2l2nu'

carddir='cards'
outdir = 'results'


masses = [
#         600,
#         800,
          1000,
#         1200,
#         1400,
#         1600,1800,
          2000,
#         2500,
#          3000,
#         3500,
#         4000,
#         4500
         ]

# for all mass points
for mass in masses:
    # loop zpt cuts
    for zptcut in zptcuts[mass]:
        # loop met cuts
        for metcut in metcuts[mass]:
            # loop mt cuts
            for mtcut in mtcuts[mass]:
                # card tag
                cardTag=tag+'_m'+str(mass)+'_'+'zptcut{:n}'.format(zptcut)+'_'+'metcut{:n}'.format(metcut)+'_'+'mtcut{:n}'.format(mtcut)
                card=carddir+'/'+cardTag+'.txt'
                #
                cmd='combine -n {cardTag} -m {mass} {options} {card}\n'.format(cardTag=cardTag, mass=mass, options=options, card=card)
                print '### Run combine for card: '+card+' ###'
                print 'command: '+cmd
                os.system(cmd)
                outfile='higgsCombine'+cardTag+'.Asymptotic.mH'+str(mass)+'.root'
                os.system('mv '+outfile+' '+outdir+'/')

            # end loop mtcuts
        # end loop metcuts
    # end loop zpt cuts
# end loop masses
      




