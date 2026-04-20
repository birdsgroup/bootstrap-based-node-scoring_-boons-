# BOOtstrap-based Node Scores (BOONS)

This repository contains scripts for implementation of the systematic workflow to generate uncertainty-aware gene rankings for downstream network (degree and PageRank centrality) measures, and their analyses.

## Overview of the Project

This project develops a systematic workflow that estimates and propagates uncertainty about the coexpression network to degree and PageRank centrality and produces robust (uncertainty-aware) gene rankings. 
The workflow uses ‘*bootstrapping*’ to generate multiple measures for the centrality – mean $(\mu)$ and variance $(\sigma^2)$ of which were used to propose different uncertainty-aware gene rankings (BCMs) of the form $\mu-c\sigma$.

The project is implemented using the following programming languages: 

-  *Functions for computations and analyses*: Python versions 3.10 and 3.12. 
   Packages like `numpy, pandas, scipy, random, corals.correlation` and `statsmodel` have been used repeatedly.
-  *Covariate adjustment of the gene expression data and GSEA analysis using WebGestalt*: R versions 4.2 and 4.4
   The WebGestalt package for R `WebGestaltR` has been used primarily.
-  *Workflows combining several scripts*: Bourne Again SHell (BASH) scripting language

Note: Some of the codes have been designed to run parallelly on a server with $50$ cores, however this is only done in the BASH scripts and can be easily modified to run sequentially on a local system.

### Getting Started

This section will help you set up the project for the first time — from cloning the repository to running a complete example. 
Follow each step in order.

1. **Clone/download the project from GitHub to your local machine.**

   ```bash
   git clone https://github.com/yourusername/yourproject.git
   cd yourproject
   ```

2. **Prepare input data.** 

   1. Create a new folder with the name of your tissue (e.g., `Tissue`) in `Original Dataset/Preprocessed Files`.
   2. Place your preprocessed gene expression data in `Original Dataset/Preprocessed Files/Tissue`.
      The required format is:
      -  Rows = genes with the first column containing the gene id’s
      -  Columns = samples with the first row containing the sample id’s
      -  Values = preprocessed gene expression values
      -  File name = `Tissue.csv`
   3. Place your genes file `genes.csv` containing the details of the genes in the same order as in `Tissue.csv` in the same location i.e., `Original Dataset/Preprocessed Files/Tissue/genes.csv`. 
      If you don’t have information on the genes, then please copy the gene id’s from the 1^st^ column of `Tissue.csv` into `genes.csv`.

3. **Bootstrapping and Computing the centrality measures for all the coexpression networks.**

   1. Use any text editor to open `Centrality Computation/run.sh`

   2. Modify the `tissues` variable with your tissue name.
      For example, if you are doing this step for the tissues `Tissue1` and `Tissue_2`, then modify the `tissues` variable as: `tissues=("Tissue1" "Tissue_2")`.

   3. Update `B` with the number of bootstrapped coexpression networks you want to compute.
      For example, if you want to compute $10$ bootstrapped coexpression networks, then modify the variable `B` as: `B=10`

   4. Run the file from terminal as:

      ```bash
      cd Centrality\ Computation
      ./run.sh
      ```

   5. The program runs on $50$ cores, however, if you want to reduce the number of cores, then use any text editor to open `Centrality Computation/main.sh` and update the `cores` variable with the number of cores you want to use.

      -  **Important Note:** Please ensure the number of cores (`cores`) you are using is a factor of the number of bootstrapped coexpression networks (`B`) you are computing.

