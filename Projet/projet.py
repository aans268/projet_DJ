class JeuSequentiel:
    """
    Represente un jeu sequentiel, a somme
    nulle, a information parfaite
    """
    def __init__(self):
        pass

    def joueurCourant(self, C):
        """
        Rend le joueur courant dans la
        configuration C
         """
        raise NotImplementedError

    def coupsPossibles(self, C):
        """
        Rend la liste des coups possibles dans
        la configuration C
        """
        raise NotImplementedError

    def f1(self, C):
        """
        Rend la valeur de l’evaluation de la
        configuration C pour le joueur 1
        """
        raise NotImplementedError

    def joueLeCoup(self, C, coup):
        """
        Rend la configuration obtenue apres
        que le joueur courant ait joue le coup
        dans la configuration C
        """
        raise NotImplementedError

    def estFini(self, C):
        """
        Rend True si la configuration C est
        une configuration finale
        """
        raise NotImplementedError
    
    def afficher_plateau(self,C):
        raise NotImplementedError
    
################################################################################################################################################################

class Morpion(JeuSequentiel):
    """
    Représente le jeu du morpion (3x3).
    """
    def __init__(self):
        super().__init__()
        self.plateau = [[str(i + 1) for i in range(j * 3, (j + 1) * 3)] for j in range(3)]
        self.joueur = 'X'  # X commence toujours

    def joueurCourant(self, C):
        return self.joueur

    def coupsPossibles(self, C):
        return [int(coup) for row in C for coup in row if coup.isdigit()]

    def f1(self, C):
        # Compter le nombre de 2 alignements pour le joueur 'X' sans être bloqué par 'O'.
        alignements = 0

        # Vérifier les lignes
        for ligne in C:
            if ligne.count('X') == 2 and 'O' not in ligne:
                alignements += 1

        # Vérifier les colonnes
        for col in range(3):
            if [C[ligne][col] for ligne in range(3)].count('X') == 2 and 'O' not in [C[ligne][col] for ligne in range(3)]:
                alignements += 1

        # Vérifier les diagonales
        if [C[i][i] for i in range(3)].count('X') == 2 and 'O' not in [C[i][i] for i in range(3)]:
            alignements += 1
        if [C[i][2-i] for i in range(3)].count('X') == 2 and 'O' not in [C[i][2-i] for i in range(3)]:
            alignements += 1

        return alignements
    
    def f2(self, C):
        # Compter le nombre de 2 alignements pour le joueur 'O' sans être bloqué par 'X'.
        alignements = 0

        # Vérifier les lignes
        for ligne in C:
            if ligne.count('O') == 2 and 'X' not in ligne:
                alignements += 1

        # Vérifier les colonnes
        for col in range(3):
            if [C[ligne][col] for ligne in range(3)].count('O') == 2 and 'X' not in [C[ligne][col] for ligne in range(3)]:
                alignements += 1

        # Vérifier les diagonales
        if [C[i][i] for i in range(3)].count('O') == 2 and 'X' not in [C[i][i] for i in range(3)]:
            alignements += 1
        if [C[i][2-i] for i in range(3)].count('O') == 2 and 'X' not in [C[i][2-i] for i in range(3)]:
            alignements += 1

        return alignements


    def joueLeCoup(self, coup):
        """
        Joue un coup sur le plateau en remplaçant le chiffre par le symbole du joueur.
        Args:
            coup (int): Le numéro du coup choisi par le joueur.
        """
        coup = str(coup)  # Convertir en chaîne pour la comparaison
        for i in range(3):
            for j in range(3):
                if self.plateau[i][j] == coup:
                    self.plateau[i][j] = self.joueur
                    self.joueur = 'O' if self.joueur == 'X' else 'X'
                    return

    def estFini(self, C):
        # Vérifie les lignes
        for ligne in C:
            if ligne[0] == ligne[1] == ligne[2] and ligne[0] in 'XO':
                return ligne[0]

        # Vérifie les colonnes
        for col in range(3):
            if C[0][col] == C[1][col] == C[2][col] and C[0][col] in 'XO':
                return C[0][col]

        # Vérifie les diagonales
        if (C[0][0] == C[1][1] == C[2][2] or C[0][2] == C[1][1] == C[2][0]) and C[1][1] in 'XO':
            return C[1][1]

        # Vérifie si le plateau est plein (aucun chiffre restant)
        if not any(c.isdigit() for row in C for c in row):
            return True

        # Aucun gagnant et le plateau n'est pas plein
        return False


    def afficher_plateau(self,plateau):
        """
        Affiche le plateau de jeu du morpion.
        Args:
        plateau (list[list[str]]): Configuration actuelle du plateau.
        """
        print()
        for ligne in plateau:
            print(" | ".join(ligne))
            print("-" * 9)
        print()

