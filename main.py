from model.heroi import Heroi
from model.missao import MissaoCaca, MissaoColeta, MissaoEntrega
from model.enums import ClasseHeroi, StatusMissao

def main():
    # 1) Herói e uma missão de cada tipo
    heroi = Heroi("Aragorn", ClasseHeroi.GUERREIRO, 100, 100, 15, 5)

    caca = MissaoCaca("Caçada aos Orcs", "eliminar os orcs da floresta", 100, 5)
    coleta = MissaoColeta("Ervas Raras", "coletar ervas na montanha", 60, 8)
    entrega = MissaoEntrega("Carta Real", "entregar a carta ao rei", 50, 20)

    missoes = [caca, coleta, entrega]

    # 2) Polimorfismo: mesmo método em todas as missões
    print("=== Recompensa das missões (ainda pendentes) ===")
    for missao in missoes:
        print(f"{missao} -> recompensa: {missao.calcular_recompensa()}")

    # 3) Ciclo completo de uma missão até o herói subir de nível
    print("\n=== Antes da missão ===")
    print(heroi.exibir_dados())

    print(caca.iniciar_missao())
    print(f"Recompensa em andamento: {caca.calcular_recompensa()}")
    xp = caca.concluir_missao(heroi)
    print(f"Missão concluída! XP ganho: {xp}")

    print("\n=== Depois da missão ===")
    print(heroi.exibir_dados())

    print("=== Recompensa das missões (após concluir a caça) ===")
    for missao in missoes:
        print(f"{missao} -> recompensa: {missao.calcular_recompensa()}")

    # 4) Erros de propósito tratados com try/except
    print("\n=== Testando erros ===")
    try:
        coleta.concluir_missao(heroi)  # coleta ainda está PENDENTE (pulou etapa)
    except ValueError as erro:
        print(f"Erro: {erro}")

    try:
        caca.status = StatusMissao.PENDENTE  # tentativa de retroceder
    except ValueError as erro:
        print(f"Erro: {erro}")

    try:
        entrega.status = "CONCLUIDA"  # status inválido (string)
    except TypeError as erro:
        print(f"Erro: {erro}")

main()
