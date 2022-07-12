import random
from lista_de_propriedades import get_lista_de_propriedades

class Jogador(object):

    def __init__(self, tipo):
        self._saldo = 300
        self._comportamento = tipo
        self._numero_de_propriedades_percorridas = 0
        self._proxima_proprieda = 0

    @property
    def saldo(self):
        return self._saldo

    @saldo.setter
    def saldo(self, valor):
        self._saldo = valor

    @property
    def comportamento(self):
        return self._comportamento

    @comportamento.setter
    def comportamento(self, tipo):
        self._comportamento = tipo

    def recebe(self, valor):
        self.saldo = self.saldo + valor

    def paga(self, valor):
        self.saldo = self.saldo - valor

    def joga_o_dado(self):
        return random.randint(1, 6)

    def proxima_proprieda(self, resultado_do_dado):
        self._proxima_proprieda += resultado_do_dado
        if self._proxima_proprieda > 20:
            self._proxima_proprieda -= 20
        return self._proxima_proprieda

    def verifica_se_completou_uma_volta_no_tabuleiro(self, resultado_do_dado):
        self._numero_de_propriedades_percorridas += resultado_do_dado
        if self._numero_de_propriedades_percorridas >= 20:
            self._numero_de_propriedades_percorridas = 0
            self.recebe(100)


class Partida(object):

    def __init__(self):
        self.jogador_um = Jogador("impulsivo")
        self.jogador_dois = Jogador("exigente")
        self.jogador_tres = Jogador("cauteloso")
        self.jogador_quatro = Jogador("aleatorio")
        self._total_de_rodadas = 0
        self.encerada_por_timeout = False
        self.propriedades = get_lista_de_propriedades()

    @property
    def total_de_rodadas(self):
        return self._total_de_rodadas

    @total_de_rodadas.setter
    def total_de_rodadas(self, valor):
        self._total_de_rodadas += valor

    def gerenciamento_da_partida(self):
        ordem_dos_jogadores_da_partida = self.define_ordem_de_jogadores()
        fim_da_partida = False
        nome_do_vencedor = None
        while not fim_da_partida:
            resultado = self.rodada(ordem_dos_jogadores_da_partida)
            fim_da_partida, nome_do_vencedor = self.fim_da_partida(resultado)
        return resultado, nome_do_vencedor, self.encerada_por_timeout, self.total_de_rodadas

    def define_ordem_de_jogadores(self):
        jogadores = [
            self.jogador_um,
            self.jogador_dois,
            self.jogador_tres,
            self.jogador_quatro
        ]
        resultado = list()
        total_de_jogadores = len(jogadores)
        for _ in range(total_de_jogadores):
            jogador_escolhido_da_vez = random.choice(jogadores)
            resultado.append(jogador_escolhido_da_vez)
            jogadores.remove(jogador_escolhido_da_vez)
        return resultado

    def fim_da_partida(self, jogadores):
        conta_jogadores_eliminados = 0
        nome_do_vencedor = None
        if self.total_de_rodadas == 1000:
            self.encerada_por_timeout = True
            return True, "terminou por time out"

        for jogador in jogadores:
            if jogador.saldo <= 0:
                conta_jogadores_eliminados += 1
            else:
                nome_do_vencedor = jogador.comportamento

        if conta_jogadores_eliminados == len(jogadores):
            return True, "Não houve vencedor..."
        elif conta_jogadores_eliminados == len(jogadores)-1:
            return True, nome_do_vencedor
        return False, None

    def rodada(self, jogadores):
        self.total_de_rodadas = 1
        for jogador in jogadores:
            if jogador.saldo > 0:
                self.tabuleiro(jogador)
            else:
                for propriedade in self.propriedades:
                    if propriedade.get("proprietario"):
                        if propriedade.get("proprietario").comportamento == jogador.comportamento:
                            propriedade["proprietario"] = ""

        return jogadores

    def tabuleiro(self, jogador):
        resultado_do_dado = jogador.joga_o_dado()
        vai_para_essa_propriedade = jogador.proxima_proprieda(resultado_do_dado)
        propriedade = self.propriedades[vai_para_essa_propriedade - 1]

        if not propriedade.get("proprietario") and jogador.saldo >= propriedade.get("custo_de_venda"):

            if jogador.comportamento == 'exigente' and propriedade.get('valor_aluguel') > 50:

               propriedade["proprietario"] = jogador
               jogador.paga(propriedade.get("custo_de_venda"))

            elif jogador.comportamento == 'cauteloso':
                saldo_reserva = jogador.saldo - propriedade.get("custo_de_venda")
                if saldo_reserva >= 80:

                    propriedade["proprietario"] = jogador
                    jogador.paga(propriedade.get("custo_de_venda"))

            elif jogador.comportamento == "aleatorio" and random.choice(['compro', 'não compro']) == 'compro':
                propriedade["proprietario"] = jogador
                jogador.paga(propriedade.get("custo_de_venda"))

            elif jogador.comportamento == "impulsivo":
                propriedade["proprietario"] = jogador
                jogador.paga(propriedade.get("custo_de_venda"))

        else:
            if propriedade.get('proprietario'):
                if propriedade.get("proprietario").comportamento != jogador.comportamento:
                    jogador.paga(propriedade.get("valor_aluguel"))
                    propriedade.get("proprietario").recebe(propriedade.get("valor_aluguel"))

        jogador.verifica_se_completou_uma_volta_no_tabuleiro(resultado_do_dado)