################################################################################################################################################################

class Allumettes(JeuSequentiel):
    """
    Représente le jeu des allumettes pour g groupes de m allumettes chacun.
    """
    def __init__(self, g: int, m: int):
        super().__init__()
        self.plateau = [m] * g
        self.joueur = 'X'  # Le joueur 1 commence toujours

    def joueurCourant(self, C):
        return self.joueur

    def coupsPossibles(self, C):
        """
        Rend la liste des coups possibles dans la configuration C.
        Un coup est représenté par un tuple (index_groupe, nombre_allumettes).
        """
        coups_possibles = []
        for i, nb_allumettes in enumerate(C):
            for j in range(1, nb_allumettes + 1):
                coups_possibles.append((i, j))
        return coups_possibles

    def f1(self, C):
        """
        Rend la valeur de l’évaluation de la configuration C pour le joueur 1.
        Plus la valeur est grande, plus la configuration est favorable au joueur 1.
        """
        # Une simple évaluation basée sur le nombre d'allumettes restantes dans le jeu
        return sum(C)

    def joueLeCoup(self, coup, affichage=False):
        """
        Joue un coup en retirant un certain nombre d'allumettes d'un groupe.
        Args:
            coup (tuple): Le coup à jouer, représenté par un tuple (index_groupe, nombre_allumettes).
        """
        index_groupe, nombre_allumettes = coup
        self.plateau[index_groupe] -= nombre_allumettes
        if affichage: print("Le joueur ",self.joueur," a enlevé ",nombre_allumettes," dans le groupe ",index_groupe+1,"\n")
        self.joueur = 'O' if self.joueur == 'X' else 'X'

    def estFini(self, C):
        """
        Rend True si la configuration C est une configuration finale.
        """
        if all(nb == 0 for nb in C): return self.joueur
        return False
    
    def afficher_plateau(self):
        """
        Affiche l'état actuel du jeu, y compris le plateau et le joueur courant.
        """
        for i, nb_allumettes in enumerate(self.plateau):
            print(f"Groupe {i + 1}: {'|' * nb_allumettes} ({nb_allumettes} allumettes)")


################################################################################################################################################################

class Strategie:
    """
    Represente une strategie de jeu
    """
    def __init__(self,jeu:JeuSequentiel):
        self.jeu = jeu

    def choisirProchainCoup(self, C):
        """
        Choisit un coup parmi les coups possibles dans la configuration C
        """
        raise NotImplementedError
    
    def decision(self,jeu,listecv):
        raise NotImplementedError
        
    def estimation(self,jeu,coup,profondeur):
        raise NotImplementedError
        
    def maxValue(jeu,profondeur):
        raise NotImplementedError
    
    def minValue(jeu,profondeur):
        raise NotImplementedError       
        
################################################################################################################################################################    

