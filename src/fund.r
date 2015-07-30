setwd("~/work/pension-fund-performance/output")
fund <- read.csv(file="fund.csv",head=FALSE,sep=" ")

x <- fund$V1
x <- as.Date(x, "%Y-%m-%d")
y <- fund$V2
fit <- lm(y ~ x)

plot(x, y, 'l')
abline(fit)
