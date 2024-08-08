import random
import time
from colorama import init, Fore, Style
from leaderboard import load_leaderboard, save_leaderboard, afficher_leaderboard

# Initialisation de colorama
init(autoreset=True)

# Configuration du jeu par défaut
DEFAULT_ATTEMPTS = 6
DEFAULT_TIMING = 300
DEFAULT_LOW_PRICE = 1
DEFAULT_HIGH_PRICE = 200


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

    leaderboard = load_leaderboard()

    player_name = input("Entrez votre nom : ")
    high_price = choisir_difficulte()
    right_price = random.randint(DEFAULT_LOW_PRICE, high_price)
    attempts = DEFAULT_ATTEMPTS
    start_time = time.time()
    propositions = []

    afficher_meilleur_score(leaderboard)

    low_bound = DEFAULT_LOW_PRICE
    high_bound = high_price

    while attempts:
        try:
            proposition = int(
                input(f"\nEntrez votre proposition (tentatives restantes : {attempts}) : "))
        except ValueError:
            print("Veuillez entrer un nombre valide.")
            continue

        if proposition < low_bound or proposition > high_bound:
            print(f"Le nombre doit être entre {low_bound} et {high_bound}.")
            continue

        propositions.append(proposition)

        if proposition > right_price:
            print(f"{Fore.YELLOW}C'est moins{Style.RESET_ALL}")
            high_bound = proposition - 1
        elif proposition < right_price:
            print(f"{Fore.YELLOW}C'est plus{Style.RESET_ALL}")
            low_bound = proposition + 1
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
        print(f"Intervalle restant pour la prochaine proposition : {
              low_bound} à {high_bound}")

        if past_time > DEFAULT_TIMING:
            print(f"\n{Fore.RED}Temps écoulé{Style.RESET_ALL}")
            print(f"{Fore.RED}Le juste prix était : {
                  right_price}{Style.RESET_ALL}")
            break

        attempts -= 1
        time.sleep(2)  # Ralentir le jeu de deux secondes entre les tentatives

    if attempts == 0 and proposition != right_price:
        print(f"\n{Fore.RED}PERDU {player_name}. Le juste prix était : {
              right_price}{Style.RESET_ALL}")

    afficher_leaderboard(leaderboard)

    rejouer = input("\nVoulez-vous rejouer ? (oui/non) : ").lower()
    if rejouer == "oui":
        jeu_du_juste_prix()
    else:
        print("Merci d'avoir joué ! À bientôt.")