class StrategieAleatoire(Strategie):
    """
    Represente une strategie de jeu
    """
    def __init__(self,jeu:JeuSequentiel):
        super().__init__(jeu)

    def choisirProchainCoup(self, C):
        """
        Choisit un coup parmi les coups possibles dans la configuration C
        """
        import random
        coups_possibles=self.jeu.coupsPossibles(C)
        if coups_possibles:
            return random.choice(coups_possibles)
        else:
            print("Aucun coup dispo")
            return None

################################################################################################################################################################

class StrategieMinMax(Strategie):
    """
    Represente un strategie utilisant un arbre min-max de profondeur k
    """
    def __init__(self, jeu: JeuSequentiel, k: int):#, ...):
        super().__init__(jeu)
        self.jeu = jeu
        self.horizon=k
        
    def choisirProchainCoup(self, C):
        global joueur, horizon
        horizon= self.horizon
        joueur = self.jeu.joueur
        liste=self.jeu.coupsPossibles(C)
        cp=self.decision(self.jeu,liste)
        #print("cp:",cp)
        if (cp==[]):
            return []
        return cp
        
    def decision(self,jeu,listecv):
        max_score=-1000000000000000000000
    
        if joueur == 'X':
            bestone=listecv[0]
        else: 
            bestone=listecv[-1]
    
        est_list = []

        for coup in listecv:
            val=self.estimation(jeu,coup, horizon)
            est_list.append(val)
            #print(coup,val)
            if val>max_score:
                max_score=val
                bestone=coup

        best_list = []
        for i in range(len(listecv)):
            if est_list[i] == max_score:
                best_list.append(listecv[i])
        #print("BESTONE : ",score)
        import random
        return random.choice(best_list)

    def estimation(self,jeu,coup,profondeur):
        import copy
        jeuclone=copy.deepcopy(jeu)
        jeuclone.joueLeCoup(coup)
        if profondeur==0:
            #return self.evaluation(jeuclone)
            return jeuclone.f1(jeuclone.plateau)
        result=jeuclone.estFini(jeuclone.plateau)
        if result:
            if result=='X':
                return 100000 #bcp psq win condition
            elif result=='O':
                return -100000 #loose
            else:
                return -1000 #draw
        if jeuclone.joueur == joueur:
            return self.maxValue(jeuclone,profondeur)
        else :
            return self.minValue(jeuclone,profondeur)


    def maxValue(self,jeu,profondeur):
        liste=jeu.coupsPossibles(jeu.plateau)
        m=-100000
        for c in liste:
            #jeuclone=game.getCopieJeu(jeu)
            m = max(m,self.estimation(jeu,c,profondeur-1))
        return m

    def minValue(self,jeu,profondeur):
        liste=jeu.coupsPossibles(jeu.plateau)
        m=100000
        for c in liste:
            #jeuclone=game.getCopieJeu(jeu)
            m = min(m,self.estimation(jeu,c,profondeur-1))
        return m

################################################################################################################################################################

class StrategieAllumettes(Strategie):
    def __init__(self, jeu: Allumettes):
        super().__init__(jeu)
        self.valeurs_grundy = {}
        

    def valeurGrundy(self, C):
        if self.jeu.estFini(C):
            return 0
        if tuple(C) in self.valeurs_grundy:
            return self.valeurs_grundy[tuple(C)]

        valeurs_fils = [self.valeurGrundy(self.simuleCoup(C, coup)) for coup in self.jeu.coupsPossibles(C)]
        val_grundy = self.premiere_petite_valeur(valeurs_fils)
        self.valeurs_grundy[tuple(C)] = val_grundy  # Stockage dans la table
        return val_grundy

    def premiere_petite_valeur(self, valeurs):
        """
        Prend la premiere plus petite valeur possible qui n'est pas déjà dans la liste valeurs
        """
        valeurs.sort()
        res = 0
        for val in valeurs:
            if val == res:
                res += 1
            else:
                break
        return res

    def choisirProchainCoup(self, C):
        coups = self.jeu.coupsPossibles(C)
        for coup in coups:
            if self.valeurGrundy(self.simuleCoup(C, coup)) == 1:
                return coup
        import random
        return random.choice(coups)  # Si aucun coup avec valeur de Grundy 1, choisir au hasard

    def simuleCoup(self, C, coup):
        """Simule un coup sans modifier le plateau actuel."""
        nouveau_C = C[:]
        nouveau_C[coup[0]] -= coup[1]
        return nouveau_C


