import questionary
import pyfiglet
import time
import os
import shutil
from datetime import datetime
from colorama import Style,Fore

largura = shutil.get_terminal_size((80, 20)).columns


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

def formatar_moeda(valor):
    valor_str = f"{valor:,.2f}"
    return valor_str.replace(",", "X").replace(".", ",").replace("X", ".")




def inicializar():
    apagar()
    print(f"{Style.BRIGHT}Seja bem-vindo a Locadora de Veículos!\n{Style.RESET_ALL}".center(largura))
    while True:
        entrada = questionary.select("Selecione seu tipo de usuário:",choices=["Clientes",
                                                                    "Colaborador",
                                                                    "Sair"],
                                                                    qmark="",
                                                                    instruction=" "
                                                                    ).ask()
        
        if entrada == "Clientes":
            return "clientes"
        elif entrada == "Colaborador":
            return "colaborador"
        elif entrada == "Sair" or entrada is None:
            return "sair"
        else:
            continue
    

def autenticar_usuario(texto):
    apagar()
    ent_usuario = questionary.text("Digite seu código de usuário: ").ask()
    apagar()
    ent_senha = questionary.password("Digite sua senha: ").ask()

    sucesso = False
    nome_usuario = ""
    
    if not os.path.exists(texto):
        print("Nenhum registro encontrado no banco de dados.")
        time.sleep(1.5)
        return None, False

    with open(texto,"r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            dados = linha.strip().split(",")

            if len(dados) >= 3:
                usuario_salvo, nome_salvo, senha_salva = dados[0], dados[1], dados[2]
            elif len(dados) == 2:
                usuario_salvo, senha_salva = dados[0], dados[1]
                nome_salvo = usuario_salvo
            else:
                continue

            if ent_usuario == usuario_salvo and ent_senha == senha_salva:
                sucesso = True
                nome_usuario = nome_salvo
                return nome_usuario, sucesso
    if sucesso:
        print("Acesso liberado!")
    else:
        print("Usuário ou senha incorretos.")
        time.sleep(1.5)
        sucesso = False
        return None, sucesso    


def locacao(cliente_nome, colab_nome):
    apagar()
    print(f"{Style.BRIGHT}----- Locação de Veículo -----{Style.RESET_ALL}".center(largura))
    print(Fore.BLUE + ("=" * largura) + "\n" + Fore.RESET)


    veiculos = []

    if not os.path.exists("banco-de-dados/veiculos.txt"):
        print("Nenhum veículo cadastrado.")
        time.sleep(1.5)
        return

    with open("banco-de-dados/veiculos.txt","r",encoding="utf-8") as arquivo:
        for linha in arquivo:
            dados = linha.strip().replace(";", ",").split(",")
            if len(dados) >= 6:
                veiculo = {
                    "codigo": dados[0],
                    "placa": dados[1],
                    "marca": dados[2],
                    "modelo": dados[3],
                    "quantidade": int(dados[4]),
                    "valor": float(dados[5])
                }       
                veiculos.append(veiculo)

    disponiveis = [v for v in veiculos if v["quantidade"] > 0]
    
    if len(disponiveis) == 0:
        print("Nenhum veículo disponível.")
        input("\nPressione Enter para voltar.")
        return
    
    print(f"{Style.BRIGHT}{Fore.CYAN}Veículos Disponíveis:\n{Style.RESET_ALL}{Fore.RESET}")

    for veiculo in disponiveis:
        print(
            f"Código: {veiculo['codigo']} | "
            f"{veiculo['marca']} {veiculo['modelo']} | "
            f"R$ {formatar_moeda(veiculo['valor'])}/dia"
        )
        time.sleep(0.05)

    codigo = questionary.text("\nDigite o código do veículo: ", qmark="").ask()

    encontrado = None
    for veiculo in disponiveis:
        if veiculo["codigo"]  == codigo:
            encontrado = veiculo
            break

    if encontrado is None:
        print("Veículo não encontrado.")
        time.sleep(1.5)
        return
        
    print(f"\nSua escolha foi {encontrado['marca']} {encontrado['modelo']} - VALOR: R$ {formatar_moeda(encontrado['valor'])}/dia")
    
    try:
        dias = int(questionary.text("Digite a quantidade de dias de locação: ").ask())
    except ValueError:
        print("Quantidade inválida.")
        time.sleep(1.5)
        return

    diaria = encontrado["valor"]
    valor_locacao = diaria * dias
    seguro = valor_locacao * 0.25
    
    desconto = 0
    if dias > 30:
        desconto = valor_locacao * 0.20
    elif dias > 15:
        desconto = valor_locacao * 0.10
    elif dias > 5:
        desconto = valor_locacao * 0.05

    valor_final = valor_locacao + seguro - desconto

    apagar()
    print("\nGerando comprovante...")
    time.sleep(1.5)

    print("\n" + "="*20 + " COMPROVANTE " + "="*20)
    print(f"Cliente: {cliente_nome}")
    print(f"Colaborador: {colab_nome}")
    
    print(f"\n[Dados do Veículo]")
    print(f"Marca/Modelo: {encontrado['marca']} {encontrado['modelo']}")
    print(f"Placa: {encontrado['placa']}")
    
    print(f"\n[Detalhes Financeiros]")
    print(f"Valor unitário do aluguel: R$ {formatar_moeda(diaria)}")
    print(f"Dias locados: {dias}")
    print(f"Valor total do aluguel: R$ {formatar_moeda(valor_locacao)}")
    print(f"Valor do seguro (25%): R$ {formatar_moeda(seguro)}")
    
    if desconto > 0:
        print(f"Desconto aplicado: R$ {formatar_moeda(desconto)}")
        
    print(f"\nValor total da locação (com desconto, se houver): R$ {formatar_moeda(valor_final)}")
    print("="*53)

    os.makedirs("banco-de-dados", exist_ok=True)
    with open("banco-de-dados/locacoes.txt", "a", encoding="utf-8") as f:
        f.write(f"{cliente_nome},{colab_nome},{encontrado['placa']},{dias},{valor_locacao:.2f},{seguro:.2f},{desconto:.2f},{valor_final:.2f}\n")

    for v in veiculos:
        if v["codigo"] == encontrado["codigo"]:
            v["quantidade"] -= 1

    with open("banco-de-dados/veiculos.txt", "w", encoding="utf-8") as f:
        for v in veiculos:
            f.write(f"{v['codigo']},{v['placa']},{v['marca']},{v['modelo']},{v['quantidade']},{v['valor']:.2f}\n")

    input("\nPressione Enter para continuar...")


def cliente():
    cliente_nome, sucesso = autenticar_usuario("banco-de-dados/clientes.txt")
    if sucesso:
        while True:
            apagar()
            print(f"{Fore.GREEN}CLIENTE {cliente_nome.upper()} SELECIONADO\n{Fore.RESET}".center(largura))
            entrada = questionary.select("SELECIONE O QUE DESEJA FAZER:",choices=["Ver Veículos Disponíveis", "Sair"]).ask()
            
            if entrada == "Ver Veículos Disponíveis":
                apagar()
                print(f"{Style.BRIGHT}{Fore.CYAN}--- Veículos Disponíveis ---{Fore.RESET}{Style.RESET_ALL}")
                if os.path.exists("banco-de-dados/veiculos.txt"):
                    with open("banco-de-dados/veiculos.txt","r",encoding="utf-8") as arquivo:
                        for linha in arquivo:
                            dados = linha.strip().replace(";", ",").split(",")
                            if len(dados) >= 6 and int(dados[4]) > 0:
                                print(f"Marca: {dados[2]} | Modelo: {dados[3]} | R$ {formatar_moeda(float(dados[5]))}/dia")
                else:
                    print("Nenhum veículo cadastrado.")
                input("\nPressione Enter para voltar...")

            elif entrada == "Sair" or entrada is None:
                break


def colaborador():
    if not os.path.exists("banco-de-dados/colaborador.txt"):
        os.makedirs("banco-de-dados", exist_ok=True)
        with open("banco-de-dados/colaborador.txt", "w", encoding="utf-8") as f:
            f.write("admin,Administrador,admin\n")
        print("Nenhum colaborador encontrado. Criado usuário padrão -> Código: admin, Senha: admin")
        time.sleep(2)

    colab_nome, sucesso = autenticar_usuario("banco-de-dados/colaborador.txt")

    if sucesso:
        while True:
            apagar()
            print(f"{Fore.GREEN}COLABORADOR {colab_nome.upper()} SELECIONADO\n{Fore.RESET}".center(largura))
            entrada = questionary.select("SELECIONE O QUE DESEJA FAZER:", choices=[
                "Realizar Locação",
                "Cadastrar Cliente",
                "Cadastrar Colaborador",
                "Cadastrar Veículo",
                "Gerar Relatório",
                "Sair"
            ]).ask()
            
            if entrada == "Realizar Locação":
                if not os.path.exists("banco-de-dados/clientes.txt"):
                    print("Nenhum cliente cadastrado. Cadastre um cliente primeiro.")
                    time.sleep(2)
                    continue
                
                clientes = []
                with open("banco-de-dados/clientes.txt", "r", encoding="utf-8") as f:
                    for linha in f:
                        dados = linha.strip().split(",")
                        if len(dados) >= 2:
                            nome = dados[1] if len(dados) >= 3 else dados[0]
                            clientes.append({"codigo": dados[0], "nome": nome})
                
                if not clientes:
                    print("Nenhum cliente cadastrado.")
                    time.sleep(2)
                    continue

                escolhas = [f"{c['codigo']} - {c['nome']}" for c in clientes]
                escolhas.append("Cancelar")
                
                cliente_escolhido = questionary.select("Selecione o Cliente:", choices=escolhas).ask()
                if cliente_escolhido != "Cancelar":
                    nome_c = cliente_escolhido.split(" - ")[1]
                    locacao(nome_c, colab_nome)

            elif entrada == "Cadastrar Cliente":
                cadastrar_cliente()

            elif entrada == "Cadastrar Colaborador":
                cadastrar_colaborador()

            elif entrada == "Cadastrar Veículo":
                cadastro_veiculos()

            elif entrada == "Gerar Relatório":
                gerar_relatorio()

            elif entrada == "Sair" or entrada is None:
                break


def cadastrar_cliente():
    apagar()
    print(f"{Style.BRIGHT}--- Cadastro de Novo Cliente ---{Style.RESET_ALL}".center(largura))

    ccodigo = questionary.text("Digite o código do cliente: ").ask().replace(",", "")
    cnome = questionary.text("Digite o nome do cliente: ").ask().replace(",", "")
    csenha = questionary.password("Digite uma nova senha: ").ask().replace(",", "")

    linha = f"{ccodigo},{cnome},{csenha}\n"

    os.makedirs("banco-de-dados", exist_ok=True)
    try:
        with open("banco-de-dados/clientes.txt","a", encoding="utf-8") as arquivo:
            arquivo.write(linha)
            arquivo.flush()
            os.fsync(arquivo.fileno())
        apagar()
        print(f"{Fore.GREEN}Cliente Cadastrado com Sucesso!{Fore.RESET}")
        time.sleep(1.5)
    except Exception as e:
        print(f"{Fore.RED}Erro ao salvar: {e}{Fore.RESET}")
        input("Pressione Qualquer Tecla para Continuar: ")


def cadastrar_colaborador():
    apagar()
    print(f"{Style.BRIGHT}--- Cadastro de Novo Colaborador ---{Style.RESET_ALL}".center(largura))

    ccodigo = questionary.text("Digite o código do colaborador: ").ask().replace(",", "")
    cnome = questionary.text("Digite o nome do colaborador: ").ask().replace(",", "")
    csenha = questionary.password("Digite uma nova senha: ").ask().replace(",", "")

    linha = f"{ccodigo},{cnome},{csenha}\n"

    os.makedirs("banco-de-dados", exist_ok=True)
    try: 
        with open("banco-de-dados/colaborador.txt","a",encoding="utf-8") as arquivo:
            arquivo.write(linha)
            arquivo.flush()
            os.fsync(arquivo.fileno())
        apagar()
        print(f"{Fore.GREEN}Colaborador Cadastrado com Sucesso!{Fore.RESET}")
        time.sleep(1.5)
    except Exception as e:
        print(f"{Fore.RED} Erro ao salvar; {e}{Fore.RESET}")
        input("Pressione Qualquer Tecla para Continuar: ")


def cadastro_veiculos():
    apagar()
    print(f"{Style.BRIGHT}--- Cadastro de Novo Veículo ---{Style.RESET_ALL}".center(largura))

    codigo = questionary.text("Código: ").ask().replace(",", "")
    placa = questionary.text("Placa: ").ask().replace(",", "")
    marca = questionary.text("Marca: ").ask().replace(",", "")
    modelo = questionary.text("Modelo: ").ask().replace(",", "")
    quantidade = questionary.text("Quantidade: ").ask()
    valor_aluguel = questionary.text("Valor do Aluguel: ").ask()

    valor_aluguel = valor_aluguel.replace(",", ".")
    try:
        int(quantidade)
        valor_aluguel_float = float(valor_aluguel)
    except ValueError:
        print(f"{Fore.RED}A quantidade e o valor do aluguel precisam ser números.{Fore.RESET}")
        time.sleep(1.5)
        return

    linha = f"{codigo},{placa},{marca},{modelo},{quantidade},{valor_aluguel_float:.2f}\n"

    os.makedirs("banco-de-dados", exist_ok=True)
    try:
        with open("banco-de-dados/veiculos.txt", "a", encoding="utf-8") as arquivo:
            arquivo.write(linha)
            arquivo.flush()
            os.fsync(arquivo.fileno())
        apagar()    
        print(f"{Fore.GREEN}Veículo Cadastrado com Sucesso!{Fore.RESET}")
        time.sleep(1.5)    
    except Exception as e:
        print(f"{Fore.RED}Erro ao salvar: {e}{Fore.RESET}")
        input("Pressione Qualquer Tecla para Continuar: ")

def gerar_relatorio():
    apagar()
    print(f"{Style.BRIGHT}--- Relatório Gerencial ---{Style.RESET_ALL}".center(largura))
    
    veiculos = []
    if os.path.exists("banco-de-dados/veiculos.txt"):
        with open("banco-de-dados/veiculos.txt","r",encoding="utf-8") as f:
            for linha in f:
                dados = linha.strip().replace(";", ",").split(",")
                if len(dados) >= 6:
                    veiculos.append({
                        "codigo": dados[0], "placa": dados[1], "marca": dados[2], "modelo": dados[3], 
                        "quantidade": int(dados[4]), "valor": float(dados[5])
                    })
                    
    print(f"\n{Fore.CYAN}[VEÍCULOS DISPONÍVEIS]{Fore.RESET}")
    for v in veiculos:
        if v["quantidade"] > 0:
            print(f"- {v['marca']} {v['modelo']} (Placa: {v['placa']}) - Qtd Livre: {v['quantidade']}")

    total_locacoes = 0.0
    total_seguros = 0.0
    total_final = 0.0
    placas_locadas = set()

    if os.path.exists("banco-de-dados/locacoes.txt"):
        with open("banco-de-dados/locacoes.txt","r",encoding="utf-8") as f:
            for linha in f:
                dados = linha.strip().split(",")
                if len(dados) >= 8:
                    placas_locadas.add(dados[2])
                    total_locacoes += float(dados[4])
                    total_seguros += float(dados[5])
                    total_final += float(dados[7])

    print(f"\n{Fore.CYAN}[VEÍCULOS LOCADOS]{Fore.RESET}")
    for placa in placas_locadas:
        for v in veiculos:
            if v["placa"] == placa:
                print(f"- {v['marca']} {v['modelo']} (Placa: {v['placa']}) encontra-se em posse de clientes.")
                break

    print(f"\n{Fore.CYAN}[CLIENTES CADASTRADOS]{Fore.RESET}")
    if os.path.exists("banco-de-dados/clientes.txt"):
        with open("banco-de-dados/clientes.txt","r",encoding="utf-8") as f:
            for linha in f:
                dados = linha.strip().split(",")
                if len(dados) >= 2:
                    nome = dados[1] if len(dados) >= 3 else dados[0]
                    print(f"- Cód: {dados[0]} | Nome: {nome}")
                    
    print(f"\n{Fore.CYAN}[MÉTRICAS FINANCEIRAS]{Fore.RESET}")
    print(f"Total de Locações (Bruto): R$ {formatar_moeda(total_locacoes)}")
    print(f"Total de Seguros: R$ {formatar_moeda(total_seguros)}")
    print(f"Total Final (Considerando Descontos e Seguros): R$ {formatar_moeda(total_final)}")
    
    input("\nPressione Enter para voltar...")

def main():
    boas_vindas()
    while True:
        inicial = inicializar()
        if inicial == "clientes":
            cliente()
        elif inicial == "colaborador":
            colaborador()
        elif inicial == "sair":
            break

if __name__ == "__main__":
    main()