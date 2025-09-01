#!/usr/bin/env python3
"""
Script de test pour vérifier la gestion des minerais de base
"""

from config_manager import ConfigManager

def test_base_ores_management():
    """Test la gestion des minerais de base"""
    
    print("=== Test de la gestion des minerais de base ===")
    
    # Créer une instance du config manager
    cm = ConfigManager()
    cm.DEV_MODE = False  # Utiliser le vrai fichier de config
    
    # Charger le fichier de configuration
    print("1. Chargement de la configuration...")
    result = cm.load_yaml()
    print(f"   Résultat: {result}")
    
    if cm.yaml_data:
        print("\n2. État initial des minerais de base...")
        if "ores" in cm.yaml_data:
            ores_objects = cm.yaml_data["ores"]["individualConfiguredObjects"]
            base_ores = cm.ores_mapping["base_ores"]
            
            print("   Minerais de base:")
            for ore in base_ores:
                if ore in ores_objects:
                    is_active = ores_objects[ore].get("isActive", False)
                    status = "✓" if is_active else "✗"
                    name = ores_objects[ore].get("name", ore)
                    print(f"     {status} {ore} ({name}): {is_active}")
        
        print("\n3. Test de désactivation de la catégorie 'ores'...")
        success, message = cm.set_category_status("ores", False)
        print(f"   Résultat: {message}")
        
        if success:
            print("   État après désactivation:")
            ores_objects = cm.yaml_data["ores"]["individualConfiguredObjects"]
            base_ores = cm.ores_mapping["base_ores"]
            
            for ore in base_ores:
                if ore in ores_objects:
                    is_active = ores_objects[ore].get("isActive", False)
                    status = "✓" if is_active else "✗"
                    name = ores_objects[ore].get("name", ore)
                    print(f"     {status} {ore} ({name}): {is_active}")
        
        print("\n4. Test de réactivation de la catégorie 'ores'...")
        success, message = cm.set_category_status("ores", True)
        print(f"   Résultat: {message}")
        
        if success:
            print("   État après réactivation:")
            ores_objects = cm.yaml_data["ores"]["individualConfiguredObjects"]
            base_ores = cm.ores_mapping["base_ores"]
            
            for ore in base_ores:
                if ore in ores_objects:
                    is_active = ores_objects[ore].get("isActive", False)
                    status = "✓" if is_active else "✗"
                    name = ores_objects[ore].get("name", ore)
                    print(f"     {status} {ore} ({name}): {is_active}")
        
        print("\n5. Test de contrôle individuel des minerais de base...")
        success, message = cm.set_category_status("base_ores", False)
        print(f"   Désactivation de 'base_ores': {message}")
        
        if success:
            print("   État des minerais de base après désactivation individuelle:")
            ores_objects = cm.yaml_data["ores"]["individualConfiguredObjects"]
            base_ores = cm.ores_mapping["base_ores"]
            
            for ore in base_ores:
                if ore in ores_objects:
                    is_active = ores_objects[ore].get("isActive", False)
                    status = "✓" if is_active else "✗"
                    name = ores_objects[ore].get("name", ore)
                    print(f"     {status} {ore} ({name}): {is_active}")
        
        print("\n6. Sauvegarde des modifications...")
        save_result = cm.save_yaml()
        print(f"   Résultat: {save_result}")
            
        print("\n=== Test terminé ===")
    else:
        print("   Erreur lors du chargement de la configuration")

if __name__ == "__main__":
    test_base_ores_management()
