#!/usr/bin/env python3
"""
Script de test pour vérifier la configuration par défaut avec base_ores
"""

from config_manager import ConfigManager

def test_default_config_with_base_ores():
    """Test la configuration par défaut avec base_ores inclus"""
    
    print("=== Test de la configuration par défaut avec base_ores ===")
    
    # Créer une instance du config manager
    cm = ConfigManager()
    cm.DEV_MODE = False  # Utiliser le vrai fichier de config
    
    # Charger le fichier de configuration
    print("1. Chargement de la configuration...")
    result = cm.load_yaml()
    print(f"   Résultat: {result}")
    
    if cm.yaml_data:
        print("\n2. État actuel des catégories...")
        categories_status = cm.get_categories_status()
        
        if isinstance(categories_status, dict):
            active_categories = [cat for cat, active in categories_status.items() if active]
            print(f"   Catégories actuellement actives: {active_categories}")
        
        print("\n3. Réinitialisation aux valeurs par défaut...")
        result = cm.reset_to_default()
        print(f"   Résultat: {result}")
        
        print("\n4. État après réinitialisation...")
        categories_status = cm.get_categories_status()
        
        if isinstance(categories_status, dict):
            print("   Catégories par défaut:")
            for category in cm.default_active_categories:
                status = categories_status.get(category, False)
                status_icon = "✓" if status else "✗"
                print(f"     {status_icon} {category}: {status}")
            
            print(f"\n   Vérification que base_ores est dans les catégories par défaut:")
            if "base_ores" in cm.default_active_categories:
                print("     ✓ base_ores est inclus dans default_active_categories")
                
                base_ores_status = categories_status.get("base_ores", False)
                if base_ores_status:
                    print("     ✓ base_ores est actif après reset_to_default")
                else:
                    print("     ✗ base_ores n'est pas actif après reset_to_default")
            else:
                print("     ✗ base_ores manque dans default_active_categories")
        
        print("\n5. Sauvegarde de la configuration par défaut...")
        save_result = cm.save_yaml()
        print(f"   Résultat: {save_result}")
        
        print(f"\n6. Liste complète des catégories par défaut:")
        print(f"   {cm.default_active_categories}")
            
        print("\n=== Test terminé ===")
    else:
        print("   Erreur lors du chargement de la configuration")

if __name__ == "__main__":
    test_default_config_with_base_ores()
