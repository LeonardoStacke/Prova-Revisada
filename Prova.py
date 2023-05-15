
#1
def informar_rendimento():
    try:
        mes_ano = input("Digite o mês e ano (mm/aaaa): ")
        rendimento = float(input("Digite o rendimento líquido mensal: "))

        with open("rendimentos.txt", "a") as f:
            f.write(f"{mes_ano},{rendimento}\n")

    except ValueError:
        print("Valor inválido! Certifique-se de que está digitando um número para o rendimento.")

#2
def alterar_rendimento():
    try:
        mes_ano = input("Digite o mês e ano (mm/aaaa) do rendimento que deseja alterar: ")
        novo_valor = float(input("Digite o novo valor do rendimento: "))

        with open("rendimentos.txt", "r+") as f:
            linhas = f.readlines()
            f.seek(0)
            for linha in linhas:
                if linha.startswith(mes_ano):
                    f.write(f"{mes_ano},{novo_valor}\n")
                else:
                    f.write(linha)
            f.truncate()

    except ValueError:
        print("Valor inválido! Certifique-se de que está digitando um número para o rendimento.")

import os
from datetime import datetime

#3
def excluir_rendimento():

    mes = input("Digite o mês (MM) do rendimento a ser excluído: ")
    ano = input("Digite o ano (AAAA) do rendimento a ser excluído: ")

    try:
        with open('rendimentos.txt', 'r') as file:
            linhas = file.readlines()


        with open('rendimentos.txt', 'w') as file:
            excluido = False
            for linha in linhas:

                campos = linha.strip().split(',')
                data_atual = campos[0].split('/')
                mes_atual = data_atual[0]
                ano_atual = data_atual[1]

                if mes_atual != mes or ano_atual != ano:
                    file.write(linha)
                else:
                    excluido = True

            if not excluido:
                print(f"Não foi encontrado rendimento no mês {mes}/{ano}.")
            else:
                print(f"\033Rendimento do mês {mes}/{ano} excluído com sucesso.\033[0m\n")

    except FileNotFoundError:
        print("Arquivo de rendimentos não encontrado.")


#4
def listar_rendimentos():
    rendimentos = []
    with open('rendimentos.txt', 'r') as file:
        for line in file:
            line = line.strip()
            campos = line.split(',')
            if len(campos) >= 2:
                rendimentos.append(line)

    rendimentos_ordenados = sorted(rendimentos, key=lambda x: datetime.strptime(x.split(',')[0], '%m/%Y'))

    if rendimentos:
        total_rendimentos = sum(float(r.split(',')[1]) for r in rendimentos)
        print("\n\033[32m==== RENDIMENTOS ====\033[0m\n")
        for rendimento in rendimentos_ordenados:
            mes_ano, valor = rendimento.split(',')
            mes, ano = mes_ano.split('/')
            print(f"{mes}/{ano}: R${valor}")
        print(f"Total: R${total_rendimentos:.2f}")
    else:
        print("Não há rendimentos registrados.")


#5
def informar_despesa():
    mes_ano = input("Digite o mês e ano da despesa (MM/AAAA): ")
    descricao = input("Digite a descrição da despesa: ")
    valor = float(input("Digite o valor da despesa: "))

    try:
        with open("rendimentos.txt", "r+") as f:
            linhas = f.readlines()
            f.seek(0)
            for linha in linhas:
                data, saldo_mes = linha.strip().split(',')
                saldo_mes = float(saldo_mes)
                if linha.startswith(mes_ano):
                    if saldo_mes >= valor:
                        f.write(f"{mes_ano},{saldo_mes - valor}\n")
                        with open('despesas.txt', 'a') as file:
                            file.write(f"{mes_ano},{descricao},{valor}\n")
                        print("Despesa registrada com sucesso.\n")
                    else:
                        print("Saldo insuficiente. Não é possível registrar a despesa.\n")
                else:
                    f.write(linha)

    except SyntaxError:
        print('Saldo insuficiente\n')

#6
def alterar_despesa():
    try:
        mes_ano = input("Digite o mês/ano da despesa que deseja alterar (MM/AAAA): ")
        with open('despesas.txt', 'r') as file:
            despesas = file.readlines()

            if not despesas:
                print('Não há despesas cadastradas.\n')
                return
            for i in range(len(despesas)):
                data, descricao, valor = despesas[i].split(',')
                if data == mes_ano:
                    nova_despesa = input(f"Digite o novo valor da despesa {mes_ano}: R$")
                    despesas[i] = f"{mes_ano},{descricao},{nova_despesa}\n"
                    with open('despesas.txt', 'w') as file:
                        file.writelines(despesas)
                    print('Despesa alterada com sucesso.')
                    return
            print(f"Não há despesas cadastradas para o mês/ano {mes_ano}.\n")
    except ValueError:
        print('Valor da despesa inválido.\n')
    except FileNotFoundError:
        print('Não há despesas cadastradas.\n')