if __name__ == '__main__':
    contador_de_exigente = 0
    contador_de_impulsivo = 0
    contador_de_cauteloso = 0
    contador_de_aleatorio = 0
    quantas_partidas_terminam_por_time_out=0
    media_de_rodadas_por_partida = 0
    comportamento_que_mais_vence=0
    soma_de_todas_rodadas = 0

    for _ in range(299):
        partida = Partida()
        jogadores, nome_do_vencedor, encerada_por_timeout, total_de_rodadas = partida.gerenciamento_da_partida()

        if encerada_por_timeout:
            quantas_partidas_terminam_por_time_out += 1

        if nome_do_vencedor == 'exigente':
            contador_de_exigente += 1

        if nome_do_vencedor == 'impulsivo':
            contador_de_impulsivo += 1

        if nome_do_vencedor == 'cauteloso':
            contador_de_cauteloso += 1

        if nome_do_vencedor == 'aleatorio':
            contador_de_aleatorio += 1

        if total_de_rodadas < 1000:
            soma_de_todas_rodadas += total_de_rodadas

    media_de_rodadas_por_partida = soma_de_todas_rodadas / 300
    porcentagem_de_exigentes = (contador_de_exigente / 300) * 100
    porcentagem_de_impulsivos = (contador_de_impulsivo / 300) * 100
    porcentagem_de_cautelosos = (contador_de_cauteloso / 300) * 100
    porcentagem_de_aleatorio = (contador_de_aleatorio / 300) * 100

    print('*' * 50)
    print(f"Total de partidas que terminam por Time out {quantas_partidas_terminam_por_time_out}")
    print(f"Média de turnos por partida (sem Time out) {media_de_rodadas_por_partida:.0f}")
    print(f'Porcentagem de vitórias de exigentes {porcentagem_de_exigentes:.2f}%')
    print(f"Porcentagem de vitórias de impulsivos {porcentagem_de_impulsivos:.2f}%")
    print(f"Porcentagem de vitórias de cautelosos {porcentagem_de_cautelosos:.2f}%")
    print(f"Porcentagem de vitórias de aleatorio {porcentagem_de_aleatorio:.2f}%")
    comportamento_que_mais_vence = [
        contador_de_impulsivo,
        contador_de_exigente,
        contador_de_aleatorio,
        contador_de_cauteloso
    ]
    comportamento_que_mais_vence.sort()
    print(f"Comportamento que mais vence {comportamento_que_mais_vence[-1]}")
    print('*' * 50)


