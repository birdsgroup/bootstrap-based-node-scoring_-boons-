s <- 500000

#Tissues <- c('Muscle_Skeletal', 'Pituitary', 'Kidney_Cortex')
Tissues <- c('Brain_Amygdala', 'Brain_Cerebellum', 'Brain_Cortex', 'Brain_Substantia_nigra', 'Kidney_Cortex', 'Lung', 'Muscle_Skeletal', 'Pancreas', 'Pituitary', 'Skin_Sun_Exposed_Lower_leg', 'Stomach', 'Thyroid', 'Uterus', 'Vagina', 'Whole_Blood')

for (tissue in Tissues) {
  # Create Output Directory
  if (!dir.exists(tissue)) {
    dir.create(tissue, recursive = TRUE)
  }
  
  # Read original dataset
  gtex_data_file <- paste0('../Original Dataset/Preprocessed Files/', tissue, '/', tissue, '_orig_filtered.csv')
  gtex_data <- read.csv(gtex_data_file)
  
  df <- gtex_data[, 5:ncol(gtex_data)]
  rownames(df) <- gtex_data$gene_id
  
  # Find variance of genes
  gene_vars <- apply(df, 1, var)
  
  # Different values of n
  for (n in c(1000, 500, 100)) {
    cat(tissue, '\t', n, '\n')
    
    # Extract the subset of genes that should be simulated
    top_genes <- names(sort(gene_vars, decreasing = TRUE))[1:n]
    df_subset <- df[top_genes,]
    mat_data <- as.matrix(df_subset)
    
    # Set the seed
    seed_path <- file.path(tissue, 'seed.txt')
    if (file.exists(seed_path)) {
      seed <- as.integer(readLines(seed_path, n = 1))
    } else {
      seed = as.integer(Sys.time())
      write(seed, paste0(tissue, '/seed.txt'))
    }
    set.seed(seed)
    
    # Simulate the Dataset
    rs <- dependentsimr::get_random_structure(
      datasets = list(mysim = mat_data),
      method = 'corpcor',
      types = c(mysim = 'normal')
    )
    sim_results <- dependentsimr::draw_from_multivariate_corr(rs, n_samples = s)
    final_results <- as.data.frame(t(sim_results$mysim))
    
    # Write the dataset to a csv file
    data.table::fwrite(
      final_results, file = paste0(tissue, '/pop_', n, '.csv'), row.names = FALSE
    )
    data.table::fwrite(
      df_subset, file = paste0(tissue, '/orig_', n, '.csv'), row.names = TRUE
    )
  }
}