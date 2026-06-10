import FWCore.ParameterSet.Config as cms


from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunesRun3ECM13p6TeV.PythiaCP5Settings_cfi import *
from Configuration.Generator.PSweightsPythia.PythiaPSweightsSettings_cfi import *


generator = cms.EDFilter(
    "Pythia8GeneratorFilter",
    maxEventsToPrint=cms.untracked.int32(1),
    pythiaPylistVerbosity=cms.untracked.int32(1),
    filterEfficiency=cms.untracked.double(1.0),
    pythiaHepMCVerbosity=cms.untracked.bool(False),
    comEnergy=cms.double(13600.0),
    RandomizedParameters=cms.VPSet(),
)


grid_points = [
    {
        "gridpack_path": "/eos/cms/store/group/phys_susy/sus-23-008/run3_2HDMa_typeII_bbdm_gridpacks_LHAID325300/bbDM_2HDMa_MH3_600_MH4_10_Mchi_1_el8_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz",
        "name": "MH3_600_MH4_10_Mchi_1",
        "weight": 0.03448275862,
    },
    {
        "gridpack_path": "/eos/cms/store/group/phys_susy/sus-23-008/run3_2HDMa_typeII_bbdm_gridpacks_LHAID325300/bbDM_2HDMa_MH3_600_MH4_50_Mchi_1_el8_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz",
        "name": "MH3_600_MH4_50_Mchi_1",
        "weight": 0.03448275862,
    },
    {
        "gridpack_path": "/eos/cms/store/group/phys_susy/sus-23-008/run3_2HDMa_typeII_bbdm_gridpacks_LHAID325300/bbDM_2HDMa_MH3_600_MH4_100_Mchi_1_el8_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz",
        "name": "MH3_600_MH4_100_Mchi_1",
        "weight": 0.03448275862,
    },
    {
        "gridpack_path": "/eos/cms/store/group/phys_susy/sus-23-008/run3_2HDMa_typeII_bbdm_gridpacks_LHAID325300/bbDM_2HDMa_MH3_600_MH4_150_Mchi_1_el8_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz",
        "name": "MH3_600_MH4_150_Mchi_1",
        "weight": 0.03448275862,
    },
    {
        "gridpack_path": "/eos/cms/store/group/phys_susy/sus-23-008/run3_2HDMa_typeII_bbdm_gridpacks_LHAID325300/bbDM_2HDMa_MH3_600_MH4_200_Mchi_1_el8_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz",
        "name": "MH3_600_MH4_200_Mchi_1",
        "weight": 0.03448275862,
    },
    {
        "gridpack_path": "/eos/cms/store/group/phys_susy/sus-23-008/run3_2HDMa_typeII_bbdm_gridpacks_LHAID325300/bbDM_2HDMa_MH3_600_MH4_250_Mchi_1_el8_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz",
        "name": "MH3_600_MH4_250_Mchi_1",
        "weight": 0.03448275862,
    },
    {
        "gridpack_path": "/eos/cms/store/group/phys_susy/sus-23-008/run3_2HDMa_typeII_bbdm_gridpacks_LHAID325300/bbDM_2HDMa_MH3_600_MH4_300_Mchi_1_el8_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz",
        "name": "MH3_600_MH4_300_Mchi_1",
        "weight": 0.03448275862,
    },
    {
        "gridpack_path": "/eos/cms/store/group/phys_susy/sus-23-008/run3_2HDMa_typeII_bbdm_gridpacks_LHAID325300/bbDM_2HDMa_MH3_600_MH4_350_Mchi_1_el8_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz",
        "name": "MH3_600_MH4_350_Mchi_1",
        "weight": 0.03448275862,
    },
    {
        "gridpack_path": "/eos/cms/store/group/phys_susy/sus-23-008/run3_2HDMa_typeII_bbdm_gridpacks_LHAID325300/bbDM_2HDMa_MH3_600_MH4_400_Mchi_1_el8_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz",
        "name": "MH3_600_MH4_400_Mchi_1",
        "weight": 0.03448275862,
    },
    {
        "gridpack_path": "/eos/cms/store/group/phys_susy/sus-23-008/run3_2HDMa_typeII_bbdm_gridpacks_LHAID325300/bbDM_2HDMa_MH3_600_MH4_450_Mchi_1_el8_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz",
        "name": "MH3_600_MH4_450_Mchi_1",
        "weight": 0.03448275862,
    },
    {
        "gridpack_path": "/eos/cms/store/group/phys_susy/sus-23-008/run3_2HDMa_typeII_bbdm_gridpacks_LHAID325300/bbDM_2HDMa_MH3_600_MH4_500_Mchi_1_el8_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz",
        "name": "MH3_600_MH4_500_Mchi_1",
        "weight": 0.03448275862,
    },
    {
        "gridpack_path": "/eos/cms/store/group/phys_susy/sus-23-008/run3_2HDMa_typeII_bbdm_gridpacks_LHAID325300/bbDM_2HDMa_MH3_1500_MH4_10_Mchi_1_el8_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz",
        "name": "MH3_1500_MH4_10_Mchi_1",
        "weight": 0.03448275862,
    },
    {
        "gridpack_path": "/eos/cms/store/group/phys_susy/sus-23-008/run3_2HDMa_typeII_bbdm_gridpacks_LHAID325300/bbDM_2HDMa_MH3_1500_MH4_50_Mchi_1_el8_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz",
        "name": "MH3_1500_MH4_50_Mchi_1",
        "weight": 0.03448275862,
    },
    {
        "gridpack_path": "/eos/cms/store/group/phys_susy/sus-23-008/run3_2HDMa_typeII_bbdm_gridpacks_LHAID325300/bbDM_2HDMa_MH3_1500_MH4_100_Mchi_1_el8_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz",
        "name": "MH3_1500_MH4_100_Mchi_1",
        "weight": 0.03448275862,
    },
    {
        "gridpack_path": "/eos/cms/store/group/phys_susy/sus-23-008/run3_2HDMa_typeII_bbdm_gridpacks_LHAID325300/bbDM_2HDMa_MH3_1500_MH4_150_Mchi_1_el8_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz",
        "name": "MH3_1500_MH4_150_Mchi_1",
        "weight": 0.03448275862,
    },
    {
        "gridpack_path": "/eos/cms/store/group/phys_susy/sus-23-008/run3_2HDMa_typeII_bbdm_gridpacks_LHAID325300/bbDM_2HDMa_MH3_1500_MH4_200_Mchi_1_el8_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz",
        "name": "MH3_1500_MH4_200_Mchi_1",
        "weight": 0.03448275862,
    },
    {
        "gridpack_path": "/eos/cms/store/group/phys_susy/sus-23-008/run3_2HDMa_typeII_bbdm_gridpacks_LHAID325300/bbDM_2HDMa_MH3_1500_MH4_250_Mchi_1_el8_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz",
        "name": "MH3_1500_MH4_250_Mchi_1",
        "weight": 0.03448275862,
    },
    {
        "gridpack_path": "/eos/cms/store/group/phys_susy/sus-23-008/run3_2HDMa_typeII_bbdm_gridpacks_LHAID325300/bbDM_2HDMa_MH3_1500_MH4_300_Mchi_1_el8_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz",
        "name": "MH3_1500_MH4_300_Mchi_1",
        "weight": 0.03448275862,
    },
    {
        "gridpack_path": "/eos/cms/store/group/phys_susy/sus-23-008/run3_2HDMa_typeII_bbdm_gridpacks_LHAID325300/bbDM_2HDMa_MH3_1500_MH4_350_Mchi_1_el8_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz",
        "name": "MH3_1500_MH4_350_Mchi_1",
        "weight": 0.03448275862,
    },
    {
        "gridpack_path": "/eos/cms/store/group/phys_susy/sus-23-008/run3_2HDMa_typeII_bbdm_gridpacks_LHAID325300/bbDM_2HDMa_MH3_1500_MH4_400_Mchi_1_el8_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz",
        "name": "MH3_1500_MH4_400_Mchi_1",
        "weight": 0.03448275862,
    },
    {
        "gridpack_path": "/eos/cms/store/group/phys_susy/sus-23-008/run3_2HDMa_typeII_bbdm_gridpacks_LHAID325300/bbDM_2HDMa_MH3_1500_MH4_450_Mchi_1_el8_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz",
        "name": "MH3_1500_MH4_450_Mchi_1",
        "weight": 0.03448275862,
    },
    {
        "gridpack_path": "/eos/cms/store/group/phys_susy/sus-23-008/run3_2HDMa_typeII_bbdm_gridpacks_LHAID325300/bbDM_2HDMa_MH3_1500_MH4_500_Mchi_1_el8_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz",
        "name": "MH3_1500_MH4_500_Mchi_1",
        "weight": 0.03448275862,
    },
    {
        "gridpack_path": "/eos/cms/store/group/phys_susy/sus-23-008/run3_2HDMa_typeII_bbdm_gridpacks_LHAID325300/bbDM_2HDMa_MH3_1500_MH4_600_Mchi_1_el8_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz",
        "name": "MH3_1500_MH4_600_Mchi_1",
        "weight": 0.03448275862,
    },
    {
        "gridpack_path": "/eos/cms/store/group/phys_susy/sus-23-008/run3_2HDMa_typeII_bbdm_gridpacks_LHAID325300/bbDM_2HDMa_MH3_1500_MH4_700_Mchi_1_el8_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz",
        "name": "MH3_1500_MH4_700_Mchi_1",
        "weight": 0.03448275862,
    },
    {
        "gridpack_path": "/eos/cms/store/group/phys_susy/sus-23-008/run3_2HDMa_typeII_bbdm_gridpacks_LHAID325300/bbDM_2HDMa_MH3_1500_MH4_850_Mchi_1_el8_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz",
        "name": "MH3_1500_MH4_850_Mchi_1",
        "weight": 0.03448275862,
    },
    {
        "gridpack_path": "/eos/cms/store/group/phys_susy/sus-23-008/run3_2HDMa_typeII_bbdm_gridpacks_LHAID325300/bbDM_2HDMa_MH3_1500_MH4_1000_Mchi_1_el8_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz",
        "name": "MH3_1500_MH4_1000_Mchi_1",
        "weight": 0.03448275862,
    },
    {
        "gridpack_path": "/eos/cms/store/group/phys_susy/sus-23-008/run3_2HDMa_typeII_bbdm_gridpacks_LHAID325300/bbDM_2HDMa_MH3_1500_MH4_1150_Mchi_1_el8_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz",
        "name": "MH3_1500_MH4_1150_Mchi_1",
        "weight": 0.03448275862,
    },
    {
        "gridpack_path": "/eos/cms/store/group/phys_susy/sus-23-008/run3_2HDMa_typeII_bbdm_gridpacks_LHAID325300/bbDM_2HDMa_MH3_1500_MH4_1300_Mchi_1_el8_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz",
        "name": "MH3_1500_MH4_1300_Mchi_1",
        "weight": 0.03448275862,
    },
    {
        "gridpack_path": "/eos/cms/store/group/phys_susy/sus-23-008/run3_2HDMa_typeII_bbdm_gridpacks_LHAID325300/bbDM_2HDMa_MH3_1500_MH4_1450_Mchi_1_el8_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz",
        "name": "MH3_1500_MH4_1450_Mchi_1",
        "weight": 0.03448275862,
    },
]

for grid_point in grid_points:
    basePythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        pythia8PSweightsSettingsBlock,
        parameterSets=cms.vstring(
            "pythia8CommonSettings",
            "pythia8CP5Settings",
            "pythia8PSweightsSettings",
        ),
    )

    generator.RandomizedParameters.append(
        cms.PSet(
            ConfigWeight=cms.double(grid_point["weight"]),
            ConfigDescription=cms.string(grid_point["name"]),
            PythiaParameters=basePythiaParameters,
            GridpackPath=cms.string(grid_point["gridpack_path"]),
        )
    )

ProductionFilterSequence = cms.Sequence(generator)
