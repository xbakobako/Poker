class PokerGame:
    def __init__(self, player_names):
        self.players = {name: 0 for name in player_names}
        self.rounds = 0

    def add_points(self, player_name, points):
        if player_name in self.players:
            self.players[player_name] += points
        else:
            print(f"Player {player_name} does not exist.")

    def subtract_points(self, player_name, points):
        if player_name in self.players:
            self.players[player_name] -= points
        else:
            print(f"Player {player_name} does not exist.")

    def show_scores(self):
        print(f"Scores after round {self.rounds}:")
        for player, score in self.players.items():
            print(f"{player}: {score} points")

    def next_round(self):
        self.rounds += 1
        print(f"Starting round {self.rounds}")

    def get_winner(self):
        winner = max(self.players, key=self.players.get)
        return winner, self.players[winner]

# 使用例
player_names = ["Alice", "Bob", "Charlie"]
game = PokerGame(player_names)

# ラウンド1
game.next_round()
game.add_points("Alice", 10)
game.add_points("Bob", 5)
game.add_points("Charlie", 7)
game.show_scores()

# ラウンド2
game.next_round()
game.add_points("Alice", 3)
game.subtract_points("Bob", 2)
game.add_points("Charlie", 8)
game.show_scores()

# 勝者を表示
winner, score = game.get_winner()
print(f"The winner is {winner} with {score} points!")