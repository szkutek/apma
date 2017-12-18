setwd("~/Documents/apma/sem2/estimation")
## LIST 4
###########################################################################################
# # # Ex.2 p.1
# # log-likelihood
# loglike <- function(sigma, mu, p, y) {
#   sum(log(p * dnorm(y) + (1 - p) * dnorm(y, mean = mu, sd = sigma)))
# }
# library(readxl)
# Y <- read_excel('data_lab4-1.xlsx', col_names = FALSE)
# Y <- as.matrix(Y)
# p <- 0.8
# mu <- Y[1]
# 
# # simga in (0.01, 4)
# # sigma.vector <- seq(0.01, 4, 0.01)
# N <- length(Y)
# sigma.vector <- 1/exp(1:N)
# loglike.sigma <- sapply(sigma.vector, function(s) loglike(sigma = s, mu = mu, p = p, y = Y))
# plot(sigma.vector, loglike.sigma, type = "b", log = "x")

###########################################################################################
# # Ex.3 

library(readxl)
data <- read_excel('data_lab4-2.xlsx', col_names = FALSE)
data <- as.matrix(data)
y <- data[, 1]
x <- data[, 2]

# built-in function
model <- glm(y ~ x, family = binomial(link = "logit"))
model # theta1 = -0.2914      theta2 = 1.0766 
vcov(model) # covariance matrix for estimators

# Numerical optimization (we can use newtons method)
loglike.fun <- function(x, y){
  function(theta){
    t1 <- theta[1]; t2 <- theta[2];
    sum(y * log(exp(t1 + t2*x)/(1+exp(t1 + t2*x))) + (1-y) * log(1/(1+exp(t1 + t2*x))))
  }
}

t1.start <- 0; t2.start <- 0; 
loglike <- loglike.fun(x,y)
est <- optim(par = c(t1.start, t2.start), fn = loglike, control = list(fnscale = -1), hessian = TRUE)
est$par # theta1 = -0.2913384  theta2 = 1.0768976
# ? optim

I = -est$hessian
vcov2 <- solve(I) # asymptotic covatiance matrix
vcov2

