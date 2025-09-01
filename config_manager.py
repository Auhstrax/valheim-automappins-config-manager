import sys
import os
from pathlib import Path
from tkinter import filedialog
import tkinter as tk
import yaml
import shutil
from datetime import datetime
from backup_manager import BackupManager

class ConfigManager():
    def __init__(self):
        self.DEV_MODE = False  # Mettre à True pour tester en dev local
        self.config_path = None
        self.filename = "FixItFelix.AutoMapPins.categories.vanilla.yaml"
        self.yaml_data = None
        self.default_active_categories = [
            "ores",
            "base_ores",
            "tarpits",
            "boss_spawners",
            "spawners",
            "dungeon"
        ]
        # Mapping des catégories d'origine vers les objets individuels
        self.ores_mapping = {
            "guck_ores": ["GuckSack", "GuckSack_small"],
            "giant_ores": ["giant_brain", "giant_helmet1", "giant_helmet2", "giant_ribs", "giant_skull", "giant_sword1", "giant_sword2"],
            "other_ores": ["LeviathanLava", "Mistlands_Swords1"],
            "base_ores": ["rock4_copper", "MineRock_Tin", "MineRock_Obsidian", "silvervein"]
        }

    def _get_default_config_path(self):
        # Récupérer %APPDATA%
        appdata_path = os.path.expandvars("%APPDATA%")

        # Construire le chemin complet avec Path
        config_path = Path(appdata_path) / "r2modmanPlus-local" / "Valheim" / "profiles" / "Boux s Valheim" / "BepInEx" / "config" / self.filename

        return config_path

    def _find_config_file(self):
        if self.DEV_MODE:
            local_path = Path(self.filename)
            if local_path.exists():
                self.config_path = local_path
            else:
                raise FileNotFoundError(f"ERREUR DEV: {self.filename} introuvable !")

        else:
            default_path = self._get_default_config_path()
            if default_path.exists():
                self.config_path = default_path
            else:
                self._ask_user_for_file()

    def _ask_user_for_file(self):
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(
            title="Sélectionner le fichier de configuration",
            filetypes=[("YAML files", "*.yaml"), ("All files", "*.*")]
        )
        if file_path:
            self.config_path = Path(file_path)
        else:
            sys.exit(1)

    def load_yaml(self):
        """ 
        Charger le fichier YAML en mémoire avec validation
        Returns: str - Message de résultat pour l'interface
        """
        if not self.config_path:
            try:
                self._find_config_file()
            except FileNotFoundError as e:
                return f"Erreur: {e}"
            except SystemExit:
                return "Erreur lors du chargement du fichier"

        try:
            with open(self.config_path, 'r', encoding='utf-8') as file:
                self.yaml_data = yaml.safe_load(file)

                if not self.yaml_data:
                    return "Erreur, fichier de configuration vide"

            # Fusionner automatiquement les catégories de minerais si elles existent séparément
            if any(cat in self.yaml_data for cat in ["giant_ores", "guck_ores", "other_ores"]):
                merge_result = self._merge_ores_categories()
                if merge_result.startswith("Erreur"):
                    return merge_result

            # Valider la configuration
            is_valid, validation_message = self._validate_config()
        
            if not is_valid:
                # Configuration invalide, proposer la restauration
                restore_result = self._restore_default_config()
                return f"Configuration invalide détectée ({validation_message}). {restore_result}"
        
            return f"Configuration chargée avec succès depuis : {self.config_path.name}"
        
        except FileNotFoundError:
            return f"Erreur: Fichier de configuration introuvable"
        except PermissionError:
            return f"Erreur: Permission refusée pour lire le fichier"
        except yaml.YAMLError as e:
            return f"Erreur: Problème lors de l'analyse du fichier YAML - {str(e)}"
        except UnicodeDecodeError:
            return f"Erreur: Problème d'encodage du fichier, vérifier qu'il est en UTF-8"
        except Exception as e:
            return f"Erreur inattendue: {str(e)}"

    def save_yaml(self):
        """
        Sauvegarde les donneés YAML dans le fichier
        Returns: str - Message de résultat pour l'interface
        """

        if not self.yaml_data:
            return "Erreur: Aucune donnée à sauvegarder"
        
        if not self.config_path:
            return "Erreur: Aucun chemin défini"
        
        # Créer le backup avant sauvegarde
        try:
            backup_manager = BackupManager()
            backup_result = backup_manager._create_backup(self.config_path)
            if not backup_result.startswith("Backup"):
                return f"Erreur lors de la création de la sauvegarde: {backup_result}"
        except Exception as e:
            return f"Erreur inattendue lors de la création de la sauvegarde: {e}"
        
        # Sauvegarder le fichier
        try:
            with open(self.config_path, 'w', encoding='utf-8') as file:
                yaml.dump(
                    self.yaml_data,
                    file,
                    default_flow_style=False,
                    allow_unicode=True,
                    sort_keys=False
                )
                return f"Configuration sauvegardée avec succès dans : {self.config_path.name}"
        except PermissionError:
            return f"Erreur: Permission refusée pour écrire - {self.config_path}"
        except OSError as e:
            return f"Erreur système : {e}"
        except yaml.YAMLError as e:
            return f"Erreur lors de la sauvegarde du YAML : {e}"
        except Exception as e:
            return f"Erreur inattendue lors de la sauvegarde : {e}"

    def get_categories_status(self):
        """
        Récupère le statut (isActive) de toutes les catégories
        Returns: dict ou str - Dictionnaire {categorie: bool} ou message d'erreur
        """
        if not self.yaml_data:
            return "Erreur : Aucune donnée chargée (utilisez load_yaml() d'abord)"
    
        try:
            categories_status = {}
        
            # Liste de toutes les catégories attendues (y compris les sous-catégories virtuelles)
            expected_categories = [
                "ores", "base_ores", "guck_ores", "giant_ores", "other_ores", "flower", "tarpits", 
                "seeds", "portals", "runestones", "mushrooms", "berry", "crypt", 
                "special", "pickable", "morgenholes", "dungeon", "spawners", 
                "boss_spawners", "treasures", "environment"
            ]
        
            # Parcourir les catégories dans le YAML
            for category in expected_categories:
                if category in self.yaml_data:
                    # Récupérer le statut isActive, par défaut False si absent
                    is_active = self.yaml_data[category].get('isActive', False)
                    categories_status[category] = is_active
                elif category in self.ores_mapping:
                    # Pour les sous-catégories virtuelles, vérifier si tous leurs objets sont actifs
                    categories_status[category] = self._get_virtual_category_status(category)
                else:
                    # Catégorie manquante dans le fichier
                    categories_status[category] = False
        
            return categories_status
        
        except Exception as e:
            return f"Erreur lors de la lecture des catégories : {str(e)}"

    def _get_virtual_category_status(self, virtual_category):
        """
        Obtient le statut d'une catégorie virtuelle en vérifiant ses objets individuels
        Args: virtual_category (str) - Nom de la catégorie virtuelle
        Returns: bool - True si tous les objets de la catégorie sont actifs
        """
        if virtual_category not in self.ores_mapping:
            return False
        
        if "ores" not in self.yaml_data:
            return False
        
        ores_objects = self.yaml_data["ores"].get("individualConfiguredObjects", {})
        objects_for_category = self.ores_mapping[virtual_category]
        
        # Vérifier si tous les objets de cette catégorie virtuelle sont actifs
        for obj_name in objects_for_category:
            if obj_name not in ores_objects:
                return False
            if not ores_objects[obj_name].get("isActive", False):
                return False
        
        return True

    def update_categories(self, categories_dict):
        """
        Met à jour le statut isActive des catégories
        Args: categories_dict (dict) - {categorie: bool}
        Returns: str - Message de résultat
        """
        if not self.yaml_data:
            return "Erreur : Aucune donnée chargée (utilisez load_yaml() d'abord)"
    
        if not isinstance(categories_dict, dict):
            return "Erreur : Le paramètre doit être un dictionnaire"
    
        try:
            updated_count = 0
        
            for category, is_active in categories_dict.items():
                if category in self.yaml_data:
                    # Mettre à jour le statut pour les catégories réelles
                    self.yaml_data[category]['isActive'] = bool(is_active)
                    updated_count += 1
                elif category in self.ores_mapping:
                    # Mettre à jour les objets individuels pour les catégories virtuelles
                    success = self._update_virtual_category(category, bool(is_active))
                    if success:
                        updated_count += 1
                else:
                    # Optionnel : créer la catégorie si elle n'existe pas
                    # (à voir selon tes besoins)
                    pass
        
            return f"{updated_count} catégories mises à jour avec succès"
        
        except Exception as e:
            return f"Erreur lors de la mise à jour : {str(e)}"

    def _update_virtual_category(self, virtual_category, is_active):
        """
        Met à jour le statut des objets individuels d'une catégorie virtuelle
        Args: 
            virtual_category (str) - Nom de la catégorie virtuelle
            is_active (bool) - Nouveau statut
        Returns: bool - True si succès
        """
        if virtual_category not in self.ores_mapping:
            return False
        
        if "ores" not in self.yaml_data:
            return False
        
        ores_objects = self.yaml_data["ores"].get("individualConfiguredObjects", {})
        objects_for_category = self.ores_mapping[virtual_category]
        
        # Mettre à jour le statut de tous les objets de cette catégorie virtuelle
        for obj_name in objects_for_category:
            if obj_name in ores_objects:
                ores_objects[obj_name]["isActive"] = is_active
        
        return True

    def set_category_status(self, category, is_active):
        """
        Met à jour le statut actif/inactif d'une catégorie
        Args:
            category (str): Nom de la catégorie
            is_active (bool): Nouveau statut
        Returns:
            tuple: (success, message)
        """
        if not self.yaml_data:
            return False, "Aucune configuration chargée"
    
        try:
            if category in self.yaml_data:
                # Catégorie réelle
                self.yaml_data[category]['isActive'] = is_active
                
                # Si c'est la catégorie "ores", mettre à jour aussi tous les objets individuels
                if category == "ores" and "ores" in self.yaml_data:
                    ores_objects = self.yaml_data["ores"].get("individualConfiguredObjects", {})
                    for obj_name in ores_objects:
                        ores_objects[obj_name]["isActive"] = is_active
                
                return True, f"Statut de '{category}' mis à jour"
            elif category in self.ores_mapping:
                # Catégorie virtuelle
                success = self._update_virtual_category(category, is_active)
                if success:
                    return True, f"Statut de '{category}' mis à jour (objets individuels)"
                else:
                    return False, f"Erreur lors de la mise à jour de '{category}'"
            else:
                return False, f"Catégorie '{category}' introuvable"
        except Exception as e:
            return False, f"Erreur lors de la mise à jour: {str(e)}"
        
    def reset_to_default(self):
        """
        Remet toutes les catégories à False sauf celles par défaut
        Returns: str - Message de résultat
        """
        if not self.yaml_data:
            return "Erreur : Aucune donnée chargée (utilisez load_yaml() d'abord)"
    
        try:
            # Créer le dictionnaire avec toutes les catégories à False
            default_dict = {}
            
            # Toutes les catégories à False d'abord (y compris les catégories virtuelles)
            all_categories = [
                "ores", "base_ores", "guck_ores", "giant_ores", "other_ores", "flower", "tarpits", 
                "seeds", "portals", "runestones", "mushrooms", "berry", "crypt", 
                "special", "pickable", "morgenholes", "dungeon", "spawners", 
                "boss_spawners", "treasures", "environment"
            ]
        
            for category in all_categories:
                default_dict[category] = False
        
            # Mettre les catégories par défaut à True
            for category in self.default_active_categories:
                default_dict[category] = True
        
            # Appliquer les changements
            result = self.update_categories(default_dict)
        
            if result.startswith("Erreur"):
                return result
        
            return f"Configuration remise aux valeurs par défaut : {', '.join(self.default_active_categories)} activées"
        
        except Exception as e:
            return f"Erreur lors de la remise à zéro : {str(e)}"
    
    def _validate_config(self):
        """
        Vérifie que le fichier de configuration respecte les critères requis
        Returns: tuple (bool, str) - (is_valid, message)
        """
        if not self.yaml_data:
            return False, "Aucune donnée à valider"
    
        # Liste de toutes les catégories attendues (sans les anciennes catégories de minerais)
        expected_categories = {
            "ores", "flower", "tarpits", "seeds", "portals", "runestones", 
            "mushrooms", "berry", "crypt", "special", "pickable", 
            "morgenholes", "dungeon", "spawners", "boss_spawners", "treasures", 
            "environment"
        }
    
        try:
            # Vérifier que toutes les catégories sont présentes
            existing_categories = set(self.yaml_data.keys())
            missing_categories = expected_categories - existing_categories
        
            if missing_categories:
                return False, f"Catégories manquantes: {', '.join(missing_categories)}"
        
            # Vérifier la structure de base de chaque catégorie
            for category, data in self.yaml_data.items():
                if not isinstance(data, dict):
                    return False, f"Catégorie '{category}': doit être un objet"
            
                # Vérifier que isActive existe
                if 'isActive' not in data:
                    return False, f"Catégorie '{category}': clé manquante 'isActive'"
            
                if not isinstance(data['isActive'], bool):
                    return False, f"Catégorie '{category}': 'isActive' doit être true/false"
            
                # iconName est optionnel (certaines catégories n'en ont pas)
                if 'iconName' in data and not isinstance(data['iconName'], str):
                    return False, f"Catégorie '{category}': 'iconName' doit être une chaîne de caractères"
            
                # Vérifier qu'il y a au moins individualConfiguredObjects OU categoryConfiguredObjects
                has_individual = 'individualConfiguredObjects' in data
                has_category = 'categoryConfiguredObjects' in data
            
                if not has_individual and not has_category:
                    return False, f"Catégorie '{category}': doit avoir 'individualConfiguredObjects' ou 'categoryConfiguredObjects'"
            
                # Si individualConfiguredObjects existe, vérifier sa structure
                if has_individual:
                    individual_objects = data['individualConfiguredObjects']
                    if not isinstance(individual_objects, dict):
                        return False, f"Catégorie '{category}': 'individualConfiguredObjects' doit être un objet"
                
                    # Vérifier chaque objet individuel
                    for obj_name, obj_data in individual_objects.items():
                        if not isinstance(obj_data, dict):
                            return False, f"Catégorie '{category}', objet '{obj_name}': doit être un objet"
                    
                        # isActive est obligatoire pour les objets individuels
                        if 'isActive' not in obj_data:
                            return False, f"Catégorie '{category}', objet '{obj_name}': clé manquante 'isActive'"
            
                # Si categoryConfiguredObjects existe, vérifier que c'est une liste
                if has_category:
                    category_objects = data['categoryConfiguredObjects']
                    if not isinstance(category_objects, list):
                        return False, f"Catégorie '{category}': 'categoryConfiguredObjects' doit être une liste"
        
            return True, "Configuration valide"
        
        except Exception as e:
            return False, f"Erreur de validation: {str(e)}"

    def _merge_ores_categories(self):
        """
        Fusionne les catégories giant_ores, guck_ores et other_ores dans la catégorie ores
        Utilise les iconColorRGBA des catégories d'origine pour chaque objet individuel
        """
        if not self.yaml_data:
            return "Erreur : Aucune donnée chargée"
        
        try:
            # Vérifier que la catégorie ores existe
            if "ores" not in self.yaml_data:
                return "Erreur : Catégorie 'ores' introuvable"
            
            # Récupérer les données des catégories à fusionner
            categories_to_merge = {
                "giant_ores": self.yaml_data.get("giant_ores", {}),
                "guck_ores": self.yaml_data.get("guck_ores", {}),
                "other_ores": self.yaml_data.get("other_ores", {})
            }
            
            # Fusionner les objets individuels dans la catégorie ores
            for category_name, category_data in categories_to_merge.items():
                if category_data and "individualConfiguredObjects" in category_data:
                    individual_objects = category_data["individualConfiguredObjects"]
                    category_color = category_data.get("iconColorRGBA", {})
                    
                    for obj_name, obj_data in individual_objects.items():
                        # Ajouter l'objet à la catégorie ores
                        self.yaml_data["ores"]["individualConfiguredObjects"][obj_name] = obj_data.copy()
                        
                        # Ajouter la couleur de la catégorie si l'objet n'en a pas
                        if "iconColorRGBA" not in obj_data and category_color:
                            self.yaml_data["ores"]["individualConfiguredObjects"][obj_name]["iconColorRGBA"] = category_color.copy()
            
            # Supprimer les anciennes catégories
            for category_name in categories_to_merge.keys():
                if category_name in self.yaml_data:
                    del self.yaml_data[category_name]
            
            return "Fusion des catégories de minerais réussie"
            
        except Exception as e:
            return f"Erreur lors de la fusion : {str(e)}"
        try:
            # Chemin vers le fichier de configuration par défaut
            default_config_path = Path("default_config.yaml")
        
            if not default_config_path.exists():
                return "Erreur: Fichier default_config.yaml introuvable dans le projet"
        
            # Charger la configuration par défaut
            with open(default_config_path, 'r', encoding='utf-8') as file:
                default_data = yaml.safe_load(file)
            
            if not default_data:
                return "Erreur: Fichier default_config.yaml vide ou invalide"
        
            # Créer un backup du fichier corrompu
            if self.config_path and self.config_path.exists():
                from backup_manager import BackupManager
                backup_manager = BackupManager()
                backup_result = backup_manager._create_backup(self.config_path)
                # On continue même si le backup échoue
        
            # Remplacer les données en mémoire
            self.yaml_data = default_data
        
            # Sauvegarder le fichier
            save_result = self.save_yaml()
            if save_result.startswith("Erreur"):
                return f"Erreur lors de la sauvegarde de la config par défaut: {save_result}"
        
            return "Configuration restaurée aux valeurs par défaut"
        
        except Exception as e:
            return f"Erreur lors de la restauration: {str(e)}"