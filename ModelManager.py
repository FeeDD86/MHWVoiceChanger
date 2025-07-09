import os
import urllib.request
import json
import Query

class ModelManager:
    def __init__(self):
        self.models_dir = "models"
        self.ensure_models_directory()
    
    def ensure_models_directory(self):
        if not os.path.exists(self.models_dir):
            os.makedirs(self.models_dir)
            print(f"Created models directory: {self.models_dir}")
    
    def get_available_models(self):
        models = []
        if os.path.exists(self.models_dir):
            for filename in os.listdir(self.models_dir):
                if filename.endswith('.pth'):
                    voice_id = filename[:-4]
                    voice_info = Query.identifyFileID((voice_id,))
                    if voice_info:
                        models.append({
                            'voice_id': voice_id,
                            'filename': filename,
                            'name': f"{voice_info[1]} Voice {voice_info[2]}",
                            'path': os.path.join(self.models_dir, filename)
                        })
        return models
    
    def is_model_available(self, voice_id):
        model_path = os.path.join(self.models_dir, f"{voice_id}.pth")
        return os.path.exists(model_path)
    
    def get_model_path(self, voice_id):
        return os.path.join(self.models_dir, f"{voice_id}.pth")
    
    def create_placeholder_model(self, voice_id):
        model_path = self.get_model_path(voice_id)
        try:
            with open(model_path, 'w') as f:
                f.write(f"# Placeholder model for {voice_id}\n")
                f.write("# Replace this with actual RVC model file\n")
            print(f"Created placeholder model: {model_path}")
            return True
        except Exception as e:
            print(f"Error creating placeholder model: {e}")
            return False
    
    def get_missing_models(self):
        missing = []
        try:
            for gender in ['FEMALE', 'MALE']:
                for voice_num in range(1, 21):
                    voice_id = f"{gender}_{voice_num}"
                    voice_info = Query.identifyFileID((voice_id,))
                    if voice_info and voice_info[4] == 1:
                        if not self.is_model_available(voice_id):
                            missing.append({
                                'voice_id': voice_id,
                                'name': f"{voice_info[1]} Voice {voice_info[2]}",
                                'filename': voice_info[3]
                            })
        except Exception as e:
            print(f"Error checking missing models: {e}")
        return missing
    
    def setup_default_models(self):
        missing_models = self.get_missing_models()
        created_count = 0
        
        for model_info in missing_models[:5]:
            if self.create_placeholder_model(model_info['voice_id']):
                created_count += 1
        
        print(f"Created {created_count} placeholder models")
        return created_count > 0
