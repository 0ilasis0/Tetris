from core.tetris_game.manager import TetrisCore, player0, player1
from core.tetris_game.variable import GameState


class BattleManager:
    def __init__(self, players: list[TetrisCore]):
        self.players = players
        for player in self.players:
            player.attack_mg.enabled = True

        self.logs = []  # 攻擊紀錄

    def resolve_attack(self, defender: TetrisCore, net: int):
        ko_counter, alive = defender.attack_mg.raise_bottom(defender, net)
        self.logs.append({"lines": net, "ko_counter": ko_counter, "alive": alive})

    def get_alive_players(self):
        """取得仍存活的玩家"""
        return [player for player in self.players if player.state != GameState.GAMEOVER]

battle_manager = BattleManager([player0, player1])
