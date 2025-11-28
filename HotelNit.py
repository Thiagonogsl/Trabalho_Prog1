import time
import os
from typing import List, Optional

# ==============================================================================
#  CLASSE E DADOS (Igual ao Backend)
# ==============================================================================
class Hospede:
    def __init__(self, nome, idade, telefone, pagamento, numero_quarto, contatos_emergencia, valor_diaria, checkin, checkout):
        self.nome = nome
        self.idade = idade
        self.telefone = telefone
        self.pagamento = pagamento
        self.quarto = int(numero_quarto)
        self.contatos_emergencia = contatos_emergencia
        self.valor_diaria = float(valor_diaria)
        self.checkin = checkin
        self.checkout = checkout

    def to_line(self) -> str:
        # Formata para salvar no TXT
        contatos_str = "[" + ",".join(self.contatos_emergencia) + "]"
        return f"{self.nome};{self.idade};{self.telefone};{self.pagamento};{self.quarto};{contatos_str};{self.valor_diaria};{self.checkin};{self.checkout}\n"

    def __str__(self):
        # Formatação bonita para mostrar no print do terminal
        return f"[Quarto {self.quarto}] {self.nome} | Check-in: {self.checkin} | R$ {self.valor_diaria:.2f}"

def carregar_dados(nome_arquivo):
    lista = []
    if not os.path.exists(nome_arquivo):
        return lista
    
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as f:
            for linha in f:
                linha = linha.strip()
                if not linha: continue
                partes = linha.split(';')
                if len(partes) < 9: continue
                
                extras = []
                try:
                    conteudo = partes[5].replace('[','').replace(']','')
                    if conteudo: extras = conteudo.split(',')
                except: pass

                h = Hospede(partes[0], partes[1], partes[2], partes[3], partes[4], extras, partes[6], partes[7], partes[8])
                lista.append(h)
    except Exception as e:
        print(f"Erro ao ler arquivo: {e}")
    return lista

# ==============================================================================
#  OPERAÇÕES (Lógica da Etapa 3 - Console)
# ==============================================================================

def buscar(hospedes: List[Hospede]):
    print("\n--- BUSCAR HÓSPEDE ---")
    termo = input("Digite nome ou número do quarto: ").strip()
    
    t0 = time.time() # Medição de tempo
    res = []
    
    if termo.isdigit():
        q = int(termo)
        res = [h for h in hospedes if h.quarto == q]
    else:
        termo_low = termo.lower()
        res = [h for h in hospedes if termo_low in h.nome.lower()]
    
    t1 = time.time()
    
    print(f"Resultados encontrados: {len(res)} (Tempo: {t1 - t0:.6f}s)")
    print("-" * 40)
    for h in res:
        print(h)
    print("-" * 40)
    input("Pressione Enter para voltar...")

def adicionar(hospedes: List[Hospede]):
    print("\n--- ADICIONAR NOVO HÓSPEDE ---")
    # Coleta de dados (Inputs)
    nome = input("Nome Completo: ").strip()
    idade = input("Idade: ").strip()
    telefone = input("Telefone: ").strip()
    quarto = input("Número do Quarto: ").strip()
    valor = input("Valor Diária: ").strip()
    checkin = input("Data Entrada (DD/MM/AAAA): ").strip()
    checkout = input("Data Saída (DD/MM/AAAA): ").strip()
    
    print("Pagamento confirmado? (s/n)")
    pg = input("> ").lower().startswith('s')
    
    print("Contatos extra (separe por vírgula):")
    extras = input("> ").strip().split(',')
    
    # Processamento (Tempo medido apenas aqui)
    t0 = time.time()
    try:
        novo = Hospede(nome, idade, telefone, str(pg), quarto, extras, valor, checkin, checkout)
        hospedes.append(novo)
        t1 = time.time()
        print(f"\nSucesso! Hóspede adicionado na memória. (Tempo: {t1 - t0:.6f}s)")
    except ValueError:
        print("\nErro: Quarto e Valor devem ser números!")
    
    input("Pressione Enter para continuar...")

def remover(hospedes: List[Hospede]):
    print("\n--- REMOVER HÓSPEDE ---")
    try:
        quarto = int(input("Digite o número do quarto para liberar: ").strip())
    except ValueError:
        print("Número inválido.")
        return

    t0 = time.time()
    tam_antes = len(hospedes)
    
    # Slice Assignment (A técnica que você citou no relatório)
    hospedes[:] = [h for h in hospedes if h.quarto != quarto]
    
    tam_depois = len(hospedes)
    t1 = time.time()
    
    removidos = tam_antes - tam_depois
    if removidos > 0:
        print(f"Sucesso! {removidos} registro(s) removido(s). (Tempo: {t1 - t0:.6f}s)")
    else:
        print("Nenhum quarto encontrado com esse número.")
    input("Pressione Enter para continuar...")

def salvar(hospedes: List[Hospede]):
    nome_arquivo = "dados_hotel.txt"
    print(f"\nSalvando dados em '{nome_arquivo}'...")
    
    t0 = time.time()
    try:
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            for h in hospedes:
                f.write(h.to_line())
        t1 = time.time()
        print(f"Salvo com sucesso! (Tempo IO: {t1 - t0:.6f}s)")
    except Exception as e:
        print(f"Erro ao salvar: {e}")
    
    input("Pressione Enter para continuar...")

# ==============================================================================
#  MENU PRINCIPAL
# ==============================================================================
def menu():
    arquivo_db = "dados_hotel.txt"
    # Carrega dados ao iniciar (Etapa 2)
    hospedes = carregar_dados(arquivo_db)
    print(f"Sistema iniciado. {len(hospedes)} registros carregados.")

    while True:
        # Limpa tela (opcional, funciona em Windows/Linux)
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("\n=== SISTEMA HOTEL UFF (Console) ===")
        print("1 - Buscar Hóspede")
        print("2 - Adicionar Hóspede")
        print("3 - Remover Hóspede")
        print("4 - Salvar Dados")
        print("5 - Sair")
        print("===================================")
        
        op = input("Opção: ").strip()

        if op == "1":
            buscar(hospedes)
        elif op == "2":
            adicionar(hospedes)
        elif op == "3":
            remover(hospedes)
        elif op == "4":
            salvar(hospedes)
        elif op == "5":
            print("Encerrando sistema...")
            break
        else:
            input("Opção inválida. Enter para tentar novamente.")

if __name__ == "__main__":
    menu()