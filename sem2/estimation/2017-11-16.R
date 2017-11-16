setwd("~/Documents/apma/sem2/estimation")
library(readxl)
Y <- read_excel('dataLab3.xlsx', col_names = FALSE)
Y <- as.matrix(Y)
dim(Y)
N <- ncol(Y) # 100
T <- nrow(Y) # 100

# estimate factor model
eigen.decomp <- eigen(Y %*% t(Y)) #  ? eigen
eigen.values <- eigen.decomp$values
eigen.vectors <- eigen.decomp$vector
plot(eigen.values) # so we take only the 3 most important values

K <- 5
F.hat <- sqrt(T) * eigen.vectors[, 1:K]
lambda.hat <- t(F.hat) %*% Y / T

# portion of explained variance
explained.variance <- cumsum(eigen.values) / sum(eigen.values)
plot(1:T, explained.variance, xlab = "K", type = "b")
grid()

factor.model.est <- function(Y, K) {
  # ...
  return(list(F.hat = F.hat, lambda.hat = lambda.hat))
}

res <- factor.model.est(Y, K = 2)
res$F.hat
res$lambda.hat