##########################################################
##      configuration for XZZ2l2nu 
##########################################################

import CMGTools.XZZ2l2nu.fwlite.Config as cfg
from CMGTools.XZZ2l2nu.fwlite.Config import printComps
from CMGTools.XZZ2l2nu.RootTools import *
from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption


#Load all common analyzers
from CMGTools.XZZ2l2nu.analyzers.coreXZZ_cff import *

#-------- SAMPLES AND TRIGGERS -----------
from CMGTools.XZZ2l2nu.samples.loadSamples76x import *
selectedComponents = mcSamples+dataSamples

triggerFlagsAna.triggerBits ={
    "ISOMU":triggers_1mu_iso,
    "MU":triggers_1mu_noniso,
    "ISOELE":triggers_1e,
    "ELE":triggers_1e_noniso,
    "HT800":triggers_HT800,
    "HT900":triggers_HT900,
    "JJ":triggers_dijet_fat,
    "MET90":triggers_met90_mht90+triggers_metNoMu90_mhtNoMu90,
    "MET120":triggers_metNoMu120_mhtNoMu120
}

#-------- Analyzer
from CMGTools.XZZ2l2nu.analyzers.treeXZZ_cff import *

lepAna.electronIDVersion = 'HEEPv6' # can be looseID or HEEPv6
lepAna.electronIsoVersion = 'miniISO' # can be pfISO or miniISO
lepAna.do_filter=False

jetAna.smearJets=True
#metAna.old74XMiniAODs = True

#-------- SEQUENCE
#sequence = cfg.Sequence(coreSequence+[vvSkimmer,vvTreeProducer])

coreSequence = [
    skimAnalyzer,
    genAna,
    jsonAna,
#    triggerAna,
    pileUpAna,
    vertexAna,
    lepAna,
    jetAna,
    metAna,
#    leptonicVAna,
#    multiStateAna,
    triggerFlagsAna,
]
    
#sequence = cfg.Sequence(coreSequence)
#sequence = cfg.Sequence(coreSequence+[vvSkimmer,vvTreeProducer])
sequence = cfg.Sequence(coreSequence+[jetTreeProducer])
 

#-------- HOW TO RUN
test = 1
if test==1:
    # test a single component, using a single thread.
    selectedComponents = [JERCRef_MC_eos]
    for c in selectedComponents:
        for i in c.files:
            if ROOT.TString(i).Contains("02837459-03C2-E511-8EA2-002590A887AC.root"):
                c.files=i
                print c.files
        #c.files = c.files[0]
        #c.splitFactor = (len(c.files)/10 if len(c.files)>10 else 1)
        c.splitFactor = 1
        #c.triggers=triggers_1mu_noniso
        #c.triggers=triggers_1e_noniso

## output histogram
outputService=[]
from PhysicsTools.HeppyCore.framework.services.tfile import TFileService
output_service = cfg.Service(
    TFileService,
    'outputfile',
    name="outputfile",
    fname='vvTreeProducer/tree.root',
    option='recreate'
    )
outputService.append(output_service)

from PhysicsTools.HeppyCore.framework.eventsfwlite import Events
from CMGTools.TTHAnalysis.tools.EOSEventsWithDownload import EOSEventsWithDownload
event_class = EOSEventsWithDownload
event_class = Events
if getHeppyOption("nofetch"):
    event_class = Events
config = cfg.Config( components = selectedComponents,
                     sequence = sequence,
                     services = [],
                     events_class = event_class)




