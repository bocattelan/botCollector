library(RSQLite)
#library(ggplot2)
library(lattice)

setwd("data/")
sqlite <- dbDriver("SQLite")
conn <- dbConnect(sqlite, "database.db", create = FALSE)

df = dbGetQuery(conn, paste("SELECT * from jairbolsonaro WHERE capUniversal >= 0"))

plot1 = histogram(df$capUniversal * 100, type = "percent",
    main = paste("Twitter: jairbolsonaro, pop: ", nrow(df)), xlab = "Prob. of being a bot | Prob. de ser um robô",
    ylab = "Relative number of accounts | Número relativo de contas",
    breaks=seq(from=0,to=100,by=5))

invisible(pdf('../plots/plot.pdf'))
plot1
invisible(dev.off())

invisible(png('../plots/plot.png'))
plot1
invisible(dev.off())

percentage75bot = (sum(df$capUniversal > 0.75)/nrow(df))*100
populationPlot = nrow(df)
df = dbGetQuery(conn, paste("SELECT * from jairbolsonaro"))
percentageNoTimeline = (sum(df$capUniversal == -1)/nrow(df))*100
populationAll = nrow(df)

# cutValue, percentageBots, populationPlot, percentageNoTimeline, populationAll
paste(75, percentage75bot, populationPlot, percentageNoTimeline, populationAll, sep=" ")

#print("Statistics")
#print(paste("Percentage of accounts with prob 75% or higher: ", percentage75bot))
#print(paste("Percentage of accounts with no timeline: ", percentageNoTimeline))

#print("Estatísticas")
#print(paste("Porcentagem de contas com prob. acima de 75%: ", percentage75bot))
#print(paste("Porcentagem de contas sem timeline: ", percentageNoTimeline))