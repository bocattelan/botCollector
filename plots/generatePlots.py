from rpy2 import robjects
from rpy2.robjects.packages import importr

from utils import config


def generate_plot(TARGET_USER):
    # The R 'print' function
    # rprint = robjects.globalenv.get("print")
    # grdevices = importr('grDevices')
    #
    # databaseList = dplyr.src_sqlite("/Users/bocattelan/Workspace/botCollector/data/database.db", create=False)
    # lattice = importr('lattice')
    # target_table = databaseList.get_table(TARGET_USER)
    # dataFrame = DataFrame(target_table.select("capUniversal","lastCheck").filter("capUniversal >= 0 & lastCheck != 0").mutate(capUniversal="capUniversal*100").collect())
    # p = lattice.histogram(x=dataFrame.rx2("capUniversal"), type="percent")
    #
    # grdevices.png('test.png')
    # rprint(p)
    # grdevices.dev_off()
    #
    # grdevices.pdf('test.pdf')
    # rprint(p)
    # grdevices.dev_off()
    grdevices = importr('grDevices')
    lattice = importr('lattice')
    robjects.r('''
    
library(RSQLite)
#library(ggplot2)
library(lattice)

sqlite <- dbDriver("SQLite")
path = paste("''' + config.MAIN_DIRECTORY + '''", "/data/database.db",sep="")
conn <- dbConnect(sqlite, path, create = FALSE)

df = dbGetQuery(conn, "SELECT * from {} WHERE capUniversal >= 0 AND lastCheck != '0'")
#print(df$createdAt)
#print(?strptime)
#"Fri Jul 13 21:18:49 +0000 2018"
print(head(df))
df$createdAt <- as.Date(df$createdAt, "%a %b %d %X %z %Y")
df$createdAt <- format(df$createdAt, "%Y")
print(head(df))
print(as.factor(df$createdAt))
histPlot = histogram(df$capUniversal * 100, type = "percent", main = paste("Twitter: {}, pop: ", nrow(df)), xlab = "Prob. of being a bot | Prob. de ser um robô", ylab = "Relative number of accounts | Número relativo de contas", breaks=seq(from=0,to=100,by=5))
histCreatedAt = histogram(as.factor(df$createdAt), type = "percent", main = paste("Twitter: {}, pop: ", nrow(df)), xlab = "Date of creation | Data de criação", ylab = "Relative number of accounts | Número relativo de contas")

percentage90bot = (sum(df$capUniversal >= 0.9)/nrow(df))*100
populationPlot = nrow(df)
df = dbGetQuery(conn, paste("SELECT * from {}"))
percentageNoTimeline = (sum(df$capUniversal == -1)/nrow(df))*100
populationAll = nrow(df)
percentageRemoved = (sum(df$lastCheck == "0", na.rm = TRUE)/nrow(df))*100
percentageReported = (sum(df$reported == 1, na.rm = TRUE)/nrow(df))*100
percentageReportedAndRemoved = (sum(df$reported == 1 & df$lastCheck == "0", na.rm = TRUE)/nrow(df))*100

'''.format(TARGET_USER, TARGET_USER, TARGET_USER, TARGET_USER))
    rprint = robjects.globalenv.get("print")
    grdevices.png(file=config.MAIN_DIRECTORY + "/plots/png/plot_" + TARGET_USER + ".png")
    rprint(x=robjects.r['histPlot'])
    grdevices.dev_off()

    grdevices.pdf(file=config.MAIN_DIRECTORY + "/plots/pdf/plot_" + TARGET_USER + ".pdf")
    rprint(x=robjects.r['histPlot'])
    grdevices.dev_off()

    grdevices.png(file=config.MAIN_DIRECTORY + "/plots/png/plot_" + TARGET_USER + "_createdAt.png")
    rprint(x=robjects.r['histCreatedAt'])
    grdevices.dev_off()

    grdevices.pdf(file=config.MAIN_DIRECTORY + "/plots/pdf/plot_" + TARGET_USER + "_createdAt.pdf")
    rprint(x=robjects.r['histCreatedAt'])
    grdevices.dev_off()

    print("Estatísticas para " + TARGET_USER + " com pop. total " + robjects.r["populationAll"][0].__str__())
    print("Porcentagem de contas ativas com prob. acima de 90%: " + robjects.r["percentage90bot"][0].__str__())
    print("Porcentagem de contas sem timeline: " + robjects.r["percentageNoTimeline"][0].__str__())
    print("Porcentagem de contas removidas: " + robjects.r["percentageRemoved"][0].__str__())
    print("Porcentagem de contas reportadas: " + robjects.r["percentageReported"][0].__str__())
    print("Porcentagem de contas reportadas que foram removidas: " + robjects.r["percentageReportedAndRemoved"][
        0].__str__())
    print("")

    file_object = open(config.MAIN_DIRECTORY + "/data/facebook_post.txt", "a")
    file_object.write("---------------------------------------------------------\n")
    file_object.write(
        "Estatísticas para " + TARGET_USER + " com pop. total " + robjects.r["populationAll"][0].__str__() + '\n')
    file_object.write(
        "Porcentagem de contas ativas com prob. acima de 90%: " + robjects.r["percentage90bot"][0].__str__() + '\n')
    file_object.write("Mesma pop. do gráfico: " + robjects.r["populationPlot"][0].__str__() + '\n')
    file_object.write('\n')
    file_object.write("Porcentagem de contas sem timeline: " + robjects.r["percentageNoTimeline"][0].__str__() + '\n')
    file_object.write("Porcentagem de contas removidas: " + robjects.r["percentageRemoved"][0].__str__() + '\n')
    file_object.write("Porcentagem de contas reportadas: " + robjects.r["percentageReported"][0].__str__() + '\n')
    file_object.write(
        "Porcentagem de contas reportadas que foram removidas: " + robjects.r["percentageReportedAndRemoved"][
            0].__str__() + '\n')
    file_object.write("Pop. total: " + robjects.r["populationAll"][0].__str__() + '\n')
    file_object.write('\n')
    file_object.close()


def generate_all_plots():
    file = open(config.MAIN_DIRECTORY + "/data/facebook_post.txt", "w")
    c = config.conn.cursor()
    targets = c.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    tweet_text = [dict() for x in targets]
    message_index = 0
    for target in targets:
        generate_plot(target[0])
        tweet_text[message_index]["status"] = ""
        tweet_text[message_index]["status"] = tweet_text[message_index]["status"] + "Usuário Alvo: " + target[0] + "\n"
        tweet_text[message_index]["status"] = tweet_text[message_index]["status"] + "Usuários com prob. acima de 90%: " + "{:.3f}".format(robjects.r["percentage90bot"][0]) + "%\n"
        tweet_text[message_index]["status"] = tweet_text[message_index]["status"] + "População ativa total: " + robjects.r["populationPlot"][0].__str__() + "\n"
        tweet_text[message_index]["media"] = config.MAIN_DIRECTORY + "/plots/png/plot_" + target[0] + ".png"
        message_index = message_index + 1
    c.close()
    return tweet_text


if __name__ == '__main__':
    message = generate_all_plots()
    print(message)