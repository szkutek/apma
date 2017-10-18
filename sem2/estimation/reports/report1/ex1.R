library(MASS)
# exercise 1.1
Y <- rnorm(n = 1000, mean = 2, sd = 2)
Y1 <- 3 * (Y - 1) # indicate what property do we use (linearity?)
hist(Y1, freq = FALSE)
mean(Y1)
var(Y1) # policzyc analitycznie

fitdistr(Y1, "normal")
x <- seq(-20, 25, by = 0.01)
y <- dnorm(x, 3, 6)
lines(x, y, col = "red")

# exercise 1.2
Y2 <- ((Y1 - 2) / 2) ^ 2
hist(Y2, freq = FALSE)
fitdistr(Y2, "exponential")
x <- seq(0, 120, by = 0.01)
y <- dexp(x, rate = 1 / mean(Y2))
lines(x, y, col = "red")

# exercise 1.3
nn = 1000
N <- seq(1, nn,by=1)
Y <- rnorm(n = nn, mean = 2, sd = 2)
M <- cumsum(Y) / N
# V <- cumsum((Y - mean(Y)) ^ 2)/N


plot(N, M)
lines(N, rep(2, length(N), type = "l", col = "red"))
errM  <- abs(M-2)/2
# errV
plot(N, errM)


plot(N, V)
lines(N, rep(4, length(N), type = "l", col = "red"))