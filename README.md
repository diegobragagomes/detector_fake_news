# Projeto Fake News Detection

## Descrição Inicial

Neste projeto se procurou cobrir todas as etapas de um projeto real de Data Science, desde o entendimento do problema, ideação da solução, análise, etapas de machine learning. O cerne da proposta do projeto é a detecção de fake news em notícias, via texto. A pergunta que gera todo o projeto é:

- É possível definir se determinado texto é uma fake news ou não?

Ao final do projeto, um modelo de predição, baseado em classificação, é disponibilizado para a verificação se determinado texto é potencialmente uma fake news ou não, a partir da combinação do título do texto e o corpo do texto em si.

Para resolver esse problema foi construído uma solução completa para armazenamento, gestão e automatização de fluxos de dados utilizando tecnologias como **Apache Airflow, Docker e MinIO**, além de explorar uma suíte poderosa de tecnologias para trabalhar com Análise de Dados e Machine Learning que são: **Pandas, Scikit-learn, Pycaret**.

A escolha do **Apache Airflow** foi devido ao seu poder de orquestração, uma automatização, dos processos de extração e pequenas transformações nos arquivos se mostrava interessante.

Em relação ao **Docker e MinIO**, ambos serviram como ferramentas para a configuração ideal para auxiliar o manejo dos arquivos e sua orquestração. Um dando possibilidade do **MinIO*** e **Airflow** funcionarem de forma adequada, graças ao seu poder de compartimentalização, enquanto o outro foi responsável pela criação de um Data Lake, onde os arquivos ficaram dispostos e foram acionados nos momentos necessários.

Para as etapas de análise e Machine Learning, utilizou-se extensamente as possibilidades das bibliotecas **Pandas**, passando pelo entendimento dos dados, através dos dataframes, transformações nesses dados. Houve, ainda, o uso do **PyCaret**, ferramenta interessante no que tange o AutoML (processos de machine learning mais automatizados), no qual pude comparar diversos algoritmos de machine learning de maneira bastante ágil e prática.

## Etapas do Projeto

Os arquivos estavam inicialmente disposto no formotato .csv, contendo, ao todo, dois arquivos, Fake.csv e True.csv.

Foram criadas Dags para serem empregadas pelo **Airflow**, nas quais elas liam os arquivos no **Minio**, depois faziam suas transformações e retornavam os novos arquivos ao **MinIO**. Por fim, com um arquivo transformado e único, esse foi aproveitado na etapa de Análise Exploratória.

O principal ponto dessa etapa é a automatização da leitura e transoformação desses dados, como criação de colunas e junção dos dois arquivos, isso tudo sendo extraído e enviado ao MinIO para que pudesse ser armazenado no Data Lake e requisitado quando necessário.

**Etapa de NLP**

Nessa etapa, utilizou-se o PyCaret para ler os dados do dataframe final e começar o pré-processamaneto, a partir do pycaret.nlp. Esse pré-processamento conta com a retirada de caracteres especiais e numéricos, a tokenização, o stemming e a lematização, retirando-se ainda as stopwords padrões da lingua inglesa. 

Seguindo-se, o PyCaret permite utilizar para a modelagem de NLP, as técnicas de modelagem em tópicos, a fim de extrair tópicos de uma grande gama de documentos. Para a realização dessa tarefa, foram selecionados dois modelos dentre os possíveis, **Latent Dirichlet Allocation (LDA) e o Non-Negative matrix factorization (NMF)**, sendo o primeiro deles um modelo probabilístico e o segundo uma técnica de análise multivariada.

Ao final, um dataframe contendo os tópicos e a coluna *Status* criada manualmente, que servirá como target, é gerado. Esse dataframe servirá como base para os modelos de classificação, sendo os tópicos as features numéricas que auxiliarão na determinação da classificação dos Status.

**Etapa de Classificação**

Após a etapa de NLP, ainda utilizando o **PyCaret** foram realizadas comparações entre diversos modelos. Foram selecionados os modelos: **Extra Trees Classifier e Random Forest Classifier**. Essa escolha é devido aos dois possuírem os maiores valores de precisão. A precisão foi escolhida como métrica principal porque um Falso Positivo geraria um custo, em termos monetários ou informativos, muito maiores que um falso negativo.

Com isso, combinei os dois modelos, através de um blend model. O modelo com maior precisão, foi o modelo utilizando **NMF** e o blend de Extra Trees e Random Forest. O valor da **Precisão foi de 0.93**. Por fim, persisti o modelo em disco e o enviei ao MinIO.

## Conclusão

Através desse projeto foi possível praticar e implementar conceitos importantes da Ciência e Engenharia de Dados e propor uma solução para um problema latente e recorrente do meio jornalístico e mídias sociais.

Em relação a futuras melhoriais, destacaria a criação de um deploy utilizando o **Flask**, que permitisse fugir do problema do **Gradio**, que utilizando conjuntamente com o **PyCaret**, tem como determinação da classificaçaõ os Tópicos, que se torna zero intuitivo para o usuário. Além disso, a extensão da automatização do AutoML com o **Airflow** se mostra interessante.



