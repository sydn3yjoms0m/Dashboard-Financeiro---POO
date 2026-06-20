from abc import ABC, abstractmethod

# 1. ABSTRAÇÃO: Classe base que serve apenas como molde
class Transacao(ABC):
    def __init__(self, descricao: str, valor: float, categoria: str):
        self.descricao = descricao
        self.categoria = categoria
        self.__valor = 0.0  # 3. ENCAPSULAMENTO: Atributo privado
        self.valor = valor  # Dispara o setter para validação inicial

    # Getter seguro para o valor
    @property
    def valor(self) -> float:
        return self.__valor

    # Setter com validação (Regra de negócio)
    @valor.setter
    def valor(self, novo_valor: float):
        if novo_valor <= 0:
            raise ValueError("O valor deve ser estritamente maior que zero.")
        self.__valor = novo_valor

    # Método abstrato: obriga as filhas a implementarem
    @abstractmethod
    def calcular_impacto(self) -> float:
        pass


# 2. HERANÇA E POLIMORFISMO: Cada classe filha responde ao impacto de seu próprio jeito
class Entrada(Transacao):
    def calcular_impacto(self) -> float:
        return self.valor  # Entradas somam ao saldo


class Despesa(Transacao):
    def calcular_impacto(self) -> float:
        return -self.valor  # Despesas subtraem do saldo (Polimorfismo!)


# 4. COMPOSIÇÃO: A Carteira gerencia a existência dos objetos de transação
class Carteira:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao: Transacao):
        self.transacoes.append(transacao)

    def obter_saldo_total(self) -> float:
        # Uso do Polimorfismo: chama o mesmo método independente de ser Entrada ou Despesa
        return sum(t.calcular_impacto() for t in self.transacoes)

    def obter_total_entradas(self) -> float:
        return sum(t.valor for t in self.transacoes if isinstance(t, Entrada))

    def obter_total_despesas(self) -> float:
        return sum(t.valor for t in self.transacoes if isinstance(t, Despesa))