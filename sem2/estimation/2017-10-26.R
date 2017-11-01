library(gdata)

# dataset <- read.xls("data_lab_2.xlsx", sheet = 1, header = FALSE)
dataset <-
  read.csv("data_lab_2.csv",
           header = FALSE,
           sep = ";",
           dec = ",")
dim(dataset)

# library(MASS)
# data(Cars93)
# View(Cars93)
# print(names(Cars93))

# print(names(dataset))
# #  "V1" "V2" "V3" "V4"


# y <- dataset[, 1]; y <- dataset[, "V1"]
y <- dataset$V1 # choose column
attach(dataset) # all columns are now separate vectors with names = names of the columns
V1
# detach(dataset)
# V1

# scatterplot
plot(V1, V2)
pairs(dataset) # scatterplot for all pairs
cor(dataset)

is.data.frame(dataset)
is.matrix(dataset)
# convert dataframe to matrix
datam <- as.matrix(dataset)
is.matrix(datam)



# MODEL 1
model1 <- lm(V1 ~ V2)
model1a <- lm(V1 ~ V2 - 1)
model1 # V1 = 2.129 * V2 + 5.666
model1a # only slope coefficient
summary(model1)

plot(V2, V1)
abline(model1, col = "red")
abline(model1a, col = "green")


# MODEL 2
model2 <-
  lm(V1 ~ . - 1, data = dataset) # no intercept (no constant)
model2 # coefficients: 2.0586  1.0748  0.8897

summary(model2)

X <- as.matrix(dataset[,-1])
y <- as.matrix(dataset[, 1])
# y <- as.vector(dataset[, 1])
plot(X, y)
abline(model1, col = "red")
