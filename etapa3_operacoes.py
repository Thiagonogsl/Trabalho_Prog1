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
        else: print("Opcao invalida










                import time
class Hospede:
    def __init__(self, nome, sobrenome, idade, telefone, num_quarto, valor_diaria, data_checkin, data_checkout, pagou):
        self.nome = nome                
        self.sobrenome = sobrenome      
        self.idade = idade              
        self.telefone = telefone        
        self.num_quarto = num_quarto    
        self.valor_diaria = valor_diaria
        self.data_checkin = data_checkin 
        self.data_checkout = data_checkout 
        self.pagou = pagou              

    def to_string_arquivo(self):
        data_fmt = f"{self.data_checkin[0]}/{self.data_checkin[1]}/{self.data_checkin[2]}"
        return (f"{self.nome},{self.sobrenome},{self.idade},{self.telefone},"
                f"{self.num_quarto},{self.valor_diaria:.2f},{data_fmt},"
                f"{self.data_checkout},{self.pagou}")

    def __str__(self):
        status = "Pago" if self.pagou else "Pendente"
        return f"Quarto: {self.num_quarto} | Hóspede: {self.nome} {self.sobrenome} | Status: {status}"


def adicionar_elemento(lista_reservas):
    print("\n--- Nova Reserva ---")
    try:
        nome = input("Nome: ")
        sobrenome = input("Sobrenome: ")
        idade = int(input("Idade: "))
        tel = input("Telefone: ")
        quarto = int(input("Número do Quarto: "))
        valor = float(input("Valor da Diária (R$): "))
        
        # Tratando a DATA como LISTA para cumprir o requisito do trabalho
        entrada_data = input("Data Check-in (dia/mes/ano): ")
        # Transforma "23/11/2024" em [23, 11, 2024]
        checkin_lista = [int(x) for x in entrada_data.split('/')] 
        
        checkout = input("Data Check-out (dia/mes/ano): ")
        
        pag_input = input("Pagamento confirmado? (s/n): ").lower()
        pagou = True if pag_input == 's' else False

        inicio = time.time()
        
        nova_reserva = Reserva(nome, sobrenome, idade, tel, quarto, valor, checkin_lista, checkout, pagou)
        lista_reservas.append(nova_reserva)
        
        fim = time.time()
        

        print("✅ Reserva adicionada!")
        print(f"⏱️ Tempo para adicionar: {fim - inicio:.10f} segundos")

    except ValueError:
        print("❌ Erro: Digite números onde for solicitado (idade, quarto, valor, data).")

def buscar_elemento(lista_reservas):
    # Vamos buscar pelo Sobrenome ou Quarto
    alvo = input("\nDigite o SOBRENOME do hóspede para buscar: ").lower()

    inicio = time.time()
    
    encontrado = None
    for reserva in lista_reservas:
        if reserva.sobrenome.lower() == alvo:
            encontrado = reserva
            break
            
    fim = time.time()


    if encontrado:
        print(f"\n🔍 Encontrado:\n{encontrado}")
        print(f"Detalhes: {encontrado.nome}, Quarto {encontrado.num_quarto}, Data Check-in: {encontrado.data_checkin}")
    else:
        print("❌ Hóspede não encontrado.")
    
    print(f"⏱️ Tempo de busca: {fim - inicio:.10f} segundos")

def remover_elemento(lista_reservas):
    try:
        alvo_quarto = int(input("\nDigite o NÚMERO DO QUARTO para remover a reserva: "))
        
        inicio = time.time()
        
        removido = False
        for reserva in lista_reservas:
            if reserva.num_quarto == alvo_quarto:
                lista_reservas.remove(reserva)
                removido = True
                break
        
        fim = time.time()


        if removido:
            print("🗑️ Reserva removida com sucesso.")
        else:
            print("❌ Quarto não encontrado na lista.")
        
        print(f"⏱️ Tempo de remoção: {fim - inicio:.10f} segundos")
        
    except ValueError:
        print("Erro: Digite um número inteiro para o quarto.")

def salvar_novo_arquivo(lista_reservas):
    nome_arquivo = "reservas_atualizadas.txt"
    print(f"\n💾 Salvando em '{nome_arquivo}'...")

    inicio = time.time()

    try:
        with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
            # Cabeçalho (opcional)
            arquivo.write("Nome,Sobrenome,Idade,Telefone,Quarto,Valor,Checkin,Checkout,Pago\n")
            for reserva in lista_reservas:
                arquivo.write(reserva.to_string_arquivo() + "\n")
        
        fim = time.time()
        
        print("✅ Arquivo salvo!")
        print(f"⏱️ Tempo de escrita: {fim - inicio:.10f} segundos")
    except Exception as e:
        print(f"Erro ao salvar: {e}")

def main():
    banco_de_dados = [] 

    while True:
        print("\n=== SISTEMA HOTELEIRO (Etapa 3) ===")
        print("1. Adicionar Nova Reserva")
        print("2. Buscar Reserva (por Sobrenome)")
        print("3. Remover Reserva (por Quarto)")
        print("4. Salvar e Sair")
        
        opcao = input(">> Escolha: ")
        
        if opcao == '1':
            adicionar_elemento(banco_de_dados)
        elif opcao == '2':
            buscar_elemento(banco_de_dados)
        elif opcao == '3':
            remover_elemento(banco_de_dados)
        elif opcao == '4':
            salvar_novo_arquivo(banco_de_dados)
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    menu()

