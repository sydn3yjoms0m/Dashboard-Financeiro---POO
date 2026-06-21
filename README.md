# Dashboard Financeiro 📈

O projeto é um aplicativo desktop de controle financeiro pessoal desenvolvido em Python. Ele adota um design moderno, escuro e totalmente responsivo de três colunas, focado em separar o fluxo de caixa entre receitas e despesas para uma análise visual precisa e em tempo real.

---

## 🚀 Funcionalidades Principal

* **Dashboard em Resolução Nativa:** O aplicativo se adapta automaticamente ao tamanho do monitor do usuário, distribuindo os componentes de forma proporcional.
* **Top Cards de Métricas:** Visualização rápida e centralizada do Saldo Atual, Total de Entradas e Total de Gastos.
* **Fluxo de Caixa Separado:** Duas colunas dedicadas para inserção de dados, separando os formulários e análises de receitas e despesas.
* **Gráficos de Pizza Duplos (Matplotlib):** * Gráfico 1: Aproveitamento das Receitas (Sobra em Caixa vs. Gastos).
  * Gráfico 2: Distribuição de Despesas categorizadas por tipo (Alimentação, Moradia, Lazer, etc.).
* **Histórico Geral:** Lista dinâmica e rolável com numeração de linhas e suporte para exclusão de registros por índice.
* **Persistência de Dados:** Salvamento e carregamento automático em tempo real utilizando arquivos estruturados JSON.

---

## 🧱 Conceitos de POO Aplicados

O projeto foi estruturado utilizando os quatro pilares da **Programação Orientada a Objetos**, garantindo um código modular, escalável e de fácil manutenção:

### 1. Abstração
A classe base `Transacao` (presente em `modelos.py`) foi definida como uma classe abstrata utilizando o módulo nativo `abc`. Ela funciona como um molde obrigatório, definindo que toda movimentação financeira precisa ter uma descrição, uma categoria, um valor e um método para calcular seu impacto.

### 2. Herança
As classes `Entrada` e `Despesa` herdam diretamente as propriedades e atributos da classe mãe `Transacao`. Isso evita a duplicação de código e estabelece uma relação clara de especialização (uma Entrada *é uma* Transação).

### 3. Encapsulamento
O atributo de valor das transações (`__valor`) foi protegido usando o modificador privado (duplo sublinhado). O acesso e a modificação desse dado são controlados estritamente por propriedades (`@property` e `@valor.setter`), o que impede que o saldo seja alterado por valores inválidos (como números negativos ou zero).

### 4. Polimorfismo
O método abstrato `calcular_impacto()` é implementado de formas diferentes pelas classes filhas. Enquanto a classe `Entrada` retorna o valor positivo (somando ao caixa), a classe `Despesa` retorna o valor negativo (subtraindo do caixa). A classe `Carteira` consegue varrer toda a lista de transações e calcular o saldo final chamando o mesmo método, sem precisar saber explicitamente o tipo de cada objeto.

### 5. Composição / Associação
A classe `Carteira` possui uma relação de composição com as transações, gerenciando uma lista de objetos na memória, centralizando os cálculos matemáticos do aplicativo e servindo de ponte para a camada de persistência.

---

## 📁 Estrutura do Projeto

Para garantir a separação de responsabilidades, o código foi dividido em três arquivos:

* `modelos.py`: Contém as regras de negócio puras e a estrutura das classes de POO.
* `json_gerente.py`: Responsável exclusivamente pelo mapeamento dos objetos, salvamento e leitura do arquivo JSON.
* `app.py`: Camada visual e interface gráfica desenvolvida em `CustomTkinter` integrada com o `Matplotlib`.

---

## 🛠️ Como Executar o Projeto

### Pré-requisitos
Certifique-se de ter o Python 3 instalado em sua máquina. 

### Primeiro método

### 1. Clonar o repositório
git clone https://github.com/sydn3yjoms0m/Dashboard-Financeiro---POO.git
cd Dashboard-Financeiro---POO

### 2. Executar o app.exe
Dentro da pasta `app_empacotado` tem todas as dependências empacotados para executar o aplicativo e 
dentro da pasta `dist/app` há um executável que pode ser aberto para executar a aplicação diretamente em seu computador.

### Segundo método

### 1. Clonar o repositório
git clone https://github.com/sydn3yjoms0m/Dashboard-Financeiro---POO.git
cd Dashboard-Financeiro---POO

### 3. Instalar as dependências externas
Este projeto utiliza duas bibliotecas externas principais para a interface e gráficos:
pip install customtkinter matplotlib

### 4. Rodar a aplicação
Execute o arquivo principal da interface:
python app.py



