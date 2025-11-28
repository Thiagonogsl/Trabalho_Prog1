import random
import datetime
import time
import ast
from typing import List, Optional

# ==============================================================================
#  CLASSE HOSPEDE (Base do Modelo de Dados)
# ==============================================================================
class Hospede:
    def __init__(self, nome, idade, telefone, pagamento, numero_quarto, contatos_emergencia, valor_diaria, checkin, checkout):
        self.nome = nome
        self.idade = int(idade)
        self.telefone = telefone
        # Tratamento para booleano vindo de string ou bool direto
        if isinstance(pagamento, str):
            self.pagamento = pagamento.lower() == 'true'
        else:
            self.pagamento = bool(pagamento)
            
        self.quarto = int(numero_quarto)
        self.contatos_emergencia = contatos_emergencia # Lista
        self.valor_diaria = float(valor_diaria)
        self.checkin = checkin
        self.checkout = checkout

    def to_line(self) -> str:
        """Formata o objeto para ser salvo no arquivo .txt"""
        contatos_str = "[" + ",".join(self.contatos_emergencia) + "]"
        return f"{self.nome};{self.idade};{self.telefone};{self.pagamento};{self.quarto};{contatos_str};{self.valor_diaria};{self.checkin};{self.checkout}\n"

    def __repr__(self):
        return f"Hospede: {self.nome} | Quarto: {self.quarto} | Check-in: {self.checkin}"

# ==============================================================================
#  PARTE 1: GERADOR DE DADOS (Mock Data)
# ==============================================================================
def gerar_dia_checkin():        
    data_inicial = datetime.date(day=1, month=1, year=2025)
    numero_dias = random.randint(0, 365)
    data_checkin = data_inicial + datetime.timedelta(days=numero_dias)
    return data_checkin

def gerar_telefone():
    ddd = random.randint(11, 99)
    primeiros_numeros = random.randint(0, 9999)
    ultimos_numeros = random.randint(0, 9999)
    primeiros_numeros = str(primeiros_numeros).zfill(4)
    ultimos_numeros = str(ultimos_numeros).zfill(4)
    return (f"({ddd})9{primeiros_numeros}-{ultimos_numeros}")

def gerar_numero_quarto():
    andar = random.randint(3, 12)
    numero = random.randint(0, 20)
    # Garante formatação correta ex: 305, 1201
    numero_quarto = f"{andar}{str(numero).zfill(2)}"
    return int(numero_quarto)

def gerar_nome():
    lista_nomes = ["Thiago", "Lucas", "Marcos", "Antônio", "Gabriel", "João Pedro", "Juan", "Davi", "Claudio",
                "Igor", "Icaro", "Caio", "Eduardo", "Maria", "Victoria", "Ana", "Claudia", "Nicole", 
                "Fernanda", "Michelle","Julia", "Mariana", "Aline", "Paula", "Patricia", "Giorgian"]
    lista_sobrenomes = ["Silva", "Santos", "Ferreira", "Oliveira", "Souza", "Rodrigues", "Alves", "Pereira",
                    "Lima", "Gomes", "Costa", "Ribeiro", "Arrascaeta", "Barbosa", "Martins", "Carvalho" ]
    return random.choice(lista_nomes) + " " + random.choice(lista_sobrenomes)

def gerar_precos():
    return random.choice([199.99, 349.99, 650.00, 1300.00])

def gerar_idade():
    return random.randint(18, 80)

def gerar_confirmacao_pagamento():
    return bool(random.randint(0,1))

def gerar_arquivo_inicial(nome_arquivo, tamanho_arquivo):
    """Gera o arquivo inicial se ele não existir ou para teste"""
    print(f"Gerando arquivo '{nome_arquivo}' com {tamanho_arquivo} registros...")
    with open(nome_arquivo, "w", encoding="utf-8")  as arquivo:
        for _ in range (tamanho_arquivo):
            nome = gerar_nome()
            idade = gerar_idade()
            telefone = gerar_telefone()
            confirmacao = gerar_confirmacao_pagamento()
            numero_quarto = gerar_numero_quarto()
            diaria = gerar_precos()
            
            # Datas
            dt_in = gerar_dia_checkin()
            dias_estadia = random.randint(1, 20)
            dt_out = dt_in + datetime.timedelta(days=dias_estadia)
            str_checkin = dt_in.strftime("%d/%m/%Y")
            str_checkout = dt_out.strftime("%d/%m/%Y")

            # Lista de telefones formatada como string
            telefones_emergencia = [gerar_telefone(), gerar_telefone()]
            # Importante: formata como lista Python mas dentro da string CSV
            telefones_formatados = "[" + ",".join(telefones_emergencia) + "]"

            # Formato CSV separado por ;
            linha = f"{nome};{idade};{telefone};{confirmacao};{numero_quarto};{telefones_formatados};{diaria};{str_checkin};{str_checkout}\n"
            arquivo.write(linha)
    print("Arquivo gerado com sucesso.\n")

