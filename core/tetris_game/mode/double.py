from core.tetris_game.attack.manager import battle_manager


def main_double():
    """
    每次更新都從內部 players 依序檢查落地攻擊值，
    兩人都落地就自動結算攻擊。
    """
    # 兩人都準備好 → 結算
    if battle_manager.players[0].attack_mg.attack_enable and battle_manager.players[1].attack_mg.attack_enable:
        net = battle_manager.players[0].attack_mg.attack - battle_manager.players[1].attack_mg.attack
        if net > 0:
            battle_manager.resolve_attack(battle_manager.players[1], net)
        elif net < 0:
            battle_manager.resolve_attack(battle_manager.players[0], -net)

        battle_manager.players[0].attack_mg.clear_attack()
        battle_manager.players[1].attack_mg.clear_attack()
