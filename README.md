# 🎮 AutoMapPins Config Manager

Un gestionnaire graphique simple et intuitif pour configurer les catégories du mod **AutoMapPins** de Valheim.

![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![PyQt5](https://img.shields.io/badge/GUI-PyQt5-green)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🚀 Fonctionnalités

- ✅ **Interface graphique intuitive** avec PyQt5
- ✅ **Gestion des catégories** - Activer/désactiver facilement
- ✅ **Sauvegarde automatique** avant chaque modification
- ✅ **Support YAML** pour les fichiers de configuration
- ✅ **Validation des données** avant sauvegarde
- ✅ **Historique des backups** avec timestamp
- ✅ **Exécutable Windows** - Aucune installation Python requise

## 🛠️ Installation

### Option 1: Exécutable Windows (Recommandé)
1. **Téléchargez** `AutoMapPins-ConfigManager.exe` depuis les [Releases](../../releases)
2. **Double-cliquez** sur le fichier
3. **C'est tout !** Aucune installation requise

### Option 2: Code source Python
```bash
# Clonez le repository
git clone https://github.com/votre-username/AutoMapPins-ConfigManager.git
cd AutoMapPins-ConfigManager

# Installez les dépendances
pip install -r requirements.txt

# Lancez l'application
python main.py
📋 Prérequis
```
Pour l'exécutable:

Windows 10/11
Rien d'autre ! 🎉

Pour le code source:

Python 3.7+
PyQt5
PyYAML

🎯 Utilisation

Lancez l'application
Sélectionnez votre fichier de configuration AutoMapPins
Généralement dans: C:\Users\[Nom]\AppData\LocalLow\IronGate\Valheim\BepInEx\config\


Cochez/décochez les catégories que vous voulez activer
Cliquez sur "Sauvegarder"
Relancez Valheim pour voir les changements

📁 Structure du projet
AutoMapPins-ConfigManager/
├── 📄 main.py                    # Point d'entrée
├── 🎨 gui.py                     # Interface utilisateur
├── ⚙️ config_manager.py          # Gestion des configs YAML
├── 💾 backup_manager.py          # Système de sauvegarde
├── 📋 default_config.yaml        # Configuration par défaut
├── 📦 requirements.txt           # Dépendances Python
├── 🏗️ build_exe.py              # Script de compilation
└── 📁 backup/                    # Sauvegardes automatiques
🔧 Compilation en exécutable
# Installez PyInstaller
pip install pyinstaller

# Compilez l'application
python build_exe.py
L'exécutable sera créé dans le dossier release/.
🛡️ Sauvegardes
L'application crée automatiquement des sauvegardes avant chaque modification:

Format: fichier_backup_YYYYMMDD_HHMMSS.yaml
Dossier: backup/
Conservation: Illimitée

🐛 Signaler un bug
Utilisez les Issues GitHub pour signaler des bugs ou proposer des fonctionnalités.
Template de bug:
**Environnement:**
- OS: Windows 10/11
- Version: v1.0.0

**Description:**
Description claire du problème...

**Étapes pour reproduire:**
1. Ouvrir l'application
2. Cliquer sur...
3. Voir l'erreur

**Comportement attendu:**
Ce qui devrait se passer...
📚 Documentation technique
Architecture

GUI: PyQt5 pour l'interface utilisateur
Config: PyYAML pour la manipulation des fichiers YAML
Backup: Système de sauvegarde avec horodatage
Validation: Vérification de l'intégrité des données

Fichiers supportés

FixItFelix.AutoMapPins.categories.vanilla.yaml
Tout fichier YAML avec la structure AutoMapPins

📄 License
Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.
🙏 Remerciements

FixItFelix pour le mod AutoMapPins original
Iron Gate Studio pour Valheim
Communauté Valheim pour le support des mods

📊 Stats






  Fait avec ❤️ pour la communauté Valheim



  ⭐ N'oubliez pas de donner une étoile si ce projet vous aide !
