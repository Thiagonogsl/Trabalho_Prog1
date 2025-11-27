# etapa3_operacoes.py
import time
from typing import List, Optional
from etapa2_leitura import Hospede

########################################## buscar ####################################################################

def buscar(hospedes: List[Hospede]) -> List[Hospede]:
    termo = input("Digite nome ou número do quarto: ").strip()
    t0 = time.time()
    res = []
    if termo.isdigit():
        q = int(termo)
        res = [h for h in hospedes if h.quarto == q]
    else:
        termo_low = termo.lower()
        res = [h for h in hospedes if termo_low in h.nome.lower()]
    t1 = time.time()
    print(f"Buscar: encontrados {len(res)} em {t1 - t0:.6f} s")
    for h in res[:50]:  # mostra no máximo 50 para não lotar a tela
        print(h)
    return res

########################################## adicionar ####################################################################

def adicionar(hospedes: List[Hospede]) -> Hospede:
    print("=== Adicionar novo hóspede ===")
    nome = input("Nome: ").strip()
    idade = int(input("Idade: ").strip())
    telefone = input("Telefone: ").strip()
    pagamento_input = input("Pagamento confirmado? (s/n): ").strip().lower()
    pagamento = pagamento_input in ("s", "sim", "true", "y", "yes")

    quarto = int(input("Número do quarto: ").strip())
    contatos_emergencia_input = input("Contatos de emergência (separe por vírgula): ").strip()
    contatos_emergencia = [c.strip() for c in contatos_emergencia_input.split(",")] if contatos_emergencia_input else []

    diaria = float(input("Valor da diária: ").strip())
    checkin = input("Data check-in (DD/MM/YYYY): ").strip()
    checkout = input("Data check-out (DD/MM/YYYY): ").strip()

    t0 = time.time()
    h = Hospede(nome, idade, telefone, pagamento, quarto, contatos_emergencia, diaria, checkin, checkout)
    hospedes.append(h)
    t1 = time.time()
    print(f"Hóspede adicionado. Tempo: {t1 - t0:.6f} s")
    return h

########################################## remover ####################################################################

def remover(hospedes: List[Hospede]) -> int:
    try:
        quarto = int(input("Número do quarto a remover: ").strip())
    except ValueError:
        print("Entrada inválida.")
        return 0
    t0 = time.time()
    tam_antes = len(hospedes)
    hospedes[:] = [h for h in hospedes if h.quarto != quarto]
    removidos = tam_antes - len(hospedes)
    t1 = time.time()
    print(f"{removidos} registro(s) removido(s). Tempo: {t1 - t0:.6f} s")
    return removidos

########################################## salvar ####################################################################

def salvar(hospedes: List[Hospede], nome_arquivo: Optional[str] = None) -> None:
    if not nome_arquivo:
        nome_arquivo = input("Nome do arquivo para salvar: ").strip()
    t0 = time.time()
    try:
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            for h in hospedes:
                f.write(h.to_line())
        t1 = time.time()
        print(f"Arquivo '{nome_arquivo}' salvo ({len(hospedes)} registros). Tempo: {t1 - t0:.4f} s")
    except Exception as e:
        print(f"Erro ao salvar: {e}")

########################################## menu ####################################################################

def menu_interativo(hospedes: List[Hospede]) -> None:
    while True:
        print("\n--- Menu de operações ---")
        print("1 - Buscar")
        print("2 - Adicionar")
        print("3 - Remover")
        print("4 - Salvar em novo arquivo")
        print("5 - Sair")
        op = input("Escolha: ").strip()

        if op == "1":
            buscar(hospedes)
        elif op == "2":
            adicionar(hospedes)
        elif op == "3":
            remover(hospedes)
        elif op == "4":
            salvar(hospedes)
        elif op == "5":
            print("Saindo do menu de operações")
            break
        else:
            print("Opção inválida.")