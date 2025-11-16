import time
from etapa1_geracao import gerar_arquivo

def main():
    opcoes = \
    {
        1 : ("Pequeno.txt", 100),
        2 : ("Medio.txt", 1000),
        3 : ("Grande.txt", 10000),
        4 : ("Gigante.txt", 100000)
    }

    print("Escolha o tamanho do arquivo")
    print("(1) Pequeno")
    print("(2) Médio")
    print("(3) Grande")
    print("(4) Gigante")
    temp = int(input(">"))

    if temp not in opcoes:
        print("Opção inválida")
        exit()
    
    nome, tamanho = opcoes[temp]

    inicio = time.time()
    gerar_arquivo(nome, tamanho)
    fim = time.time()

    tempo_execucao = fim - inicio

    print(f"Arquivo {nome} gerado com {tamanho} registros")
    print(f"Tempo de execução = {tempo_execucao} segundos")

if __name__ == "__main__":
    main()