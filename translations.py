# translations.py
TRANSLATIONS = {
    "ru": {
        # Основные команды
        "welcome": "🎌 <b>Добро пожаловать в AniBot!</b>\n\n🏆 <i>Ваш персональный аниме-гид</i>\n\n📁 <b>Что умеет бот:</b>\n• 🔍 Поиск по базе MyAnimeList\n• 📋 Личный список просмотра\n• 🎯 Персональные рекомендации\n• 📊 Топы и новинки\n• 🔔 Уведомления о выходе\n\n👇 <b>Используйте меню ниже</b> или команды",
        "menu": "🏠 <b>Главное меню AniBot</b>\n\n<i>Выберите раздел:</i>",
        "help": "📚 <b>Доступные команды:</b>\n\n<b>Основные команды:</b>\n/start - Начало работы с меню\n/menu - Показать меню\n/hide - Скрыть меню\n/help - Эта справка\n\n<b>Поиск аниме:</b>\n/search [название] - Найти аниме\n/anime [id] - Подробности об аниме\n/random - Случайное аниме\n\n<b>Мой список:</b>\n/add [id] - Добавить в список\n/mylist - Показать мой список\n/update [id] [статус] - Изменить статус\n/delete [id] - Удалить из списка\n\n💡 <b>Как искать:</b>\n• На русском: <code>/search Наруто</code>\n• На английском: <code>/search naruto</code>\n• На японском: <code>/search shingeki no kyojin</code>\n\n📌 <b>Популярные запросы:</b>\n• Наруто (naruto)\n• Атака титанов (attack on titan)\n• Ван Пис (one piece)\n• Блич (bleach)\n• Твоё имя (your name)\n\n📱 <b>Используйте меню внизу</b> для быстрого доступа!",
        "hide": "⌨️ <b>Клавиатура скрыта</b>\n\nИспользуйте команды или:\n/menu - показать меню",
        
        # Кнопки меню
        "search_btn": "🔍 Поиск аниме",
        "random_btn": "🎲 Случайное",
        "mylist_btn": "📋 Мой список",
        "top_btn": "📊 Топ недели",
        "ongoing_btn": "📺 Онгоинги",
        "help_btn": "ℹ️ Помощь",
        "settings_btn": "⚙️ Настройки",
        "hide_btn": "❌ Скрыть меню",
        
        # Поиск
        "search_prompt": "🔍 <b>Поиск аниме</b>\n\nНапишите название аниме:\n• На русском: <i>Наруто, Атака титанов</i>\n• На английском: <i>naruto, attack on titan</i>\n\nИли выберите действие ниже:",
        "searching": "🔍 Ищу аниме: <b>{query}</b>...",
        "no_results": "😔 Ничего не найдено.\n\n💡 <b>Подсказки:</b>\n• Попробуйте английское название\n• Или японское название\n• Примеры:\n  - <code>/search naruto</code>\n  - <code>/search attack on titan</code>\n  - <code>/search one piece</code>\n\n📌 Популярные аниме:\n• Наруто (naruto)\n• Атака титанов (attack on titan)\n• Ван Пис (one piece)\n• Блич (bleach)",
        "found_anime": "📺 <b>Найдено аниме:</b>\n\n",
        
        # Список
        "my_list": "📋 <b>Мой список аниме</b>\n\n",
        "list_empty": "📋 <b>Ваш список пуст</b>\n\nДобавьте аниме с помощью:\n• Команды <code>/add [id]</code>\n• Кнопки '✅ Добавить' под аниме\n• Поиска аниме",
        "stats": "📊 <b>Статистика:</b>\n• Всего: {total}\n• 📥 Запланировано: {planned}\n• 👁️ Смотрю: {watching}\n• ✅ Просмотрено: {completed}\n• ❌ Брошено: {dropped}",
        
        # Настройки
        "settings": "⚙️ <b>Настройки пользователя</b>\n\n🆔 ID: <code>{user_id}</code>\n📅 Зарегистрирован: {created}\n📊 Аниме в списке: {anime_count}\n\n👇 Выберите опцию для изменения:",
        "notifications_on": "🔔 Уведомления: ✅ Вкл",
        "notifications_off": "🔔 Уведомления: ❌ Выкл",
        "language": "🌐 Язык: Русский",
        "theme": "🎨 Тема: Тёмная",
        "translate_on": "🔤 Автоперевод: ✅ Вкл",
        "translate_off": "🔤 Автоперевод: ❌ Выкл",
        "stats_btn": "📊 Статистика",
        "clear_list_btn": "🗑️ Очистить список",
        "export_btn": "💾 Экспорт данных",
        "close_btn": "❌ Закрыть",
        
        # Статусы
        "planned": "📥 Запланировано",
        "watching": "👁️ Смотрю",
        "completed": "✅ Просмотрено",
        "dropped": "❌ Брошено",
        
        # Ошибки
        "error": "⚠️ Произошла ошибка. Попробуйте позже.",
        "not_found": "❌ Не найдено.",
        "added": "✅ Добавлено в список!",
        "already_exists": "❌ Уже есть в списке!",
        "deleted": "🗑️ Удалено из списка!",
        "updated": "🔄 Обновлено!",
        
        # Подтверждения
        "confirm_delete": "⚠️ <b>Внимание!</b>\n\nВы уверены, что хотите удалить это аниме из вашего списка?\nЭто действие нельзя отменить!",
        "yes": "✅ Да",
        "no": "❌ Нет",
        "back": "🔙 Назад",
        
        # Оценка
        "rate": "⭐ <b>Оценить: {title}</b>\n\nВыберите вашу оценку (от 1 до 10):",
        "rating_saved": "⭐ <b>Оценка сохранена!</b>\n\n🎬 Аниме: {title}\n⭐ Ваша оценка: <b>{rating}/10</b>\n\nСпасибо за оценку! 👍",
        
        # Похожие
        "similar": "🔍 <b>Похожие на: {title}</b>\n\n",
        "by_genre": "🎭 По жанру: <i>{genre}</i>\n\n",
        
        # Трейлер
        "trailer": "🎬 <b>Трейлер: {title}</b>\n\n",
        "watch_on_youtube": "📺 Смотреть на YouTube",
        "search_on_youtube": "🔍 Поиск на YouTube",
        
        # Клавиатура поиска
        "new_search": "🔎 Новый поиск",
        "popular": "🎬 Популярное",
        "back_to_menu": "🔙 Назад в меню",
        "how_to_search": "❓ Как искать?",
    },
    
    "en": {
        # Основные команды
        "welcome": "🎌 <b>Welcome to AniBot!</b>\n\n🏆 <i>Your personal anime guide</i>\n\n📁 <b>What the bot can do:</b>\n• 🔍 Search MyAnimeList database\n• 📋 Personal watchlist\n• 🎯 Personalized recommendations\n• 📊 Tops and new releases\n• 🔔 Release notifications\n\n👇 <b>Use the menu below</b> or commands",
        "menu": "🏠 <b>Main Menu AniBot</b>\n\n<i>Select a section:</i>",
        "help": "📚 <b>Available commands:</b>\n\n<b>Basic commands:</b>\n/start - Start with menu\n/menu - Show menu\n/hide - Hide menu\n/help - This help\n\n<b>Anime search:</b>\n/search [name] - Find anime\n/anime [id] - Anime details\n/random - Random anime\n\n<b>My list:</b>\n/add [id] - Add to list\n/mylist - Show my list\n/update [id] [status] - Change status\n/delete [id] - Delete from list\n\n💡 <b>How to search:</b>\n• In Russian: <code>/search Наруто</code>\n• In English: <code>/search naruto</code>\n• In Japanese: <code>/search shingeki no kyojin</code>\n\n📌 <b>Popular queries:</b>\n• Naruto (naruto)\n• Attack on Titan (attack on titan)\n• One Piece (one piece)\n• Bleach (bleach)\n• Your Name (your name)\n\n📱 <b>Use the menu below</b> for quick access!",
        "hide": "⌨️ <b>Keyboard hidden</b>\n\nUse commands or:\n/menu - show menu",
        
        # Кнопки меню
        "search_btn": "🔍 Search anime",
        "random_btn": "🎲 Random",
        "mylist_btn": "📋 My list",
        "top_btn": "📊 Top weekly",
        "ongoing_btn": "📺 Ongoing",
        "help_btn": "ℹ️ Help",
        "settings_btn": "⚙️ Settings",
        "hide_btn": "❌ Hide menu",
        
        # Поиск
        "search_prompt": "🔍 <b>Anime search</b>\n\nWrite anime name:\n• In Russian: <i>Наруто, Атака титанов</i>\n• In English: <i>naruto, attack on titan</i>\n\nOr select action below:",
        "searching": "🔍 Searching anime: <b>{query}</b>...",
        "no_results": "😔 Nothing found.\n\n💡 <b>Tips:</b>\n• Try English name\n• Or Japanese name\n• Examples:\n  - <code>/search naruto</code>\n  - <code>/search attack on titan</code>\n  - <code>/search one piece</code>\n\n📌 Popular anime:\n• Naruto (naruto)\n• Attack on Titan (attack on titan)\n• One Piece (one piece)\n• Bleach (bleach)",
        "found_anime": "📺 <b>Found anime:</b>\n\n",
        
        # Список
        "my_list": "📋 <b>My anime list</b>\n\n",
        "list_empty": "📋 <b>Your list is empty</b>\n\nAdd anime using:\n• Command <code>/add [id]</code>\n• '✅ Add' button under anime\n• Anime search",
        "stats": "📊 <b>Statistics:</b>\n• Total: {total}\n• 📥 Planned: {planned}\n• 👁️ Watching: {watching}\n• ✅ Completed: {completed}\n• ❌ Dropped: {dropped}",
        
        # Настройки
        "settings": "⚙️ <b>User settings</b>\n\n🆔 ID: <code>{user_id}</code>\n📅 Registered: {created}\n📊 Anime in list: {anime_count}\n\n👇 Select option to change:",
        "notifications_on": "🔔 Notifications: ✅ On",
        "notifications_off": "🔔 Notifications: ❌ Off",
        "language": "🌐 Language: English",
        "theme": "🎨 Theme: Dark",
        "translate_on": "🔤 Auto-translate: ✅ On",
        "translate_off": "🔤 Auto-translate: ❌ Off",
        "stats_btn": "📊 Statistics",
        "clear_list_btn": "🗑️ Clear list",
        "export_btn": "💾 Export data",
        "close_btn": "❌ Close",
        
        # Статусы
        "planned": "📥 Planned",
        "watching": "👁️ Watching",
        "completed": "✅ Completed",
        "dropped": "❌ Dropped",
        
        # Ошибки
        "error": "⚠️ An error occurred. Try again later.",
        "not_found": "❌ Not found.",
        "added": "✅ Added to list!",
        "already_exists": "❌ Already in list!",
        "deleted": "🗑️ Deleted from list!",
        "updated": "🔄 Updated!",
        
        # Подтверждения
        "confirm_delete": "⚠️ <b>Warning!</b>\n\nAre you sure you want to delete this anime from your list?\nThis action cannot be undone!",
        "yes": "✅ Yes",
        "no": "❌ No",
        "back": "🔙 Back",
        
        # Оценка
        "rate": "⭐ <b>Rate: {title}</b>\n\nSelect your rating (1 to 10):",
        "rating_saved": "⭐ <b>Rating saved!</b>\n\n🎬 Anime: {title}\n⭐ Your rating: <b>{rating}/10</b>\n\nThank you for rating! 👍",
        
        # Похожие
        "similar": "🔍 <b>Similar to: {title}</b>\n\n",
        "by_genre": "🎭 By genre: <i>{genre}</i>\n\n",
        
        # Трейлер
        "trailer": "🎬 <b>Trailer: {title}</b>\n\n",
        "watch_on_youtube": "📺 Watch on YouTube",
        "search_on_youtube": "🔍 Search on YouTube",
        
        # Клавиатура поиска
        "new_search": "🔎 New search",
        "popular": "🎬 Popular",
        "back_to_menu": "🔙 Back to menu",
        "how_to_search": "❓ How to search?",
    },
    
    "kz": {
        # Основные команды
        "welcome": "🎌 <b>AniBot-қа қош келдіңіз!</b>\n\n🏆 <i>Сіздің жеке аниме-гидіңіз</i>\n\n📁 <b>Бот не істей алады:</b>\n• 🔍 MyAnimeList базасынан іздеу\n• 📋 Жеке көру тізімі\n• 🎯 Жекелендірілген ұсыныстар\n• 📊 Топтар және жаңа шығарылымдар\n• 🔔 Шығарылым туралы хабарландырулар\n\n👇 <b>Төмендегі мәзірді қолданыңыз</b> немесе командалар",
        "menu": "🏠 <b>AniBot басты мәзірі</b>\n\n<i>Бөлімді таңдаңыз:</i>",
        "help": "📚 <b>Қол жетімді командалар:</b>\n\n<b>Негізгі командалар:</b>\n/start - Мәзірмен жұмысты бастау\n/menu - Мәзірді көрсету\n/hide - Мәзірді жасыру\n/help - Бұл көмек\n\n<b>Аниме іздеу:</b>\n/search [атауы] - Аниме табу\n/anime [id] - Аниме туралы егжей-тегжей\n/random - Кездейсоқ аниме\n\n<b>Менің тізімім:</b>\n/add [id] - Тізімге қосу\n/mylist - Менің тізімді көрсету\n/update [id] [күй] - Күйін өзгерту\n/delete [id] - Тізімнен жою\n\n💡 <b>Қалай іздеу керек:</b>\n• Орысша: <code>/search Наруто</code>\n• Ағылшынша: <code>/search naruto</code>\n• Жапонша: <code>/search shingeki no kyojin</code>\n\n📌 <b>Танымал сұраныстар:</b>\n• Наруто (naruto)\n• Титандарға шабуыл (attack on titan)\n• Бір бөлік (one piece)\n• Блич (bleach)\n• Сенің атың (your name)\n\n📱 <b>Жылдам қол жеткізу үшін төмендегі мәзірді қолданыңыз!</b>",
        "hide": "⌨️ <b>Пернетақта жасырылды</b>\n\nКомандаларды қолданыңыз немесе:\n/menu - мәзірді көрсету",
        
        # Кнопки меню
        "search_btn": "🔍 Аниме іздеу",
        "random_btn": "🎲 Кездейсоқ",
        "mylist_btn": "📋 Менің тізім",
        "top_btn": "📊 Апталық топ",
        "ongoing_btn": "📺 Жарияланымдар",
        "help_btn": "ℹ️ Көмек",
        "settings_btn": "⚙️ Баптаулар",
        "hide_btn": "❌ Мәзірді жасыру",
        
        # Поиск
        "search_prompt": "🔍 <b>Аниме іздеу</b>\n\nАниме атауын жазыңыз:\n• Орысша: <i>Наруто, Титандарға шабуыл</i>\n• Ағылшынша: <i>naruto, attack on titan</i>\n\nНемесе төмендегі әрекетті таңдаңыз:",
        "searching": "🔍 Аниме іздеу: <b>{query}</b>...",
        "no_results": "😔 Ештеңе табылмады.\n\n💡 <b>Кеңестер:</b>\n• Ағылшынша атауын көріңіз\n• Немесе жапонша атауын\n• Мысалдар:\n  - <code>/search naruto</code>\n  - <code>/search attack on titan</code>\n  - <code>/search one piece</code>\n\n📌 Танымал анимелер:\n• Наруто (naruto)\n• Титандарға шабуыл (attack on titan)\n• Бір бөлік (one piece)\n• Блич (bleach)",
        "found_anime": "📺 <b>Табылған анимелер:</b>\n\n",
        
        # Список
        "my_list": "📋 <b>Менің аниме тізімім</b>\n\n",
        "list_empty": "📋 <b>Сіздің тізіміңіз бос</b>\n\nАниме қосу үшін:\n• <code>/add [id]</code> командасы\n• Аниме астындағы '✅ Қосу' түймесі\n• Аниме іздеу",
        "stats": "📊 <b>Статистика:</b>\n• Барлығы: {total}\n• 📥 Жоспарланған: {planned}\n• 👁️ Қарап жатқан: {watching}\n• ✅ Аяқталған: {completed}\n• ❌ Тасталған: {dropped}",
        
        # Настройки
        "settings": "⚙️ <b>Пайдаланушы баптаулары</b>\n\n🆔 ID: <code>{user_id}</code>\n📅 Тіркелген: {created}\n📊 Тізімдегі аниме: {anime_count}\n\n👇 Өзгерту үшін опцияны таңдаңыз:",
        "notifications_on": "🔔 Хабарландырулар: ✅ Қосылған",
        "notifications_off": "🔔 Хабарландырулар: ❌ Өшірілген",
        "language": "🌐 Тіл: Қазақша",
        "theme": "🎨 Тақырып: Қараңғы",
        "translate_on": "🔤 Автоаудару: ✅ Қосылған",
        "translate_off": "🔤 Автоаудару: ❌ Өшірілген",
        "stats_btn": "📊 Статистика",
        "clear_list_btn": "🗑️ Тізімді тазалау",
        "export_btn": "💾 Деректерді экспорттау",
        "close_btn": "❌ Жабу",
        
        # Статусы
        "planned": "📥 Жоспарланған",
        "watching": "👁️ Қарап жатқан",
        "completed": "✅ Аяқталған",
        "dropped": "❌ Тасталған",
        
        # Ошибки
        "error": "⚠️ Қате орын алды. Кейінірек қайталаңыз.",
        "not_found": "❌ Табылмады.",
        "added": "✅ Тізімге қосылды!",
        "already_exists": "❌ Тізімде бар!",
        "deleted": "🗑️ Тізімнен жойылды!",
        "updated": "🔄 Жаңартылды!",
        
        # Подтверждения
        "confirm_delete": "⚠️ <b>Назар!</b>\n\nБұл анимені тізіміңізден жоюға сенімдісіз бе?\nБұл әрекетті болдырмау мүмкін емес!",
        "yes": "✅ Иә",
        "no": "❌ Жоқ",
        "back": "🔙 Артқа",
        
        # Оценка
        "rate": "⭐ <b>Бағалау: {title}</b>\n\nБағаңызды таңдаңыз (1-ден 10-ға дейін):",
        "rating_saved": "⭐ <b>Баға сақталды!</b>\n\n🎬 Аниме: {title}\n⭐ Сіздің бағаңыз: <b>{rating}/10</b>\n\nБағалағаныңыз үшін рахмет! 👍",
        
        # Похожие
        "similar": "🔍 <b>Ұқсас: {title}</b>\n\n",
        "by_genre": "🎭 Жанр бойынша: <i>{genre}</i>\n\n",
        
        # Трейлер
        "trailer": "🎬 <b>Трейлер: {title}</b>\n\n",
        "watch_on_youtube": "📺 YouTube-та көру",
        "search_on_youtube": "🔍 YouTube-та іздеу",
        
        # Клавиатура поиска
        "new_search": "🔎 Жаңа іздеу",
        "popular": "🎬 Танымал",
        "back_to_menu": "🔙 Мәзірге оралу",
        "how_to_search": "❓ Қалай іздеу керек?",
    }
}

def get_text(user_id: int, key: str, **kwargs):
    """Get localized text for user"""
    from storage import storage
    
    user_data = storage.get_user_data(user_id)
    lang = user_data["settings"].get("language", "ru")
    
    text = TRANSLATIONS[lang].get(key, TRANSLATIONS["ru"].get(key, key))
    
    # Заменяем переменные в тексте
    if kwargs:
        for k, v in kwargs.items():
            text = text.replace(f"{{{k}}}", str(v))
    
    return text

def get_button_text(user_id: int, key: str):
    """Get localized button text"""
    from storage import storage
    
    user_data = storage.get_user_data(user_id)
    lang = user_data["settings"].get("language", "ru")
    
    return TRANSLATIONS[lang].get(key + "_btn", TRANSLATIONS["ru"].get(key + "_btn", key))