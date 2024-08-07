import random
import time
import os
from colorama import init, Fore, Style

# Initialisation de colorama
init(autoreset=True)

# Configuration du jeu par défaut
DEFAULT_ATTEMPTS = 6
DEFAULT_TIMING = 30
DEFAULT_LOW_PRICE = 1
DEFAULT_HIGH_PRICE = 200
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


def choisir_difficulte():
    print("Choisissez un niveau de difficulté :")
    print("1. Facile (1 à 100)")
    print("2. Moyen (1 à 200)")
    print("3. Difficile (1 à 500)")
    choix = input("Votre choix (1/2/3) : ")
    if choix == "1":
        return 100
    elif choix == "2":
        return 200
    elif choix == "3":
        return 500
    else:
        print("Choix invalide, niveau moyen sélectionné par défaut.")
        return 200


def afficher_meilleur_score(leaderboard):
    if leaderboard:
        meilleur_score = min(leaderboard, key=lambda x: x[1])
        print(f"\n{Fore.GREEN}Meilleur score actuel : {
              meilleur_score[0]} - {meilleur_score[1]} secondes{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.GREEN}Pas de score enregistré pour le moment.{
              Style.RESET_ALL}")


def jeu_du_juste_prix():
    print(f"{Fore.BLUE}Bienvenue dans le jeu du Juste Prix !{Style.RESET_ALL}\n\
Devinez le prix de l'objet caché dans ma droite.\n\
Vous aurez {DEFAULT_ATTEMPTS} tentatives et {DEFAULT_TIMING} secondes maximum\n\
Bonne chance !\n")

    player_name = input("Entrez votre nom : ")
    high_price = choisir_difficulte()
    right_price = random.randint(DEFAULT_LOW_PRICE, high_price)
    attempts = DEFAULT_ATTEMPTS
    start_time = time.time()
    propositions = []

    afficher_meilleur_score(leaderboard)

    while attempts:
        try:
            proposition = int(
                input(f"\nEntrez votre proposition (tentatives restantes : {attempts}) : "))
        except ValueError:
            print("Veuillez entrer un nombre valide.")
            continue

        if proposition < DEFAULT_LOW_PRICE or proposition > high_price:
            print(f"Le nombre doit être entre {
                  DEFAULT_LOW_PRICE} et {high_price}.")
            continue

        propositions.append(proposition)

        if proposition > right_price:
            print(f"{Fore.YELLOW}C'est moins{Style.RESET_ALL}")
        elif proposition < right_price:
            print(f"{Fore.YELLOW}C'est plus{Style.RESET_ALL}")
        else:
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"{Fore.GREEN}BRAVO {player_name} ! Le juste prix était : {
                  right_price}{Style.RESET_ALL}")
            print(f"Vous avez trouvé en {int(elapsed_time)} secondes.")
            leaderboard.append((player_name, int(elapsed_time)))
            save_leaderboard(leaderboard)
            break

        past_time = time.time() - start_time
        print(f"Temps écoulé : {int(past_time)} secondes")
        print(f"Historique des propositions : {propositions}")

        if past_time > DEFAULT_TIMING:
            print(f"\n{Fore.RED}Temps écoulé{Style.RESET_ALL}")
            break

        attempts -= 1

    if attempts == 0 and proposition != right_price:
        print(f"\n{Fore.RED}PERDU {player_name}. Le juste prix était : {
              right_price}{Style.RESET_ALL}")

    afficher_leaderboard()

    rejouer = input("\nVoulez-vous rejouer ? (oui/non) : ").lower()
    if rejouer == "oui":
        jeu_du_juste_prix()
    else:
        print("Merci d'avoir joué ! À bientôt.")


def afficher_leaderboard():
    leaderboard = load_leaderboard()
    if leaderboard:
        print(f"\n{Fore.CYAN}--- Leaderboard ---{Style.RESET_ALL}")
        leaderboard.sort(key=lambda x: x[1])
        for rank, (name, time_val) in enumerate(leaderboard[:5], start=1):
            print(f"{rank}. {name} - {time_val} secondes")
    else:
        print(f"\n{Fore.CYAN}--- Leaderboard vide ---{Style.RESET_ALL}")


# Charger le leaderboard existant
leaderboard = load_leaderboard()

# Lancer le jeu
jeu_du_juste_prix()
