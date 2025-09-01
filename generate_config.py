#!/usr/bin/env python3
"""
Script pour générer un fichier de configuration avec la structure fusionnée
"""

import yaml
from config_manager import ConfigManager
from pathlib import Path

def generate_merged_config():
    """Génère un fichier de configuration avec les catégories fusionnées"""
    
    print("=== Génération de la configuration fusionnée ===")
    
    # Créer une instance du config manager
    cm = ConfigManager()
    cm.DEV_MODE = True
    
    # Charger le fichier de configuration par défaut
    print("1. Chargement de la configuration par défaut...")
    result = cm.load_yaml()
    print(f"   Résultat: {result}")
    
    if cm.yaml_data:
        # Sauvegarder dans un fichier de test
        output_file = Path("merged_config_test.yaml")
        
        print(f"2. Sauvegarde dans {output_file}...")
        
        try:
            with open(output_file, 'w', encoding='utf-8') as file:
                yaml.dump(
                    cm.yaml_data,
                    file,
                    default_flow_style=False,
                    allow_unicode=True,
                    sort_keys=False
                )
            print(f"   Configuration sauvegardée dans : {output_file}")
            
            # Afficher le contenu de la catégorie ores
            print("3. Contenu de la catégorie 'ores' fusionnée:")
            ores_data = cm.yaml_data.get("ores", {})
            individual_objects = ores_data.get("individualConfiguredObjects", {})
            
            print(f"   Nombre d'objets: {len(individual_objects)}")
            for obj_name, obj_data in individual_objects.items():
                status = "✓" if obj_data.get("isActive", False) else "✗"
                name = obj_data.get("name", obj_name)
                print(f"   {status} {obj_name} ({name})")
                
        except Exception as e:
            print(f"   Erreur lors de la sauvegarde: {e}")
    
    print("\n=== Génération terminée ===")

if __name__ == "__main__":
    generate_merged_config()
