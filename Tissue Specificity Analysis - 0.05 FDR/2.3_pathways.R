library(foreach)
library(doParallel)

pathwayAnalysis <- function(centrality, gtype, tissue, opfile, parameter, seed){
  cat(tissue, parameter, '\n', sep = '\t')
  
  ipfile <- paste0('ranks_', centrality, '/', tissue, '/', parameter, '.rnk')
  dbfile <- paste0(gtype, '.gmt')
  opfile <- opfile
  set.seed(seed)
  
  WebGestaltR::WebGestaltR(enrichMethod = "GSEA", enrichDatabase = "others", enrichDatabaseFile = dbfile, enrichDatabaseType = 'ensembl_gene_id', interestGeneFile = ipfile, interestGeneType = "ensembl_gene_id", isOutput = TRUE, minNum = 5, maxNum = 2000, collapseMethod = 'mean', sigMethod = "fdr", fdrThr = 0.05, setCoverNum = 50, reportNum = 40, outputDirectory = opfile, projectName = parameter)
}


Tissues <- c('Kidney_Cortex', 'Lung', 'Muscle_Skeletal', 'Pancreas', 'Pituitary', 'Stomach', 'Thyroid', 'Whole_Blood', 'Muscle_Skeletal_73', 'Muscle_Skeletal_237', 'Whole_Blood_73', 'Whole_Blood_237', 'Lung_237', 'Lung_73', 'Thyroid_237', 'Thyroid_73', 'Vagina')
Parameters <- c('EstNS_0', 'BooNS_0', 'BooNS_1', 'BooNS_2', 'BPNS_25')
cores <- 5

for (gtype in c('Elevated')) {
  if (gtype == 'Enriched') {
    Tissues <- Tissues[-length(Tissues)]
  }
  for (centrality in c('degree', 'pagerank')) {
    for (tissue in Tissues) {
      cat(centrality, tissue, '\n', sep = '\t')
      
      opfile <- paste0('Specificity Analysis/', gtype, '_', centrality, '/', tissue)
      dir.create(opfile, recursive = TRUE)
      
      seed = as.integer(Sys.time())
      write(seed, paste(opfile, '/seed.txt', sep = ''))
      set.seed(seed)
      sample_seeds = sample(x=.Machine$integer.max, size=cores, replace=T)
      
      cluster <- makeCluster(cores)
      registerDoParallel(cluster)
      foreach(idx = seq_along(Parameters)) %dopar% {
        parameter = Parameters[idx]
        pathwayAnalysis(centrality, gtype, tissue, opfile, parameter, seed = sample_seeds[idx])
      }
      stopCluster(cluster)
    }
  }
}