import os
import sys

class Score:
    def __init__(self, n_players, initial_score, namelist):
        self.n_players = n_players
        self.initial_score = initial_score
        self.namelist = namelist
        self.field = 0
        self.dealer = 0
        self.scores = [initial_score] * n_players
        self.stage = 0
        self.status = [0] * n_players
        self.falded = [0] * n_players
        self.bets = [0] * n_players
        self.turn = 1
        self.round = 1
        self.max = 0
        self.allIn = 0

    def show(self):
        print(f"Round: {self.round}")
        print(f"Stage: {self.stage + 1}")
        print(f"Dealer: {self.namelist[self.dealer]}")
        print(f"Current Player: {self.namelist[self.turn]}")
        print(f"Field: {self.field}")
        print("")
        print("Player's remaining tips:")
        for i in range(self.n_players):
            print(f"{self.namelist[i]}: {self.scores[i]}")
        print("")
        print("Bets:")
        for i in range(self.n_players):
            if self.falded[i] == 1:
                print("")
            else:
                print(f"{self.namelist[i]}: {self.bets[i]}")
        print("")

    def changeStage(self):
        for i in range(self.n_players):
            if self.status[i] == 0:
                return True
        self.stage += 1
        self.turn = (self.dealer + 1) % self.n_players
        if self.stage == 4:
            return False
        self.status = self.falded.copy()
        self.field += sum(self.bets)
        for i in range(self.n_players):
            self.scores[i] -= self.bets[i]
            self.bets[i] = 0
        self.max = 0
        return True
            

    def oneGame(self):
        self.field = 0
        self.stage = 0
        self.status = [0] * self.n_players
        self.bets = [0] * self.n_players
        self.turn = (self.dealer + 1) % self.n_players
        self.max = 0
        for i in range(self.n_players):
            if self.scores[i] <= 0:
                self.falded[i] = 1
        while self.changeStage():
            if self.falded[self.turn] == 1 or self.scores[self.turn] <= 0:
                self.status[self.turn] = 1
                self.turn = (self.turn + 1) % self.n_players
                continue
            clear()
            self.show()
            print("Press r to raise, c to call, f to fold, or e to end the game.")
            choice = input(f"{self.namelist[self.turn]}, enter your choice: ")
            if choice == 'r':
                if self.max >= self.scores[self.turn]:
                    print("You cannot raise more than your remaining tips.")
                    continue
                while True:
                    raise_amount = input("Enter the amount to bet: ")
                    try:
                        raise_amount = int(raise_amount)
                        if raise_amount > self.scores[self.turn]:
                            print("You cannot raise more than your remaining score.")
                            continue
                        if raise_amount < self.bets[self.turn]:
                            print("You cannot bet less than your previous bet.")
                            continue
                        if raise_amount <= self.max:
                            print("You cannot bet less than the maximum bet.")
                            continue
                        break
                    except ValueError:
                        print("Invalid input. Please enter a valid number.")
                self.bets[self.turn] = raise_amount
                if raise_amount == self.scores[self.turn]:
                    self.allIn = 1
                self.max = raise_amount
                self.status= self.falded.copy()
                self.status[self.turn] = 1
                self.turn = (self.turn + 1) % self.n_players
            elif choice == 'c':
                self.bets[self.turn] = min(self.max, self.scores[self.turn])
                if self.bets[self.turn] == self.scores[self.turn]:
                    self.allIn = 1
                self.status[self.turn] = 1
                self.turn = (self.turn + 1) % self.n_players
            elif choice == 'f':
                self.falded[self.turn] = 1
                self.status[self.turn] = 1
                self.turn = (self.turn + 1) % self.n_players
            elif choice == 'e':
                sys.exit()
            else:
                print("Invalid choice, please try again.")



    def edit(self):
        while True:
            clear()
            self.show()
            print("Press the number of the player you want to change the point.")
            print("Press q to quit, or a to add a player, or d to delete a player.")
            choice = input("Enter your choice: ")
            if choice == 'q':
                break
            elif choice == 'a':
                name = input("Enter the name of the new player: ")
                while not name or name.isspace():
                    print("Name cannot be empty. Please enter a valid name.")
                    name = input("Enter the name of the new player: ")
                self.n_players += 1
                self.namelist.append(name)
                self.scores.append(self.initial_score)
                self.status.append(0)
                self.falded.append(0)
                self.bets.append(0)
            elif choice == 'd':
                while True:
                    try:
                        choice = int(input("Enter the number of the player to delete: "))
                        if 1 <= choice <= self.n_players:
                            break
                        else:
                            print("Invalid choice, please try again.")
                    except ValueError:
                        print("Invalid input. Please enter a valid number.")
                self.n_players -= 1
                del self.namelist[choice - 1]
                del self.scores[choice - 1]
                del self.status[choice - 1]
                del self.falded[choice - 1]
                del self.bets[choice - 1]
                continue
            try:
                choice = int(choice)
                if 1 <= choice <= self.n_players:
                    while True:
                        try:
                            new_score = int(input(f"Enter new score for {self.namelist[choice - 1]}: "))
                            break
                        except ValueError:
                            print("Invalid input. Please enter a valid number.")
                    self.scores[choice - 1] = new_score
                else:
                    print("Invalid choice, please try again.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    def all(self):
        N = self.field
        while N > 0:
            clear()
            self.show()
            print(f'{N}points left')
            print("Press the number of the player to give them points.")
            try:
                choice = int(input("Enter your choice: "))
                if 1 <= choice <= self.n_players and self.falded[choice - 1] == 0:
                    while True:
                        try:
                            n = int(input(f"Enter the number of points to give {self.namelist[choice - 1]}: "))
                            break
                        except ValueError:
                            print("Invalid input. Please enter a valid number.")
                    if n > N:
                        print("You cannot give more points than the tips left.")
                        continue
                    if n < 0:
                        print("You cannot give negative points.")
                        continue
                    if n > 0:
                        N -= n
                        self.scores[choice - 1] += n
                        print(f"{self.namelist[choice - 1]} has been given {n} points.")
                    else:
                        print("Not enough points.")
                else:
                    print("Invalid choice, please try again.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")
                continue

    def Game(self):
        while True:
            while True:
                clear()
                self.show()
                print("Press c to continue, or e to edit")
                choice = input("Enter your choice: ")
                if choice == 'c':
                    break
                elif choice == 'e':
                    self.edit()
                    continue
                else:
                    print("Invalid choice, please try again.")
            self.oneGame()
            clear()
            print("The game is over.")
            if self.allIn == 1:
                print("All in occurred.")
                self.all()
            else:
                print("Enter the number of the player who won.")
                for i in range(self.n_players):
                    if self.falded[i] == 0:
                        print(f"{i + 1}: {self.namelist[i]}")
                    else:
                        print("")
                while True:
                    try:
                        winner = int(input("Enter your choice: "))
                    except ValueError:
                        print("Invalid input. Please enter a valid number.")
                        continue
                    if 1 <= winner <= self.n_players and self.falded[winner - 1] == 0:
                        break
                    else:
                        print("Invalid choice, please try again.")
                self.scores[winner - 1] += self.field
            self.round += 1
            self.field = 0
            self.dealer = (self.dealer + 1) % self.n_players
            self.status = [0] * self.n_players
            self.falded = [0] * self.n_players
            self.bets = [0] * self.n_players
            self.stage = 0
            self.turn = (self.dealer + 1) % self.n_players
            self.max = 0
            self.allIn = 0


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    n = int(input("Enter a number of players: "))
    clear()
    namelist = []
    print("Welcome to the game!")
    print("Please enter the names of the players.")
    for i in range(n):
        name = input(f"Enter name of player {i + 1}: ")
        while not name or name.isspace():
            print("Name cannot be empty. Please enter a valid name.")
            name = input(f"Enter name of player {i + 1}: ")
        namelist.append(name)
    clear()
    print("The players are as follows:")
    for i in range(n):
        print(f"Player {i + 1}: {namelist[i]}")
    print("Press the number of the player you want to change the name of.")
    print("Press 0 to continue.")
    while True:
        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            continue
        if choice == 0:
            break
        elif 1 <= choice <= n:
            new_name = input(f"Enter new name for player {choice}: ")
            namelist[choice - 1] = new_name
            clear()
            print("The players are as follows:")
            for i in range(n):
                print(f"Player {i + 1}: {namelist[i]}")
        else:
            print("Invalid choice, please try again.")
        print("Press the number of the player you want to change the name of.")
        print("Press 0 to continue.")
    clear()
    while True:
        initialScore = input("Enter the initial score for each player: ")
        try:
            initialScore = int(initialScore)
            break
        except ValueError:
            clear()
            print("Invalid input. Please enter a valid number.")
    clear()
    score = Score(n, initialScore, namelist)
    score.Game()

if __name__ == "__main__":
    main()