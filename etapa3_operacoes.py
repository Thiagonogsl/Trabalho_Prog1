import time

class Hospede:
    def __init__(self, linha=None):
        # Inicializa variáveis padrão
        self.nome, self.idade, self.telefone, self.pagamento, self.quarto = "", 0, "", "False", 0
        self.contatos, self.diaria, self.checkin, self.checkout = [], 0.0, "", ""

        if linha: # Se veio do arquivo, preenche e limpa
            d = linha.strip().split(';') 
            self.nome, self.idade, self.telefone, self.pagamento, self.quarto = d[0], int(d[1]), d[2], d[3], int(d[4])
            # Remove [] e R$ durante a leitura
            self.contatos = d[5].strip("[]").split(',') if len(d[5]) > 2 else []
            self.diaria = float(d[6].replace("R$", "").replace(",", "."))
            self.checkin, self.checkout = d[7], d[8]

    def __repr__(self):
        # Exibição do objeto na lista
        return f"Quarto {self.quarto} | {self.nome} | R${self.diaria:.2f}"

def buscar(lista):
    busca = input("\nBusca (Nome ou Quarto): ").lower()
    t0 = time.time()
    # Filtra a lista numa linha só
    res = [h for h in lista if busca in h.nome.lower() or busca == str(h.quarto)]
    
    if res:
        print(f"Tempo: {time.time()-t0:.5f}s | Encontrados: {len(res)}\n{res}")
    else:
        print("Nada encontrado.")

def adicionar(lista):
    h = Hospede()
    print("\n--- Novo Hospede ---")
    h.nome, h.idade = input("Nome: "), int(input("Idade: "))
    h.telefone, h.quarto = input("Tel: "), int(input("Quarto: "))
    h.diaria = float(input("Diaria: "))
    h.checkin, h.checkout = input("Entrada: "), input("Saida: ")
    h.contatos = input("Contatos extras (separar por virgula): ").split(',')
    h.pagamento = "True"

    t0 = time.time()
    lista.append(h)
    print(f"Salvo! Tempo: {time.time()-t0:.5f}s")

def remover(lista):
    try: q = int(input("\nQuarto para remover: "))
    except: return print("Numero invalido.")

    t0 = time.time()
    tam_antes = len(lista)
    # Reconstrói a lista mantendo apenas quem NÃO é do quarto alvo
    lista[:] = [h for h in lista if h.quarto != q]
    
    msg = "Removido!" if len(lista) < tam_antes else "Nao encontrado."
    print(f"{msg} Tempo: {time.time()-t0:.5f}s")

def salvar(lista):
    nome = input("\nNome arquivo (ex: hotel.txt): ")
    t0 = time.time()
    try:
        with open(nome, 'w', encoding='utf-8') as f:
            for h in lista:
                # Reconstrói o formato original (com [] e R$) numa linha só
                f.write(f"{h.nome};{h.idade};{h.telefone};{h.pagamento};{h.quarto};"
                        f"[{','.join(h.contatos)}];R${h.diaria};{h.checkin};{h.checkout}\n")
        print(f"Arquivo salvo! Tempo: {time.time()-t0:.5f}s")
    except Exception as e: print(f"Erro: {e}")

def menu():
    # Mock para teste rápido
    L = [Hospede("Teste;30;99;True;101;[99];R$200;01/01;02/01")]
    opcoes = {'1': buscar, '2': adicionar, '3': remover, '4': salvar}
    
    while True:
        print("\n1.Buscar 2.Add 3.Remover 4.Salvar 5.Sair")
        op = input("Opcao: ")
        if op == '5': break
        if op in opcoes: opcoes[op](L)
        else: print("Opcao invalida")

if __name__ == "__main__":
    menu()
