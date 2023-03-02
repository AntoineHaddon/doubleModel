# Double Modelling Method 
Method to solve an optimal control probleme, applied here to crop irrigation and fertilisation, with complex model STICS and simple model SWAN (Soil WAter Nitrogen).

See article

# Dependencies
STICS : [https://www6.paca.inrae.fr/stics/](https://www6.paca.inrae.fr/stics/)

Bocop(HJB) :  [https://www.bocop.org/](https://www.bocop.org/)

Python libarires : numpy, pandas, matplotlib.


# Running STICS
The main library to run simulations of STICS is the file ```stics/pyScripts/sticsIOutils.py```. 
For this to work you need the following :

1. Download and install STICS from the STICS website [https://www6.paca.inrae.fr/stics/](https://www6.paca.inrae.fr/stics/). You should end up with a directory containing JavaSTICS executable (by default named ```JavaSTICS-x.x-stics-x.x```).  

2. The variable ```JavaSticsDir``` should have the path to the directory containing JavaSTICS. 2 options :

   - Change the default in the sticsIOutils library. In file ```stics/pyScripts/sticsIOutils.py``` change the value of the variable ```JavaSticsDir``` to the path :
   ```
   JavaSticsDir = '/path/to/JavaSTICS/'
   ```

   - Update variable ```JavaSticsDir``` after loading sticsIOutils library. In a script to run STICS, first load the sticsIOutils library, then the variable ```JavaSticsDir``` can be updated :  
   ```
   import sticsIOutils as stiIO
   stiIO.JavaSticsDir = '/path/to/JavaSTICS/'
   ```

3. The variable ```dirStics``` should have the path to the directory with all files needed to run STICS simulation (parameter files, initial condition, weather , etc... ).