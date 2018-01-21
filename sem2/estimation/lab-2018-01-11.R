library(readxl)
data <- read_excel('dataLab6.xlsx', col_names = F)
data <- as.matrix(data)
N <- nrow(data)
y <- data[, 1]
x <- data[, 2]
n <- length(y)
lm_fit <- lm(y~x)
summary(lm_fit)

coef(lm_fit)
fitted(lm_fit)
resid(lm_fit)
confint(lm_fit) # 95% confidence intervals
