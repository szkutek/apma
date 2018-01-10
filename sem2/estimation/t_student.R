N <- 1000
T <- 200

Monte_Carlo_test_normal <- function(alpha0,alpha,N,T)
{
  a <- 0.05
  critical.val <- qt(1 - a, df = T-2)
  rejecting = 0
  for (i in 1:N)
  {
    x <- rnorm(200,mean = 5, sd = 1)
    e <- rnorm(200,mean = 0, sd = 1)
    y <- alpha*x + e
    X <- as.matrix(x)
    Y <- as.matrix(y)
    alpha_est = solve(t(X)%*%X)%*%t(X)%*%Y
    SE_alpha_est = sqrt(sum((y-alpha_est*x)^2)/(T-2))/sqrt(sum((x-mean(x))^2))
    t_student_test = abs(alpha_est - alpha0)/SE_alpha_est
    if (abs(t_student_test)>=critical.val)
    {
      rejecting = rejecting + 1
    }
  }
  return(rejecting/N)
}

Monte_Carlo_test_random_walk <- function(alpha0,alpha,N,T)
{
  a <- 0.05
  critical.val <- qt(1 - a, df = T-2)
  rejecting = 0
  for (i in 1:N)
  {
    x <- cumsum(rnorm(200,mean = 5, sd = 1))
    e <- rnorm(200,mean = 0, sd = 1)
    y <- alpha*x + e
    X <- as.matrix(x)
    Y <- as.matrix(y)
    alpha_est = solve(t(X)%*%X)%*%t(X)%*%Y
    SE_alpha_est = sqrt(sum((y-alpha_est*x)^2)/(T-2))/sqrt(sum((x-mean(x))^2))
    t_student_test = abs(alpha_est - alpha0)/SE_alpha_est
    if (abs(t_student_test)>=critical.val)
    {
      rejecting = rejecting + 1
    }
  }
  return(rejecting/N)
}

# residua from normal distribution
alpha <- 2
alpha0 <- seq(alpha-0.2,alpha+0.2,0.01)
res <- rep(0,length(alpha0))
j <- 1
for (i in alpha0)
{
  res[j] <- Monte_Carlo_test_normal(i,alpha,N,T)
  j = j+1
}
plot(alpha0,res)

# residua from random walk
alpha <- 2
alpha0 <- seq(alpha-0.2,alpha+0.2,0.01)
res <- rep(0,length(alpha0))
j <- 1
for (i in alpha0)
{
  res[j] <- Monte_Carlo_test_random_walk(i,alpha,N,T)
  j = j+1
}
plot(alpha0,res)

# size
Monte_Carlo_test_normal(2,2,N,T)
Monte_Carlo_test_random_walk(2,2,N,T)

# power
# residua from normal distribution
alpha0 <- c(seq(-1,-0.1,0.05),seq(0.1,1,0.05))
power <- rep(0,length(alpha0))
j <- 1
for (i in alpha0)
{
  power[j] <- Monte_Carlo_test_normal(i,0,N,T)
  j = j+1
}
plot(alpha0,power)

# residua from random walk
alpha0 <- c(seq(-1,-0.1,0.05),seq(0.1,1,0.05))
power <- rep(0,length(alpha0))
j <- 1
for (i in alpha0)
{
  power[j] <- Monte_Carlo_test_random_walk(i,0,N,T)
  j = j+1
}
plot(alpha0,power)