4. **Computation of the metric values.**

   1. [Optional] Use any text editor to open `Validation Analysis/gene ordering.py` to generate a random ordering of the genes and modify as given below.

   2. Use any text editor to open `Validation Analysis/rankings.py`
   
   3. Modify the `Tissues` variable with your tissue name.
      For example, if you are doing this step for the tissues `Tissue1` and `Tissue_2` with sample sizes `s1` and `s2`, then modify the `Tissues` variable as: `Tissues = {"Tissue1": s1, "Tissue_2":s2}`.
   
   4. Modify the `centrality` variable with the centrality for which you want to compute the metric values.
      For example, if you are want to compute the values by the metrics for `degree` centrality, then set `centrality = 'degree'`.

      -  **Important Note:** In the current version, only `degree` or `pagerank` are the allowed options.

   5. You can either run the file using your own python environments/compilers, or from the terminal as:
   
      ```bash
      cd ..\Validation\ Analysis
      python "gene ordering.py"
      python "rankings.py"
      ```
   
   6. The program will create `Rankings/ranks_<centrality>.xlsx`, and  all your outputs will be stored in the file.

### Repository Structure

Each folder contains the scripts and results for the same analyses. The codes have been implemented such that the functions will read the files from the corresponding directory structure directly, so that manual duplication of the output files will not be necessary. Hence, we suggest to maintain the same directory structure to run the codes without any hassle. 

<details>
<summary> Click here to view the overall directory structure. </summary>

```python
+---Bias	# Scripts to estimate the Estimator and Bootstrap Bias

+---Centrality Computation # scripts to generate centrality values. 
	'''
	For each tissue T, a folder is generated containing 7 files. 
	Directory structure of the same is given below as an example.
	/---T
	|	error.txt 	# errors during the running of the code.
	|	original_degree.csv # the degree cetrality of the genes (in the same order as in the 'genes.csv' file) by obs.
	|	original_pagerank.csv # the PageRank cetrality of the genes (in the same order as in the 'genes.csv' file) by obs.
	|	output.txt # outputs (if any) pertaining to the computation of centrality for the same tissue.
	|	sample_degree.csv # the degree centrality values of the genes (in the same order as in the 'gnes.csv' file) in each bootstrapped coexpression network.
    |	sample_pagerank.csv # the PageRank centrality values of the genes (in the same order as in the 'genes.csv' file) in each bootstrapped coexpression network.
    |	seed.txt # the seed used to perform bootstrapping on the same tissue (necessary to replicate the results exactly).
	'''

+---Gene Ordering # scripts to generate a random order of the genes
	# For each tissue, a csv file <tissue_name>_order.csv is generated in the same folder

+---Original Dataset
|   +---Covariates 
	# extracted covariate files for each tissue as provided by GTEx.
|   +---Gene Expression Matrices 
	# extracted gene expression files for each tissue as provided by GTEx.
|   +---Genes
	# extracted list of genes for each tissue as provided by GTEx.
|   +---Preprocessed Files # the covariate adjusted files for each tissue.
	'''
	For each tissue T, a folder with 3 files are generated.
	- T.csv: the covariate adjusted coexpression matrix for T
	- T_orig_filtered.csv: the original gene expression matrix for T but only for the protein-coding genes.
	- genes.csv: information related to all protein-coding genes in T. Both degree/PageRank centrality values of all the genes are generated in the same order as in this file. 
	'''

+---Parameter Analysis
	'''
	For every tissue T and for both the centrality measures, it contains scripts to generate:
	1. values by all the four metrics in T.
	2. the ranks for each metric in T.
	3. the Spearman correlation among all genes for T.
	'''
    
+---Replication Analysis on RW Datasets
|   +---Centrality Computation 
	# scripts for centrality comptation of the discovery and real-world datasets
	# similar to the centrality computation on the GTEx tissues.
|   +---Original Dataset
	'''
	Scripts to preprocess and generate the final datasets. Preprocessing involves
	- covariate adjustment of replication dataset
	- extraction of protein-coding genes to both datasets
	'''
|   |   +---Muscle_Skeletal_gtex
|   |   +---Muscle_Skeletal_recount
|   |   +---Preprocessed Files
|   +---Results 
	# scripts to compute the gene ranking by each metric and generate the plots.

+---Simulations and Validation Analysis
	'''
	This contains scripts for two analyses:
	1. Generation of simlated data and all analyses on the same.
		- all of these scripts are named as 'SIM_*.py'.
	2. Validation analysis of centrality measures on GTEx tissues.
		- these scripts compute the gene ranking by each metric and generate the plots.
		- all of these scripts are named as 'RW_*.py'
	'''

+---Tissue Specificity Analysis - 0.05 FDR
	# Specificity Analysis with 5% FDR
|   +---Elevated Genes # list of specific genes as downloaded from Human Protein Atlas
|   +---Parameter Analysis 
	# scripts to generate correlations of specific genes and other genes. 
|   +---Pathway Analysis
	'''
	Stores results of the GSEA analysis by WebGestalt. 
	E.g., the output directory structure for centrality C and tissue T is given below.
	+---Elevated_C
	|	+---T
	|	|	+---Project_deg	# results from gene ranking of obs
	|	|	+---Project_mu
	|	|	+---Project_mu_2sigma
	|	|	+---Project_mu_sigma
	+---Pathway Results # scripts to generate the heatmaps and boxplots.
	'''
    
+---Tissue Specificity Analysis - 0.05 FDR
	# Specificity Analysis with 10% FDR
|   +---Elevated Genes # list of specific genes as downloaded from Human Protein Atlas
|   +---Parameter Analysis 
	# scripts to generate correlations of specific genes and other genes. 
|   +---Pathway Analysis
	'''
	Stores results of the GSEA analysis by WebGestalt. 
	E.g., the output directory structure for centrality C and tissue T is given below.
	+---Elevated_C
	|	+---T
	|	|	+---Project_deg	# results from gene ranking of obs
	|	|	+---Project_mu
	|	|	+---Project_mu_2sigma
	|	|	+---Project_mu_sigma
	+---Pathway Results # scripts to generate the heatmaps and boxplots.
	'''
```
</details>

