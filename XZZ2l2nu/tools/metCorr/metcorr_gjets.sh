#!/bin/sh

#inputs
#inputdir=/data2/XZZ2/80X_20170202_GJets_light_hlt
#outputdir=/home/heli/XZZ/80X_20170202_GJets_light_hlt_RcSkim
#outputdir=/home/heli/XZZ/80X_20170202_GJets_light_hlt_allcorV2Skim
#outputdir=/home/heli/XZZ/80X_20170202_GJets_light_hlt_Skim
inputdir=/home/heli/XZZ/80X_20170202_GJets_light
outputdir=/home/heli/XZZ/80X_20170202_GJets_light_Skim
config=config/parameters_light_gjets

mkdir -p ${outputdir}

gmake all

njob="0"

#for infile in $inputdir/GJet_Pt_20toInf_DoubleEMEnriched/vvTreeProducer/tree.root ; 
#for infile in $inputdir/GJet_Pt_*/vvTreeProducer/tree.root ; 
#for infile in $inputdir/ZNuNuGJets*/vvTreeProducer/tree.root ; 
#for infile in $inputdir/GJets_HT40to*/vvTreeProducer/tree.root ; 
#for infile in $inputdir/WJetsToLNu_HT*_BIG/vvTreeProducer/tree.root ; 
#for infile in $inputdir/QCD_*/vvTreeProducer/tree.root ; 
#for infile in $inputdir/SinglePhoton_Run2016B2H_ReReco_36p22fbinv/vvTreeProducer/tree.root ; 
#for infile in $inputdir/WGToLNuG/vvTreeProducer/tree.root ; 
#for infile in $(ls $inputdir/*/vvTreeProducer/tree.root | grep -v "/GJet" | grep -v "/QCD" | grep -v "/SinglePhoton" ); 
#for infile in $(ls $inputdir/*/vvTreeProducer/tree.root | grep -v SinglePhoton ); 
#for infile in $inputdir/SinglePhoton_Run2016B2H_ReReco_36p46/vvTreeProducer/tree.root ; 
#for infile in $inputdir/GJets_HT*/vvTreeProducer/tree.root ; 
#for infile in $inputdir/QCD_HT*/vvTreeProducer/tree.root ; 
#for infile in $inputdir/GJet_Pt_40toInf_DoubleEMEnriched/vvTreeProducer/tree.root ; 
#for infile in $(ls $inputdir/*/vvTreeProducer/tree.root | grep -v SinglePhoton | grep -v GJet_Pt_ ); 
#for infile in $(ls $inputdir/*/vvTreeProducer/tree.root | grep  SinglePhoton_Run2016Full ); 
#for infile in $(ls $inputdir/*/vvTreeProducer/tree.root | grep -v  SinglePhoton_Run2016Full ); 
#for infile in $(ls $inputdir/*/vvTreeProducer/tree.root  ); 
#for infile in $(ls $inputdir/*/vvTreeProducer/tree.root | grep -v  Single | grep -v halo15 | grep -v "/GJets_HT" | grep -v "/QCD_Pt" ); 
#for infile in $(ls $inputdir/*/vvTreeProducer/tree.root | grep "SinglePhoton_Run2016Full" | grep -v halo15 ); 
#for infile in $(ls $inputdir/*/vvTreeProducer/tree.root | grep DYJetsToLL_M50_Ext  ); 
#for infile in $(ls $inputdir/*/vvTreeProducer/tree.root | grep -v SinglePhoton_Run2016Full_03Feb2017  ); 
#for infile in $(ls $inputdir/*/vvTreeProducer/tree.root | grep  SinglePhoton_Run2016Full_03Feb2017  ); 
#for infile in $(ls $inputdir/*/vvTreeProducer/tree.root | grep  SinglePhoton_Run2016Full_03Feb2017_uncorr  ); 
#for infile in $(ls $inputdir/*/vvTreeProducer/tree.root | grep  SinglePhoton_Run2016Full_03Feb2017_allcor  ); 
#for infile in $inputdir/SinglePhoton_Run2016Full_ReReco_v2/vvTreeProducer/tree.root ;
#for infile in $inputdir/T_tWch/vvTreeProducer/tree.root ;
#for infile in $inputdir/TBar_tWch/vvTreeProducer/tree.root ;
#for infile in $inputdir/SinglePhoton_Run2016Full_ReReco_v2_RePreSkim/vvTreeProducer/tree.root ;
#for infile in $(ls $inputdir/*/vvTreeProducer/tree.root | grep -v  Single  ); 
for infile in $inputdir/SinglePhoton_Run2016Full_03Feb2017_allcorV2/vvTreeProducer/tree.root ;
do
  echo "+++ skimming $infile +++"
  outfile="${outputdir}/${infile/$inputdir\//}"

  # options for outputs
  outfile="${outfile/\/vvTreeProducer\/tree/}"
  #outfile="${outfile/\/vvTreeProducer\/tree/_ZMassFineBin}"
  #outfile="${outfile/\/vvTreeProducer\/tree/_ZMassFineBinSmooth}"
  #outfile="${outfile/\/vvTreeProducer\/tree/_ZMassFineBinGraphSmooth}"
  #outfile="${outfile/\/vvTreeProducer\/tree/_ZMassGraphSmooth}"
  #outfile="${outfile/\/vvTreeProducer\/tree/_RcNoSmooth}"
  #outfile="${outfile/\/vvTreeProducer\/tree/_NoRecoil}"
  #outfile="${outfile/\/vvTreeProducer\/tree/_test}"
  #outfile="${outfile/\/vvTreeProducer\/tree/_ReSkim}"
  #outfile="${outfile/\/vvTreeProducer\/tree/_RePreSkim}"

  inSkimFile=${infile/vvTreeProducer\/tree.root/skimAnalyzerCount\/SkimReport.txt}

  #echo $inSkimFile
  AllEvents=`grep "All Events" ${inSkimFile} | awk {'print $3'}`
  SumWeights=`grep "Sum Weights" ${inSkimFile} | awk {'print $3'}`

  if [ -z $AllEvents ]; then
    echo Fail to get All Events from file ${inSkimFile}
    continue
  fi
  if [ -z $SumWeights ]; then
    SumWeights=$AllEvents
  fi

  echo -- Input file: $infile
  echo -- Output file: $outfile
  echo -- AllEvents: $AllEvents , SumWeights: $SumWeights
  echo -- Selection: $selection
  echo -- Command: ./bin/metcorr.exe $config $infile $outfile $AllEvents $SumWeights

  ./bin/metcorr.exe $config $infile $outfile $AllEvents $SumWeights &> ${outfile}.skim.log &

  njob=$(( njob + 1 ))
  if [ "$njob" -eq "100" ]; then
   # wait
    njob="0"
  fi

done

