# **Saudações, invocador! A partir de hoje eu serei seu guia**

Criei esse programa inspirado nos *personal gaming coaches* já existentes e conhecidos pela comunidade de *League of Legends* com o intuito de desenvolver 
as minhas habilidades como programador! Portanto, não é um produto e sim o resultado de muito esforço e pesquisa de um aluno curioso. A ideia é ir aperfeiçoando
ele ao longo do tempo conforme vou aprofundando o meu conhecimento na área.  
### **Como usar**  
Dentro da pasta **dist/gui_main existe um executável de nome gui_main** o qual irá abrir uma janela solicitando o nome de um Campeão existente no jogo (ex.: Leona). Insira
e clique no botão de busca ao lado.
Feito isso, irá abrir outra janela com todos os itens recomendados do herói que você solicitou! 😉  
Há, também, um menu em cima com a opção de Manutenção onde pode ser realizada a atualização do banco de dados a fim de atualizar a lista de recomendações,
no entanto, esta opção apenas funcionará se você tiver acesso a uma chave da API da RIOT GAMES cadastrada.

### **Problemas com a API da RIOT GAMES**
A princípio foi bem mais tranquilo do que imaginei que seria trabalhar com uma API para desenvolver um programa, no entanto, o fato da chave expirar a cada 
24 horas e ter uma limitação de 20 requests por segundo e 100 requests a cada dois minutos, fez com que o tempo de retirada dos dados das partidas ficasse
bastante longo.  
Mais sobre a api você pode encontrar em 
https://developer.riotgames.com/  

### **Considerações** 
Na criação do projeto foram usados Python, Banco de dados, a api da riot games, interface gráfica Tkinter.  
Mais uma vez, é importante salientar que esta solução foi criada com o intuito de estudo e desenvolvimento pessoal.
