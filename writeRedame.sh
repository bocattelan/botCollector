#!/usr/bin/env bash

# cutValue, percentageBots, populationPlot, percentageNoTimeline, populationAll
cutValue=$2
cutValue="${cutValue//\"}"
percentageBots=$3
populationPlot=$4
percentageNoTimeline=$5
populationAll=$6
populationAll="${populationAll//\"}"

echo "# Português  "

echo "## botCollector  "
echo "Esse programa analisa as contas que seguem uma conta alvo."
echo "Cada conta que segue a conta alvo é analizada usando a API do projeto botometer  "

echo "## Resultados  "

echo "Gráfico mais recente:  "

echo "![](plots/plot.png)  "

echo "[Versão em PDF](plots/plot.pdf)  "

echo "## Referências  "

echo "Botometer: https://botometer.iuni.iu.edu/#!/  "

echo "Twitter API: https://developer.twitter.com/en/docs.html  "

echo "## Estatísticas:  "

echo "Porcentagem de contas com probabilidade acima de **${cutValue}%** de serem bots: **${percentageBots}%**  "

echo "Obs: essa porcentagem foi feita com base em uma população de **${populationPlot}** ( a mesma usada no gráfico )  "

echo "Porcentagem de contas sem timeline: **${percentageNoTimeline}%**  "

echo "Obs: essa porcentagem foi feita com base na população total verificada: **${populationAll}** ( Botometer não consegue estudar contas sem timeline )  "

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
