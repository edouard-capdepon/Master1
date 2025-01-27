# Cybersecurity Toolbox

## Description
Cybersecurity Toolbox est une application graphique pour effectuer diverses analyses de sécurité réseau en utilisant des outils tels que Nmap, SQLMap et Wireshark. Cette application permet de scanner des adresses IP, de tester des vulnérabilités SQL et de capturer des paquets réseau. Les résultats peuvent être enregistrés sous forme de fichiers PDF pour une analyse ultérieure.

## Fonctionnalités
- **Nmap Scan** : Effectue des analyses de port, de services, de détection d'OS et plus encore.
- **SQLMap Scan** : Teste les vulnérabilités SQL sur des URL spécifiées.
- **Wireshark Capture** : Capture les paquets réseau sur une interface spécifiée.
- **Téléchargement de PDF** : Les résultats des analyses peuvent être téléchargés en fichiers PDF.
- **Arrêt des Scans** : Possibilité d'arrêter les scans en cours.

## Installation

### Prérequis
- Python 3.6+
- pip (Python package installer)

### Dépendances
Les dépendances Python nécessaires peuvent être installées à l'aide de pip. Voici la liste des bibliothèques nécessaires :

```bash
pip install customtkinter scapy psutil reportlab

```
Outils Externes
Assurez-vous que les outils externes Nmap et SQLMap sont installés et disponibles dans le chemin du système.

Nmap : Télécharger Nmap
SQLMap : Télécharger SQLMap
Installation des outils sur un système Linux
```bash
sudo apt-get install nmap
sudo apt-get install tshark
```


Lancer l'Application
Pour lancer l'application, exécutez le script MainApp.py :


Interface de Connexion
L'application démarre par une interface de connexion. Vous pouvez soit vous connecter avec un compte existant, soit en créer un nouveau.

Fonctionnalités des Outils
Nmap
Ouvrez l'onglet Nmap.
Entrez l'adresse IP à scanner.
Sélectionnez les options de scan souhaitées.
Cliquez sur Run Nmap pour démarrer le scan.
Cliquez sur Arrêter pour arrêter le scan en cours.
Une fois le scan terminé, cliquez sur Télécharger PDF pour enregistrer les résultats.

SQLMap
Ouvrez l'onglet SQLMap.
Entrez l'URL à tester.
Sélectionnez les options de test souhaitées.
Cliquez sur Run SQLMap pour démarrer le test.
Cliquez sur Arrêter pour arrêter le test en cours.
Une fois le test terminé, cliquez sur Télécharger PDF pour enregistrer les résultats.

Wireshark
Ouvrez l'onglet Wireshark.
Sélectionnez l'interface réseau à capturer.
Entrez le nombre de paquets à capturer.
Cliquez sur Start Capture pour démarrer la capture.
Cliquez sur Arrêter pour arrêter la capture en cours.
Une fois la capture terminée, cliquez sur Télécharger PDF pour enregistrer les résultats.

Gestionnaire de Résultats
Ouvrez l'onglet Gestionnaire de Résultats.
Sélectionnez l'outil dont vous voulez voir les résultats.
Cliquez sur un fichier PDF pour l'ouvrir.
Cliquez sur Actualiser pour mettre à jour la liste des fichiers PDF disponibles.
Contributions
Les contributions sont les bienvenues ! Veuillez soumettre des pull requests et signaler des problèmes sur la page GitHub du projet.
## Authors

- [@EdouardCapdepon](https://github.com/edouard-capdepon/Master1)

