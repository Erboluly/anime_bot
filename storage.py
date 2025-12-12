import json
import os
from datetime import datetime
from typing import Dict, List, Optional

class JSONStorage:
    """Хранилище данных в JSON файле"""
    
    def __init__(self, filename: str = "data/users_data.json"):
        self.filename = filename
        self.ensure_directory()
        self.data = self.load_data()
    
    def ensure_directory(self):
        """Создаёт папку для данных, если её нет"""
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
    
    def load_data(self) -> Dict:
        """Загружает данные из JSON файла"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return {}
        return {}
    
    def save_data(self):
        """Сохраняет данные в JSON файл"""
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    # ========== ПОЛЬЗОВАТЕЛИ ==========
    
    def get_user_data(self, user_id: int) -> Dict:
        """Получить данные пользователя"""
        user_id_str = str(user_id)
        if user_id_str not in self.data:
            self.data[user_id_str] = {
                "user_id": user_id,
                "username": "",
                "anime_list": [],
                "settings": {
                    "language": "ru",
                    "theme": "dark",
                    "notifications": True,
                    "auto_translate": True
                },
                "created_at": datetime.now().isoformat(),
                "stats": {
                    "total_anime": 0,
                    "completed": 0,
                    "watching": 0,
                    "planned": 0,
                    "dropped": 0
                }
            }
            self.save_data()
        return self.data[user_id_str]
    
    def update_user_settings(self, user_id: int, settings: Dict):
        """Обновить настройки пользователя"""
        user_data = self.get_user_data(user_id)
        user_data["settings"].update(settings)
        self.save_data()
        return True
    
    # ========== АНИМЕ СПИСОК ==========
    
    def add_anime_to_list(self, user_id: int, anime_data: Dict, status: str = "planned") -> bool:
        """Добавить аниме в список пользователя"""
        user_data = self.get_user_data(user_id)
        
        anime_id = anime_data.get("mal_id")
        if not anime_id:
            return False
        
        # Проверяем, нет ли уже этого аниме
        for anime in user_data["anime_list"]:
            if anime["anime_id"] == anime_id:
                return False  # Уже есть
        
        # Добавляем новое аниме
        new_anime = {
            "anime_id": anime_id,
            "title": anime_data.get("title", ""),
            "title_english": anime_data.get("title_english", ""),
            "image_url": anime_data.get("images", {}).get("jpg", {}).get("image_url", ""),
            "score": anime_data.get("score", 0),
            "episodes": anime_data.get("episodes", 0),
            "status": status,
            "added_date": datetime.now().isoformat(),
            "updated_date": datetime.now().isoformat(),
            "user_rating": 0,
            "watched_episodes": 0,
            "notes": ""
        }
        
        user_data["anime_list"].append(new_anime)
        
        # Обновляем статистику
        user_data["stats"]["total_anime"] = len(user_data["anime_list"])
        user_data["stats"][status] = user_data["stats"].get(status, 0) + 1
        
        self.save_data()
        return True
    
    def get_user_anime_list(self, user_id: int, status_filter: str = None) -> List[Dict]:
        """Получить список аниме пользователя"""
        user_data = self.get_user_data(user_id)
        
        if status_filter:
            return [anime for anime in user_data["anime_list"] if anime["status"] == status_filter]
        return user_data["anime_list"]
    
    def update_anime_status(self, user_id: int, anime_id: int, new_status: str) -> bool:
        """Изменить статус аниме"""
        user_data = self.get_user_data(user_id)
        
        for anime in user_data["anime_list"]:
            if anime["anime_id"] == anime_id:
                old_status = anime["status"]
                anime["status"] = new_status
                anime["updated_date"] = datetime.now().isoformat()
                
                # Обновляем статистику
                if old_status != new_status:
                    user_data["stats"][old_status] = max(0, user_data["stats"].get(old_status, 1) - 1)
                    user_data["stats"][new_status] = user_data["stats"].get(new_status, 0) + 1
                
                self.save_data()
                return True
        return False
    
    def delete_anime_from_list(self, user_id: int, anime_id: int) -> bool:
        """Удалить аниме из списка"""
        user_data = self.get_user_data(user_id)
        
        # Находим аниме для удаления
        for i, anime in enumerate(user_data["anime_list"]):
            if anime["anime_id"] == anime_id:
                status = anime["status"]
                # Удаляем
                user_data["anime_list"].pop(i)
                
                # Обновляем статистику
                user_data["stats"]["total_anime"] = len(user_data["anime_list"])
                user_data["stats"][status] = max(0, user_data["stats"].get(status, 1) - 1)
                
                self.save_data()
                return True
        return False
    
    def update_anime_progress(self, user_id: int, anime_id: int, watched_episodes: int, user_rating: int = None, notes: str = None) -> bool:
        """Обновить прогресс просмотра"""
        user_data = self.get_user_data(user_id)
        
        for anime in user_data["anime_list"]:
            if anime["anime_id"] == anime_id:
                anime["watched_episodes"] = watched_episodes
                anime["updated_date"] = datetime.now().isoformat()
                
                if user_rating is not None:
                    anime["user_rating"] = user_rating
                
                if notes is not None:
                    anime["notes"] = notes
                
                # Если просмотрены все эпизоды, меняем статус на "completed"
                if watched_episodes >= anime.get("episodes", 999) and anime["episodes"] > 0:
                    if anime["status"] != "completed":
                        old_status = anime["status"]
                        anime["status"] = "completed"
                        user_data["stats"][old_status] = max(0, user_data["stats"].get(old_status, 1) - 1)
                        user_data["stats"]["completed"] = user_data["stats"].get("completed", 0) + 1
                
                self.save_data()
                return True
        return False

# Глобальный экземпляр хранилища
storage = JSONStorage()