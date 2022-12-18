


# Structure d'un exo python 

exo.title = "un titre" 
exo.text = f" Définir une {{typecible}} {{nomvariable}} qui vérifie {{statement_text}}"




exo.groupetest = f"""
>>> {{setup}}
for assertion, mode in basictests:
>>> {{assertion}}{{mode}}
True
for code,want, mode in wanttests:
>>> {{code}}{{mode}}
want
"""


exo.modetype= standard|hidden|title|caviard
exo.mode="""(vide)|#|# {test_title}|#{caviard}#"""


# Comment utiliser pltest pour coder plsoluce

import soluce
want = soluce.funcundertest(params)
print(f"""pltest{i}==
>>> import student
>>> student.funcundertest({{param}})
{want}
""")





# Générateur de question de python:

1) Vous ne souhaitez pas écrire de code solution.
2) Vous avez un code "solution.py" qui répond à l'exercice.


## Sans code solution


### Sans aléatoire 

### Avec aléatoire 

=> implique que l'énoncé utilise une variable 


