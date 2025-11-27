import time
from etapa1_geracao import gerar_arquivo
from etapa3_operacoes import menu_interativo

def escolher_arquivo_para_carregar():
    nome = input("Nome do arquivo a carregar: ").strip()
    inicio = time.time()
    hospedes = ler_arquivo(nome)
    fim = time.time()
    print(f"Carregado {len(hospedes)} registros em {fim - inicio:.3f} s")
    return hospedes


def menu_gerar_arquivo():
    print("Escolha o tamanho do arquivo")
    print("(1) Pequeno (10 hospedes)")
    print("(2) Médio   (100 hospedes)")
    print("(3) Grande  (1000 hospedes)")
    print("(4) Gigante (10000 hospedes)")
    opcao = int(input(">"))

    if opcao == 1:
        tamanho = 10
    elif opcao == 2:
        tamanho = 100
    elif opcao == 3:
        tamanho = 1000
    elif opcao == 4:
        tamanho = 10000

    print("\nEscolha o nome do arquivo que sera criado")
    nome = input(">")

    inicio = time.time()
    gerar_arquivo(nome, tamanho)
    fim = time.time()

    tempo_execucao = fim - inicio

    print(f"Arquivo {nome} gerado com {tamanho} registros")
    print(f"Tempo de execução = {tempo_execucao} segundos")


def main():
    hospedes = []  # lista em memória
    while True:
        print("\n=== Menu Principal ===")
        print("1 - Gerar arquivos")
        print("2 - Carregar arquivo")
        print("3 - Abrir menu de operações")
        print("4 - Sair")
        op = input("Escolha: ").strip()
        print("")

        if op == "1":
            menu_gerar_arquivo()
        elif op == "2":
            hospedes = escolher_arquivo_para_carregar()
        elif op == "3":
            if not hospedes:
                print("Nenhuma lista carregada. Primeiro carregue um arquivo (opção 2).")
            else:
                menu_interativo(hospedes)
        elif op == "4":
            print("Saindo...")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()