import FWCore.ParameterSet.Config as cms

#Link to datacards:
#https://github.com/cms-sw/genproductions/tree/master/bin/MadGraph5_aMCatNLO/cards/production/2017/13TeV/BulkGraviton_hh_granular
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *
from Configuration.Generator.PSweightsPythia.PythiaPSweightsSettings_cfi import *

generator = cms.EDFilter("Pythia8GeneratorFilter",
    maxEventsToPrint = cms.untracked.int32(1),
    pythiaPylistVerbosity = cms.untracked.int32(1),
    filterEfficiency = cms.untracked.double(1.0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    comEnergy = cms.double(13000.),
    RandomizedParameters = cms.VPSet(),
)

import numpy as np
m_higgs = np.arange(95, 180, 1)
# print(mpoints)

for mh in m_higgs:
    # print('BulkGravitonToHH_MX%.0f_MH%.0f' % (mx, mh))
    generator.RandomizedParameters.append(
        cms.PSet(
            ConfigWeight = cms.double(1),
            # what gridpack to use
            GridpackPath =  cms.string('instMG://GluGluHToZG_ZToLL_TuneCP5_13TeV_madgraphMLM_pythia8/MG5_aMC_v2.6.5/%.0f' % (mh)),
            ConfigDescription = cms.string('GluGluHToZG_ZToLL_M%.0f_TuneCP5_13TeV_madgraphMLM_pythia8' % (mh)),
            PythiaParameters = cms.PSet(
                pythia8CommonSettingsBlock,
                pythia8CP5SettingsBlock,
                pythia8PSweightsSettingsBlock,
                # how to translate powerheg parameters to madgraph ones(Done)
                processParameters = cms.vstring(
                    'JetMatching:setMad = off',
                    'JetMatching:scheme = 1',
                    'JetMatching:merge = on',
                    'JetMatching:jetAlgorithm = 2',
                    'JetMatching:etaJetMax = 999.',
                    'JetMatching:coneRadius = 1.',
                    'JetMatching:slowJetPower = 1',
                    'JetMatching:qCut = 15.', #this is the actual merging scale
                    'JetMatching:nQmatch = 4', #4 corresponds to 4-flavour scheme (no matching of b-quarks), 5 for 5-flavour scheme
                    'JetMatching:nJetMax = 1', #number of partons in born matrix element for highest multiplicity
                    'JetMatching:doShowerKt = off', #off for MLM matching, turn on for shower-kT matching
                ),
                parameterSets = cms.vstring('pythia8CommonSettings',
                                            'pythia8CP5Settings',
                                            'pythia8PSweightsSettings'
		        )
            )
        )
    )