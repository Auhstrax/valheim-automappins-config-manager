#!/usr/bin/env python3
"""
Script de test pour vérifier les mises à jour du config manager
"""

from config_manager import ConfigManager

def test_updated_config_manager():
    """Test le config manager avec les nouvelles catégories"""
    
    print("=== Test du Config Manager mis à jour ===")
    
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
            
            # Vérifier les nouvelles catégories
            new_categories = ["flower", "berry", "pickable", "environment"]
            old_categories = ["flowers", "berries", "pickables"]
            
            for category, status in categories_status.items():
                status_icon = "✓" if status else "✗"
                highlight = " (NOUVEAU)" if category in new_categories else ""
                print(f"   {status_icon} {category}: {status}{highlight}")
            
            print(f"\n3. Vérification des changements de noms:")
            
            # Vérifier que les nouvelles catégories existent
            for new_cat in new_categories:
                if new_cat in categories_status:
                    print(f"   ✓ Nouvelle catégorie '{new_cat}' trouvée")
                else:
                    print(f"   ✗ Nouvelle catégorie '{new_cat}' manquante")
            
            # Vérifier que les anciennes catégories n'existent plus
            for old_cat in old_categories:
                if old_cat in categories_status:
                    print(f"   ✗ Ancienne catégorie '{old_cat}' encore présente")
                else:
                    print(f"   ✓ Ancienne catégorie '{old_cat}' supprimée")
            
            print(f"\n4. Test de mise à jour d'une catégorie...")
            success, message = cm.set_category_status("flower", False)
            print(f"   Désactivation de 'flower': {message}")
            
            if success:
                # Vérifier le changement
                new_status = cm.get_categories_status()
                if isinstance(new_status, dict):
                    flower_status = new_status.get("flower", None)
                    print(f"   Statut de 'flower' après modification: {flower_status}")
                    
            print(f"\n5. Nombre total de catégories gérées:")
            print(f"   Total: {len(categories_status)} catégories")
            
            # Compter les catégories actives
            active_count = sum(1 for status in categories_status.values() if status)
            print(f"   Actives: {active_count}")
            print(f"   Inactives: {len(categories_status) - active_count}")
                
        else:
            print(f"   Erreur: {categories_status}")
            
        print("\n=== Test terminé ===")
    else:
        print("   Erreur lors du chargement de la configuration")

if __name__ == "__main__":
    test_updated_config_manager()
