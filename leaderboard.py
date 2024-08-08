import os
from colorama import Fore, Style

LEADERBOARD_FILE = "leaderboard.txt"


def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        return []

    with open(LEADERBOARD_FILE, "r") as file:
        leaderboard = []
        for line in file:
            name, time_str = line.strip().split(',')
            leaderboard.append((name, int(time_str)))
    return leaderboard


def save_leaderboard(leaderboard):
    with open(LEADERBOARD_FILE, "w") as file:
        for name, time_val in leaderboard:
            file.write(f"{name},{time_val}\n")


def afficher_leaderboard(leaderboard):
    if leaderboard:
        print(f"\n{Fore.CYAN}--- Leaderboard ---{Style.RESET_ALL}")
        leaderboard.sort(key=lambda x: x[1])
        for rank, (name, time_val) in enumerate(leaderboard[:5], start=1):
            print(f"{rank}. {name} - {time_val} secondes")
    else:
        print(f"\n{Fore.CYAN}--- Leaderboard vide ---{Style.RESET_ALL}")
