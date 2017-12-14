setwd("~/Documents/apma/sem2/estimation")
## LIST 4
###########################################################################################
# Ex.1 p.2

# TRUE VALUES
alpha <- 0
sigma2 <- 4
N <- 200

Y <- rnorm(n = N,
           mean = alpha,
           sd = sqrt(sigma2))

# log likelihood function
normal.loglike <- function(theta, y) {
  N <- length(y)
  alpha <- theta[1]
  sigma2 <- theta[2]
  return (-.5 * N * log(2 * pi) - .5 * N * log(sigma2) - 0.5 / sigma2 * sum((y - alpha) ^ 2))
}

normal.loglike.2 <- function(theta, y) {
  log.f <- dnorm(y, mean = theta[1], sd <- sqrt(theta[2]), log = TRUE)
  return (sum(log.f))
}

# res1 <- normal.loglike(c(0, 4), Y)
# res2 <- normal.loglike.2(c(0, 4), Y)

n.grid <- 200
alpha.grid <- seq(-1, 1, length.out = n.grid)
sigma2.grid <- seq(2, 6, length.out = n.grid)
alpha.sigma2.grid <-
  expand.grid(alpha.grid, sigma2.grid) # matrix with dimension 200 x 2

loglike.values <- # margin=1 -> calc across rows
  apply(
    alpha.sigma2.grid,
    MARGIN = 1,
    FUN = function(theta, y)
      normal.loglike.2(theta, y = Y),
    Y
  )
loglike.values <-
  matrix(loglike.values, nrow = n.grid, ncol = n.grid)

# PERSPECTIVE PLOT
persp(alpha.grid, sigma2.grid, loglike.values, ticktype = "detailed")

# CONTOUR PLOT
contour(
  alpha.grid,
  sigma2.grid,
  loglike.values,
  nlevels = 50,
  xlab = "alpha",
  ylab = "sigma2"
)

# Ex.1 p.3
alpha.est <- mean(Y)
sigma2.est <- 1 / length(Y) * sum((Y - alpha.est) ^ 2)

points(alpha.est,
       sigma2.est,
       pch = 16,
       col = "red",
       cex = 3)

# FILLED CONTOUR PLOT
filled.contour(
  alpha.grid,
  sigma2.grid,
  loglike.values,
  nlevels = 50,
  xlab = "alpha",
  ylab = "sigma2"
)

# IMAGE PLOT
# image()
# contour()
# points()

###########################################################################################
# # Ex.2 p.1
#
# library(readxl)
# Y <- read_excel('data_lab4-1.xlsx', col_names = FALSE)
# Y <- as.matrix(Y)
#
# dim(Y)
# N <- ncol(Y) # 100
# K <- nrow(Y) # 100