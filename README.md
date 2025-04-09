# controle de Estoque: Adega Inteligente

Este software se trata de um sistema de gerenciamento de um estoque de adega. Com a finalidade de realizar funções básicas deste tipo de estabelecimento de maneira mais prática.

## Funcionalidades

- *Visualização Geral dos Produtos*: A tela de visão geral é a primeira tela a ser aberta no momento de execução do sistema de controle de estoque, oferece uma visão geral de todos os produtos cadastrados no sistema. 
	Nesta tela de exibição há um botão de redirecionamento para cada uma das funcionalidades do projeto, além de haver um botão que realiza a exclusão total do produto selecionado pelo usuário.
	 

- *Cadastrar um Novo Produto*: Permite realizar o cadastro de um novo produto, desde que todos os dados estejam preenchidos de maneira correta na qual é necessária para que o gerenciamento do estoque seja feito adequadamente.
	As entidades nas quais é possível realizar a inserção de caracteres do tipo texto, podem ser preenchidas com todo tipo de caractere, pois muitas marcas apresentam letras e caracteres especiais em seus nomes.
	As entidades nas quais devem ser ocupadas apenas por valores numéricos,não sendo possível realizar o preenchimento com qualquer outro tipo de caractere.
 

- *Editar Produto*: Possibilita efetuar a edição dos dados principais de um determinado produto. 
As alterações neste campos devem ser feitas de maneira controlada e compatíveis com os demais dados. 
As entidades “Nome do Produto” e “Nome da Marca” podem ser preenchidas tanto com caracteres especiais quanto com números, pois existem produtos que apresentam estes tipos de caracteres em suas descrições.
A entidade “Valor” deve ser preenchida apenas com valores numéricos, sendo possível o preenchimento com números decimais, porém com uma limitação de apenas dois algarismos após a vírgula e sendo impossível realizar a edição com números negativos preenchendo este campo.


- *Visualizar Produto*:Exibe os dados de um produto de maneira única, permitindo sua visualização de maneira mais nítida . 
Também permitindo verificar o valor total em que se tem no estoque do determinado produto. 
Não podendo ser realizada nenhuma ação nesta tela além da visualização dos dados gerais do produto
 

- *Registrar Quantidade de Vendas*: Faz com que seja possível registrar a venda de vários produtos de uma única vez de maneira controlada, desde que atenda todos os padrões delimitados.
Todos os números a serem inseridos devem ser maiores ou igual a zero, também não é possível realizar a inserção de números decimais. Para que o processo ocorra corretamente não se pode registrar uma venda de produtos com o quantidade superior da qual se tem cadastrada no sistema.


- *Adicionar ao Estoque*: Permite realizar a adição de diversos produtos do estoque de uma única vez.
Para que a finalização deste processo de adição seja possível todos os números a serem inseridos devem ser maiores ou igual a zero e devem manter um padrão de números inteiros. Caso haja a tentativa de  adicionar algum valor fora do padrão, não será possível seguir com o processo.


## Tecnologias

 - [Django](https://pypi.org/project/Django/)
 - [Python](https://www.python.org/downloads/)
 - [CDN](https://getbootstrap.com/docs/5.3/getting-started/download/)
 - [SQLite](https://sqlitebrowser.org/dl/)
 - [VScode](https://code.visualstudio.com/download)
 - [HTML](https://code.visualstudio.com/docs/languages/html)
 - [JavaScript](https://code.visualstudio.com/docs/languages/javascript)
 - [DjangoModels](https://www.w3schools.com/django/django_models.php)
 

## Como Rodar o Projeto

Antes de começar, você vai precisar ter instalado em sua máquina as seguintes ferramentas:
[Git](https://git-scm.com), [python](https://www.python.org/). 
Além disto é bom ter um editor para trabalhar com o código como [VSCode](https://code.visualstudio.com/)

## Colaboradores

Agradecemos a todos os contribuidores que ajudaram a tornar este projeto possível:

- [Guilherme Rodrigues] - Contribuidor
- [João Fernandes] - Contribuidor
- [Marcel Dantas] - Contribuidor
- [Railton Rocha](https://github.com/rocha-Railton) - Contribuidor
- [Samuel Mineiro](https://github.com/SamuelMineiro) -Contribuidor

```bash

# Clone este repositório
$ git clone https://github.com/SamuelMineiro/Estoque-Inteligente.git

# Acesse a pasta do projeto no terminal/cmd 
$ cd Estoque-inteligente\venv\Scripts

# ative o ambiente virtual
$ activate

#volte a pasta raiz
$ cd ../..

# Instale as dependências
$ pip install -r requirements.txt

# Configure o Banco de dados (se necessário)
$ python manage.py migrate

# Execute o servidor
$ python manage.py runserver

# O servidor inciará na porta:8000 - acesse http://127.0.0.1:8000/
