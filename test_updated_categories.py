#!/usr/bin/env python3
"""
Script de test pour vérifier les nouveaux noms de catégories
"""

from config_manager import ConfigManager

def test_updated_categories():
    """Test les nouvelles catégories mises à jour"""
    
    print("=== Test des catégories mises à jour ===")
    
    # Créer une instance du config manager
    cm = ConfigManager()
    cm.DEV_MODE = True
    
    # Charger le fichier de configuration
    print("1. Chargement de la configuration...")
    result = cm.load_yaml()
    print(f"   Résultat: {result}")
    
    if cm.yaml_data:
        print("2. Vérification des catégories disponibles...")
        categories_status = cm.get_categories_status()
        
        if isinstance(categories_status, dict):
            print("   Catégories trouvées:")
            for category, status in categories_status.items():
                status_icon = "✓" if status else "✗"
                print(f"   {status_icon} {category}: {status}")
            
            # Vérifier spécifiquement si 'flower' existe et 'flowers' n'existe pas
            print(f"\n3. Vérification des changements de noms:")
            if "flower" in categories_status:
                print("   ✓ Catégorie 'flower' trouvée")
            else:
                print("   ✗ Catégorie 'flower' manquante")
            
            if "flowers" in categories_status:
                print("   ✗ Ancienne catégorie 'flowers' encore présente")
            else:
                print("   ✓ Ancienne catégorie 'flowers' supprimée")
                
            # Vérifier si la catégorie flower est bien dans le fichier YAML
            if "flower" in cm.yaml_data:
                print("   ✓ Catégorie 'flower' présente dans le YAML")
                flower_active = cm.yaml_data["flower"].get("isActive", False)
                print(f"   État de la catégorie flower: {flower_active}")
            else:
                print("   ✗ Catégorie 'flower' absente du YAML")
        else:
            print(f"   Erreur: {categories_status}")
            
        print("\n=== Test terminé ===")
    else:
        print("   Erreur lors du chargement de la configuration")

if __name__ == "__main__":
    test_updated_categories()
