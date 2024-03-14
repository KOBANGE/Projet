#realisé par : KOBANGE OBED GC
#              MUNZUMBU ANDRE GC

class Client:
    def __init__(self, identifiant):
        self.identifiant = identifiant
        self.appels = []
        self.sms = []
        self.internet = []

    def ajouter_appel(self, appel):
        self.appels.append(appel)

    def ajouter_sms(self, sms):
        self.sms.append(sms)

    def ajouter_internet(self, internet):
        self.internet.append(internet)

    def calculer_facture(self):
        montant_total = 0.0
        for appel in self.appels:
            montant_total += appel.calculer_cout()
        for sms in self.sms:
            montant_total += sms.calculer_cout()
        for internet in self.internet:
            montant_total += internet.calculer_cout()
        return montant_total


class Appel:
    def __init__(self, duree, meme_reseau):
        self.duree = duree
        self.meme_reseau = meme_reseau

    def calculer_cout(self):
        if self.meme_reseau:
            return 0.025 * self.duree
        else:
            return 0.05 * self.duree


class SMS:
    def __init__(self, meme_reseau):
        self.meme_reseau = meme_reseau

    def calculer_cout(self):
        if self.meme_reseau:
            return 0.001
        else:
            return 0.002


class Internet:
    def __init__(self, volume):
        self.volume = volume

    def calculer_cout(self):
        return 0.03 * self.volume


class ImportCDR:
    def __init__(self, fichier):
        self.pile_cdr = self.importer_fichier_cdr(fichier)

    def importer_fichier_cdr(self, fichier):
        pile_cdr = []
        with open(fichier, 'r') as file:
            for line in file:
                cdr = self.parse_cdr(line)
                pile_cdr.append(cdr)
        return pile_cdr

    def parse_cdr(self, cdr_string):
        cdr_fields = cdr_string.strip().split('|')
        cdr = {
            'identifiant': int(cdr_fields[0]),
            'type_call': int(cdr_fields[1]),
            'date_heure': cdr_fields[2],
            'appelant': cdr_fields[3],
            'appele': cdr_fields[4],
            'duree': int(cdr_fields[5]) if cdr_fields[5] != '' else 0,
            'taxe': int(cdr_fields[6]),
            'total_volume': int(cdr_fields[7])
        }
        return cdr


class Statistiques:
    def __init__(self, pile_cdr):
        self.pile_cdr = pile_cdr

    def calculer_statistiques(self, num_client, date_debut, date_fin):
        nb_appels = 0
        duree_appels = 0
        nb_sms = 0
        nb_internet = 0
        volume_internet = 0

        for cdr in self.pile_cdr:
            if cdr['appelant'] == num_client and date_debut <= cdr['date_heure'] <= date_fin:
                if cdr['type_call'] == 0:
                    nb_appels += 1
                    duree_appels += cdr['duree']
                elif cdr['type_call'] == 1:
                    nb_sms += 1
                elif cdr['type_call'] == 2:
                    nb_internet += 1
                    volume_internet += cdr['total_volume']

        return nb_appels, duree_appels, nb_sms, nb_internet, volume_internet


# Exemple d'utilisation
if __name__ == "__main__":
    # Importation du fichier CDR
    import_cdr_1 = ImportCDR('cdr.txt')
    import_cdr_2 = ImportCDR('tp_algo.txt')

    pile_cdr_1 = import_cdr_1.pile_cdr
    pile_cdr_2 = import_cdr_2.pile_cdr

    pile_cdr = pile_cdr_1 + pile_cdr_2
    # Création du client POLYTECHNIQUE
    client_polytechnique = Client("POLYTECHNIQUE")

    # Parcours de la pile CDR et ajout des informations au client
    for cdr in pile_cdr:
        if cdr['appelant'] == '243818140560' or cdr['appelant'] == '243818140120':
            if cdr['type_call'] == 0:
                meme_reseau = cdr['appelant'][:6] == cdr['appele'][:6]
                appel = Appel(cdr['duree'], meme_reseau)
                client_polytechnique.ajouter_appel(appel)
            elif cdr['type_call'] == 1:
                meme_reseau = cdr['appelant'][:6] == cdr['appele'][:6]
                sms = SMS(meme_reseau)
                client_polytechnique.ajouter_sms(sms)
            elif cdr['type_call'] == 2:
                internet = Internet(cdr['total_volume'])
                client_polytechnique.ajouter_internet(internet)

    # Calcul de la facture du client POLYTECHNIQUE
    facture_polytechnique = client_polytechnique.calculer_facture()
    print("Facture du client POLYTECHNIQUE:", facture_polytechnique)

    # Calcul des statistiques pour le client POLYTECHNIQUE entre deux dates
    statistiques = Statistiques(pile_cdr)
    nb_appels_1, duree_appels_1, nb_sms_1, nb_internet_1, volume_internet_1 = statistiques.calculer_statistiques(
        '243818140560', '20230101000000', '20231231000000'
    )
    print("Voici les statistiques pour le numéro 243818140560 :")
    print("Nombre d'appels:", nb_appels_1)
    print("Durée totale des appels:", duree_appels_1)
    print("Nombre de SMS:", nb_sms_1)
    print("Nombre d'utilisations d'internet:", nb_internet_1)
    print("Volume internet utilisé:", volume_internet_1)

    nb_appels_2, duree_appels_2, nb_sms_2, nb_internet_2, volume_internet_2 = statistiques.calculer_statistiques(
        '243818140120', '20230101000000', '20231231000000'
    )
    print("Voici les statistiques pour le numéro 243818140120 :")
    print("Nombre d'appels:", nb_appels_2)
    print("Durée totale des appels:", duree_appels_2)
    print("Nombre de SMS:", nb_sms_2)
    print("Nombre d'utilisations d'internet:", nb_internet_2)
    print("Volume internet utilisé:", volume_internet_2)