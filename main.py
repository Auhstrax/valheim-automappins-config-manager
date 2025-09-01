import sys
from PyQt5.QtWidgets import QApplication
from gui import AutoMapPinsGUI

def main():
    """Point d'entrée principal de l'application"""
    app = QApplication(sys.argv)
    
    # Configuration de l'application
    app.setApplicationName("AutoMapPins Configuration Manager")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("Valheim Tools")
    
    # Créer et afficher la fenêtre principale
    window = AutoMapPinsGUI()
    window.show()
    
    # Lancer l'application
    return app.exec_()

if __name__ == "__main__":
    sys.exit(main())