## Executing the Pipelines

### Generating the centrality measures

Before generating the centrality files, please ensure that the gene expression matrix ($\textrm{genes} \times \textrm{samples}$) is stored in a  comma-separated `.csv` file with the gene id’s as the first column and the sample ids as the first row.

To generate the centrality measures for both degree and PageRank centrality and to replicate our the results, run `Centrality Computation/run.sh`

1. Ensure the working directory is `Centrality Computation`.
2. Set the value of `B` with the number of bootstrap coexpression networks you want to generate. 
   Ensure `B` is set to a multiple of the number of cores you are using. For you are running the codes sequentially, then this constraint is irrelevant.  
3. Set `tissues` with the list of tissues for which you want to generate – each tissue name should be enclosed within quotes and separated by space.
4. Run the file from the terminal or GIT Bash (in a windows system) as `./run.sh`.

To run the program on a local system, edit `Centrality Computation/main.sh` as follows:

1. Comment line number $32$ `((counter++)); ((counter % cores == 0)) && wait`.
2. Remove `&` from line number $31$ `time python compute.py $tissue $((b-1))`.

Edit `Centrality Computation/compute.py` (and `Centrality Computation/compute.py` for values of the $\mathrm{obs}$ metric) under the following scenarios:

-  *You want to generate the centrality values for a specific centrality measure* – comment / remove the block corresponding to the centrality measure that you don’t want to generate.
-  *Your input/preprocessed file is in a different location* – update the `in_file` variable with the location of your file.
-  *Your input/preprocessed file has a different structure as mentioned above* – please update the code to read your gene expression matrix and enter the code to update the structure of the data frame before invoking the `bootstrap.BootstrapSample()` function.

### Validation Analysis on GTEx Datasets

To generate the plots for the validation analysis, run `Simulations and Validation Analysis/RW_validation.py` with the necessary inputs. 

For e.g., to generate the plots for centrality `C` ( `degree` or `pagerank` ) for `Lung`  tissue on the observed dataset with $237$ samples, do the following

1. Ensure the working directory is `Simulations and Validation Analysis`.
2. Ensure the folder `Semi-Simulated Data/Lung/C` exists in the same directory.
3. Set `klim` – the x-axis limit of the CAT and recall plots.
4. Run the code from the terminal as: `time python RW_validation.py Lung C 237`

