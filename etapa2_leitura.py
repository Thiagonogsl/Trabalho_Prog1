import time
from typing import List, Optional

class Hospede:
    def __init__(self,
                 nome: str = "",
                 idade: int = 0,
                 telefone: str = "",
                 pagamento: bool = False,
                 quarto: int = 0,
                 contatos: Optional[List[str]] = None,
                 diaria: float = 0.0,
                 checkin: str = "",
                 checkout: str = ""):
        self.nome = nome
        self.idade = idade
        self.telefone = telefone
        self.pagamento = pagamento
        self.quarto = quarto
        self.contatos = contatos or []
        self.diaria = diaria
        self.checkin = checkin
        self.checkout = checkout

    @classmethod
    def ler_linha(cls, linha: str):
        d = linha.strip().split(";")
        # Proteção contra linhas mal-formadas:
        if len(d) < 9:
            raise ValueError(f"Linha inválida: {linha}")

        nome = d[0]
        idade = int(d[1]) if d[1] else 0
        telefone = d[2]
        pagamento = d[3].strip().lower() in ("true", "1", "s", "sim", "yes")
        quarto = int(d[4]) if d[4] else 0

        contatos_raw = d[5].strip()
        contatos = [c.strip() for c in contatos_raw.split(",")] if contatos_raw else []

        diaria_raw = d[6].strip().replace("R$", "").replace(",", ".")
        diaria = float(diaria_raw) if diaria_raw else 0.0

        checkin = d[7].strip()
        checkout = d[8].strip()

        return cls(nome, idade, telefone, pagamento, quarto, contatos, diaria, checkin, checkout)

    def escrever_linha(self) -> str:
        contatos_field = ",".join(self.contatos)
        return f"{self.nome};{self.idade};{self.telefone};{str(self.pagamento)};{self.quarto};{contatos_field};R${self.diaria:.2f};{self.checkin};{self.checkout}\n"

    def __repr__(self):
        return f"Hospede(nome={self.nome!r}, quarto={self.quarto}, diaria=R${self.diaria:.2f})"

def carregar_dados_hotel(nome_arquivo: str) -> List[Hospede]:
    inicio = time.time()
    hospedes = []
    with open(nome_arquivo, "r", encoding="utf-8") as f:
        for linha in f:
            if linha.strip() == "":
                continue
            try:
                h = Hospede.ler_linha(linha)
                hospedes.append(h)
            except Exception as e:
                print(f"Aviso: ignorada linha inválida ({e})")
    fim = time.time()
    print(f"Leitura de {nome_arquivo} concluída: {len(hospedes)} registros em {fim - inicio:.4f} s")
    return hospedes
