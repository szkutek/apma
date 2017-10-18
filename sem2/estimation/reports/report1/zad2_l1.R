#zadanie2
#1
library(mvtnorm)
n <- 1000
mean <- c(0, 0)
sigma <- diag(2)
X = rmvnorm(n, mean, sigma)
plot(X)

#2
library(matlib)
library(plot3D)
mean <- matrix(c(0, 1), 1, 2)
sigma <- matrix(c(2, 0.5, 0.5, 2), 2, 2)
A <-
  mpower(sigma, 0.5) # macierz A jest symetryczno (a to jest pierwiastek z sigmy)
a <- mean
Y <- A %*% t(X) + t(apply(t(a), 1, rep, n))
plot(t(Y))
mean1 <- mean(Y[1,])
mean2 <- mean(Y[2,])
var1 <- var(Y[1,])
var2 <- var(Y[2,])
print(mean1)
print(mean2)
print(var1)
print(var2)
hist(Y[1,], freq = FALSE)
x <- seq(-5, 5, by = 0.01)
y <- dnorm(x, 0, sqrt(2))
lines(x, y, col = "red")
hist(Y[2,], freq = FALSE)
x <- seq(-5, 5, by = 0.01)
y <- dnorm(x, 1, sqrt(2))
lines(x, y, col = "red")
z <- table(Y[1,], Y[2,])

# tutaj jest funkcja liczaca histogram3D, bo pieprzony R nie umie tego zrobi?
my_hist3D <- function(x, y, nclassx, nclassy)
{
  bx <- seq(min(x), max(x), length = (nclassx + 1))
  by <- seq(min(y), max(y), length = (nclassy + 1))
  z <- matrix(0, nrow = nclassx, ncol = nclassy)
  n <- 2 * length(x)
  for (i in 1:nclassx)
  {
    for (j in 1:nclassy)
    {
      z[i, j] <-
        (1 / n) * sum(x < bx[i + 1] &
                        y < by[j + 1] & x >= bx[i] & y >= by[j])
    }
  }
  hist3D(z = z)
}
# tutaj rysuj? histogram
my_hist3D(Y[1,], Y[2,], 5, 6)

#3
Z <- t(Y) %*% solve(sigma) %*% Y
my_hist3D(Z[1,], Z[2,], 5, 6)
