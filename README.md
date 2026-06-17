# Sistema de Locadora de Veículos
<p align="center">
  <img src="https://github.com/user-attachments/assets/cbebcf39-f5a1-4ede-8896-4399d3515e15" alt="Relatório Gerencial do Sistema" width="550px" />
</p>

<table align="center">
  <tr>
    <td>
      <p align="center"><b>Autenticação e Inicialização</b></p>
      <img src="https://github.com/user-attachments/assets/03d4f6af-3db2-4ac6-98f7-406d5b521171" alt="Código de Autenticação" width="350px" />
    </td>
    <td>
      <p align="center"><b>Lógica de Locação e Descontos</b></p>
      <img src="https://github.com/user-attachments/assets/c77e3bbb-13a0-4bd6-ad74-1a7e51757f18" alt="Código de Locação" width="350px" />
    </td>
  </tr>
</table>



Este projeto visa a implementação de um sistema robusto para o gerenciamento de uma locadora de veículos.
**(Projeto da disciplina de Introdução a Programação - UNIESP)**

## 👥 Equipe
* Danilo Marques Fernandes
* Gabriel Costa
* João Marcelo

## 🛠 Funcionalidades
O sistema foi projetado para atender aos seguintes requisitos:
* **Cadastros:** Gestão de veículos (código, placa, marca, modelo, quantidade, valor), clientes e colaboradores.
* **Locação:** Processo automatizado com validação de cliente e colaborador.
* **Cálculos Financeiros:**
    * **Seguro:** Adicional fixo de 25% sobre o valor bruto.
    * **Descontos Progressivos:**
        * > 5 dias: 5% de desconto.
        * > 15 dias: 10% de desconto.
        * > 30 dias: 20% de desconto.
* **Saídas:** Emissão de comprovantes detalhados e geração de relatórios gerenciais (veículos, clientes e métricas financeiras).

## 🛠 Arquitetura e Lógica do Sistema
O desenvolvimento deste sistema baseia-se em uma estrutura de classes que modela os pilares de uma locadora: Veículos, Clientes e Colaboradores. 

* **Lógica de Negócios:** O sistema aplica uma regra de cálculo em cascata. O valor total é determinado pelo período de locação, acrescido de uma taxa fixa de 25% referente ao seguro.
* **Gestão de Descontos:** A aplicação de descontos é automatizada por meio de condicionais (if/else) que avaliam o tempo de permanência, garantindo que a regra de descontos progressivos (5%, 10% ou 20%) seja aplicada com precisão matemática sobre o subtotal.
* **Persistência de Dados:** O sistema foi projetado para manter a integridade dos dados durante a geração de comprovantes e relatórios, garantindo que o histórico de locações e o estado atual da frota (disponível ou locado) sejam consultáveis em tempo real.

## 🚀 Como Executar
1. Clone este repositório.
2. ```bash
git clone [https://github.com/daniloofrs/locadora-veiculos-python.git](https://github.com/daniloofrs/locadora-veiculos-python.git)
cd locadora-veiculos-python
3. Certifique-se de ter o ambiente configurado para **Python**.
4. Talvez no seu sistema não tenha algumas bibliotecas, será preciso instalá-las. Para um tutorial. Basta ir para a seção **📥 Instalação de Dependências**

### 📥 Instalação de Dependências
Para instalar as bibliotecas necessárias para o funcionamento do projeto, utilize o terminal do VS Code:

1. **Comando padrão:**
   ```bash
   pip install nome-da-biblioteca

2. **Comando Alternativo:**
   ```bash
   python -m pip install nome-da-biblioteca




