# Projeto Recomendação de vídeos do Youtube
Projeto de recomendação de vídeos do youtube com assuntos sobre data-science e machine learning.

Desenvolvido em quatro etapas:

1. Definição do Problema
2. Preparação dos Dados
3. Modelagem
4. Deploy

Foi utilizado alguns modelos para comparação de resultado e algumas técnicas como active learning. Entre os modelos estão Random Forest, LightGBM e Regressão Logistíca.

No deploy foi utilizado Flask (de maneira básica, apenas para demonstração) e Docker para utilizar o conceito de container para colocar em produção.

O resultado final da primeira versão você pode ver clicando [aqui](https://sleepy-river-48950.herokuapp.com/).

2ª versão:
1. Os dados antes armazenados em arquivos, agora estão sendo armazenados em uma banco de dados (SQLite3)
2. A parte do html foi separada em novos arquivos para melhor organização
3. Foi criado um novo visual mais agradável.

O resultado final da segunda versão você pode ver clicando [aqui](https://still-reaches-80354.herokuapp.com/).
