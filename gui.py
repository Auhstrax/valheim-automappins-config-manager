import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                            QWidget, QCheckBox, QPushButton, QLabel, QScrollArea, 
                            QGroupBox, QMessageBox, QStatusBar, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QColor
from config_manager import ConfigManager

class AutoMapPinsGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config_manager = ConfigManager()
        self.category_checkboxes = {}
        self.init_ui()
        self.load_config()
    
    def init_ui(self):
        """Initialise l'interface utilisateur"""
        self.setWindowTitle("AutoMapPins - Configuration Manager")
        self.setGeometry(100, 100, 700, 800)
        self.setMinimumSize(700, 800)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Titre
        title = QLabel("🗺️ AutoMapPins Configuration")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setStyleSheet("color: #2c3e50; padding: 10px;")
        main_layout.addWidget(title)
        
        # Zone de statut du fichier
        self.file_status = QLabel("Fichier: Non chargé")
        self.file_status.setStyleSheet("padding: 5px; background-color: #ecf0f1; border: 1px solid #bdc3c7; border-radius: 3px;")
        main_layout.addWidget(self.file_status)
        
        # Boutons de contrôle principaux
        control_layout = QHBoxLayout()
        
        self.load_btn = QPushButton("📁 Charger Config")
        self.load_btn.clicked.connect(self.load_config)
        self.load_btn.setStyleSheet("QPushButton { padding: 8px; font-weight: bold; }")
        
        self.save_btn = QPushButton("💾 Sauvegarder")
        self.save_btn.clicked.connect(self.save_config)
        self.save_btn.setEnabled(False)
        self.save_btn.setStyleSheet("QPushButton { padding: 8px; font-weight: bold; }")
        
        control_layout.addWidget(self.load_btn)
        control_layout.addWidget(self.save_btn)
        main_layout.addLayout(control_layout)
        
        # Séparateur
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(separator)
        
        # Zone des catégories avec scroll
        categories_group = QGroupBox("Catégories de marqueurs")
        categories_group.setFont(QFont("Arial", 12, QFont.Bold))
        categories_layout = QVBoxLayout(categories_group)
        
        # Boutons de sélection rapide
        selection_layout = QHBoxLayout()
        
        self.select_default_btn = QPushButton("✅ Sélection par défaut")
        self.select_default_btn.clicked.connect(self.select_default_categories)
        self.select_default_btn.setEnabled(False)
        
        self.select_all_btn = QPushButton("☑️ Tout sélectionner")
        self.select_all_btn.clicked.connect(self.select_all_categories)
        self.select_all_btn.setEnabled(False)
        
        self.select_none_btn = QPushButton("☐ Tout désélectionner")
        self.select_none_btn.clicked.connect(self.select_none_categories)
        self.select_none_btn.setEnabled(False)
        
        selection_layout.addWidget(self.select_default_btn)
        selection_layout.addWidget(self.select_all_btn)
        selection_layout.addWidget(self.select_none_btn)
        categories_layout.addLayout(selection_layout)
        
        # Zone scrollable pour les checkboxes
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(scroll_widget)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setMaximumHeight(350)
        categories_layout.addWidget(scroll_area)
        
        main_layout.addWidget(categories_group)
        
        # Boutons d'action avancés
        advanced_layout = QHBoxLayout()
        
        self.backup_btn = QPushButton("🔄 Créer Backup")
        self.backup_btn.clicked.connect(self.create_backup)
        self.backup_btn.setEnabled(False)
        
        self.reset_btn = QPushButton("⚠️ Réinitialiser")
        self.reset_btn.clicked.connect(self.reset_to_default)
        self.reset_btn.setEnabled(False)
        self.reset_btn.setStyleSheet("QPushButton { background-color: #e74c3c; color: white; }")
        
        advanced_layout.addWidget(self.backup_btn)
        advanced_layout.addWidget(self.reset_btn)
        advanced_layout.addStretch()
        main_layout.addLayout(advanced_layout)
        
        # Barre de statut
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Prêt")
        
        # Style général
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8f9fa;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                margin: 10px 0px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px 0 10px;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 3px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:disabled {
                background-color: #95a5a6;
            }
            QCheckBox {
                padding: 3px;
                font-size: 11px;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
            }
        """)
    
    def create_category_checkboxes(self):
        """Crée les checkboxes pour chaque catégorie"""
        # Vider le layout existant
        for i in reversed(range(self.scroll_layout.count())):
            self.scroll_layout.itemAt(i).widget().setParent(None)
        
        self.category_checkboxes.clear()
        
        # Définir les noms d'affichage plus jolis
        category_names = {
            "ores": "🪨 Minerais",
            "base_ores": "⚪ Minerais de base",
            "guck_ores": "🟢 Minerais Guck", 
            "giant_ores": "⛰️ Minerais géants",
            "other_ores": "🔸 Autres minerais",
            "flower": "🌸 Fleur",
            "tarpits": "🖤 Fosses de goudron",
            "seeds": "🌱 Graines",
            "portals": "🌀 Portails",
            "runestones": "🗿 Pierres runiques",
            "mushrooms": "🍄 Champignons",
            "berry": "🫐 Baie",
            "crypt": "⚰️ Cryptes",
            "special": "⭐ Spéciaux",
            "pickable": "📦 Objets ramassables",
            "morgenholes": "🕳️ Trous Morgen",
            "dungeon": "🏰 Donjons",
            "spawners": "👹 Spawners",
            "boss_spawners": "👑 Spawners de boss",
            "treasures": "💰 Trésors",
            "environment": "🌍 Environnement"
        }
        
        # Récupérer le statut des catégories
        categories_status = self.config_manager.get_categories_status()
        
        if isinstance(categories_status, str):  # Erreur
            self.show_message("Erreur", categories_status, QMessageBox.Warning)
            return
        
        # Créer les checkboxes
        for category, is_active in categories_status.items():
            display_name = category_names.get(category, category.replace("_", " ").title())
            checkbox = QCheckBox(display_name)
            checkbox.setChecked(is_active)
            checkbox.stateChanged.connect(self.on_category_changed)
            
            # Mettre en évidence les catégories par défaut
            if category in self.config_manager.default_active_categories:
                checkbox.setStyleSheet("QCheckBox { font-weight: bold; color: #27ae60; }")
            
            self.category_checkboxes[category] = checkbox
            self.scroll_layout.addWidget(checkbox)
    
    def load_config(self):
        """Charge la configuration"""
        self.status_bar.showMessage("Chargement de la configuration...")
        result = self.config_manager.load_yaml()
        
        if result.startswith("Erreur") or "invalide" in result:
            self.show_message("Erreur de chargement", result, QMessageBox.Warning)
            self.status_bar.showMessage("Erreur de chargement")
            return
        
        # Mise à jour de l'interface
        self.file_status.setText(f"Fichier: {self.config_manager.config_path.name}")
        self.file_status.setStyleSheet("padding: 5px; background-color: #d5f4e6; border: 1px solid #27ae60; border-radius: 3px; color: #27ae60;")
        
        self.create_category_checkboxes()
        
        # Activer les boutons
        self.save_btn.setEnabled(True)
        self.select_default_btn.setEnabled(True)
        self.select_all_btn.setEnabled(True)
        self.select_none_btn.setEnabled(True)
        self.backup_btn.setEnabled(True)
        self.reset_btn.setEnabled(True)
        
        self.status_bar.showMessage(result)
    
    def save_config(self):
        """Sauvegarde la configuration"""
        if not self.category_checkboxes:
            return
        
        self.status_bar.showMessage("Sauvegarde en cours...")
        
        # Mettre à jour les données avec les checkboxes
        for category, checkbox in self.category_checkboxes.items():
            result = self.config_manager.set_category_status(category, checkbox.isChecked())
        
        # Sauvegarder le fichier
        result = self.config_manager.save_yaml()
        
        if result.startswith("Erreur"):
            self.show_message("Erreur de sauvegarde", result, QMessageBox.Critical)
            self.status_bar.showMessage("Erreur de sauvegarde")
        else:
            self.status_bar.showMessage(result)
            self.show_message("Succès", "Configuration sauvegardée avec succès!", QMessageBox.Information)
    
    def on_category_changed(self):
        """Appelé quand une checkbox change d'état"""
        self.status_bar.showMessage("Configuration modifiée (non sauvegardée)")
    
    def select_default_categories(self):
        """Sélectionne les catégories par défaut"""
        for category, checkbox in self.category_checkboxes.items():
            checkbox.setChecked(category in self.config_manager.default_active_categories)
        self.status_bar.showMessage("Sélection par défaut appliquée")
    
    def select_all_categories(self):
        """Sélectionne toutes les catégories"""
        for checkbox in self.category_checkboxes.values():
            checkbox.setChecked(True)
        self.status_bar.showMessage("Toutes les catégories sélectionnées")
    
    def select_none_categories(self):
        """Désélectionne toutes les catégories"""
        for checkbox in self.category_checkboxes.values():
            checkbox.setChecked(False)
        self.status_bar.showMessage("Toutes les catégories désélectionnées")
    
    def create_backup(self):
        """Crée un backup"""
        from backup_manager import BackupManager
        backup_manager = BackupManager()
        result = backup_manager.create_backup(self.config_manager.config_path)
        
        if result.startswith("Erreur"):
            self.show_message("Erreur de backup", result, QMessageBox.Warning)
        else:
            self.show_message("Backup créé", result, QMessageBox.Information)
        
        self.status_bar.showMessage(result)
    
    def reset_to_default(self):
        """Remet la configuration aux valeurs par défaut"""
        reply = QMessageBox.question(
            self, 
            "Confirmation", 
            "Êtes-vous sûr de vouloir réinitialiser la configuration aux valeurs par défaut?\n\nCette action créera automatiquement un backup.",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            result = self.config_manager._restore_default_config()
            
            if result.startswith("Erreur"):
                self.show_message("Erreur", result, QMessageBox.Critical)
            else:
                self.show_message("Réinitialisation", result, QMessageBox.Information)
                self.load_config()  # Recharger l'interface
            
            self.status_bar.showMessage(result)
    
    def show_message(self, title, message, icon=QMessageBox.Information):
        """Affiche une boîte de message"""
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(icon)
        msg_box.exec_()
