library(RSQLite)
#library(ggplot2)
library(lattice)

setwd("../data/")
sqlite <- dbDriver("SQLite")
conn <- dbConnect(sqlite, "database.db", create = FALSE)

alltables = dbListTables(conn)

print(alltables[1])

df = dbGetQuery(conn, paste("SELECT * from jairbolsonaro WHERE capUniversal >= 0"))

pdf('../plots/plot.pdf')
#ggplot(data=df, aes(df$capUniversal)) + geom_histogram(bins = 30, aes(fill=..count..)) +
#  ggtitle("Twitter: jairbolsonaro") +
#  xlab("Prob. of being a bot | Prob. de ser um robô") + ylab("Number of accounts | Número de contas")
histogram(df$capUniversal * 100, type = "percent",
    main = "Twitter: jairbolsonaro", xlab = "Prob. of being a bot | Prob. de ser um robô",
    ylab = "Relative number of accounts | Número relativo de contas",
    breaks=seq(from=0,to=100,by=5))

percentage75bot = (sum(df$capUniversal > 0.75)/nrow(df))*100
df = dbGetQuery(conn, paste("SELECT * from jairbolsonaro WHERE capUniversal < 0"))
percentageNoTimeline = (sum(df$capUniversal == -1)/nrow(df))*100
print("Statistics")
print(paste("Percentage of accounts with prob 75% or higher: ", percentage75bot))
print(paste("Percentage of accounts with no timeline: ", percentageNoTimeline))

print("Estatísticas")
print(paste("Porcentagem de contas com prob. acima de 75%: ", percentage75bot))
print(paste("Porcentagem de contas sem timeline: ", percentageNoTimeline))
dev.off()