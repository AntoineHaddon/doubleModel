# Double Modélisation 
Méthode pour résoudre un problème de controle optimal d'irrigation et de fertilisation pour le modèle complexe STICS en utilisant un modèle réduit SWAN (Soil WAter Nitrogen)
voir article

# Dépendance
STICS : [https://www6.paca.inrae.fr/stics/](https://www6.paca.inrae.fr/stics/)

Bocop(HJB) :  [https://www.bocop.org/](https://www.bocop.org/)

Python libarires : numpy, pandas, matplotlib, ...


# Running STICS
To run STICS the path to the directory containing JavaSTICS must be given. 2 options :

-1- Change the default in the sticsIOutils library :
In file ```stics/pyScripts/sticsIOutils.py``` change the value of the variable ```JavaSticsDir``` to the path
```
JavaSticsDir = '/path/to/JavaSTICS/'
```

-2- Update variable ```JavaSticsDir``` after loading sticsIOutils library:
In a script to run STICS, first load the sticsIOutils library, then the variable ```JavaSticsDir``` can be updated
```
import sticsIOutils as stiIO
stiIO.JavaSticsDir = '/path/to/JavaSTICS/'
```
