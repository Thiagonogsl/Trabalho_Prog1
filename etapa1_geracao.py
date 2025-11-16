import random
import datetime

#Dados escolhdos: Nome(str), Sobrenome(str), Idade(int), Telefone(str), Numero do Quarto(int), diaria_quarto(Float), 
#data_checkin, data_checkout, pagamento_Confirmado(Bool)

#Gerar Datas de Check-in e check-out
def gerar_dia_checkin():        
    data_inicial = datetime.date(day=1, month=1, year=2025)
    numero_dias = random.randint(0, 365)
        
    data_checkin = data_inicial + datetime.timedelta(days=numero_dias)
    return data_checkin

#Gerar Numeros de telefone
def gerar_telefone():
    ddd = random.randint(11, 99)

    primeiros_numeros = random.randint(0, 9999)
    ultimos_numeros = random.randint(0, 9999)
    
    primeiros_numeros = str(primeiros_numeros).zfill(4)
    ultimos_numeros = str(ultimos_numeros).zfill(4)

    telefone = (f"({ddd})9{primeiros_numeros}-{ultimos_numeros}")
    return telefone
def gerar_numero_quarto():
    andar = random.randint(3, 12)
    andar = str(andar)

    numero = random.randint(0, 20)
    numero = str(numero).zfill(2)

    numero_quarto = andar + numero
    return int(numero_quarto)

def gerar_nome():
    lista_nomes = ["Thiago", "Lucas", "Marcos", "Antônio", "Gabriel", "João Pedro", "Juan", "Davi", "Claudio",\
                "Igor", "Icaro", "Caio", "Eduardo", "Maria", "Victoria", "Ana", "Claudia", "Nicole", \
                "Fernanda", "Michelle","Julia", "Mariana", "Aline", "Paula", "Patricia", "Giorgian"]
    
    lista_sobrenomes = ["Silva", "Santos", "Ferreira", "Oliveira", "Souza", "Rodrigues", "Alves", "Pereira",\
                    "Lima", "Gomes", "Costa", "Ribeiro", "Arrascaeta", "Barbosa", "Martins", "Carvalho" ]

    nome = random.choice(lista_nomes)
    sobrenome = random.choice(lista_sobrenomes)

    nome_completo = nome + " " + sobrenome
    return nome_completo

def gerar_precos():
    lista_Precos = [199.99, 349.99, 650.00, 1300.00]
    preco = random.choice(lista_Precos)

    return preco

def gerar_idade():
    idade = random.randint(18, 80)
    return idade

def gerar_confirmacao_pagamento():
    pagamento = bool(random.randint(0,1))
    return pagamento
#######################################################################################

def gerar_arquivo(nome_arquivo, tamanho_arquivo):
    with open(nome_arquivo, "w", encoding="utf-8")  as arquivo:
        for _ in range (tamanho_arquivo):
            nome = gerar_nome()
            idade = gerar_idade()
            telefone = gerar_telefone()
            confirmacao = gerar_confirmacao_pagamento()
            numero_quarto = gerar_numero_quarto()
            diaria = gerar_precos()
            data_checkin = gerar_dia_checkin()

            telefones_emergencia = [gerar_telefone(), gerar_telefone()]
            telefones_formatados = ",".join(telefones_emergencia)

            dias_estadia = random.randint(1, 20)
            data_checkout = data_checkin + datetime.timedelta(days=dias_estadia)

            data_checkin = data_checkin.strftime("%d/%m/%Y")
            data_checkout = data_checkout.strftime("%d/%m/%Y")

            linha = f"{nome};{idade};{telefone};{confirmacao};{numero_quarto};[{telefones_formatados}];R${diaria};{data_checkin};{data_checkout}\n"

            arquivo.write(linha)