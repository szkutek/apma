library(readxl)
data <- read_excel('data_Lab5.xlsx', col_names = F)
data <- as.matrix(data)
N <- nrow(data)
y <- data[, 1]
x <- data[, 2]
X <- cbind(rep(1, N), x, x ^ 2)

# MLE
beta.mle <- solve(t(X) %*% X) %*% t(X) %*% y
sigma2.mle <- t(y - X %*% beta.mle) %*% (y - X %*% beta.mle) / N

theta.hat <- c(beta.mle, sigma2.mle)
sigma2.mle <- as.numeric(sigma2.mle)
I.inv <- rbind(cbind(sigma2.mle * solve(t(X) %*% X), rep(0, 3)),
               cbind(t(rep(0, 3)), 2 * sigma2.mle ^ 2 / N))

# Wald test
R <- matrix(c(0, 0, 0, 1), 1, 4)
W <-
  t(R %*% theta.hat - 1) %*% solve(R %*% I.inv %*% t(R)) %*% (R %*% theta.hat - 1)
W
alpha <- 0.05
alpha
critical.val <- qchisq(1 - alpha, df = 1) # 3.841459
critical.val
W.pval <- 1 - pchisq(1 - alpha, df = 1) # 0.3297193
W.pval