"""
=================================================================================================================================================================================
=================================================================================================================================================================================
==============================================================                 ==================================================================================================
============================================================== FIN DES CLASSES ==================================================================================================
==============================================================                 ==================================================================================================
=================================================================================================================================================================================
=================================================================================================================================================================================
"""

def morpionManuel():
    jeu = Morpion()

    while not jeu.estFini(jeu.plateau):
        # Afficher le plateau
        jeu.afficher_plateau(jeu.plateau)
        
        # Obtenir les coups possibles
        coups = jeu.coupsPossibles(jeu.plateau)
        
        # Demander au joueur courant de choisir un coup
        print(f"C'est au tour du joueur {jeu.joueurCourant(jeu.plateau)}")
        coup = None
        while coup not in coups:
            try:
                coup = int(input("Entrez le coup souhaité: "))
                if coup not in coups:
                    print("Coup invalide, veuillez réessayer.")
            except ValueError:
                print("Entrée invalide, veuillez entrer des nombres.")
        
        # Jouer le coup
        jeu.joueLeCoup(coup)
    
    # La partie est finie, afficher le résultat
    jeu.afficher_plateau(jeu.plateau)
    print("La partie est finie!")

    end=jeu.estFini(jeu.plateau)
    if type(end)==str:
        print("Le joueur ",end," a gagné !")
    else:
        print("EGALITE")


def morpionAleatoire(affichage=True):
    jeu = Morpion()
    strategie_joueur_X = StrategieAleatoire(jeu)
    strategie_joueur_O = StrategieAleatoire(jeu)

    while not jeu.estFini(jeu.plateau):
        # Afficher le plateau
        if affichage : jeu.afficher_plateau(jeu.plateau)
        
        # Obtenir les coups possibles
        coups = jeu.coupsPossibles(jeu.plateau)
        
        # Choisir un coup aléatoire pour le joueur courant
        if jeu.joueurCourant(jeu.plateau) == 'X':
            if affichage : print("Au tour du joueur X de jouer !")
            coup = strategie_joueur_X.choisirProchainCoup(jeu.plateau)
        else:
            if affichage : print("Au tour du joueur O de jouer !")
            coup = strategie_joueur_O.choisirProchainCoup(jeu.plateau)
        
        # Jouer le coup
        jeu.joueLeCoup(coup)
    
    # La partie est finie, afficher le résultat
    jeu.afficher_plateau(jeu.plateau)
    print("La partie est finie!")

    end=jeu.estFini(jeu.plateau)
    if type(end)==str:
        print("Le joueur ",end," a gagné !")
    else:
        print("EGALITE")


def morpionMinMaxVSAlea(affichage = True,horizon=1):
    jeu = Morpion()
    strategie_joueur_X = StrategieMinMax(jeu,horizon)
    strategie_joueur_O = StrategieAleatoire(jeu)

    while not jeu.estFini(jeu.plateau):
        # Afficher le plateau
        if affichage : jeu.afficher_plateau(jeu.plateau)
        
        # Obtenir les coups possibles
        coups = jeu.coupsPossibles(jeu.plateau)
        
        # Choisir un coup aléatoire pour le joueur courant
        if jeu.joueurCourant(jeu.plateau) == 'X':
            if affichage : print("Au tour du joueur X de jouer !")
            coup = strategie_joueur_X.choisirProchainCoup(jeu.plateau)
        else:
            if affichage : print("Au tour du joueur O de jouer !")
            coup = strategie_joueur_O.choisirProchainCoup(jeu.plateau)
        
        # Jouer le coup
        jeu.joueLeCoup(coup)
    
    # La partie est finie, afficher le résultat
    if affichage : jeu.afficher_plateau(jeu.plateau)
    if affichage : print("La partie est finie!")

    end=jeu.estFini(jeu.plateau)
    if type(end)==str:
        if affichage : print("Le joueur ",end," a gagné !")
        return end
    else:
        if affichage : print("EGALITE")
        return 'EGALITE'


