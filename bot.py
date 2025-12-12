import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# Импорт нашего клиента для работы с API
from jikan_client import JikanClient
from storage import storage

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Ваш токен от @BotFather
TOKEN = "8454208833:AAFQzSrNWC6nrx9iHl37qQ05Xjl8mfNa5iE"

# Создаём бота и диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher()

# ========== КЛАВИАТУРЫ ==========

def get_main_keyboard():
    """Главная клавиатура меню"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔍 Поиск аниме"), KeyboardButton(text="🎲 Случайное")],
            [KeyboardButton(text="📋 Мой список"), KeyboardButton(text="📊 Топ недели")],
            [KeyboardButton(text="📺 Онгоинги"), KeyboardButton(text="ℹ️ Помощь")],
            [KeyboardButton(text="⚙️ Настройки"), KeyboardButton(text="❌ Скрыть меню")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )

def get_search_keyboard():
    """Клавиатура для поиска"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔎 Новый поиск"), KeyboardButton(text="🎬 Популярное")],
            [KeyboardButton(text="🔙 Назад в меню"), KeyboardButton(text="❓ Как искать?")]
        ],
        resize_keyboard=True
    )

def get_anime_actions_keyboard(anime_id: int):
    """Inline-кнопки для действий с аниме"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Добавить в список", callback_data=f"add_{anime_id}"),
                InlineKeyboardButton(text="📖 Подробнее", callback_data=f"info_{anime_id}")
            ],
            [
                InlineKeyboardButton(text="🎥 Трейлер", callback_data=f"trailer_{anime_id}"),
                InlineKeyboardButton(text="🔍 Похожие", callback_data=f"similar_{anime_id}")
            ],
            [
                InlineKeyboardButton(text="⭐ Оценить", callback_data=f"rate_{anime_id}"),
                InlineKeyboardButton(text="🗑️ Удалить из списка", callback_data=f"remove_{anime_id}")
            ]
        ]
    )

# ========== КОМАНДЫ БОТА ==========

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """Команда /start - приветствие с меню"""
    keyboard = get_main_keyboard()
    
    # Инициализируем пользователя в хранилище
    storage.get_user_data(message.from_user.id)
    
    await message.answer(
        "🎌 <b>Добро пожаловать в AniBot!</b>\n\n"
        "🏆 <i>Ваш персональный аниме-гид</i>\n\n"
        "📁 <b>Что умеет бот:</b>\n"
        "• 🔍 Поиск по базе MyAnimeList\n"
        "• 📋 Личный список просмотра\n"
        "• 🎯 Персональные рекомендации\n"
        "• 📊 Топы и новинки\n"
        "• 🔔 Уведомления о выходе\n\n"
        "👇 <b>Используйте меню ниже</b> или команды",
        reply_markup=keyboard,
        parse_mode="HTML"
    )

@dp.message(Command("menu"))
async def cmd_menu(message: types.Message):
    """Показать меню"""
    keyboard = get_main_keyboard()
    await message.answer(
        "🏠 <b>Главное меню AniBot</b>\n\n"
        "<i>Выберите раздел:</i>",
        reply_markup=keyboard,
        parse_mode="HTML"
    )

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    """Команда /help - справка"""
    await message.answer(
        "📚 <b>Доступные команды:</b>\n\n"
        
        "<b>Основные команды:</b>\n"
        "/start - Начало работы с меню\n"
        "/menu - Показать меню\n"
        "/hide - Скрыть меню\n"
        "/help - Эта справка\n\n"
        
        "<b>Поиск аниме:</b>\n"
        "/search [название] - Найти аниме\n"
        "/anime [id] - Подробности об аниме\n"
        "/random - Случайное аниме\n\n"
        
        "<b>Мой список:</b>\n"
        "/add [id] - Добавить в список\n"
        "/mylist - Показать мой список\n"
        "/update [id] [статус] - Изменить статус\n"
        "/delete [id] - Удалить из списка\n\n"
        
        "💡 <b>Как искать:</b>\n"
        "• На русском: <code>/search Наруто</code>\n"
        "• На английском: <code>/search naruto</code>\n"
        "• На японском: <code>/search shingeki no kyojin</code>\n\n"
        
        "📌 <b>Популярные запросы:</b>\n"
        "• Наруто (naruto)\n"
        "• Атака титанов (attack on titan)\n"
        "• Ван Пис (one piece)\n"
        "• Блич (bleach)\n"
        "• Твоё имя (your name)\n\n"
        
        "📱 <b>Используйте меню внизу</b> для быстрого доступа!",
        parse_mode="HTML"
    )

@dp.message(Command("hide"))
async def cmd_hide(message: types.Message):
    """Скрыть меню"""
    remove_keyboard = types.ReplyKeyboardRemove()
    await message.answer(
        "⌨️ <b>Клавиатура скрыта</b>\n\n"
        "Используйте команды или:\n"
        "/menu - показать меню",
        reply_markup=remove_keyboard,
        parse_mode="HTML"
    )

# ========== ОБРАБОТЧИКИ КНОПОК МЕНЮ ==========

@dp.message(F.text == "🔍 Поиск аниме")
async def search_button(message: types.Message):
    """Обработка кнопки поиска"""
    keyboard = get_search_keyboard()
    await message.answer(
        "🔍 <b>Поиск аниме</b>\n\n"
        "Напишите название аниме:\n"
        "• На русском: <i>Наруто, Атака титанов</i>\n"
        "• На английском: <i>naruto, attack on titan</i>\n\n"
        "Или выберите действие ниже:",
        reply_markup=keyboard,
        parse_mode="HTML"
    )

@dp.message(F.text == "🎲 Случайное")
async def random_button(message: types.Message):
    """Кнопка случайного аниме"""
    await cmd_random(message)

@dp.message(F.text == "📋 Мой список")
async def mylist_button(message: types.Message):
    """Кнопка моего списка"""
    await cmd_mylist(message)

@dp.message(F.text == "📊 Топ недели")
async def top_button(message: types.Message):
    """Кнопка топа недели"""
    await message.answer("📊 <b>Загружаю топ недели...</b>", parse_mode="HTML")
    
    try:
        async with JikanClient() as client:
            # Ищем популярные аниме
            results = await client.search_anime("", limit=10)
            
            if results:
                response = "🏆 <b>Топ недели по популярности:</b>\n\n"
                
                for i, anime in enumerate(results[:5], 1):
                    title = anime.get('title', 'Без названия')
                    score = anime.get('score', '?')
                    members = anime.get('members', 0)
                    
                    # Форматируем количество просмотров
                    if members > 1000000:
                        members_str = f"{members/1000000:.1f}M"
                    elif members > 1000:
                        members_str = f"{members/1000:.0f}K"
                    else:
                        members_str = str(members)
                    
                    response += f"{i}. <b>{title}</b>\n"
                    response += f"   ⭐ {score}/10 | 👥 {members_str}\n"
                    response += f"   🆔 ID: {anime.get('mal_id')}\n\n"
                
                await message.answer(response, parse_mode="HTML")
            else:
                await message.answer("😔 Не удалось загрузить топ.")
                
    except Exception as e:
        logging.error(f"Ошибка в топе: {e}")
        await message.answer("⚠️ Произошла ошибка при загрузке топа.")

@dp.message(F.text == "📺 Онгоинги")
async def ongoing_button(message: types.Message):
    """Кнопка онгоингов (выходящих сейчас)"""
    await message.answer(
        "📺 <b>Сейчас в эфире:</b>\n\n"
        "⏳ <i>Функция в разработке...</i>\n\n"
        "Скоро здесь будут аниме, которые выходят прямо сейчас!",
        parse_mode="HTML"
    )

@dp.message(F.text == "⚙️ Настройки")
async def settings_button(message: types.Message):
    """Кнопка настроек"""
    user_id = message.from_user.id
    user_data = storage.get_user_data(user_id)
    settings = user_data.get("settings", {})
    
    # Получаем текущие значения настроек
    notifications = "✅ Вкл" if settings.get("notifications", True) else "❌ Выкл"
    language = "🇷🇺 Русский"
    theme = "🌙 Тёмная"
    auto_translate = "✅ Вкл" if settings.get("auto_translate", True) else "❌ Выкл"
    
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"🔔 Уведомления: {notifications}",
                    callback_data="toggle_notifications"
                )
            ],
            [
                InlineKeyboardButton(text=f"🌐 Язык: {language}", callback_data="change_language"),
                InlineKeyboardButton(text=f"🎨 Тема: {theme}", callback_data="change_theme")
            ],
            [
                InlineKeyboardButton(
                    text=f"🔤 Автоперевод: {auto_translate}",
                    callback_data="toggle_translate"
                )
            ],
            [
                InlineKeyboardButton(text="📊 Статистика", callback_data="user_stats"),
                InlineKeyboardButton(text="🗑️ Очистить список", callback_data="clear_list_confirm")
            ],
            [
                InlineKeyboardButton(text="💾 Экспорт данных", callback_data="export_data"),
                InlineKeyboardButton(text="❌ Закрыть", callback_data="close_settings")
            ]
        ]
    )
    
    stats = user_data.get("stats", {})
    
    await message.answer(
        f"⚙️ <b>Настройки пользователя</b>\n\n"
        f"🆔 ID: <code>{user_id}</code>\n"
        f"📅 Зарегистрирован: {user_data.get('created_at', 'Неизвестно')[:10]}\n"
        f"📊 Аниме в списке: {stats.get('total_anime', 0)}\n\n"
        f"👇 Выберите опцию для изменения:",
        reply_markup=keyboard,
        parse_mode="HTML"
    )

@dp.message(F.text == "❌ Скрыть меню")
async def hide_menu_button(message: types.Message):
    """Кнопка скрытия меню"""
    await cmd_hide(message)

@dp.message(F.text == "🔙 Назад в меню")
async def back_to_menu_button(message: types.Message):
    """Кнопка возврата в меню"""
    await cmd_menu(message)

@dp.message(F.text == "🔎 Новый поиск")
async def new_search_button(message: types.Message):
    """Кнопка нового поиска"""
    await search_button(message)

@dp.message(F.text == "🎬 Популярное")
async def popular_button(message: types.Message):
    """Кнопка популярного"""
    await top_button(message)

@dp.message(F.text == "❓ Как искать?")
async def how_to_search_button(message: types.Message):
    """Кнопка помощи по поиску"""
    await message.answer(
        "❓ <b>Как правильно искать аниме:</b>\n\n"
        "1. <b>На русском:</b> (бот переведёт автоматически)\n"
        "   • Наруто\n"
        "   • Атака титанов\n"
        "   • Ван Пис\n\n"
        "2. <b>На английском:</b> (лучший вариант)\n"
        "   • naruto\n"
        "   • attack on titan\n"
        "   • one piece\n\n"
        "3. <b>На японском:</b>\n"
        "   • shingeki no kyojin\n"
        "   • kimetsu no yaiba\n"
        "   • boku no hero academia\n\n"
        "4. <b>По ID:</b>\n"
        "   • /anime 20\n"
        "   • /anime 16498",
        parse_mode="HTML"
    )

# ========== КОМАНДЫ ПОИСКА ==========

@dp.message(Command("search"))
async def cmd_search(message: types.Message):
    """Команда /search - поиск аниме"""
    try:
        # Получаем запрос из сообщения
        text = message.text.split(maxsplit=1)
        if len(text) < 2:
            await message.answer("❌ Напишите: <b>/search [название аниме]</b>\nПример: /search Наруто", parse_mode="HTML")
            return
        
        query = text[1]
        original_query = query
        
        # Словарь перевода русских названий на английские
        russian_to_english = {
            "наруто": "naruto",
            "атака титанов": "attack on titan",
            "атака на титанов": "attack on titan",
            "штурм титанов": "attack on titan",
            "шингеки но кёдзин": "attack on titan",
            "ван пис": "one piece",
            "ванпис": "one piece",
            "уан пис": "one piece",
            "блич": "bleach",
            "блич": "bleach",
            "демон-убийца": "demon slayer",
            "токийский гуль": "tokyo ghoul",
            "торadora": "toradora",
            "тородора": "toradora",
            "фуллметал алхимик": "fullmetal alchemist",
            "фуллметал": "fullmetal alchemist",
            "хвост феи": "fairy tail",
            "фейри тейл": "fairy tail",
            "сайлормун": "sailor moon",
            "прекрасная воительница": "sailor moon",
            "клинок рассекающий демонов": "demon slayer",
            "кими но нава": "your name",
            "твоё имя": "your name",
            "твое имя": "your name",
            "могила светлячков": "grave of the fireflies",
            "аниме": "",  # Пустой запрос для случайного
            "случайное": "",  # Пустой запрос для случайного
        }
        
        # Приводим к нижнему регистру для поиска в словаре
        query_lower = query.lower().strip()
        
        # Проверяем, есть ли русское название в словаре
        english_query = russian_to_english.get(query_lower, query)
        
        await message.answer(f"🔍 Ищу аниме: <b>{original_query}</b>...", parse_mode="HTML")
        
        # Ищем через API
        async with JikanClient() as client:
            # Сначала ищем как есть (может быть английское название)
            results = await client.search_anime(query, limit=5)
            
            # Если не нашли и запрос был на русском, пробуем переведённый вариант
            if not results and english_query != query:
                await message.answer(f"🔄 Ищу на английском: <b>{english_query}</b>...")
                results = await client.search_anime(english_query, limit=5)
            
            # Если всё равно не нашли, попробуем пустой запрос для популярного
            if not results and query_lower in ["аниме", "случайное", ""]:
                await message.answer("🎲 Показываю популярные аниме...")
                results = await client.search_anime("", limit=5)
            
            if not results:
                await message.answer(
                    "😔 Ничего не найдено.\n\n"
                    "💡 <b>Подсказки:</b>\n"
                    "• Попробуйте английское название\n"
                    "• Или японское название\n"
                    "• Примеры:\n"
                    "  - <code>/search naruto</code>\n"
                    "  - <code>/search attack on titan</code>\n"
                    "  - <code>/search one piece</code>\n\n"
                    "📌 Популярные аниме:\n"
                    "• Наруто (naruto)\n"
                    "• Атака титанов (attack on titan)\n"
                    "• Ван Пис (one piece)\n"
                    "• Блич (bleach)",
                    parse_mode="HTML"
                )
                return
            
            # Формируем ответ с inline-кнопками
            response = "📺 <b>Найдено аниме:</b>\n\n"
            
            for i, anime in enumerate(results, 1):
                title = anime.get('title', 'Без названия')
                title_eng = anime.get('title_english', '')
                episodes = anime.get('episodes', '?')
                score = anime.get('score', '?')
                year = anime.get('year', '?')
                anime_id = anime.get('mal_id')
                
                response += f"{i}. <b>{title}</b>"
                if title_eng and title_eng != title:
                    response += f" ({title_eng})"
                
                response += f"\n   ⭐ {score}/10 | 📊 {episodes} эп. | 📅 {year}\n"
                response += f"   🆔 ID: {anime_id}\n\n"
            
            # Создаём inline-кнопки для первых результатов
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text="1️⃣ Подробнее", callback_data=f"info_{results[0]['mal_id']}"),
                        InlineKeyboardButton(text="✅ Добавить", callback_data=f"add_{results[0]['mal_id']}")
                    ]
                ]
            )
            
            if len(results) > 1:
                keyboard.inline_keyboard.append([
                    InlineKeyboardButton(text="2️⃣ Подробнее", callback_data=f"info_{results[1]['mal_id']}"),
                    InlineKeyboardButton(text="✅ Добавить", callback_data=f"add_{results[1]['mal_id']}")
                ])
            
            if len(results) > 2:
                keyboard.inline_keyboard.append([
                    InlineKeyboardButton(text="3️⃣ Подробнее", callback_data=f"info_{results[2]['mal_id']}"),
                    InlineKeyboardButton(text="✅ Добавить", callback_data=f"add_{results[2]['mal_id']}")
                ])
            
            keyboard.inline_keyboard.append([
                InlineKeyboardButton(text="🔍 Новый поиск", switch_inline_query_current_chat=""),
                InlineKeyboardButton(text="🎲 Случайное", callback_data="random")
            ])
            
            await message.answer(response, reply_markup=keyboard, parse_mode="HTML")
            
    except Exception as e:
        logging.error(f"Ошибка в /search: {e}")
        await message.answer("⚠️ Произошла ошибка при поиске. Попробуйте позже.")

@dp.message(Command("random"))
async def cmd_random(message: types.Message):
    """Команда /random - случайное аниме"""
    try:
        await message.answer("🎲 Ищу случайное аниме...")
        
        async with JikanClient() as client:
            anime = await client.get_random_anime()
            
            if not anime:
                await message.answer("😔 Не удалось получить случайное аниме. Попробуйте снова.")
                return
            
            # Формируем ответ
            title = anime.get('title', 'Без названия')
            title_eng = anime.get('title_english', '')
            score = anime.get('score', '?')
            episodes = anime.get('episodes', '?')
            anime_id = anime.get('mal_id', '?')
            
            response = f"🎲 <b>Случайное аниме:</b>\n\n"
            response += f"🎬 <b>{title}</b>\n"
            if title_eng:
                response += f"<i>{title_eng}</i>\n"
            
            response += f"\n⭐ <b>Рейтинг:</b> {score}/10\n"
            response += f"📊 <b>Эпизодов:</b> {episodes}\n"
            response += f"🆔 <b>ID:</b> {anime_id}\n\n"
            
            # Обрезаем описание
            synopsis = anime.get('synopsis', '')
            if synopsis:
                if len(synopsis) > 300:
                    synopsis = synopsis[:300] + "..."
                response += f"📝 {synopsis}\n\n"
            
            # Кнопки для действий
            keyboard = get_anime_actions_keyboard(anime_id)
            
            # Пытаемся отправить с картинкой
            image_url = anime.get('images', {}).get('jpg', {}).get('image_url')
            if image_url:
                try:
                    await message.answer_photo(image_url, caption=response, reply_markup=keyboard, parse_mode="HTML")
                    return
                except:
                    pass
            
            await message.answer(response, reply_markup=keyboard, parse_mode="HTML")
            
    except Exception as e:
        logging.error(f"Ошибка в /random: {e}")
        await message.answer("⚠️ Произошла ошибка. Попробуйте позже.")

# ========== КОМАНДЫ ДЛЯ СПИСКА ==========

@dp.message(Command("add"))
async def cmd_add(message: types.Message):
    """Команда /add - добавить аниме в список"""
    try:
        text = message.text.split()
        if len(text) < 2:
            await message.answer("❌ Напишите: <b>/add [id аниме]</b>\nПример: /add 20", parse_mode="HTML")
            return
        
        anime_id = int(text[1])
        
        # Получаем информацию об аниме
        async with JikanClient() as client:
            anime = await client.get_anime_by_id(anime_id)
            
            if anime:
                # Сохраняем в базу
                success = storage.add_anime_to_list(
                    user_id=message.from_user.id,
                    anime_data=anime,
                    status="planned"
                )
                
                title = anime.get('title', f'Аниме ID {anime_id}')
                
                if success:
                    # Кнопки для быстрых действий
                    keyboard = InlineKeyboardMarkup(
                        inline_keyboard=[
                            [
                                InlineKeyboardButton(text="👁️ Изменить на 'Смотрю'", callback_data=f"status_{anime_id}_watching"),
                                InlineKeyboardButton(text="✅ Изменить на 'Просмотрено'", callback_data=f"status_{anime_id}_completed")
                            ],
                            [
                                InlineKeyboardButton(text="📋 Посмотреть список", callback_data="view_list"),
                                InlineKeyboardButton(text="📖 Подробнее об аниме", callback_data=f"info_{anime_id}")
                            ]
                        ]
                    )
                    
                    await message.answer(
                        f"✅ <b>{title}</b> добавлено в ваш список!\n\n"
                        f"📝 Статус: 📥 <b>Запланировано</b>\n"
                        f"🆔 ID: {anime_id}\n\n"
                        f"Вы можете изменить статус с помощью кнопок ниже:",
                        reply_markup=keyboard,
                        parse_mode="HTML"
                    )
                else:
                    await message.answer(f"❌ <b>{title}</b> уже есть в вашем списке!", parse_mode="HTML")
            else:
                await message.answer(f"❌ Аниме с ID {anime_id} не найдено.")
        
    except ValueError:
        await message.answer("❌ ID должен быть числом. Пример: /add 20")
    except Exception as e:
        logging.error(f"Ошибка в /add: {e}")
        await message.answer("⚠️ Произошла ошибка.")

@dp.callback_query(F.data.startswith("rate_"))
async def rate_callback(callback: types.CallbackQuery):
    """Оценить аниме"""
    try:
        anime_id = int(callback.data.split("_")[1])
        
        # Получаем информацию об аниме
        async with JikanClient() as client:
            anime = await client.get_anime_by_id(anime_id)
            
            if anime:
                title = anime.get('title', f'Аниме ID {anime_id}')
                
                # Создаём inline-кнопки для оценки
                keyboard = InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton(text="1 ⭐", callback_data=f"set_rating_{anime_id}_1"),
                            InlineKeyboardButton(text="2 ⭐", callback_data=f"set_rating_{anime_id}_2"),
                            InlineKeyboardButton(text="3 ⭐", callback_data=f"set_rating_{anime_id}_3")
                        ],
                        [
                            InlineKeyboardButton(text="4 ⭐", callback_data=f"set_rating_{anime_id}_4"),
                            InlineKeyboardButton(text="5 ⭐", callback_data=f"set_rating_{anime_id}_5"),
                            InlineKeyboardButton(text="6 ⭐", callback_data=f"set_rating_{anime_id}_6")
                        ],
                        [
                            InlineKeyboardButton(text="7 ⭐", callback_data=f"set_rating_{anime_id}_7"),
                            InlineKeyboardButton(text="8 ⭐", callback_data=f"set_rating_{anime_id}_8"),
                            InlineKeyboardButton(text="9 ⭐", callback_data=f"set_rating_{anime_id}_9")
                        ],
                        [
                            InlineKeyboardButton(text="10 ⭐", callback_data=f"set_rating_{anime_id}_10")
                        ],
                        [
                            InlineKeyboardButton(text="🔙 Назад", callback_data=f"info_{anime_id}")
                        ]
                    ]
                )
                
                await callback.message.answer(
                    f"⭐ <b>Оценить: {title}</b>\n\n"
                    f"Выберите вашу оценку (от 1 до 10):",
                    reply_markup=keyboard,
                    parse_mode="HTML"
                )
                
            else:
                await callback.message.answer("❌ Аниме не найдено.")
                
        await callback.answer()
        
    except Exception as e:
        logging.error(f"Ошибка в оценке: {e}")
        await callback.answer("⚠️ Ошибка при оценке")

@dp.callback_query(F.data.startswith("set_rating_"))
async def set_rating_callback(callback: types.CallbackQuery):
    """Установить оценку аниме"""
    try:
        # Формат: set_rating_20_8 (anime_id_rating)
        parts = callback.data.split("_")
        anime_id = int(parts[2])
        rating = int(parts[3])
        
        # Обновляем оценку в хранилище
        user_id = callback.from_user.id
        
        # Проверяем, есть ли аниме в списке пользователя
        anime_list = storage.get_user_anime_list(user_id)
        anime_in_list = any(anime["anime_id"] == anime_id for anime in anime_list)
        
        if anime_in_list:
            # Обновляем оценку в списке
            storage.update_anime_progress(
                user_id=user_id,
                anime_id=anime_id,
                watched_episodes=None,  # Не меняем прогресс
                user_rating=rating,
                notes=None
            )
            
            # Получаем название аниме для ответа
            async with JikanClient() as client:
                anime = await client.get_anime_by_id(anime_id)
                title = anime.get('title', f'Аниме ID {anime_id}') if anime else f'Аниме ID {anime_id}'
            
            await callback.answer(f"✅ Оценка {rating}/10 сохранена!")
            
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text="📋 Посмотреть список", callback_data="view_list"),
                        InlineKeyboardButton(text="📖 К аниме", callback_data=f"info_{anime_id}")
                    ]
                ]
            )
            
            await callback.message.answer(
                f"⭐ <b>Оценка сохранена!</b>\n\n"
                f"🎬 Аниме: {title}\n"
                f"⭐ Ваша оценка: <b>{rating}/10</b>\n\n"
                f"Спасибо за оценку! 👍",
                reply_markup=keyboard,
                parse_mode="HTML"
            )
            
        else:
            await callback.answer("❌ Сначала добавьте аниме в список!")
            
    except Exception as e:
        logging.error(f"Ошибка установки оценки: {e}")
        await callback.answer("⚠️ Ошибка при сохранении оценки")

@dp.callback_query(F.data.startswith("remove_"))
async def remove_callback(callback: types.CallbackQuery):
    """Удалить аниме из списка"""
    try:
        anime_id = int(callback.data.split("_")[1])
        
        # Получаем информацию об аниме
        async with JikanClient() as client:
            anime = await client.get_anime_by_id(anime_id)
            
            if anime:
                title = anime.get('title', f'Аниме ID {anime_id}')
                
                # Клавиатура подтверждения
                keyboard = InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton(
                                text="✅ Да, удалить", 
                                callback_data=f"confirm_remove_{anime_id}"
                            ),
                            InlineKeyboardButton(
                                text="❌ Нет, отмена", 
                                callback_data=f"info_{anime_id}"
                            )
                        ]
                    ]
                )
                
                await callback.message.answer(
                    f"🗑️ <b>Удаление из списка</b>\n\n"
                    f"🎬 Аниме: {title}\n"
                    f"🆔 ID: {anime_id}\n\n"
                    f"⚠️ <b>Вы уверены, что хотите удалить это аниме из вашего списка?</b>\n"
                    f"Это действие нельзя отменить!",
                    reply_markup=keyboard,
                    parse_mode="HTML"
                )
                
            else:
                await callback.message.answer("❌ Аниме не найдено.")
                
        await callback.answer()
        
    except Exception as e:
        logging.error(f"Ошибка удаления: {e}")
        await callback.answer("⚠️ Ошибка при удалении")

@dp.callback_query(F.data.startswith("confirm_remove_"))
async def confirm_remove_callback(callback: types.CallbackQuery):
    """Подтверждение удаления аниме"""
    try:
        anime_id = int(callback.data.split("_")[2])
        user_id = callback.from_user.id
        
        # Удаляем аниме из списка
        success = storage.delete_anime_from_list(user_id, anime_id)
        
        if success:
            # Получаем название для ответа
            async with JikanClient() as client:
                anime = await client.get_anime_by_id(anime_id)
                title = anime.get('title', f'Аниме ID {anime_id}') if anime else f'Аниме ID {anime_id}'
            
            await callback.answer("✅ Аниме удалено из списка!")
            
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text="📋 Мой список", callback_data="view_list"),
                        InlineKeyboardButton(text="🔍 Новое аниме", callback_data="search_anime")
                    ]
                ]
            )
            
            await callback.message.answer(
                f"🗑️ <b>Аниме удалено!</b>\n\n"
                f"🎬 {title}\n"
                f"✅ Успешно удалено из вашего списка.\n\n"
                f"📋 В списке осталось аниме: {storage.get_user_data(user_id).get('stats', {}).get('total_anime', 0)}",
                reply_markup=keyboard,
                parse_mode="HTML"
            )
        else:
            await callback.answer("❌ Аниме не найдено в вашем списке!")
            
    except Exception as e:
        logging.error(f"Ошибка подтверждения удаления: {e}")
        await callback.answer("⚠️ Ошибка при удалении")

@dp.callback_query(F.data.startswith("similar_"))
async def similar_callback(callback: types.CallbackQuery):
    """Показать похожие аниме"""
    try:
        anime_id = int(callback.data.split("_")[1])
        
        await callback.answer("🔍 Ищу похожие аниме...")
        
        # Получаем информацию об аниме
        async with JikanClient() as client:
            anime = await client.get_anime_by_id(anime_id)
            
            if anime:
                title = anime.get('title', f'Аниме ID {anime_id}')
                
                # Получаем жанры текущего аниме
                genres = [g['name'] for g in anime.get('genres', [])]
                
                if genres:
                    # Ищем аниме с похожими жанрами (берем первый жанр для поиска)
                    search_genre = genres[0]
                    similar_results = await client.search_anime(search_genre, limit=5)
                    
                    if similar_results:
                        # Фильтруем, чтобы не показывать текущее аниме
                        similar_results = [a for a in similar_results if a.get('mal_id') != anime_id]
                        
                        if similar_results:
                            response = f"🔍 <b>Похожие на: {title}</b>\n\n"
                            response += f"🎭 По жанру: <i>{search_genre}</i>\n\n"
                            
                            for i, similar in enumerate(similar_results[:4], 1):
                                similar_title = similar.get('title', 'Без названия')
                                similar_score = similar.get('score', '?')
                                similar_id = similar.get('mal_id')
                                
                                response += f"{i}. <b>{similar_title}</b>\n"
                                response += f"   ⭐ {similar_score}/10 | 🆔 ID: {similar_id}\n\n"
                            
                            # Кнопки для похожих аниме
                            keyboard_rows = []
                            
                            # Кнопки для первых 3 похожих аниме
                            for i, similar in enumerate(similar_results[:3], 1):
                                similar_id = similar.get('mal_id')
                                keyboard_rows.append([
                                    InlineKeyboardButton(
                                        text=f"{i}️⃣ Подробнее", 
                                        callback_data=f"info_{similar_id}"
                                    ),
                                    InlineKeyboardButton(
                                        text=f"{i}️⃣ Добавить", 
                                        callback_data=f"add_{similar_id}"
                                    )
                                ])
                            
                            keyboard_rows.append([
                                InlineKeyboardButton(
                                    text="🔙 К исходному аниме", 
                                    callback_data=f"info_{anime_id}"
                                ),
                                InlineKeyboardButton(
                                    text="🔍 Новый поиск", 
                                    switch_inline_query_current_chat=""
                                )
                            ])
                            
                            keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_rows)
                            
                            await callback.message.answer(
                                response,
                                reply_markup=keyboard,
                                parse_mode="HTML"
                            )
                            return
                
                # Если не нашли похожих или нет жанров
                keyboard = InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton(
                                text="🎲 Случайное аниме", 
                                callback_data="random"
                            ),
                            InlineKeyboardButton(
                                text="🔍 Поиск по жанру", 
                                callback_data=f"genre_search_{anime_id}"
                            )
                        ],
                        [
                            InlineKeyboardButton(
                                text="🔙 Назад", 
                                callback_data=f"info_{anime_id}"
                            )
                        ]
                    ]
                )
                
                genre_text = f"по жанрам: {', '.join(genres)}" if genres else ""
                
                await callback.message.answer(
                    f"🔍 <b>Похожие на: {title}</b>\n\n"
                    f"К сожалению, не удалось найти похожие аниме {genre_text}.\n\n"
                    f"Попробуйте:\n"
                    f"• 🎲 Случайное аниме\n"
                    f"• 🔍 Поиск по жанрам",
                    reply_markup=keyboard,
                    parse_mode="HTML"
                )
                
            else:
                await callback.message.answer("❌ Аниме не найдено.")
                
    except Exception as e:
        logging.error(f"Ошибка в похожих аниме: {e}")
        
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🔙 Назад", 
                        callback_data=f"info_{anime_id}"
                    )
                ]
            ]
        )
        
        await callback.message.answer(
            "⚠️ <b>Произошла ошибка при поиске похожих аниме</b>\n\n"
            "Попробуйте позже или используйте поиск вручную.",
            reply_markup=keyboard,
            parse_mode="HTML"
        )

@dp.callback_query(F.data.startswith("genre_search_"))
async def genre_search_callback(callback: types.CallbackQuery):
    """Поиск по жанру"""
    try:
        anime_id = int(callback.data.split("_")[2])
        
        # Получаем жанры аниме
        async with JikanClient() as client:
            anime = await client.get_anime_by_id(anime_id)
            
            if anime and anime.get('genres'):
                genres = [g['name'] for g in anime.get('genres', [])]
                
                # Создаём кнопки для каждого жанра
                keyboard_rows = []
                row = []
                
                for i, genre in enumerate(genres[:6], 1):  # Максимум 6 жанров
                    row.append(InlineKeyboardButton(
                        text=genre,
                        callback_data=f"search_genre_{genre}"
                    ))
                    
                    if i % 2 == 0 or i == len(genres[:6]):
                        keyboard_rows.append(row)
                        row = []
                
                keyboard_rows.append([
                    InlineKeyboardButton(
                        text="🔙 Назад", 
                        callback_data=f"similar_{anime_id}"
                    )
                ])
                
                keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_rows)
                
                await callback.message.answer(
                    f"🎭 <b>Поиск по жанрам</b>\n\n"
                    f"Выберите жанр для поиска похожих аниме:",
                    reply_markup=keyboard,
                    parse_mode="HTML"
                )
                
            else:
                await callback.message.answer("❌ Не удалось получить жанры аниме.")
                
        await callback.answer()
        
    except Exception as e:
        logging.error(f"Ошибка поиска по жанру: {e}")
        await callback.answer("⚠️ Ошибка при поиске по жанру")

@dp.callback_query(F.data.startswith("search_genre_"))
async def search_by_genre_callback(callback: types.CallbackQuery):
    """Поиск аниме по выбранному жанру"""
    try:
        genre = callback.data.split("_", 2)[2]  # Получаем название жанра
        
        await callback.answer(f"🔍 Ищу аниме в жанре {genre}...")
        
        async with JikanClient() as client:
            results = await client.search_anime(genre, limit=8)
            
            if results:
                response = f"🎭 <b>Аниме в жанре: {genre}</b>\n\n"
                
                for i, anime in enumerate(results[:6], 1):
                    title = anime.get('title', 'Без названия')
                    score = anime.get('score', '?')
                    anime_id = anime.get('mal_id')
                    
                    response += f"{i}. <b>{title}</b>\n"
                    response += f"   ⭐ {score}/10 | 🆔 ID: {anime_id}\n\n"
                
                # Кнопки для результатов
                keyboard_rows = []
                
                # Кнопки для первых 3 результатов
                for i, anime in enumerate(results[:3], 1):
                    anime_id = anime.get('mal_id')
                    keyboard_rows.append([
                        InlineKeyboardButton(
                            text=f"{i}️⃣ Подробнее", 
                            callback_data=f"info_{anime_id}"
                        ),
                        InlineKeyboardButton(
                            text=f"{i}️⃣ Добавить", 
                            callback_data=f"add_{anime_id}"
                        )
                    ])
                
                keyboard_rows.append([
                    InlineKeyboardButton(
                        text="🔍 Ещё жанры", 
                        callback_data="show_genres"
                    ),
                    InlineKeyboardButton(
                        text="🎲 Случайное", 
                        callback_data="random"
                    )
                ])
                
                keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_rows)
                
                await callback.message.answer(
                    response,
                    reply_markup=keyboard,
                    parse_mode="HTML"
                )
            else:
                await callback.message.answer(f"❌ Не найдено аниме в жанре {genre}.")
                
    except Exception as e:
        logging.error(f"Ошибка поиска по жанру: {e}")
        await callback.message.answer("⚠️ Произошла ошибка при поиске.")

@dp.callback_query(F.data.startswith("trailer_"))
async def trailer_callback(callback: types.CallbackQuery):
    """Показать трейлер аниме - простая версия"""
    try:
        anime_id = int(callback.data.split("_")[1])
        
        await callback.answer("🎥 Ищу трейлер...")
        
        # Получаем информацию об аниме
        async with JikanClient() as client:
            anime = await client.get_anime_by_id(anime_id)
            
            if not anime:
                await callback.message.answer("❌ Аниме не найдено.")
                return
            
            title = anime.get('title', f'Аниме ID {anime_id}')
            
            # Проверяем, есть ли трейлер в данных API
            trailer_data = anime.get('trailer', {})
            youtube_id = trailer_data.get('youtube_id')
            
            if youtube_id:
                # Если есть YouTube ID
                trailer_url = f"https://www.youtube.com/watch?v={youtube_id}"
                
                keyboard = InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton(
                                text="📺 Смотреть на YouTube", 
                                url=trailer_url
                            )
                        ],
                        [
                            InlineKeyboardButton(
                                text="🔙 Назад к аниме", 
                                callback_data=f"info_{anime_id}"
                            )
                        ]
                    ]
                )
                
                await callback.message.answer(
                    f"🎬 <b>Трейлер: {title}</b>\n\n"
                    f"Нажмите кнопку для просмотра трейлера:",
                    reply_markup=keyboard,
                    parse_mode="HTML"
                )
                
            else:
                # Если трейлера нет, предлагаем поискать
                search_query = f"{title} official trailer"
                youtube_search = f"https://www.youtube.com/results?search_query={search_query.replace(' ', '+')}"
                
                keyboard = InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton(
                                text="🔍 Поиск на YouTube", 
                                url=youtube_search
                            )
                        ],
                        [
                            InlineKeyboardButton(
                                text="🔙 Назад к аниме", 
                                callback_data=f"info_{anime_id}"
                            )
                        ]
                    ]
                )
                
                await callback.message.answer(
                    f"🎬 <b>{title}</b>\n\n"
                    f"⚠️ Прямую ссылку на трейлер не удалось найти.\n"
                    f"Но вы можете поискать на YouTube:",
                    reply_markup=keyboard,
                    parse_mode="HTML"
                )
                
    except Exception as e:
        logging.error(f"Ошибка в трейлере: {e}")
        await callback.message.answer("⚠️ Произошла ошибка при поиске трейлера.")@dp.message(Command("mylist"))
async def cmd_mylist(message: types.Message):
    """Команда /mylist - показать мой список"""
    try:
        user_id = message.from_user.id
        anime_list = storage.get_user_anime_list(user_id)
        user_data = storage.get_user_data(user_id)
        stats = user_data.get("stats", {})
        
        if not anime_list:
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="🔍 Найти аниме", callback_data="search_anime")],
                    [InlineKeyboardButton(text="🎲 Случайное аниме", callback_data="random_anime")]
                ]
            )
            
            await message.answer(
                "📋 <b>Ваш список пуст</b>\n\n"
                "Добавьте аниме с помощью:\n"
                "• Команды <code>/add [id]</code>\n"
                "• Кнопки '✅ Добавить' под аниме\n"
                "• Поиска аниме",
                reply_markup=keyboard,
                parse_mode="HTML"
            )
            return
        
        # Статистика
        response = f"📋 <b>Мой список аниме</b>\n\n"
        response += f"📊 <b>Статистика:</b>\n"
        response += f"• Всего: {stats.get('total_anime', 0)}\n"
        response += f"• 📥 Запланировано: {stats.get('planned', 0)}\n"
        response += f"• 👁️ Смотрю: {stats.get('watching', 0)}\n"
        response += f"• ✅ Просмотрено: {stats.get('completed', 0)}\n"
        response += f"• ❌ Брошено: {stats.get('dropped', 0)}\n\n"
        
        # Группируем по статусам
        status_groups = {
            "watching": [],
            "planned": [],
            "completed": [],
            "dropped": []
        }
        
        for anime in anime_list:
            status = anime.get("status", "planned")
            if status in status_groups:
                status_groups[status].append(anime)
        
        # Показываем по группам
        status_icons = {
            "watching": "👁️",
            "planned": "📥",
            "completed": "✅",
            "dropped": "❌"
        }
        
        status_names = {
            "watching": "Смотрю",
            "planned": "Запланировано",
            "completed": "Просмотрено",
            "dropped": "Брошено"
        }
        
        for status, icon in status_icons.items():
            if status_groups[status]:
                response += f"{icon} <b>{status_names[status]}:</b>\n"
                for anime in status_groups[status][:5]:  # Показываем максимум 5 на статус
                    title = anime.get("title", f"Аниме ID {anime.get('anime_id')}")
                    episodes = anime.get("episodes", "?")
                    watched = anime.get("watched_episodes", 0)
                    user_rating = anime.get("user_rating", 0)
                    
                    response += f"  • <b>{title}</b> (ID: {anime.get('anime_id')})\n"
                    
                    if status == "watching" and watched > 0:
                        response += f"    📊 Прогресс: {watched}/{episodes} эп.\n"
                    
                    if user_rating > 0:
                        response += f"    ⭐ Ваша оценка: {user_rating}/10\n"
                
                if len(status_groups[status]) > 5:
                    response += f"  ... и ещё {len(status_groups[status]) - 5}\n"
                
                response += "\n"
        
        # Кнопки для управления
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="🔄 Обновить список", callback_data="refresh_list"),
                    InlineKeyboardButton(text="📊 Подробная статистика", callback_data="detailed_stats")
                ],
                [
                    InlineKeyboardButton(text="🗑️ Очистить список", callback_data="clear_list_confirm"),
                    InlineKeyboardButton(text="📁 Экспорт в файл", callback_data="export_list")
                ],
                [
                    InlineKeyboardButton(text="🔍 Добавить ещё аниме", callback_data="search_anime")
                ]
            ]
        )
        
        await message.answer(response, reply_markup=keyboard, parse_mode="HTML")
        
    except Exception as e:
        logging.error(f"Ошибка в /mylist: {e}")
        await message.answer("⚠️ Произошла ошибка при загрузке списка.")

@dp.message(Command("update"))
async def cmd_update(message: types.Message):
    """Команда /update - изменить статус"""
    try:
        text = message.text.split()
        if len(text) < 3:
            await message.answer(
                "❌ Напишите: <b>/update [id] [статус]</b>\n\n"
                "Пример: <code>/update 20 completed</code>\n\n"
                "📝 <b>Доступные статусы:</b>\n"
                "• <code>planned</code> - 📥 Запланировано\n"
                "• <code>watching</code> - 👁️ Смотрю\n"
                "• <code>completed</code> - ✅ Просмотрено\n"
                "• <code>dropped</code> - ❌ Брошено",
                parse_mode="HTML"
            )
            return
        
        anime_id = int(text[1])
        new_status = text[2]
        
        # Проверяем корректность статуса
        valid_statuses = ["planned", "watching", "completed", "dropped"]
        if new_status not in valid_statuses:
            await message.answer(
                "❌ Неверный статус!\n\n"
                "📝 <b>Доступные статусы:</b>\n"
                "• <code>planned</code> - 📥 Запланировано\n"
                "• <code>watching</code> - 👁️ Смотрю\n"
                "• <code>completed</code> - ✅ Просмотрено\n"
                "• <code>dropped</code> - ❌ Брошено",
                parse_mode="HTML"
            )
            return
        
        # Обновляем статус
        success = storage.update_anime_status(
            user_id=message.from_user.id,
            anime_id=anime_id,
            new_status=new_status
        )
        
        status_names = {
            "planned": "📥 Запланировано",
            "watching": "👁️ Смотрю",
            "completed": "✅ Просмотрено",
            "dropped": "❌ Брошено"
        }
        
        if success:
            await message.answer(
                f"✅ Статус аниме ID <b>{anime_id}</b> изменён на: {status_names[new_status]}",
                parse_mode="HTML"
            )
        else:
            await message.answer(f"❌ Аниме с ID {anime_id} не найдено в вашем списке.")
            
    except ValueError:
        await message.answer("❌ ID должен быть числом. Пример: /update 20 completed")
    except Exception as e:
        logging.error(f"Ошибка в /update: {e}")
        await message.answer("⚠️ Произошла ошибка.")

@dp.message(Command("delete"))
async def cmd_delete(message: types.Message):
    """Команда /delete - удалить из списка"""
    try:
        text = message.text.split()
        if len(text) < 2:
            await message.answer("❌ Напишите: <b>/delete [id аниме]</b>\nПример: /delete 20", parse_mode="HTML")
            return
        
        anime_id = int(text[1])
        
        # Удаляем из списка
        success = storage.delete_anime_from_list(
            user_id=message.from_user.id,
            anime_id=anime_id
        )
        
        if success:
            await message.answer(f"✅ Аниме ID <b>{anime_id}</b> удалено из вашего списка.", parse_mode="HTML")
        else:
            await message.answer(f"❌ Аниме с ID {anime_id} не найдено в вашем списке.")
            
    except ValueError:
        await message.answer("❌ ID должен быть числом. Пример: /delete 20")
    except Exception as e:
        logging.error(f"Ошибка в /delete: {e}")
        await message.answer("⚠️ Произошла ошибка.")

# ========== ОБРАБОТЧИКИ CALLBACK-КНОПОК ==========

@dp.callback_query(F.data.startswith("info_"))
async def anime_info_callback(callback: types.CallbackQuery):
    """Показать информацию об аниме"""
    anime_id = int(callback.data.split("_")[1])
    
    await callback.answer("📖 Загружаем информацию...")
    
    async with JikanClient() as client:
        anime = await client.get_anime_by_id(anime_id)
        
        if anime:
            title = anime.get('title', 'Без названия')
            title_eng = anime.get('title_english', '')
            title_jp = anime.get('title_japanese', '')
            
            response = f"🎬 <b>{title}</b>\n"
            if title_eng:
                response += f"<i>{title_eng}</i>\n"
            if title_jp:
                response += f"<i>{title_jp}</i>\n"
            
            response += f"\n⭐ <b>Рейтинг:</b> {anime.get('score', '?')}/10\n"
            response += f"📊 <b>Эпизодов:</b> {anime.get('episodes', '?')}\n"
            response += f"📅 <b>Год:</b> {anime.get('year', '?')}\n"
            response += f"📺 <b>Статус:</b> {anime.get('status', 'Неизвестно')}\n"
            
            # Жанры
            genres = [g['name'] for g in anime.get('genres', [])]
            if genres:
                response += f"🎭 <b>Жанры:</b> {', '.join(genres)}\n\n"
            
            # Описание
            synopsis = anime.get('synopsis', 'Нет описания')
            if synopsis and len(synopsis) > 0:
                if len(synopsis) > 400:
                    synopsis = synopsis[:400] + "..."
                response += f"📝 <b>Описание:</b>\n{synopsis}\n\n"
            
            response += f"🔗 <b>MyAnimeList:</b> {anime.get('url', 'Нет ссылки')}\n\n"
            
            keyboard = get_anime_actions_keyboard(anime_id)
            
            # Отправляем с фото если есть
            image_url = anime.get('images', {}).get('jpg', {}).get('image_url')
            if image_url:
                try:
                    await callback.message.answer_photo(
                        image_url,
                        caption=response,
                        reply_markup=keyboard,
                        parse_mode="HTML"
                    )
                    return
                except:
                    pass
            
            await callback.message.answer(response, reply_markup=keyboard, parse_mode="HTML")
        else:
            await callback.message.answer("❌ Аниме не найдено")

@dp.callback_query(F.data.startswith("add_"))
async def add_anime_callback(callback: types.CallbackQuery):
    """Добавить аниме в список"""
    anime_id = int(callback.data.split("_")[1])
    
    # Получаем информацию об аниме
    async with JikanClient() as client:
        anime = await client.get_anime_by_id(anime_id)
        
        if anime:
            # Сохраняем в базу
            success = storage.add_anime_to_list(
                user_id=callback.from_user.id,
                anime_data=anime,
                status="planned"
            )
            
            title = anime.get('title', f'Аниме ID {anime_id}')
            
            if success:
                await callback.answer(f"✅ {title} добавлено в список!")
                
                # Показываем кнопки для быстрых действий
                keyboard = InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton(text="👁️ Изменить на 'Смотрю'", callback_data=f"status_{anime_id}_watching"),
                            InlineKeyboardButton(text="📋 Посмотреть список", callback_data="view_list")
                        ]
                    ]
                )
                
                await callback.message.answer(
                    f"✅ <b>{title}</b> добавлено в ваш список!\n"
                    f"📝 Статус: 📥 <b>Запланировано</b>",
                    reply_markup=keyboard,
                    parse_mode="HTML"
                )
            else:
                await callback.answer(f"❌ {title} уже есть в списке!")
        else:
            await callback.answer("❌ Аниме не найдено!")

@dp.callback_query(F.data == "random")
async def random_callback(callback: types.CallbackQuery):
    """Случайное аниме из callback"""
    await callback.answer("🎲 Ищем случайное аниме...")
    # Вызываем функцию случайного аниме
    await cmd_random(callback.message)

# ========== ОБРАБОТЧИКИ НАСТРОЕК ==========

@dp.callback_query(F.data == "toggle_notifications")
async def toggle_notifications(callback: types.CallbackQuery):
    """Включить/выключить уведомления"""
    user_id = callback.from_user.id
    user_data = storage.get_user_data(user_id)
    
    current = user_data["settings"].get("notifications", True)
    storage.update_user_settings(user_id, {"notifications": not current})
    
    await callback.answer(f"Уведомления {'включены' if not current else 'выключены'}!")
    # Обновляем сообщение с настройками
    await settings_button(callback.message)

@dp.callback_query(F.data == "toggle_translate")
async def toggle_translate(callback: types.CallbackQuery):
    """Включить/выключить автоперевод"""
    user_id = callback.from_user.id
    user_data = storage.get_user_data(user_id)
    
    current = user_data["settings"].get("auto_translate", True)
    storage.update_user_settings(user_id, {"auto_translate": not current})
    
    await callback.answer(f"Автоперевод {'включён' if not current else 'выключен'}!")
    await settings_button(callback.message)

@dp.callback_query(F.data == "change_language")
async def change_language(callback: types.CallbackQuery):
    """Сменить язык"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="set_lang_ru")],
            [InlineKeyboardButton(text="🇬🇧 English", callback_data="set_lang_en")],
            [InlineKeyboardButton(text="🇰🇿 Қазақша", callback_data="set_lang_kz")],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_settings")]
        ]
    )
    
    await callback.message.edit_text(
        "🌐 <b>Выбор языка</b>\n\n"
        "Выберите язык интерфейса:",
        reply_markup=keyboard,
        parse_mode="HTML"
    )
    await callback.answer()

