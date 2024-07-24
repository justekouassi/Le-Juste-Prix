import random
import time

print("Bienvenue dans le jeu du Juste Prix !\n\
Devinez le prix auquel je pense.\n\
Il se situe entre 1 et 100. Bonne chance !\n")

right_price = random.randint(1, 100)
proposition = int(input("Entrez votre proposition : "))

start_time = time.time()

attempts = 5
while right_price != proposition and attempts > 0:

    if proposition > right_price:
        print("C'est moins")
    elif proposition < right_price:
        print("C'est plus")

    past_time = time.time() - start_time
    print("Seconds =", past_time)
    if time.time() - start_time > 30:
        print("\nTemps écoulé")
        break

    proposition = int(input("Entrez votre proposition : "))
    attempts -= 1

if attempts == 0 and right_price != proposition:
    print("\nPERDU. Le juste prix était :", right_price)
else:
    print("\nBRAVO ! Le juste prix était :", right_price)
