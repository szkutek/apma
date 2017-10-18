library(mvtnorm)
library(matlib)

# exercise 1.1
n <- 10000
mu <- c(0, 0)
Sigma <- diag(2)
# X <- mvrnorm(n = n, mu = m, Sigma = v) # from mvtnorm library
X <- rmvnorm(n = n, mean = mu, sigma =  Sigma)
plot(X)

mu <- t(c(0, 1))
Sigma <- matrix(c(2, .5, .5, 2), 2, 2)

A <- mpower(Sigma , .5)
a <- mu
Y <- A %*% t(X) + a
plot(Y)

mean = matrix(c(0,1),1,2)
sigma <- matrix(c(2,0.5,0.5,2),2,2)
A <- mpower(sigma, 0.5)
a <- mean
Y <- A %*% t(X) + t(apply(t(a), 1, rep, n))
plot(t(Y))