@dp.callback_query(F.data.startswith("set_lang_"))
async def set_language(callback: types.CallbackQuery):
    """Установить язык"""
    lang = callback.data.split("_")[2]
    user_id = callback.from_user.id
    
    lang_names = {"ru": "Русский", "en": "English", "kz": "Қазақша"}
    storage.update_user_settings(user_id, {"language": lang})
    
    await callback.answer(f"Язык изменён на {lang_names.get(lang, lang)}!")
    await settings_button(callback.message)

@dp.callback_query(F.data == "change_theme")
async def change_theme(callback: types.CallbackQuery):
    """Сменить тему"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🌙 Тёмная", callback_data="set_theme_dark")],
            [InlineKeyboardButton(text="☀️ Светлая", callback_data="set_theme_light")],
            [InlineKeyboardButton(text="🌈 Авто", callback_data="set_theme_auto")],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_settings")]
        ]
    )
    
    await callback.message.edit_text(
        "🎨 <b>Выбор темы</b>\n\n"
        "Выберите тему интерфейса:",
        reply_markup=keyboard,
        parse_mode="HTML"
    )
    await callback.answer()

@dp.callback_query(F.data.startswith("set_theme_"))
async def set_theme(callback: types.CallbackQuery):
    """Установить тему"""
    theme = callback.data.split("_")[2]
    user_id = callback.from_user.id
    
    theme_names = {"dark": "Тёмная", "light": "Светлая", "auto": "Авто"}
    storage.update_user_settings(user_id, {"theme": theme})
    
    await callback.answer(f"Тема изменена на {theme_names.get(theme, theme)}!")
    await settings_button(callback.message)

@dp.callback_query(F.data == "user_stats")
async def user_stats(callback: types.CallbackQuery):
    """Статистика пользователя"""
    user_id = callback.from_user.id
    user_data = storage.get_user_data(user_id)
    stats = user_data.get("stats", {})
    anime_list = storage.get_user_anime_list(user_id)
    
    # Подсчитываем общее время просмотра (примерно)
    total_episodes = sum(anime.get("watched_episodes", 0) for anime in anime_list)
    estimated_hours = total_episodes * 24 / 60  # Примерно 24 минуты на эпизод
    
    response = f"📊 <b>Ваша статистика</b>\n\n"
    response += f"🎬 <b>Всего аниме:</b> {stats.get('total_anime', 0)}\n"
    response += f"⏳ <b>Просмотрено эпизодов:</b> {total_episodes}\n"
    response += f"🕐 <b>Примерное время:</b> {estimated_hours:.1f} часов\n\n"
    
    response += f"📥 <b>Запланировано:</b> {stats.get('planned', 0)}\n"
    response += f"👁️ <b>Смотрю:</b> {stats.get('watching', 0)}\n"
    response += f"✅ <b>Просмотрено:</b> {stats.get('completed', 0)}\n"
    response += f"❌ <b>Брошено:</b> {stats.get('dropped', 0)}\n\n"
    
    # Топ оценённых аниме
    rated_anime = [a for a in anime_list if a.get("user_rating", 0) > 0]
    if rated_anime:
        rated_anime.sort(key=lambda x: x.get("user_rating", 0), reverse=True)
        response += "⭐ <b>Высшие оценки:</b>\n"
        for anime in rated_anime[:3]:
            response += f"• {anime.get('title')}: {anime.get('user_rating')}/10\n"
    
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📋 Посмотреть список", callback_data="view_list")],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_settings")]
        ]
    )
    
    await callback.message.edit_text(response, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer()

@dp.callback_query(F.data.startswith("status_"))
async def change_anime_status(callback: types.CallbackQuery):
    """Изменить статус аниме"""
    try:
        # Формат: status_20_watching
        parts = callback.data.split("_")
        if len(parts) >= 3:
            anime_id = int(parts[1])
            new_status = parts[2]
            
            success = storage.update_anime_status(
                user_id=callback.from_user.id,
                anime_id=anime_id,
                new_status=new_status
            )
            
            status_names = {
                "planned": "📥 Запланировано",
                "watching": "👁️ Смотрю",
                "completed": "✅ Просмотрено",
                "dropped": "❌ Брошено"
            }
            
            if success:
                await callback.answer(f"Статус изменён на {status_names.get(new_status, new_status)}!")
            else:
                await callback.answer("❌ Аниме не найдено в вашем списке!")
    except Exception as e:
        logging.error(f"Ошибка изменения статуса: {e}")
        await callback.answer("⚠️ Ошибка при изменении статуса!")

@dp.callback_query(F.data == "view_list")
async def view_list_callback(callback: types.CallbackQuery):
    """Показать список из callback"""
    await callback.answer("Загружаем список...")
    await cmd_mylist(callback.message)

@dp.callback_query(F.data == "back_to_settings")
async def back_to_settings_callback(callback: types.CallbackQuery):
    """Вернуться к настройкам"""
    await callback.answer()
    await settings_button(callback.message)

@dp.callback_query(F.data == "close_settings")
async def close_settings_callback(callback: types.CallbackQuery):
    """Закрыть настройки"""
    await callback.message.delete()
    await callback.answer("❌ Настройки закрыты")

@dp.callback_query(F.data == "refresh_list")
async def refresh_list_callback(callback: types.CallbackQuery):
    """Обновить список"""
    await callback.answer("🔄 Обновляем список...")
    await cmd_mylist(callback.message)

@dp.callback_query(F.data == "search_anime")
async def search_anime_callback(callback: types.CallbackQuery):
    """Поиск аниме из callback"""
    await callback.answer("🔍 Переходим к поиску...")
    await search_button(callback.message)

@dp.callback_query(F.data == "random_anime")
async def random_anime_callback(callback: types.CallbackQuery):
    """Случайное аниме из callback"""
    await callback.answer("🎲 Ищем случайное аниме...")
    await cmd_random(callback.message)

@dp.callback_query(F.data == "clear_list_confirm")
async def clear_list_confirm_callback(callback: types.CallbackQuery):
    """Подтверждение очистки списка"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Да, очистить", callback_data="clear_list")],
            [InlineKeyboardButton(text="❌ Нет, отмена", callback_data="back_to_settings")]
        ]
    )
    
    await callback.message.edit_text(
        "⚠️ <b>Внимание!</b>\n\n"
        "Вы уверены, что хотите очистить весь список аниме?\n"
        "Это действие нельзя отменить!",
        reply_markup=keyboard,
        parse_mode="HTML"
    )
    await callback.answer()

# ========== ОБРАБОТЧИК НЕИЗВЕСТНЫХ СООБЩЕНИЙ ==========

@dp.message()
async def handle_unknown(message: types.Message):
    """Обработка неизвестных сообщений"""
    if message.text and not message.text.startswith('/'):
        # Если пользователь просто написал текст (не команду), считаем это поиском
        await message.answer(
            f"🔍 <b>Вы написали:</b> {message.text}\n\n"
            f"Если вы хотите найти аниме, используйте:\n"
            f"<code>/search {message.text}</code>\n\n"
            f"Или выберите действие в меню ниже:",
            reply_markup=get_main_keyboard(),
            parse_mode="HTML"
        )

# ========== ЗАПУСК БОТА ==========

async def main():
    print("=" * 50)
    print("🤖 Anime Bot запускается...")
    print("📱 Меню как в AniLibria")
    print("📊 Реальное сохранение в JSON")
    print("⚙️ Работающие настройки")
    print("🛑 Остановить: Ctrl+C")
    print("=" * 50)
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Бот остановлен") 