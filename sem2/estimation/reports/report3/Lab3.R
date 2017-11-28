# setwd("E:/Magisterka/semestr2/ET/Lab3")
library(readxl)
data1 <- read_excel('dataLab3.xlsx', col_names = FALSE)
data2 <- read_excel('RB.xlsx', col_names = FALSE)
Y <- as.matrix(data1)
N <- ncol(Y)
T <- nrow(Y)
#estimator factor model
eigen.decomp <- eigen(Y %*% t(Y))
eigen.values <- eigen.decomp$values
eigen.vectors <- eigen.decomp$vectors
plot(eigen.values) # to check how many eigen.values take, in that case we take 3 eigen values
K <- 5
F.hat <- sqrt(T) * eigen.vectors[, 1:K]
lambda.hat <- t(F.hat) %*% Y / T
#portion of explained variance:
explained_variance <- cumsum(eigen.values) / sum(eigen.values)
plot(1:T, explained_variance, xlab = 'K', type = 'b')
grid()
#function returning which K we should choose
factor.model.est <- function(Y, K_max)
{
  F <- sqrt(T) * eigen.vectors[, 1:K_max]
  lambda <- t(F) %*% Y / T
  e <- Y - F %*% lambda
  sigma_est <- sum(e ^ 2) / (N * T) # for K_max
  
  PC1 <- 1:K_max
  IPC1 <- 1:K_max
  for (K in 1:K_max)
  {
    F <- sqrt(T) * eigen.vectors[, 1:K]
    lambda <- t(F) %*% Y / T
    e <- Y - F %*% lambda
    V <- sum(e ^ 2) / (N * T)
    # we calculate PC1 and IPC1
    PC1[K] <-
      V + K * sigma_est * ((N + T) / (N * T)) * log(N * T / (N + T))
    IPC1[K] <-
      log(V) + K * ((N + T) / (N * T)) * log(N * T / (N + T))
  }
  # K which gives the minimal value
  PC1_K <- which.min(PC1)
  IPC1_K <- which.min(IPC1)
  
  # F.hat <- sqrt(T) * eigen.vectors[, 1:final_K]
  # lambda.hat <- t(F.hat) %*% Y / T
  return (list(PC1_K, IPC1_K))
  #return (list(F.hat = F.hat,lambda.hat = lambda.hat))
}

res <- factor.model.est(Y, 10)
#res$F.hat
#res$lambda.hat



# data1 <- read_excel('dataLab3.xlsx', col_names = FALSE)
# Y <- as.matrix(data1)
# eigen.decomp <- eigen(Y%*%t(Y))
# eigen.values <- eigen.decomp$values
# explained_variance <- cumsum(eigen.values)/sum(eigen.values)
# par(mfrow=c(2,1))
# plot(1:T,explained_variance,xlab = 'K', ylab = '',type = 'b')
# plot(1:10,explained_variance[1:10],xlab = 'K', ylab = '',type = 'b')