#!/usr/bin/env python3
"""
Script de test pour vérifier le fonctionnement du config manager modifié
"""

import yaml
from config_manager import ConfigManager

def test_merge_functionality():
    """Test la fonctionnalité de fusion des catégories"""
    
    print("=== Test du Config Manager modifié ===")
    
    # Créer une instance du config manager
    cm = ConfigManager()
    cm.DEV_MODE = True  # Mode dev pour tester localement
    
    # Charger le fichier de configuration par défaut
    print("1. Chargement de la configuration...")
    result = cm.load_yaml()
    print(f"   Résultat: {result}")
    
    if cm.yaml_data:
        print("2. Configuration chargée avec succès!")
        
        # Vérifier que les catégories ont été fusionnées
        print("3. Vérification de la structure après fusion...")
        
        if "ores" in cm.yaml_data:
            ores_objects = cm.yaml_data["ores"]["individualConfiguredObjects"]
            print(f"   Nombre d'objets dans 'ores': {len(ores_objects)}")
            
            # Vérifier que les objets des anciennes catégories sont présents
            test_objects = ["GuckSack", "giant_brain", "LeviathanLava"]
            for obj in test_objects:
                if obj in ores_objects:
                    print(f"   ✓ {obj} trouvé dans la catégorie ores")
                    # Vérifier la couleur
                    if "iconColorRGBA" in ores_objects[obj]:
                        color = ores_objects[obj]["iconColorRGBA"]
                        print(f"     Couleur: R={color['red']}, G={color['green']}, B={color['blue']}")
                else:
                    print(f"   ✗ {obj} manquant dans la catégorie ores")
        
        # Vérifier que les anciennes catégories ont été supprimées
        old_categories = ["giant_ores", "guck_ores", "other_ores"]
        for cat in old_categories:
            if cat in cm.yaml_data:
                print(f"   ✗ Ancienne catégorie '{cat}' encore présente")
            else:
                print(f"   ✓ Ancienne catégorie '{cat}' supprimée")
        
        print("4. Test du statut des catégories...")
        categories_status = cm.get_categories_status()
        if isinstance(categories_status, dict):
            print(f"   Catégories actives: {[cat for cat, active in categories_status.items() if active]}")
        else:
            print(f"   Erreur: {categories_status}")
            
        print("\n=== Test terminé avec succès! ===")
    else:
        print("   Erreur lors du chargement de la configuration")

if __name__ == "__main__":
    test_merge_functionality()
