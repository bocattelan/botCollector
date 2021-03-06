#!/usr/bin/env bash

# cutValue, percentageBots, populationPlot, percentageNoTimeline, populationAll
cutValue=$2
cutValue="${cutValue//\"}"
percentageBots=$3
populationPlot=$4
percentageNoTimeline=$5
populationAll=$6
percentageRemoved=$7
percentageReported=$8
percentageReportedAndRemoved=$9
percentageReportedAndRemoved="${percentageReportedAndRemoved//\"}"

echo "# Português  "

echo "## botCollector  "
echo "Esse programa analisa as contas que seguem uma conta alvo."
echo "Cada conta que segue a conta alvo é analisada usando a API do projeto botometer."
echo "Apesar de poderosa, essa ferramenta tem seus limites."
echo "Contas sem timeline ou com sua timeline privada não são analisados."
echo "Contudo, por esse tipo de conta ser suspeita, nós mostramos abaixo a porcentagem delas em relação ao total de contas analisadas."
echo "O BotCollector é capaz de estudar qualquer conta do Twitter."
echo "Como exemplo, escolhemos nosso presidente: Jair Bolsonaro.  "

echo "## Resultados  "

echo "Gráfico mais recente:  "

echo "![](plots/plot.png)  "

echo "[Versão em PDF](plots/plot.pdf)  "

echo "## Referências  "

echo "Botometer: https://botometer.iuni.iu.edu/#!/  "

echo "Twitter API: https://developer.twitter.com/en/docs.html  "

echo "## Estatísticas:  "

echo "- Porcentagem de contas com probabilidade acima de **${cutValue}%** de serem bots: **${percentageBots}%**  "

echo "  - Obs: essa porcentagem foi feita com base em uma população de **${populationPlot}** contas ( a mesma usada no gráfico )  "

echo "- Porcentagem de contas sem timeline: **${percentageNoTimeline}%**  "
echo "- Porcentagem de contas removidas: **${percentageRemoved}%**  "
echo "- Porcentagem de contas reportadas por nós: **${percentageReported}%**  "
echo "- Porcentagem de contas reportadas por nós *e* removidas: **${percentageReportedAndRemoved}%**  "

echo "  - Obs: essas porcentagens foram feitas com base na população total verificada: **${populationAll}** contas ( Botometer não consegue estudar contas sem timeline )  "
echo "  "
echo "# English  "

echo "## botCollector  "

echo "This program aims at verifying the accounts following a target account."
echo "Each account that follows the target is given a score using the Botometer API.  "

echo "## Results  "

echo "Most recent plot:  "

echo "![](plots/plot.png)  "

echo "[PDF version](plots/plot.pdf)  "

echo "## References  "

echo "Botometer: https://botometer.iuni.iu.edu/#!/  "

echo "Twitter API: https://developer.twitter.com/en/docs.html  "