def morpionMinMaxNVSMinMax1(affichage = True,horizon=1):
    jeu = Morpion()
    strategie_joueur_X = StrategieMinMax(jeu,horizon)
    #strategie_joueur_X = StrategieAleatoire(jeu)
    strategie_joueur_O = StrategieMinMax(jeu,1)

    while not jeu.estFini(jeu.plateau):
        # Afficher le plateau
        if affichage : jeu.afficher_plateau(jeu.plateau)
        
        # Obtenir les coups possibles
        coups = jeu.coupsPossibles(jeu.plateau)
        
        # Choisir un coup aléatoire pour le joueur courant
        if jeu.joueurCourant(jeu.plateau) == 'X':
            if affichage : print("Au tour du joueur X de jouer !")
            coup = strategie_joueur_X.choisirProchainCoup(jeu.plateau)
        else:
            if affichage : print("Au tour du joueur O de jouer !")
            coup = strategie_joueur_O.choisirProchainCoup(jeu.plateau)
        
        # Jouer le coup
        jeu.joueLeCoup(coup)
    
    # La partie est finie, afficher le résultat
    if affichage : jeu.afficher_plateau(jeu.plateau)
    if affichage : print("La partie est finie!")

    end=jeu.estFini(jeu.plateau)
    if type(end)==str:
        if affichage : print("Le joueur ",end," a gagné !")
        return end
    else:
        if affichage : print("EGALITE")
        return 'EGALITE'


def allumettesAleatoire(affichage = True,g=3,m=5):
    jeu = Allumettes(g,m)
    strategie_joueur_X = StrategieAleatoire(jeu)
    strategie_joueur_O = StrategieAleatoire(jeu)

    while not jeu.estFini(jeu.plateau):
        # Afficher le plateau
        if affichage : jeu.afficher_plateau()
        
        # Obtenir les coups possibles
        coups = jeu.coupsPossibles(jeu.plateau)
        
        # Choisir un coup aléatoire pour le joueur courant
        if jeu.joueurCourant(jeu.plateau) == 'X':
            if affichage : print("Au tour du joueur X de jouer !")
            coup = strategie_joueur_X.choisirProchainCoup(jeu.plateau)
        else:
            if affichage : print("Au tour du joueur O de jouer !")
            coup = strategie_joueur_O.choisirProchainCoup(jeu.plateau)
        
        # Jouer le coup
        jeu.joueLeCoup(coup)
    
    # La partie est finie, afficher le résultat
    if affichage : jeu.afficher_plateau()
    if affichage : print("La partie est finie!")

    end=jeu.estFini(jeu.plateau)
    if type(end)==str:
        if affichage : print("Le joueur ",end," a gagné !")
        return end
    else:
        if affichage : print("EGALITE")
        return 'EGALITE'


