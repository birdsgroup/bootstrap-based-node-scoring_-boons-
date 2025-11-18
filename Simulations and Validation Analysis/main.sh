#!/bin/bash
#$ -cwd
#$ -o outputfile.txt
#$ -e errorfile.txt


echo "Simulated Dataset"
echo "Graphs"
python SIM_graphs.py
echo "Validation"
python SIM_validation.py
echo "Replication"
python SIM_replication.py

time python SIM_pog_vals_1.py
time python SIM_pog_vals_2.py

echo "Semi-Simulated Dataset"
for tissue in "Muscle_Skeletal" "Whole_Blood" "Skin_Sun_Exposed_Lower_leg" "Thyroid" "Lung";
do
	mkdir "Semi-Simulated Data/$tissue"
	for s in 73 237;
	do
		echo $tissue $s
		time python RW_validation.py $tissue "degree" $s
		time python RW_validation.py $tissue "pagerank" $s
	done
done