To edit the code for the following scenarios:

-  *If you want to generate only the CAT or recall plot* – comment / remove the corresponding blocks for the same.
-  *If you want the output results in the CAT and/or recall plots in a separate location* – update the `filepath` variable for the corresponding plot with your destination location.
-  *If your input files are in a separate location* – then the codes to read the `.csv` files using `read_csv()` function from `pandas` in lines $27, 30, 33$ and $35$ may be updated. 
-  Please *update the parameters* of the `Plot()` function in the `plots` file as per your requirements.
-  To generate the POG values, instead of the plots, please run `RW_pog_vals.py` from the same directory with the necessary modifications as already mentioned.

### Replication Analysis on Real-World Datasets

To perform the procedure is similar as on the GTEx datasets, however, here, the main directory should be `Replication Analysis on RW Datasets`.

1. *For covariate adjustment of the replication dataset*:
   1. Ensure the current working directory is `Replication Analysis on RW Datasets/Original Dataset\Muscle_Skeletal_recount`.
   2. To extract the covariates: run `time python cov extract.py` from the terminal.
   3. To perform the adjustment run the `covariates.R` script.
2. *For extraction of genes common to the datasets* – run `genes.py` from `Replication Analysis on RW Datasets`.
3. Following this, the *centralities may be similarly computed* as mentioned above from `Replication Analysis on RW Datasets/Centrality Computation`.
4. To *plot the results* (or to generate the POG values), please run `Replication Analysis on RW Datasets/Results/results.py` (or `pog_vals.py`) using the same procedure as in validation analysis.

###  Analyses on Simulated Dataset

For simulated datasets, the codes for each analysis is independent of each other. Each analysis generates the population dataset, and performs the analysis as required. Nevertheless, if the seed is the same, the same population and respective observed datasets will be generated irrespective of the script/analysis. Please ensure the current working directory is `Simulations and Validation Analysis`.

-  To generate the heatmaps of the adjacency matrix, the degree distribution and the $\mu$ vs. $\sigma$ plots, run `SIM_graphs.py`.
-  To perform validation analysis and plot the CAT and recall plots, run `SIM_validation.py`.
-  To perform replication analysis and plot the CAT and recall plots, run `SIM_replication.py`.
-  To generate the POG values in the validation and replication analysis, run `SIM_pog_vals_1.py` and `SIM_pog_vals_2.py` respectively.

The input number of genes, the number of bootstrap samples, sample sizes of the observed dataset and the x-axis limit of the CAT and recall plots can be modified with `n, B, SampleSizes` and `klim` variables respectively. In the scripts for replication analysis, set the value of `s` to modify the size of the discovery dataset.

All of modifications, if required, can be performed as in the scripts for the real-world datasets.

### Specificity Analysis

#### Generating the rank files

To generate the rank files, run `Parameter Analysis/code 1.py`. By default, the script will generate the rank files for `pagerank` centrality measures by all the metrics for all the available tissues. The output `.rnk` files will be stored in `Parameter Analysis\ranks`. 

-  *If you want to change the list of tissues*, the please update the `Tissues` variable accordingly.
-  *If you want to generate the rank files for a different centrality measure*, then please update the `centrality` variable accordingly.
-  *If you want to change the name of the output rank files*, then please update the `names` variable accordingly.
-  *If you want to generate the rank files only for a subset of the metrics*, then please update the `parameters` and `ranks` variables in lines $34$ and $41$ respectively. 
-  *If your centrality files are in a different location*, then please update lines $25,26$ and $92$ to read the `.csv` files with `read_csv()` from `pandas`.
-  *If you want to change the location of output files*, then please comment line $18$ that creates the destination folder, and update the `opfile` variable in line $96$.

#### GSEA Analysis

Please use scripts in `Tissue Specificity Analysis - 0.05 FDR` (and `Tissue Specificity Analysis - 0.05 FDR`) for specificity analysis with $5$% (and $10$%) cutoff respectively.  `Elevated Genes` contains the list of specific genes (*Total Elevated* category) downloaded from the Human Protein Atlas.

