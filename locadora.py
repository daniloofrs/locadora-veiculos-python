import questionary
import pyfiglet
import time
import os
from datetime import datetime
from colorama import Style,Fore

largura = os.get_terminal_size().columns


def texto_especial(texto):
    textoes = pyfiglet.figlet_format(texto)
    print(textoes)



def boas_vindas():
    apagar()
    texto_especial("SISTEMA")
    time.sleep(0.2)
    agora = datetime.now()
    texto = pyfiglet.figlet_format(agora.strftime("%H:%M"))
    apagar()
    print(Fore.GREEN + texto + Fore.RESET)
    time.sleep(0.4)
    apagar()




def apagar():
    os.system("cls" if os.name == "nt" else "clear")




def inicializar():
    apagar()
    print(f"{Style.BRIGHT}Seja bem-vindo a Locadora de Veículos!\n{Style.RESET_ALL}".center(largura))
    while True:
        entrada = questionary.select("Selecione seu tipo de usuário:",choices=["Clientes",
                                                                    "Colaborador"],
                                                                    qmark="",
                                                                    instruction=" "
                                                                    ).ask()
        
        if entrada == "Clientes":
            return "clientes"
        elif entrada == "Colaborador":
            return "colaborador"
            
        else:
            continue
    



def autenticar_usuario(texto):
    apagar()
    ent_usuario = questionary.text("Digite seu nome de usuário: ").ask()
    apagar()
    ent_senha = questionary.password("Digite sua senha: ").ask()

    sucesso = False
    with open(texto,"r") as arquivo:
        for linha in arquivo:
            dados = linha.strip().split(",")

            if len(dados) == 2:
                usuario_salvo, senha_salva = dados


            if ent_usuario == usuario_salvo and ent_senha == senha_salva:
                sucesso = True
                return usuario_salvo, sucesso
    if sucesso:
        print("Acesso liberado!")
    else:
        print("Usuário ou senha incorretos.")
        sucesso = False
        return None, sucesso    




def locacao():
    apagar()
    print(f"{Style.BRIGHT}----- Locação de Veículo -----{Style.RESET_ALL}".center(largura))
    print(Fore.BLUE + ("=" * largura) + "\n" + Fore.RESET)


    veiculos = []


    with open("banco-de-dados/veiculos.txt","r",encoding="utf-8") as arquivo:
        for linha in arquivo:
            dados = linha.strip().split(",")


            veiculo = {
                "codigo": dados[0],
                "placa": dados[1],
                "marca": dados[2],
                "modelo": dados[3],
                "quantidade": int(dados[4]),
                "valor": float(dados[5])
            }       

            veiculos.append(veiculo)


    disponiveis = []

    for veiculo in veiculos:
        if veiculo["quantidade"] > 0:
            disponiveis.append(veiculo)

    
    if len(disponiveis) == 0:
        print("Nenhum veículo disponível.")
        return
    

    print(f"{Style.BRIGHT}{Fore.CYAN}Veículos Disponíveis:\n{Style.RESET_ALL}{Fore.RESET}")
    time.sleep(0.5)


    for veiculo in disponiveis:
        print(
            f"Código: {veiculo['codigo']} | "
            f"{veiculo['marca']} {veiculo['modelo']} | "
            f"R$: {veiculo['valor']:.2f}",
        )
        time.sleep(0.05)

    codigo = questionary.text("\nDigite o código do veículo: ", qmark="").ask()

    encontrado = None


    for veiculo in disponiveis:
        if veiculo["codigo"]  == codigo:
            encontrado = veiculo
            print(f"Sua escolha foi {veiculo["marca"]} {veiculo['modelo']}",
                  f"VALOR: {veiculo["valor"]}")
            return encontrado
            break

    if encontrado is None:
        print("Veículo não encontrado.")
        return
    



def cliente():
    cliente, sucesso = autenticar_usuario("banco-de-dados/clientes.txt")
    if sucesso:
        apagar()
        print(f"{Fore.GREEN}CLIENTE {cliente.upper()} SELECIONADO\n{Fore.RESET}".center(largura))
        entrada = questionary.select("SELECIONE OQUE DESEJA FAZER:",choices=["Locação de Veículo",
                                                                         "ADICIONAR MAIS COISAS DEPOIS"]).ask()
        

        if entrada == "Locação de Veículo":
            locacao()

        elif entrada == "ADICIONAR MAIS COISAS DEPOIS":
            print("Ainda não fizemos essa parte!")
            input()



