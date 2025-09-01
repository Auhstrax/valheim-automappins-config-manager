#!/usr/bin/env python3
"""
Script de test pour vérifier le fonctionnement des catégories virtuelles
"""

import yaml
from config_manager import ConfigManager

def test_virtual_categories():
    """Test la fonctionnalité des catégories virtuelles"""
    
    print("=== Test des catégories virtuelles ===")
    
    # Créer une instance du config manager
    cm = ConfigManager()
    cm.DEV_MODE = True
    
    # Charger le fichier de configuration
    print("1. Chargement de la configuration...")
    result = cm.load_yaml()
    print(f"   Résultat: {result}")
    
    if cm.yaml_data:
        print("2. Test du statut initial des catégories...")
        categories_status = cm.get_categories_status()
        
        if isinstance(categories_status, dict):
            print("   Statut des catégories de minerais:")
            for category in ["ores", "guck_ores", "giant_ores", "other_ores"]:
                status = "✓" if categories_status.get(category, False) else "✗"
                print(f"   {status} {category}: {categories_status.get(category, False)}")
        
        print("\n3. Test de mise à jour d'une catégorie virtuelle...")
        print("   Désactivation de 'guck_ores'...")
        success, message = cm.set_category_status("guck_ores", False)
        print(f"   Résultat: {message}")
        
        if success:
            # Vérifier l'état des objets individuels
            ores_objects = cm.yaml_data["ores"]["individualConfiguredObjects"]
            guck_objects = cm.ores_mapping["guck_ores"]
            
            print("   État des objets Guck après désactivation:")
            for obj_name in guck_objects:
                if obj_name in ores_objects:
                    is_active = ores_objects[obj_name].get("isActive", False)
                    status = "✓" if is_active else "✗"
                    print(f"     {status} {obj_name}: {is_active}")
        
        print("\n4. Test de ré-activation...")
        print("   Activation de 'giant_ores'...")
        success, message = cm.set_category_status("giant_ores", True)
        print(f"   Résultat: {message}")
        
        if success:
            # Vérifier l'état des objets individuels
            ores_objects = cm.yaml_data["ores"]["individualConfiguredObjects"]
            giant_objects = cm.ores_mapping["giant_ores"]
            
            print("   État des objets Giant après activation:")
            for obj_name in giant_objects:
                if obj_name in ores_objects:
                    is_active = ores_objects[obj_name].get("isActive", False)
                    status = "✓" if is_active else "✗"
                    print(f"     {status} {obj_name}: {is_active}")
        
        print("\n5. Vérification finale du statut des catégories...")
        categories_status = cm.get_categories_status()
        
        if isinstance(categories_status, dict):
            print("   Statut final des catégories de minerais:")
            for category in ["ores", "guck_ores", "giant_ores", "other_ores"]:
                status = "✓" if categories_status.get(category, False) else "✗"
                print(f"   {status} {category}: {categories_status.get(category, False)}")
            
        print("\n=== Test terminé ===")
    else:
        print("   Erreur lors du chargement de la configuration")

if __name__ == "__main__":
    test_virtual_categories()
