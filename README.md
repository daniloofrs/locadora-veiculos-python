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

Projeto desenvolvido em Python para a disciplina de Introdução à Programação (UNIESP). O programa roda no terminal e simula as operações diárias de atendimento de uma locadora de carros.

## Equipe
* Danilo Marques Fernandes
* Gabriel Costa
* João Marcelo

## O que o sistema faz
* Cadastra e consulta veículos (código, placa, marca, modelo, estoque e valor da diária), clientes e colaboradores.
* Realiza locações associando o cliente ao colaborador e ao veículo escolhido.
* Calcula o custo total com seguro fixo de 25% sobre as diárias.
* Aplica descontos automáticos conforme a duração:
  * Acima de 5 dias: 5% de desconto
  * Acima de 15 dias: 10% de desconto
  * Acima de 30 dias: 20% de desconto
* Emite recibo ao finalizar a locação e gera relatórios com status da frota e balanço financeiro da sessão.

## Estrutura do código
O programa utiliza orientação a objetos para organizar as entidades do negócio (`Veiculo`, `Cliente` e `Colaborador`). As regras de negócio e cálculo de descontos são calculadas no momento do fechamento da locação, atualizando a disponibilidade dos veículos na sessão.

## Como Executar

### Pré-requisitos
* Python 3 instalado

### Passo a passo
1. Clone o repositório:
   ```bash
   git clone https://github.com/daniloofrs/locadora-veiculos-python.git
   cd locadora-veiculos-python
   ```

2. (Opcional) Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
   # Windows:
   .\venv\Scripts\activate
   # Linux/macOS:
   source venv/bin/activate
   ```

3. Instale as dependências (se houver arquivo `requirements.txt`):
   ```bash
   pip install -r requirements.txt
   ```

4. Execute o sistema:
   ```bash
   python main.py
   ```
