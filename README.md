# Projet 2
###### par **Durand Manis**


### 1. Créer un environnement virtuel

D’abord on installe “pip” :

`sudo apt-get install python3-pip`

Ensuite on installe “virtualenv” avec pip :

`sudo pip3 install virtualenv` 

Maintenant on peut créer un environnement virtuel :

`virtualenv myvenv`

en utilisant n’importe quel nom à la place de “venv”. Par exemple, le nom de votre projet.


### 2. Activer l'environnement virtuel

`source myvenv/bin/activate`

### 3. Installer les libraries requises
#### 3.1 Utiliser Pip
Certaines library sont disponibles lors de l'installation de Python3.
Pour installer les autres librairies, vous devrez utiliser pip.

Vérifiez si Pip est installé sur votre machine
`pip3 -- version`

le résultat doit être un numéro de version suivi du path vers le dossier du paquet, ex:

`pip 21.1.3 from ...`

Si ce n'est pas le cas, installez d'abord Pip

`sudo apt update`

`sudo apt install python3-pip`

#### 3.2 Installez les paquets distants

Installez requests:

`pip3 install requests`

Installez BeautifulSoup 4

`pip3 install bs4`

### 4. Executez le programme depuis votre terminal

Afin d'executer le programme P2_00_source_code.py ouvrez votre terminal à l'adresse du fichier.

Tapez la commande suivante:

`python3 P2_00_source_code.py`
