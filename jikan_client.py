import aiohttp
import json
from typing import Optional, Dict, List

class JikanClient:
    """Клиент для работы с Jikan API (MyAnimeList)"""
    
    BASE_URL = "https://api.jikan.moe/v4"
    
    def __init__(self):
        self.session = None
    
    async def __aenter__(self):
        """Открытие сессии (для использования with)"""
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Закрытие сессии"""
        if self.session:
            await self.session.close()
    
    async def search_anime(self, query: str, limit: int = 5) -> List[Dict]:
        """Поиск аниме по названию"""
        url = f"{self.BASE_URL}/anime"
        params = {"q": query, "limit": limit}
        
        try:
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("data", [])
                else:
                    print(f"Ошибка API: {response.status}")
                    return []
        except Exception as e:
            print(f"Ошибка при поиске: {e}")
            return []
    
    async def get_anime_by_id(self, anime_id: int) -> Optional[Dict]:
        """Получить аниме по ID"""
        url = f"{self.BASE_URL}/anime/{anime_id}"
        
        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("data")
                else:
                    print(f"Ошибка API для ID {anime_id}: {response.status}")
                    return None
        except Exception as e:
            print(f"Ошибка при получении аниме: {e}")
            return None
    
    async def get_random_anime(self) -> Optional[Dict]:
        """Получить случайное аниме"""
        url = f"{self.BASE_URL}/random/anime"
        
        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("data")
                else:
                    print(f"Ошибка API random: {response.status}")
                    return None
        except Exception as e:
            print(f"Ошибка при получении случайного аниме: {e}")
            return None

# Тестовая функция
async def test_api():
    """Протестируем API"""
    async with JikanClient() as client:
        # Тест поиска
        print("🔍 Тестирую поиск 'naruto'...")
        results = await client.search_anime("naruto", limit=3)
        print(f"Найдено аниме: {len(results)}")
        
        if results:
            for i, anime in enumerate(results, 1):
                print(f"{i}. {anime.get('title', 'Без названия')} (ID: {anime.get('mal_id')})")
        
        # Тест по ID
        print("\n🔍 Тестирую получение по ID 20...")
        anime = await client.get_anime_by_id(20)  # Attack on Titan
        if anime:
            print(f"Найдено: {anime.get('title')}")
            print(f"Рейтинг: {anime.get('score')}/10")
            print(f"Эпизодов: {anime.get('episodes')}")
async def get_anime_trailer(self, anime_id: int) -> Optional[Dict]:
    """Получить информацию о трейлере аниме"""
    url = f"{self.BASE_URL}/anime/{anime_id}"
    
    try:
        async with self.session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                anime_data = data.get("data", {})
                trailer_data = anime_data.get("trailer", {})
                
                if trailer_data:
                    return {
                        "youtube_id": trailer_data.get("youtube_id"),
                        "url": trailer_data.get("url"),
                        "embed_url": trailer_data.get("embed_url")
                    }
                return None
            return None
    except Exception as e:
        print(f"❌ Ошибка при получении трейлера: {e}")
        return None

# Запуск теста
if __name__ == "__main__":
    import asyncio
    asyncio.run(test_api())