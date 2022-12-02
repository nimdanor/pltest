


# Module 1 
# je veux vérifier l'existance d'une variable après l'exécution
# parametre : Varname = l'identifiant de la variable
#           :   mode  = 0=constant, 1= variablename, 2= lambda
#           :  value  = valeur attendu   
#           : silent  = False (si le text du test est visible )  
# En fonction du mode la valeur
# Il faut vérifier que les variables on été crée la lamda doit être appelée avec une variable
# Exemple :
# varname=toto, mode = 0, value = 12, silent = False
# produit le doctest
pltest==
>>> toto == 12 # 
True 
== 
# varname=toto, mode = 2, value = lambda x: x==12, silent = False, testname= truc, 
pltest==
>>> _f=lambda x: x==12 # 
>>> _f(toto) # truc
True
==
