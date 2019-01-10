# Português  
## botCollector  
Esse programa analisa as contas que seguem uma conta alvo.
Cada conta que segue a conta alvo é analisada usando a API do projeto botometer.
Apesar de poderosa, essa ferramenta tem seus limites.
Contas sem timeline ou com sua timeline privada não são analisados.
Contudo, por esse tipo de conta ser suspeita, nós mostramos abaixo a porcentagem delas em relação ao total de contas analisadas.
O BotCollector é capaz de estudar qualquer conta do Twitter.
Como exemplo, escolhemos nosso presidente: Jair Bolsonaro.  
## Resultados  
Gráfico mais recente:  
![](plots/plot.png)  
[Versão em PDF](plots/plot.pdf)  
## Referências  
Botometer: https://botometer.iuni.iu.edu/#!/  
Twitter API: https://developer.twitter.com/en/docs.html  
## Estatísticas:  
- Porcentagem de contas com probabilidade acima de **75%** de serem bots: **27.015050501018%**  
  - Obs: essa porcentagem foi feita com base em uma população de **50098** contas ( a mesma usada no gráfico )  
- Porcentagem de contas sem timeline: **39.6594111650776%**  
- Porcentagem de contas removidas: **0.495292918390598%**  
- Porcentagem de contas reportadas por nós: **2.4332913593572%**  
- Porcentagem de contas reportadas por nós *e* removidas: **0.00839479522695928%**  
  - Obs: essas porcentagens foram feitas com base na população total verificada: **83385** contas ( Botometer não consegue estudar contas sem timeline )  
  
# English  
## botCollector  
This program aims at verifying the accounts following a target account.
Each account that follows the target is given a score using the Botometer API.  
## Results  
Most recent plot:  
![](plots/plot.png)  
[PDF version](plots/plot.pdf)  
## References  
Botometer: https://botometer.iuni.iu.edu/#!/  
Twitter API: https://developer.twitter.com/en/docs.html  
