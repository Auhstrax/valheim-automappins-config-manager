import shutil
from datetime import datetime
from pathlib import Path

class BackupManager:
    def __init__(self, max_backups=5):
        self.max_backups = max_backups
    
    def _create_backup(self, file_path):
        """
        Crée un backup du fichier donné
        Args: file_path (Path) - Chemin du fichier à sauvegarder
        Returns: str - Message de résultat
        """
        if not file_path or not file_path.exists():
            return "Erreur : Aucun fichier à sauvegarder"
        
        try:
            # Créer le dossier backup s'il n'existe pas
            backup_dir = file_path.parent / "backup"
            backup_dir.mkdir(exist_ok=True)
            
            # Nom du fichier backup avec timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            original_name = file_path.stem
            backup_filename = f"{original_name}_backup_{timestamp}.yaml"
            backup_path = backup_dir / backup_filename
            
            # Copier le fichier
            shutil.copy2(file_path, backup_path)
            
            # Nettoyer les anciens backups
            self._cleanup_old_backups(backup_dir, original_name)
            
            return f"Backup créé : {backup_filename}"
            
        except PermissionError:
            return "Erreur : Permission refusée pour créer le backup"
        except OSError as e:
            return f"Erreur système lors du backup : {str(e)}"
        except Exception as e:
            return f"Erreur inattendue lors du backup : {str(e)}"
    
    def _cleanup_old_backups(self, backup_dir, original_name):
        """
        Supprime les anciens backups, garde seulement les max_backups plus récents
        """
        try:
            backup_pattern = f"{original_name}_backup_*.yaml"
            backup_files = list(backup_dir.glob(backup_pattern))
            
            # Trier par date de modification (plus récent en premier)
            backup_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            
            # Supprimer les anciens backups
            for old_backup in backup_files[self.max_backups:]:
                old_backup.unlink()
                
        except Exception:
            # Si erreur lors du nettoyage, on continue (pas critique)
            pass
    
    def restore_from_backup(self, original_path, backup_filename=None):
        """
        Restaure depuis un backup spécifique ou le plus récent
        """
        backup_dir = original_path.parent / "backup"
        
        if not backup_dir.exists():
            return "Erreur : Aucun dossier de backup trouvé"
        
        try:
            if backup_filename:
                # Restaurer un backup spécifique
                backup_path = backup_dir / backup_filename
                if not backup_path.exists():
                    return f"Erreur : Backup {backup_filename} introuvable"
            else:
                # Prendre le backup le plus récent
                original_name = original_path.stem
                backup_pattern = f"{original_name}_backup_*.yaml"
                backup_files = list(backup_dir.glob(backup_pattern))
                
                if not backup_files:
                    return "Erreur : Aucun backup disponible"
                
                # Trier et prendre le plus récent
                backup_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
                backup_path = backup_files[0]
            
            # Restaurer le fichier
            shutil.copy2(backup_path, original_path)
            return f"Fichier restauré depuis : {backup_path.name}"
            
        except Exception as e:
            return f"Erreur lors de la restauration : {str(e)}"
