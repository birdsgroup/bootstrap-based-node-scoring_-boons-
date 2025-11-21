Tissues <- c('Brain_Amygdala', 'Brain_Cerebellum', 'Brain_Cortex', 'Brain_Substantia_nigra', 'Kidney_Cortex', 'Lung', 'Muscle_Skeletal', 'Pancreas', 'Pituitary', 'Stomach', 'Uterus', 'Vagina','Skin_Sun_Exposed_Lower_leg','Whole_Blood','Thyroid')
i = 1
setwd(paste0("/kegg_pathways_deg_centrality/",Tissues[i],"/Project_mu_sigma/"))
enrichment_results <- read.delim("enrichment_results_mu_sigma.txt", header = TRUE, sep = "\t", stringsAsFactors = FALSE)

ss_res_1 <-  as.data.frame(enrichment_results[,4])  #### Column 4 is for enrichment scores, and Column 7 is for enrichment p-values
row.names(ss_res_1) <- enrichment_results$description
colnames(ss_res_1) <- Tissues[i]

ddff <- as.data.frame(ss_res_1)
for(i in 2:length(Tissues)){
  setwd(paste0("/kegg_pathways_deg_centrality/",Tissues[i],"/Project_mu_sigma/"))
  enrichment_results <- read.delim("enrichment_results_mu_sigma.txt", header = TRUE, sep = "\t", stringsAsFactors = FALSE)
  x <- which(duplicated(enrichment_results$description) | duplicated(enrichment_results$description, fromLast = TRUE))
  if(length(x) != 0){
    enrichment_results <- enrichment_results[-x,]
  }else{
    enrichment_results <- enrichment_results
  }
  ss_res_3 <- as.data.frame(enrichment_results[,4])   #### Column 4 is for enrichment scores, and Column 7 is for enrichment p-values
  row.names(ss_res_3) <- enrichment_results$description
  colnames(ss_res_3) <- Tissues[i]
  
  
  ddff <- merge(ddff, ss_res_3, by = "row.names", all = TRUE)
  
  # 2. Rename the first column back to row names
  rownames(ddff) <- ddff$Row.names
  ddff$Row.names <- NULL
  
  # 3. Replace NAs (from non-matching rows) with zero
  ddff[is.na(ddff)] <- 0
  
}


setwd("/kegg_pathways_deg_centrality/")
write.csv(ddff,file = "KEGG_pathways_ES.csv")
