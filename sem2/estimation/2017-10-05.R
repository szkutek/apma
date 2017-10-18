x <- c(1, 3, 5, 6)
y <- c(5, 7, 9, 11)
z <- 2:11
w <- seq(from = 1, to = 11, by = .1)
X <- rnorm(n = 30, mean = 2, sd = 1)
n <- 30
Y <- matrix(rnorm(n * 10, mean = 2, sd = 1), nrow = n, ncol = 10)
dim(Y)
mean(X)
var(X)
median(X)
summary(X)
colMeans(Y)
apply(Y, MARGIN = 2, FUN = mean) # MARGIN - 1 for rows, 2 for columns
apply(Y, MARGIN = 2, FUN = var) # MARGIN - 1 for rows, 2 for columns

hist(X)
plot(X, type = "l")
boxplot(X)

X <- rnorm(100)
hist(X, freq = FALSE)
x <- seq(-3, 3, by = .01)
y <- dnorm(x)
lines(x, y, col = "red")