def allumettesGrundyVSAleatoire(affichage = True,g=3,m=5):
    jeu = Allumettes(g,m)
    strategie_joueur_X = StrategieAllumettes(jeu)
    strategie_joueur_O = StrategieAleatoire(jeu)
    if affichage : jeu.afficher_plateau()

    while not jeu.estFini(jeu.plateau):
        # Afficher le plateau
        
        # Obtenir les coups possibles
        coups = jeu.coupsPossibles(jeu.plateau)
        
        # Choisir un coup aléatoire pour le joueur courant
        if jeu.joueurCourant(jeu.plateau) == 'X':
            if affichage : print("Au tour du joueur X de jouer avec le plateau ci-dessous!")
            if affichage : jeu.afficher_plateau()

            coup = strategie_joueur_X.choisirProchainCoup(jeu.plateau)
        else:
            if affichage : print("Au tour du joueur O de jouer avec le plateau ci-dessous!")
            if affichage : jeu.afficher_plateau()

            coup = strategie_joueur_O.choisirProchainCoup(jeu.plateau)
        
        # Jouer le coup
        jeu.joueLeCoup(coup)
    
    # La partie est finie, afficher le résultat
    if affichage : jeu.afficher_plateau()
    if affichage : print("La partie est finie!")

    end=jeu.estFini(jeu.plateau)
    if type(end)==str:
        if affichage : print("Le joueur ",end," a gagné !")
        return end
    else:
        if affichage : print("EGALITE")
        return 'EGALITE'


def allumettesGrundyVSMinMax(affichage = True,g=3,m=5,horizon=1):
    jeu = Allumettes(g,m)
    strategie_joueur_X = StrategieAllumettes(jeu)
    strategie_joueur_O = StrategieMinMax(jeu, horizon)
    if affichage : jeu.afficher_plateau()

    while not jeu.estFini(jeu.plateau):
        # Afficher le plateau
        
        # Obtenir les coups possibles
        coups = jeu.coupsPossibles(jeu.plateau)
        
        # Choisir un coup aléatoire pour le joueur courant
        if jeu.joueurCourant(jeu.plateau) == 'X':
            if affichage : print("Au tour du joueur X de jouer avec le plateau ci-dessous!")
            if affichage : jeu.afficher_plateau()

            coup = strategie_joueur_X.choisirProchainCoup(jeu.plateau)
        else:
            if affichage : print("Au tour du joueur O de jouer avec le plateau ci-dessous!")
            if affichage : jeu.afficher_plateau()

            coup = strategie_joueur_O.choisirProchainCoup(jeu.plateau)
        
        # Jouer le coup
        jeu.joueLeCoup(coup)
    
    # La partie est finie, afficher le résultat
    if affichage : jeu.afficher_plateau()
    if affichage : print("La partie est finie!")

    end=jeu.estFini(jeu.plateau)
    if type(end)==str:
        if affichage : print("Le joueur ",end," a gagné !")
        return end
    else:
        if affichage : print("EGALITE")
        return 'EGALITE'


def allumettesMinMaxVSAleatoire(affichage = True,g=5,m=5,horizon=1):
    jeu = Allumettes(g,m)
    strategie_joueur_X = StrategieMinMax(jeu, horizon)
    strategie_joueur_O = StrategieAleatoire(jeu)
    if affichage : jeu.afficher_plateau()

    while not jeu.estFini(jeu.plateau):
        # Afficher le plateau
        
        # Obtenir les coups possibles
        coups = jeu.coupsPossibles(jeu.plateau)
        
        # Choisir un coup aléatoire pour le joueur courant
        if jeu.joueurCourant(jeu.plateau) == 'X':
            if affichage : print("Au tour du joueur X de jouer avec le plateau ci-dessous!")
            if affichage : jeu.afficher_plateau()

            coup = strategie_joueur_X.choisirProchainCoup(jeu.plateau)
        else:
            if affichage : print("Au tour du joueur O de jouer avec le plateau ci-dessous!")
            if affichage : jeu.afficher_plateau()

            coup = strategie_joueur_O.choisirProchainCoup(jeu.plateau)
        
        # Jouer le coup
        jeu.joueLeCoup(coup)
    
    # La partie est finie, afficher le résultat
    if affichage : jeu.afficher_plateau()
    if affichage : print("La partie est finie!")

    end=jeu.estFini(jeu.plateau)
    if type(end)==str:
        if affichage : print("Le joueur ",end," a gagné !")
        return end
    else:
        if affichage : print("EGALITE")
        return 'EGALITE'



#allumettesGrundy()