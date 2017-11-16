data <-
  read.table('data_lab_2.csv',
             sep = ",",
             dec = ",",
             header = FALSE)
attach(data)

N <- 100
K <- 3

X <- as.matrix(data[,-1])
y <- as.matrix(data[, 1])

# theoretical result:
alpha.est <- solve(t(X) %*% X) %*% t(X) %*% y
alpha.est
# r model
model <- lm(V1 ~ . - 1, data)
coef(model)

# r function
res <- resid(model) # residuals

# VARIANCE OF RESIDUALS
sigma2.est.unbiased <- t(res) %*% res / (N - K)
summary(model) # Residual standard error squared
0.8956 ^ 2
sigma2.est.unbiased

# VARIANCE-COVARIANCE MATRIX OF LS ESTIMATOR
cov.alpha.est <-
  solve(t(X) %*% X) * as.numeric(sigma2.est.unbiased)
cov.alpha.est
vcov(model)

se.alpha.est <- sqrt(diag(cov.alpha.est))
t.ratio <- alpha.est / se.alpha.est
t.ratio
summary(model)
# calculate p-value ?