**I.** Run `2.1_gmt_code.py` to generate the customized gene set file. 

-  In the `main` block, set the variable `Tissues` with the list of tissues, whose specific genes you want to add in the gene set  file. Please add the list of tissues as a comma-separated list.
-  The variable `gtype` stores the type of elevated expression category (see [here](https://www.proteinatlas.org/humanproteome/tissue/tissue+specific) for different categories).

The program generates a customized gene set file `<gtype>.gmt` (in our case `Elevated.gmt`) in the same folder. 

To change the destination location and/or name of the output file, please update line $12$ (`output = gtype + '.gmt'` in  `fun()` function definition).

**II.** To perform the GSEA analysis, please ensure the `WebGestaltR` package in already installed. 
The R script `2.2_pathways.R` contains the full script to perform the GSEA analysis. 
The program has been written to run GSEA on measures for both the centralities by all the proposed metrics on all the tissues that have been used. The script invokes the rank files from `Parameter Analysis/ranks`, and performs the analysis. 
The script will create the directory structure and store the results of the analysis in the `Pathway Analysis` folder. See the overall repository structure for details on the same.

However, to run the script for different input values, please do the following:

-  *If you want to change the list of tissues*, please update the `Tissues` variable in line $16$.
-  *If you want to run the analysis only for a subset of metrics*, please update the `Parameters` variable in line $17$.
-  By default the code uses $4$ *cores* to perform the analysis. If you want to change the same, please update `cores` variable in line $18$.
-  Please set the `centrality` and `gtype` variables with the *type/s of centrality measures and the elevated expression category*, as per your requirement, respectively, before invoking the `pathwayAnalysis()` function in line $31$.
-  *If your rank files are in a different location*, please update the `ipfile` variable in line $7$ inside the `pathwayAnalysis()` with the source location of your file.
-  *If you want to change your output location*, please update the `opfile` variable in line $8$ inside the `pathwayAnalysis()` with the destination location.
-  *To modify the name and location of your customized gene set database*, please update the `dbfile` variable in line $9$ inside the `pathwayAnalysis()` accordingly.

**III.** Scripts to plot the heatmaps and boxplots are inside `Pathway Results` folder. Please run `heatmaps.py` or `boxplots.py` to generate the heatmaps or plot the boxplots respectively. 

`Heatmaps.py`:

-  *To plot for a different list of tissues*, please update `Tissues` variable in line $47$.
-  *To change the gene sets*, please update `Paths` variable in line $48$.
-  *To change the category of elevated expression*, please update the list of values for the `gtype` variable in line $50$
-  *To change the type of centrality*, please update the list of values for the `centrality` variable in line $52$.
-  *To change the names of the metrics*, please update the `names` variable in line $13$.
-  *To run on a subset of the metrics*, please update the `parameters` variable in line $17$.
-  *To change the location of your input files*, please update the `filepath` variable in line $23$.
-  *To change the destination location of your output heatmaps*, please update the location in `savefig()` function by `matplotlib.pyplot` in line $43$.

`boxplots.py`: Please use this script similarly as above. 

-  The block for Degree (PageRank) centrality from lines $64$ ($70$) onwards generates the box plots for degree (PageRank) centrality measures.
-  The first parameter of the functions is the name of the specific gene set and the second parameter is the list of tissues for which you want to plot the boxplot.
-  To generate the plots for a subset of the metrics, please update `parameter_names, file_names` and `parameters` variables in lines $13, 14$ and $40$ respectively.
-  If your centrality files are in a different location, then please update lines $31$ and $32$ to read the `.csv` files with `read_csv()` from `pandas`.
-  To change the destination location of your output boxplots, please update the location in `savefig()` function by `matplotlib.pyplot` in line $60$.

## License

This project is licensed under the Creative Commons License — see [License file](LICENSE)  for details.

## Citation, Contact

To be updated following paper acceptance.

## Acknowledgements

We thank Dr. Sanga Mitra for her invaluable suggestions and contribution towards the completion of this work.