def colaborador():
    colaborador, sucesso = "danilo",True #autenticar_usuario("banco-de-dados/colaborador.txt")

    if sucesso:
        apagar()
        print(f"{Fore.GREEN}COLABORADOR {colaborador.upper()} SELECIONADO\n{Fore.RESET}".center(largura))
        entrada = questionary.select("SELECIONE OQUE DESEJA FAZER:",choices=["Cadastrar Cliente",
                                                                         "Cadastrar Colaborador",
                                                                         "Cadastrar Veículo"]).ask()
        
        if entrada == "Cadastrar Cliente":
            cadastrar_cliente()

        elif entrada == "Cadastrar Colaborador":
            cadastrar_colaborador()

        elif entrada == "Cadastrar Veículo":
            cadastro_veiculos()




def cadastrar_cliente():
    apagar()
    print(f"{Style.BRIGHT}--- Cadastro de Novo Cliente ---{Style.RESET_ALL}".center(largura))

    ccliente = questionary.text("Digite o nome de usuário do cliente: ").ask()
    apagar()
    csenha = questionary.password("Digite uma nova senha: ").ask()

    linha = f"{ccliente},{csenha}\n"

    try:
        with open("banco-de-dados/clientes.txt","a", encoding="utf-8") as arquivo:
            arquivo.write(linha)
            arquivo.flush()
            os.fsync(arquivo.fileno())
        apagar()
        print(f"{Fore.GREEN}Cliente Cadastrado com Sucesso! {os.path.abspath("banco-de-dados/clientes.txt")}{Fore.RESET}")
    except Exception as e:
        print(f"{Fore.RED}Erro ao salvar: {e}{Fore.RESET}")
        input("Pressione Qualquer Tecla para Continuar: ")


def cadastrar_colaborador():
    apagar()
    print(f"{Style.BRIGHT}--- Cadastro de Novo Colaborador ---{Style.RESET_ALL}".center(largura))

    ccolaborador = questionary.text("Digite o nome de usuário do colaborador: ").ask()
    apagar()
    csenha = questionary.password("Digite uma nova senha: ").ask()


    linha = f"{ccolaborador},{csenha}\n"

    try: 
        with open("banco-de-dados/colaborador.txt","a",encoding="utf-8") as arquivo:
            arquivo.write(linha)
            arquivo.flush()
            os.fsync(arquivo.fileno())
        apagar()
        print(f"{Fore.GREEN}Colaborador Cadastrado com Sucesso! {os.path.abspath("banco-de-dados/colaborador.txt")}{Fore.RESET}")
    except Exception as e:
        print(f"{Fore.RED} Erro ao salvar; {e}{Fore.RESET}")
        input("Pressione Qualquer Tecla para Continuar: ")


def cadastro_veiculos():
    apagar()
    print(f"{Style.BRIGHT}--- Cadastro de Novo Veículo ---{Style.RESET_ALL}".center(largura))

    codigo = input("Código: ")
    placa = input("Placa: ")
    marca = input("Marca: ")
    modelo = input("Modelo: ")
    quantidade = input("Quantidade: ")
    valor_aluguel = input("Valor do Aluguel: ")

    linha = f"{codigo},{placa},{marca},{modelo},{quantidade},{valor_aluguel}\n"

    try:
        with open("banco-de-dados/veiculos.txt", "a", encoding="utf-8") as arquivo:
            arquivo.write(linha)
            arquivo.flush()
            os.fsync(arquivo.fileno())
        apagar()    
        print(f"{Fore.GREEN}Veículo Cadastrado com Sucesso! {os.path.abspath('banco-de-dados/veiculos.txt')}{Fore.RESET}")
        time.sleep(1.5)    
    except Exception as e:
        print(f"{Fore.RED}Erro ao salvar: {e}{Fore.RESET}")
        input("Pressione Qualquer Tecla para Continuar: ")


def main():



    boas_vindas()
    inicial = inicializar()
    if inicial == "clientes":
        cliente()
        
    elif inicial == "colaborador":
        colaborador()


if __name__ == "__main__":
   main()



