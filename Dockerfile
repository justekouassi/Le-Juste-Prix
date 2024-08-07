# Utilise une image de base officielle de Python
FROM python:3.12.4

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers locaux dans le conteneur
COPY . /app

# Installer les dépendances
# RUN pip install --no-cache-dir -r requirements.txt

# Définir la commande par défaut à exécuter
CMD ["python", "JustePrix.py"]
