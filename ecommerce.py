from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://localhost:27017/")
db = client["ecommerceDB"]

produits = db["produits"]
clients = db["clients"]
commandes = db["commandes"]


def creer_commande(client_nom, produits_list, statut="en cours"):
    montant_total = 0
    for p in produits_list:
        montant_total += p["prix"] * p["quantite"]

    commande = {
        "client": client_nom,
        "produits": produits_list,
        "date_commande": datetime.now(),
        "statut": statut,
        "montant_total": montant_total
    }
    commandes.insert_one(commande)
    print("Commande ajoutée avec succès !")

def afficher_produits():
    for p in produits.find():
        print(p)



def commandes_par_client(nom_client):
    for c in commandes.find({"client": nom_client}):
        print(c)



def commandes_livrees():
    for c in commandes.find({"statut": "livrée"}):
        print(c)



def maj_produit(nom_produit, nouveau_prix=None, nouveau_stock=None):
    update = {}

    if nouveau_prix is not None:
        update["prix"] = nouveau_prix
    if nouveau_stock is not None:
        update["stock"] = nouveau_stock

    produits.update_one({"nom": nom_produit}, {"$set": update})
    print("Produit mis à jour !")


def ajouter_champ_disponible():
    produits.update_many({}, {"$set": {"disponible": True}})
    print("Champ 'disponible' ajouté !")


def supprimer_commande(client_nom, produit_nom):
    commandes.delete_many({
        "client": client_nom,
        "produits.nom": produit_nom
    })
    print("Commande supprimée !")


def supprimer_commandes_client(nom_client):
    commandes.delete_many({"client": nom_client})
    print("Commandes du client supprimées !")


def commandes_triees():
    for c in commandes.find().sort("date_commande", -1):
        print(c)



def produits_disponibles():
    for p in produits.find({"disponible": True}):
        print(p)


def menu():
    while True:
        print("\n===== MENU =====")
        print("1. Ajouter une commande")
        print("2. Afficher tous les produits")
        print("3. Afficher les produits disponibles")
        print("4. Rechercher une commande par client")
        print("5. Mettre à jour un produit")
        print("6. Supprimer une commande")
        print("7. Supprimer les commandes d’un client")
        print("8. Afficher produits disponibles")
        print("9. Trier les commandes par date")
        print("10. Quitter")

        choix = input("Votre choix : ")

        if choix == "1":
            nom = input("Nom du client : ")
            produit = input("Nom du produit : ")
            prix = float(input("Prix : "))
            qte = int(input("Quantité : "))
            creer_commande(nom, [{"nom": produit, "prix": prix, "quantite": qte}])

        elif choix == "2":
            afficher_produits()

        elif choix == "3":
            produits_disponibles()

        elif choix == "4":
            nom = input("Nom du client : ")
            commandes_par_client(nom)

        elif choix == "5":
            nom = input("Nom du produit : ")
            prix = float(input("Nouveau prix : "))
            stock = int(input("Nouveau stock : "))
            maj_produit(nom, prix, stock)

            

        elif choix == "6":
            client = input("Nom du client : ")
            prod = input("Nom du produit : ")
            supprimer_commande(client, prod)

        elif choix == "7":
            nom = input("Nom du client : ")
            supprimer_commandes_client(nom)

        elif choix == "8":
            produits_disponibles()

        elif choix == "9":
            commandes_triees()

        elif choix == "10":
            print("Au revoir !")
            break

        else:
            print("Choix invalide.")


menu()
