library(foreach)
library(doParallel)

pathwayAnalysis <- function(centrality, gtype, tissue, parameter){
  cat(tissue, parameter, '\n', sep = '\t')
  
  ipfile <- paste0('../Parameter Analysis/ranks/', centrality, '/', tissue, '/', tissue, '_', parameter, '.rnk')
  opfile <- paste0('Pathway Analysis/', gtype, '_', centrality, '/', tissue)
  dbfile <- paste0(gtype, '.gmt')
  dir.create(opfile, recursive = TRUE)
  
  WebGestaltR::WebGestaltR(enrichMethod = "GSEA", enrichDatabase = "others", enrichDatabaseFile = dbfile, enrichDatabaseType = 'genesymbol', interestGeneFile = ipfile, interestGeneType = "genesymbol", isOutput = TRUE, minNum = 5, maxNum = 2000, collapseMethod = 'mean', sigMethod = "fdr", fdrThr = 0.05, setCoverNum = 50, reportNum = 40, outputDirectory = opfile, projectName = parameter)
}


Tissues <- c('Kidney_Cortex', 'Lung', 'Muscle_Skeletal', 'Pancreas', 'Pituitary', 'Stomach', 'Thyroid', 'Whole_Blood', 'Muscle_Skeletal_73', 'Muscle_Skeletal_237', 'Whole_Blood_73', 'Whole_Blood_237', 'Lung_237', 'Lung_73', 'Vagina')
Parameters <- c('obs', 'mu', 'mu-2sigma', 'mu-sigma')
cores <- 4

for (gtype in c('Elevated')) {
  if (gtype == 'Enriched') {
    Tissues <- Tissues[-length(Tissues)]
  }
  for (centrality in c('degree', 'pagerank')) {
    for (tissue in Tissues) {
      cat(centrality, tissue, '\n', sep = '\t')
      
      cluster <- makeCluster(cores)
      registerDoParallel(cluster)
      foreach(parameter = Parameters) %dopar% {
        pathwayAnalysis(centrality, gtype, tissue, parameter)
      }
      stopCluster(cluster)
    }
  }
}