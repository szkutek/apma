factor.model.est <-
  function(Y, K_max)
    #function returning which K we should choose
  {
    T <- nrow(Y)
    N <- ncol(Y)
    
    eigen.decomp <- eigen(Y %*% t(Y))
    eigen.values <- eigen.decomp$values
    eigen.vectors <- eigen.decomp$vector
    # we calculate F, lambda and e for K_max
    F <- sqrt(T) * eigen.vectors[, 1:K_max]
    lambda <- t(F) %*% Y / T
    e <- Y - F %*% lambda
    sigma2.hat <- sum(e ^ 2) / (N * T)
    
    PC1 <- 1:K_max
    IPC1 <- 1:K_max
    for (K in 1:K_max)
    {
      # we calculate F, lambda and e for K
      F <- sqrt(T) * eigen.vectors[, 1:K]
      lambda <- t(F) %*% Y / T
      e <- Y - F %*% lambda
      V <- sum(e ^ 2) / (N * T)
      # we calculate PC1 and IPC1 for K
      PC1[K] <-
        V + K * sigma2.hat * ((N + T) / (N * T)) * log(N * T / (N + T))
      IPC1[K] <-
        log(V) + K * ((N + T) / (N * T)) * log(N * T / (N + T))
    }
    # choose K which gives the minimal value
    PC1_K <- which.min(PC1)
    IPC1_K <- which.min(IPC1)
    return (list(PC1_K, IPC1_K))
  }