# ==============================================================================
#  PARTE 2: LEITURA DE DADOS
# ==============================================================================
def carregar_dados_hotel(nome_arquivo):
    lista_hospedes = []
    
    try:
        inicio = time.time()
        with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
            for linha in arquivo:
                linha = linha.strip()
                if not linha:
                    continue 
                
                # Modificado para split por ';' conforme o gerador
                partes = linha.split(';')
                
                # Validação básica de colunas (esperamos 9 campos)
                if len(partes) < 9:
                    continue

                # Mapeamento dos campos
                nome = partes[0]
                idade = partes[1]
                telefone = partes[2]
                pagamento = partes[3]
                quarto = partes[4]
                extras_str = partes[5] # Lista de telefones
                diaria = partes[6].replace("R$", "") # Limpeza simples caso tenha R$
                checkin = partes[7]
                checkout = partes[8]
                
                # Converter a string de lista em lista real
                try:
                    # O arquivo foi salvo como [tel1,tel2], ast consegue ler isso
                    # Mas se foi salvo sem aspas nos numeros dentro dos colchetes pelo gerador manual,
                    # precisamos garantir que seja interpretável.
                    # O gerador atual cria: [(DD)9XXXX-XXXX,(DD)9XXXX-XXXX] -> isso não é lista python válida sem aspas
                    # CORREÇÃO: O gerador manual fazia ",".join. Vamos tratar como string pura.
                    
                    if extras_str.startswith('[') and extras_str.endswith(']'):
                         conteudo = extras_str[1:-1] # Remove colchetes
                         if conteudo:
                             extras = conteudo.split(',')
                         else:
                             extras = []
                    else:
                        extras = []
                except:
                    extras = [] 

                novo_hospede = Hospede(nome, idade, telefone, pagamento, quarto, extras, diaria, checkin, checkout)
                lista_hospedes.append(novo_hospede)
        
        fim = time.time()
        print(f"Leitura concluída! Registros carregados: {len(lista_hospedes)}")
        print(f"Tempo de processamento: {fim - inicio:.6f} segundos")
        return lista_hospedes

    except FileNotFoundError:
        print(f"Erro: O arquivo '{nome_arquivo}' não foi encontrado.")
        return []

# ==============================================================================
#  PARTE 3: OPERAÇÕES (CRUD)
# ==============================================================================
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
    
    # Exibe resultados
    for h in res[:10]: # Limitado a 10 para não poluir
        print(h)
    if len(res) > 10:
        print(f"... e mais {len(res)-10} resultados.")
    return res

def adicionar(hospedes: List[Hospede]) -> Hospede:
    print("\n=== Adicionar novo hóspede ===")
    try:
        nome = input("Nome: ").strip()
        idade = int(input("Idade: ").strip())
        telefone = input("Telefone: ").strip()
        pagamento_input = input("Pagamento confirmado? (s/n): ").strip().lower()
        pagamento = pagamento_input in ("s", "sim", "true", "y", "yes")

        quarto = int(input("Número do quarto: ").strip())
        contatos_input = input("Contatos de emergência (separe por vírgula): ").strip()
        contatos_emergencia = [c.strip() for c in contatos_input.split(",")] if contatos_input else []

        diaria = float(input("Valor da diária: ").strip())
        checkin = input("Data check-in (DD/MM/YYYY): ").strip()
        checkout = input("Data check-out (DD/MM/YYYY): ").strip()

        t0 = time.time()
        h = Hospede(nome, idade, telefone, pagamento, quarto, contatos_emergencia, diaria, checkin, checkout)
        hospedes.append(h)
        t1 = time.time()
        print(f"Hóspede adicionado com sucesso. Tempo: {t1 - t0:.6f} s")
        return h
    except ValueError as e:
        print(f"Erro ao adicionar: Dados inválidos ({e})")
        return None

def remover(hospedes: List[Hospede]) -> int:
    try:
        quarto = int(input("Número do quarto a remover todos os hóspedes: ").strip())
    except ValueError:
        print("Entrada inválida.")
        return 0
        
    t0 = time.time()
    tam_antes = len(hospedes)
    # Reconstrói a lista apenas com quem NÃO está no quarto
    hospedes[:] = [h for h in hospedes if h.quarto != quarto]
    
    removidos = tam_antes - len(hospedes)
    t1 = time.time()
    print(f"{removidos} registro(s) removido(s). Tempo: {t1 - t0:.6f} s")
    return removidos

def salvar(hospedes: List[Hospede], nome_arquivo: Optional[str] = None) -> None:
    if not nome_arquivo:
        nome_arquivo = input("Nome do arquivo para salvar (ex: dados_atualizados.txt): ").strip()
    
    if not nome_arquivo:
        print("Nome de arquivo inválido.")
        return

    t0 = time.time()
    try:
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            for h in hospedes:
                f.write(h.to_line())
        t1 = time.time()
        print(f"Arquivo '{nome_arquivo}' salvo ({len(hospedes)} registros). Tempo: {t1 - t0:.4f} s")
    except Exception as e:
        print(f"Erro ao salvar: {e}")

def menu_interativo(hospedes: List[Hospede]) -> None:
    while True:
        print("\n--- Menu de operações ---")
        print("1 - Buscar")
        print("2 - Adicionar")
        print("3 - Remover")
        print("4 - Salvar em arquivo")
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
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida.")

# ==============================================================================
#  MAIN EXECUTION
# ==============================================================================
if __name__ == "__main__":
    ARQUIVO_PADRAO = "dados_hotel.txt"
    
    # 1. Tenta carregar, se não existir, pergunta se quer gerar
    dados = carregar_dados_hotel(ARQUIVO_PADRAO)
    
    if not dados:
        resp = input(f"Arquivo {ARQUIVO_PADRAO} não encontrado ou vazio. Deseja gerar dados de teste? (s/n): ")
        if resp.lower() == 's':
            qtd = int(input("Quantos registros gerar? (ex: 1000): "))
            gerar_arquivo_inicial(ARQUIVO_PADRAO, qtd)
            dados = carregar_dados_hotel(ARQUIVO_PADRAO)
    
    # 2. Inicia o menu se houver dados (ou lista vazia pronta para adição)
    if dados is not None:
        menu_interativo(dados)
