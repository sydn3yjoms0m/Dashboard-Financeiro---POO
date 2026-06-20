import json
import os
from modelos import Entrada, Despesa, Carteira

class GerenciadorJSON:
    def __init__(self, caminho_arquivo="dados_financas_v2.json"):
        self.caminho_arquivo = caminho_arquivo

    def salvar(self, carteira: Carteira):
        dados = []
        for t in carteira.transacoes:
            dados.append({
                "tipo": t.__class__.__name__,  # Armazena se é 'Entrada' ou 'Despesa'
                "descricao": t.descricao,
                "categoria": t.categoria,
                "valor": t.valor
            })
        with open(self.caminho_arquivo, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)

    def carregar(self) -> Carteira:
        carteira = Carteira()
        if not os.path.exists(self.caminho_arquivo):
            return carteira  # Retorna carteira vazia se o arquivo não existir
            
        try:
            with open(self.caminho_arquivo, "r", encoding="utf-8") as f:
                dados = json.load(f)
                for item in dados:
                    if item["tipo"] == "Entrada":
                        t = Entrada(item["descricao"], item["valor"], item["categoria"])
                    else:
                        t = Despesa(item["descricao"], item["valor"], item["categoria"])
                    carteira.adicionar_transacao(t)
        except (json.JSONDecodeError, KeyError):
            print("Erro ao ler o arquivo JSON. Iniciando sistema limpo.")
        return carteira