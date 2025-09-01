#!/usr/bin/env python3
"""
Script pour générer un exemple de configuration finale
"""

import yaml
from config_manager import ConfigManager
from pathlib import Path

def generate_example_config():
    """Génère un exemple de configuration finale après manipulation des catégories virtuelles"""
    
    print("=== Génération d'un exemple de configuration finale ===")
    
    # Créer une instance du config manager
    cm = ConfigManager()
    cm.DEV_MODE = True
    
    # Charger le fichier de configuration
    print("1. Chargement de la configuration...")
    result = cm.load_yaml()
    print(f"   Résultat: {result}")
    
    if cm.yaml_data:
        # Tester différentes configurations
        print("2. Configuration d'exemple...")
        
        # Activer seulement les minerais Guck et désactiver les autres sous-catégories
        cm.set_category_status("guck_ores", True)
        cm.set_category_status("giant_ores", False)
        cm.set_category_status("other_ores", False)
        
        print("   - Guck activé")
        print("   - Giants désactivés")
        print("   - Others désactivés")
        
        # Sauvegarder dans un fichier d'exemple
        output_file = Path("example_config.yaml")
        
        print(f"3. Sauvegarde dans {output_file}...")
        
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
            
            # Afficher un résumé de la catégorie ores
            print("4. Résumé de la catégorie 'ores':")
            ores_data = cm.yaml_data.get("ores", {})
            individual_objects = ores_data.get("individualConfiguredObjects", {})
            
            active_objects = [name for name, data in individual_objects.items() if data.get("isActive", False)]
            inactive_objects = [name for name, data in individual_objects.items() if not data.get("isActive", False)]
            
            print(f"   Objets actifs ({len(active_objects)}): {', '.join(active_objects)}")
            print(f"   Objets inactifs ({len(inactive_objects)}): {', '.join(inactive_objects)}")
            
            # Vérification des statuts des catégories virtuelles
            print("5. Statut des catégories virtuelles:")
            categories_status = cm.get_categories_status()
            for cat in ["guck_ores", "giant_ores", "other_ores"]:
                status = "✓" if categories_status.get(cat, False) else "✗"
                print(f"   {status} {cat}: {categories_status.get(cat, False)}")
                
        except Exception as e:
            print(f"   Erreur lors de la sauvegarde: {e}")
    
    print("\n=== Génération terminée ===")

if __name__ == "__main__":
    generate_example_config()
