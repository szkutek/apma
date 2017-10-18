# library(mvtnorm)
library(matlib)

# exercise 1.1
n <- 10000
mu <- c(0, 0)
Sigma <- diag(2)
# X <- mvrnorm(n = n, mu = m, Sigma = v) # from mvtnorm library
X <- rmvnorm(n = n, mean = mu, sigma =  Sigma)
plot(X)

# exercise 1.3
mu = matrix(c(0, 1), 1, 2)
Sigma <- matrix(c(2, 0.5, 0.5, 2), 2, 2)
A <- mpower(Sigma, 0.5)
a <- mu
Y <- A %*% t(X) + t(apply(t(a), 1, rep, n))
Yt = t(Y)
plot(Yt)

Y1_c <- cut(Yt[, 1], 30)
Y2_c <- cut(Yt[, 2], 30)
hist3D(z = table(Y1_c, Y2_c), border = "black")
# image2D(z = table(Y1_c, Y2_c), border = "black")

# exercise 1.4
Z = Yt %*% mpower(Sigma,-1) %*% Y
# Z <- t(Y) %*% solve(Sigma) %*% Y
plot(Z)
Z1_c <- cut(Z[, 1], 20)
Z2_c <- cut(Z[, 2], 20)
hist3D(z = table(Z1_c, Z2_c), border = "black")