#7
def remover_despesa():
    mes_ano = input("Digite o mês e ano da despesa que deseja remover (MM/AAAA): ")
    descricao = input("Digite a descrição da despesa que deseja remover: ")
    try:
        with open("despesas.txt", "r") as file:
            linhas = file.readlines()
        with open("despesas.txt", "w") as file:
            for linha in linhas:
                if not (mes_ano in linha and descricao in linha):
                    file.write(linha)
        print("Despesa removida com sucesso!\n")
    except FileNotFoundError:
        print("Arquivo de despesas não encontrado.\n")
    except Exception as e:
        print("Erro ao remover despesa:", e)

#8
def listar_despesas():
    try:
        with open("despesas.txt", "r") as file:
            despesas = [linha.strip().split(",") for linha in file.readlines()]
        if len(despesas) == 0:
            print("Não há despesas cadastradas.\n")
        else:
            print("Despesas:\n")
            for despesa in sorted(despesas, key=lambda x: x[0]):
                print(f"{despesa[0]} - {despesa[1]} - R${despesa[2]}")
            total = sum(float(despesa[2]) for despesa in despesas)
            print(f"Total: R${total}\n")
    except FileNotFoundError:
        print("Arquivo de despesas não encontrado.\n")
    except Exception as e:
        print("Erro ao listar despesas:", e)

#9
def mostrar_resultado():
    rendimentos = []
    despesas = []

    with open('rendimentos.txt', 'r') as file:
        for line in file:
            line = line.strip()
            rendimentos.append(line)

    with open('despesas.txt', 'r') as file:
        for line in file:
            line = line.strip()
            despesas.append(line)

    rendimentos_ordenados = sorted(rendimentos, key=lambda x: datetime.strptime(x.split(',')[0], '%m/%Y'))
    despesas_ordenadas = sorted(despesas, key=lambda x: datetime.strptime(x.split(',')[0], '%m/%Y'))

    print("\033[31m=============\033[0m RESULTADO \033[32m=============\033[0m\n")

    saldo = 0.0
    for rendimento in rendimentos_ordenados:
        mes_ano, valor = rendimento.split(',')
        saldo += float(valor)
        print(f"\033[32m{mes_ano}: Receita: R${valor}, Saldo: R${saldo}\033[0m")
    print('\n')
    for despesa in despesas_ordenadas:
        mes_ano, descricao, valor = despesa.split(',')
        saldo -= float(valor)
        print(f"\033[31m{mes_ano}: Despesa: R${valor}, Saldo: R${saldo}\033[0m")

    if rendimentos:
        receita_total = sum(float(r.split(',')[1]) for r in rendimentos)
        print(f"\nReceita total: \033[32mR${receita_total:.2f}\033[0m")

    if despesas:
        despesa_total = sum(float(d.split(',')[2]) for d in despesas)
        print(f"Despesa total: \033[31mR${despesa_total:.2f}\033[0m\n")

    saldo_final = saldo
    print(f"Saldo final: R${saldo_final:.2f}\n")

    meta_mes = receita_total * 0.1
    bateu_meta = saldo_final >= meta_mes
    if bateu_meta is True:
        print(f"\033[32mBateu a meta do mês!\033[0m\n")

    else:
        print(f"\033[31mNão bateu a meta do mês.\033[0m\n")

    valor_investido = saldo_final * 0.1
    rendimento_investimento = valor_investido * 0.01
    print(f"Valor investido no fundo de renda fixa: R${valor_investido:.2f}")
    print(f"Rendimento do investimento: R${rendimento_investimento:.2f}\n")


import os

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def exibir_menu():
    print("=== Controle Financeiro ===")
    print("1 - Informar rendimento líquido mensal")
    print("2 - Alterar rendimento líquido mensal")
    print("3 - Excluir rendimento")
    print("4 - Listar rendimento")
    print("5 - Informar despesa")
    print("6 - Alterar despesa")
    print("7 - Remover despesa")
    print("8 - Listar despesas")
    print("9 - Mostrar resultado")
    print("10 - Sair")
    print("==========================")

while True:
    limpar_tela()
    exibir_menu()
    opcao = input("Digite a opção desejada: ")

    if opcao == "1":
        informar_rendimento()
    elif opcao == "2":
        alterar_rendimento()
    elif opcao == "3":
        excluir_rendimento()
    elif opcao == "4":
        listar_rendimentos()
    elif opcao == "5":
        informar_despesa()
    elif opcao == "6":
        alterar_despesa()
    elif opcao == "7":
        remover_despesa()
    elif opcao == "8":
        listar_despesas()
    elif opcao == "9":
        mostrar_resultado()
    elif opcao == "10":
        print("Saindo do sistema...")
        break
    else:
        print("\033[31mOpção inválida, tente novamente.\033[0m")
        input("\033[32mPressione Enter para continuar... \033[0m")
