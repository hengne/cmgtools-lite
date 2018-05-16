#!/bin/sh


outdir=dt3mualc${1}
#config=run_xzz2l2nu_80x_cfg_loose_dt_${2}.py
config=run_xzz2l2nu_80x_cfg_loose_dt_allclean_mu${1}.py
#config=run_xzz2l2nu_80x_cfg_photon_dt_${2}.py
#config=run_xzz2l2nu_80x_cfg_photon_dt_allclean_${1}.py
otherfiles=" pogRecipes.py "

heppy_batch.py -o ${outdir} ${config}  -b 'bsub -q sssss < ./batchScript.sh' -n
for dd in ${outdir}/* ;
do cp $otherfiles ${dd}/;
done

cd $outdir
heppy_check.py * -b "bsub -q 1nd"

cd ../

