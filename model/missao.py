from model.enums import StatusMissao

# Justificativa dos setters:
# - nome, descricao e recompensa NÃO têm setter: são definidos na criação da
#   missão e não fazem sentido mudar durante o jogo (evita alterar a recompensa
#   no meio da missão, por exemplo).
# - status TEM setter, porque ele muda ao longo do jogo (PENDENTE ->
#   EM_ANDAMENTO -> CONCLUIDA). Mas o setter valida o novo valor: só aceita um
#   StatusMissao e só permite avançar para a etapa seguinte, sem pular nem voltar.
class Missao:
    def __init__(self, nome, descricao, recompensa):
        self.__nome = nome
        self.__descricao = descricao
        self.__recompensa = recompensa
        self.__status = StatusMissao.PENDENTE

    @property
    def nome(self):
        return self.__nome

    @property
    def descricao(self):
        return self.__descricao

    @property
    def recompensa(self):
        return self.__recompensa

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, novo_status):
        if not isinstance(novo_status, StatusMissao):
            raise TypeError("O status precisa ser um StatusMissao")

        sequencia = list(StatusMissao)
        posicao_atual = sequencia.index(self.__status)
        posicao_nova = sequencia.index(novo_status)

        if posicao_nova != posicao_atual + 1:
            raise ValueError(
                f"Transição inválida: não é possível ir de "
                f"{self.__status.name} para {novo_status.name}. "
                f"A sequência é PENDENTE -> EM_ANDAMENTO -> CONCLUIDA."
            )
        self.__status = novo_status

    def iniciar_missao(self):
        self.status = StatusMissao.EM_ANDAMENTO
        return f"A missão {self.nome} começou! O objetivo é {self.descricao}."

    def calcular_recompensa(self):
        if self.status is not StatusMissao.CONCLUIDA:
            return 0
        return self.recompensa

    def concluir_missao(self, heroi):
        # Primeiro muda o status; só depois a recompensa passa a valer
        self.status = StatusMissao.CONCLUIDA
        xp = self.calcular_recompensa()
        heroi.ganhar_experiencia(xp)
        return xp

    def exibir_dados(self):
        msg = f'''
[{self.__class__.__name__}]
Nome: {self.nome}
Descrição: {self.descricao}
Recompensa base: {self.recompensa}
Status: {self.status.value}
'''
        return msg

    def __str__(self):
        return f'missão [{self.__class__.__name__}]: {self.nome} | status: {self.status.value}'


class MissaoCaca(Missao):
    XP_POR_INIMIGO = 10

    def __init__(self, nome, descricao, recompensa, quantidade_inimigos):
        super().__init__(nome, descricao, recompensa)
        self.__quantidade_inimigos = quantidade_inimigos

    @property
    def quantidade_inimigos(self):
        return self.__quantidade_inimigos

    def calcular_recompensa(self):
        base = super().calcular_recompensa()
        if self.status is not StatusMissao.CONCLUIDA:
            return 0
        return base + self.quantidade_inimigos * self.XP_POR_INIMIGO

    def exibir_dados(self):
        return super().exibir_dados() + f"Inimigos a caçar: {self.quantidade_inimigos}\n"


class MissaoColeta(Missao):
    XP_POR_ITEM = 5

    def __init__(self, nome, descricao, recompensa, quantidade_itens):
        super().__init__(nome, descricao, recompensa)
        self.__quantidade_itens = quantidade_itens

    @property
    def quantidade_itens(self):
        return self.__quantidade_itens

    def calcular_recompensa(self):
        base = super().calcular_recompensa()
        if self.status is not StatusMissao.CONCLUIDA:
            return 0
        return base + self.quantidade_itens * self.XP_POR_ITEM

    def exibir_dados(self):
        return super().exibir_dados() + f"Itens a coletar: {self.quantidade_itens}\n"


class MissaoEntrega(Missao):
    XP_POR_KM = 2

    def __init__(self, nome, descricao, recompensa, distancia_km):
        super().__init__(nome, descricao, recompensa)
        self.__distancia_km = distancia_km

    @property
    def distancia_km(self):
        return self.__distancia_km

    def calcular_recompensa(self):
        base = super().calcular_recompensa()
        if self.status is not StatusMissao.CONCLUIDA:
            return 0
        return base + self.distancia_km * self.XP_POR_KM

    def exibir_dados(self):
        return super().exibir_dados() + f"Distância da entrega: {self.distancia_km} km\n"
