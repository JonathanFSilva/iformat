# IFormat : 
### FERRAMENTA DE APOIO A FORMATAÇÃO DE TRABALHOS ACADÊMICOS

Sistema web para formatação de trabalhos ciêntíficos seguindo as normas da ABNT. A versão atual conta apenas com o trabalho de Monografia (TCC), seguindo os padrões do Instituto Federal de Educação Ciência e Tecnologia do Sul de Minas Gerais campus Muzambinho.

![Página Inicial do Sistema](https://lh3.googleusercontent.com/LHsBzsCVcxeI77E-YcDpw1MvtZdyjuC2qTJQYXZ9IsdvgHZ3T22klntprjXVJf5p051nqqgCtqTFZw=w1920-h979)

## Instalação

1.  Clone este repositório: `$ git clone git@github.com:JonathanFSilva/iformat.git`. 
2.  Crie um virtual env com python-3.6.2: 
	* `$ pip install virtualenv`
	* `$ virtualenv -p /usr/bin/python3 venv`
3. Ative o virtualenv: `source venv/bin/activate`
4. Instale as dependências: `$ pip install -r requirements.txt`
5. Execute o projeto: `$ python manage.py runserver`