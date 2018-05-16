
indir=$1
mX=$2
cut=$3

cp $1/mX${mX}* .

combineCards.py ee_SR=mX${mX}ZZ2l2nu_ee_${cut}.txt mm_SR=mX${mX}ZZ2l2nu_mm_${cut}.txt > mX${mX}ZZ2l2nu_${cut}.txt

#combine -M MaxLikelihoodFit --saveNormalizations --saveShapes --saveWithUncertainties -m ${mX} mX${mX}ZZ2l2nu_SR.txt -t -1 --expectSignal 0
#mv mlfit.root mlfit_b-only_met.root

#combine -M MaxLikelihoodFit --saveNormalizations --saveShapes --saveWithUncertainties -m ${mX} mX${mX}ZZ2l2nu_SR.txt -t -1 --expectSignal 0
#mv mlfit.root mlfit_b-only.root
#combine -M MaxLikelihoodFit --saveNormalizations --saveShapes --saveWithUncertainties -m ${mX} mX${mX}ZZ2l2nu_SR.txt -t -1 --expectSignal 0.5
#mv mlfit.root mlfit_s+b.root


combine -M MaxLikelihoodFit --minimizerTolerance 0.001 --preFitValue 0.001 \
--saveOverallShapes \
--saveNormalizations --saveShapes --saveWithUncertainties -m ${mX} mX${mX}ZZ2l2nu_${cut}.txt 
mv mlfit.root mlfit_obs_$mX.root


#combine -M MaxLikelihoodFit --minimizerTolerance 0.001 --preFitValue 0.001 \
#--saveOverallShapes \
#--saveNormalizations --saveShapes --saveWithUncertainties -m ${mX} ${ee_SR}
#mv mlfit.root mlfit_obs_ee.root

#combine -m ${mX} -M Asymptotic mX${mX}ZZ2l2nu_SR.txt --rMax 10 --noFitAsimov  --saveWorkspace 

