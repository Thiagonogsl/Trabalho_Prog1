import time
import ast 

class Hospede:
    def __init__(self, id_hospede, nome, numero_quarto, valor_diaria, lista_extras):
        self.id_hospede = int(id_hospede)
        self.nome = nome
        self.numero_quarto = int(numero_quarto)
        self.valor_diaria = float(valor_diaria)
        self.lista_extras = lista_extras # é pra colocar uma lista aqui 

    def __repr__(self):
        # Apenas para facilitar a visualização se der um print no objeto
        return f"Hospede {self.nome} (Quarto {self.numero_quarto})"

def carregar_dados_hotel(nome_arquivo):
    lista_hospedes = []
    
    try:
        inicio = time.time()
        
        with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
            for linha in arquivo:
                linha = linha.strip()
                if not linha:
                    continue 
                
                partes = linha.split(',')
                
                if len(partes) < 5:
                    continue

                id_h = partes[0]
                nome = partes[1]
                quarto = partes[2]
                preco = partes[3]
                
                extras_str = partes[4] 
                try:
                    extras = ast.literal_eval(extras_str)
                except:
                    extras = [] 

                novo_hospede = Hospede(id_h, nome, quarto, preco, extras)
                
                lista_hospedes.append(novo_hospede)
        
        fim = time.time()
        tempo_total = fim - inicio
        
        print(f"Leitura concluída com sucesso!")
        print(f"Total de registros carregados: {len(lista_hospedes)}")
        print(f"Tempo de processamento: {tempo_total:.6f} segundos")
        
        return lista_hospedes, tempo_total

    except FileNotFoundError:
        print(f"Erro: O arquivo '{nome_arquivo}' não foi encontrado.")
        return [], 0

if __name__ == "__main__":
    dados, tempo = carregar_dados_hotel("dados_hotel.txt")
    
    # Ex: Mostrando o primeiro hospede carregado pra analisar
    if dados:
        print(f"\nExemplo de dados do primeiro hóspede:")
        print(vars(dados[0]))
