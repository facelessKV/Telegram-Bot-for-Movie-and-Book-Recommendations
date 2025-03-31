import logging
import random
import requests
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Токен бота (замените на свой)
API_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

# API ключи (замените на свои)
TMDB_API_KEY = 'YOUR_TMDB_API_KEY'  # API ключ для The Movie Database
GOOGLE_BOOKS_API_KEY = 'YOUR_GOOGLE_BOOKS_API_KEY'  # API ключ для Google Books API

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Класс для машины состояний пользователя
class UserState(StatesGroup):
    waiting_for_genre = State()  # Состояние ожидания выбора жанра
    waiting_for_content_type = State()  # Состояние ожидания выбора типа контента (фильм/книга)

# Словарь для маппинга жанров между локализованными названиями и кодами TMDB
TMDB_GENRE_MAP = {
    'боевик': 28,
    'приключения': 12, 
    'анимация': 16,
    'комедия': 35,
    'криминал': 80,
    'документальный': 99,
    'драма': 18,
    'семейный': 10751,
    'фэнтези': 14,
    'исторический': 36,
    'ужасы': 27,
    'музыка': 10402,
    'детектив': 9648,
    'мелодрама': 10749,
    'фантастика': 878,
    'триллер': 53,
    'военный': 10752,
    'вестерн': 37
}

# Получение списка всех доступных жанров из TMDb API
def get_all_genres():
    # Получаем жанры фильмов из TMDb
    url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={TMDB_API_KEY}&language=ru"
    response = requests.get(url)
    
    if response.status_code == 200:
        genres = response.json()['genres']
        # Возвращаем список названий жанров
        return [genre['name'].lower() for genre in genres]
    else:
        # В случае ошибки возвращаем предопределенный список жанров
        return list(TMDB_GENRE_MAP.keys())

# Функция для получения рекомендации фильма по жанру
def get_movie_recommendation(genre=None):
    try:
        # Базовый URL для запроса к TMDb
        url = f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&language=ru&sort_by=popularity.desc&include_adult=false"
        
        # Если указан жанр, добавляем его в запрос
        if genre and genre in TMDB_GENRE_MAP:
            url += f"&with_genres={TMDB_GENRE_MAP[genre]}"
        
        response = requests.get(url)
        
        if response.status_code == 200:
            movies = response.json()['results']
            if movies:
                # Выбираем случайный фильм из результатов
                movie = random.choice(movies)
                
                # Получаем дополнительную информацию о фильме
                movie_id = movie['id']
                details_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=ru"
                details_response = requests.get(details_url)
                
                if details_response.status_code == 200:
                    movie_details = details_response.json()
                    
                    # Формируем информацию о фильме
                    genres = ", ".join([g['name'] for g in movie_details.get('genres', [])])
                    
                    return {
                        'type': 'movie',
                        'title': movie['title'],
                        'genre': genres,
                        'description': movie.get('overview', 'Описание отсутствует'),
                        'rating': movie.get('vote_average', 'Нет рейтинга'),
                        'poster': f"https://image.tmdb.org/t/p/w500{movie.get('poster_path', '')}" if movie.get('poster_path') else None
                    }
        
        # В случае ошибки или отсутствия результатов
        return None
    
    except Exception as e:
        logging.error(f"Ошибка при получении рекомендации фильма: {e}")
        return None

# Функция для получения рекомендации книги по жанру
def get_book_recommendation(genre=None):
    try:
        # Базовый URL для запроса к Google Books API
        url = f"https://www.googleapis.com/books/v1/volumes?q="
        
        # Если указан жанр, добавляем его в запрос
        if genre:
            url += f"subject:{genre}&"
        
        # Добавляем параметры запроса
        url += f"orderBy=relevance&maxResults=40&langRestrict=ru&key={GOOGLE_BOOKS_API_KEY}"
        
        response = requests.get(url)
        
        if response.status_code == 200:
            books_data = response.json()
            if 'items' in books_data and books_data['items']:
                # Фильтруем книги с полной информацией
                valid_books = [book for book in books_data['items'] 
                              if 'volumeInfo' in book 
                              and 'title' in book['volumeInfo']
                              and 'authors' in book['volumeInfo']]
                
                if valid_books:
                    # Выбираем случайную книгу из результатов
                    book = random.choice(valid_books)
                    volume_info = book['volumeInfo']
                    
                    # Формируем информацию о книге
                    return {
                        'type': 'book',
                        'title': volume_info.get('title', 'Без названия'),
                        'author': ", ".join(volume_info.get('authors', ['Автор неизвестен'])),
                        'genre': ", ".join(volume_info.get('categories', [genre if genre else 'Категория не указана'])),
                        'description': volume_info.get('description', 'Описание отсутствует'),
                        'rating': volume_info.get('averageRating', 'Нет рейтинга'),
                        'thumbnail': volume_info.get('imageLinks', {}).get('thumbnail') if 'imageLinks' in volume_info else None
                    }
        
        # В случае ошибки или отсутствия результатов
        return None
    
    except Exception as e:
        logging.error(f"Ошибка при получении рекомендации книги: {e}")
        return None

# Функция для получения рекомендации в зависимости от типа контента и жанра
def get_recommendation(genre=None, content_type=None):
    if content_type == 'movie':
        return get_movie_recommendation(genre)
    elif content_type == 'book':
        return get_book_recommendation(genre)
    else:
        # Если тип контента не указан, выбираем случайно между фильмом и книгой
        if random.choice(['movie', 'book']) == 'movie':
            return get_movie_recommendation(genre)
        else:
            return get_book_recommendation(genre)

# Обработчик команды /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """
    Обработчик команды /start. Отправляет приветственное сообщение.
    """
    await message.answer(
        "👋 Привет! Я бот, который рекомендует фильмы и книги.\n\n"
        "Используйте следующие команды:\n"
        "/recommend - получить случайную рекомендацию\n"
        "/genre - выбрать жанр для рекомендаций\n"
        "/help - инструкция по использованию"
    )

# Обработчик команды /help
@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    """
    Обработчик команды /help. Отправляет справочную информацию.
    """
    await message.answer(
        "📚 Инструкция по использованию бота:\n\n"
        "1. /recommend - получить случайную рекомендацию фильма или книги.\n"
        "2. /genre - выбрать жанр для рекомендаций. После выбора жанра вы можете "
        "указать, хотите ли вы получить рекомендацию фильма или книги.\n"
        "3. /help - показать эту инструкцию.\n\n"
        "Наслаждайтесь рекомендациями! 🎬📖"
    )

# Обработчик команды /recommend
@dp.message(Command("recommend"))
async def cmd_recommend(message: types.Message, state: FSMContext):
    """
    Обработчик команды /recommend. Предлагает выбрать тип контента.
    """
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Фильм"), KeyboardButton(text="Книга")],
            [KeyboardButton(text="Любой")]
        ],
        resize_keyboard=True
    )
    
    await message.answer("Что вы хотите получить в рекомендации?", reply_markup=keyboard)
    await state.set_state(UserState.waiting_for_content_type)

# Обработчик выбора типа контента
@dp.message(UserState.waiting_for_content_type)
async def process_content_type(message: types.Message, state: FSMContext):
    """
    Обработчик выбора типа контента. Отправляет рекомендацию в зависимости от выбранного типа.
    """
    content_type = message.text.lower()
    
    # Сообщаем пользователю, что идет поиск
    await message.answer("Ищу подходящую рекомендацию... 🔍", reply_markup=ReplyKeyboardRemove())
    
    # Преобразование русского выбора в английский для внутренней логики
    if content_type == "фильм":
        content_type = "movie"
    elif content_type == "книга":
        content_type = "book"
    else:
        content_type = None
    
    # Получаем рекомендацию
    recommendation = get_recommendation(content_type=content_type)
    
    # Отправляем рекомендацию пользователю
    if recommendation:
        if recommendation['type'] == 'movie':
            # Формируем сообщение для фильма
            message_text = (
                f"🎬 *Рекомендация фильма*\n\n"
                f"*Название*: {recommendation['title']}\n"
                f"*Жанр*: {recommendation['genre']}\n"
                f"*Описание*: {recommendation['description']}\n"
                f"*Рейтинг*: {recommendation['rating']}/10"
            )
            
            # Если есть постер, отправляем фото с подписью
            if recommendation.get('poster'):
                try:
                    await bot.send_photo(
                        message.chat.id,
                        recommendation['poster'],
                        caption=message_text,
                        parse_mode="Markdown"
                    )
                except Exception:
                    # Если не удалось отправить фото, отправляем только текст
                    await message.answer(message_text, parse_mode="Markdown")
            else:
                await message.answer(message_text, parse_mode="Markdown")
        else:
            # Формируем сообщение для книги
            message_text = (
                f"📚 *Рекомендация книги*\n\n"
                f"*Название*: {recommendation['title']}\n"
                f"*Автор*: {recommendation['author']}\n"
                f"*Жанр*: {recommendation['genre']}\n"
                f"*Описание*: {recommendation['description']}\n"
                f"*Рейтинг*: {recommendation['rating']}/10"
            )
            
            # Если есть обложка, отправляем фото с подписью
            if recommendation.get('thumbnail'):
                try:
                    await bot.send_photo(
                        message.chat.id,
                        recommendation['thumbnail'],
                        caption=message_text,
                        parse_mode="Markdown"
                    )
                except Exception:
                    # Если не удалось отправить фото, отправляем только текст
                    await message.answer(message_text, parse_mode="Markdown")
            else:
                await message.answer(message_text, parse_mode="Markdown")
    else:
        await message.answer(
            "К сожалению, я не смог найти подходящую рекомендацию. Попробуйте другой жанр или тип контента."
        )
    
    # Сбрасываем состояние
    await state.clear()

# Обработчик команды /genre
@dp.message(Command("genre"))
async def cmd_genre(message: types.Message, state: FSMContext):
    """
    Обработчик команды /genre. Отображает кнопки с доступными жанрами.
    """
    # Получаем список жанров
    genres = get_all_genres()
    
    # Если список слишком большой, ограничиваем его
    if len(genres) > 15:
        genres = genres[:15]
    
    # Создаем клавиатуру с жанрами
    keyboard = []
    row = []
    for i, genre in enumerate(genres):
        row.append(KeyboardButton(text=genre.capitalize()))
        if len(row) == 2 or i == len(genres) - 1:
            keyboard.append(row)
            row = []
    
    markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
    
    await message.answer("Выберите жанр:", reply_markup=markup)
    await state.set_state(UserState.waiting_for_genre)

# Обработчик выбора жанра
@dp.message(UserState.waiting_for_genre)
async def process_genre(message: types.Message, state: FSMContext):
    """
    Обработчик выбора жанра. Сохраняет выбранный жанр и предлагает выбрать тип контента.
    """
    genre = message.text.lower()
    
    # Сохраняем выбранный жанр в состоянии
    await state.update_data(genre=genre)
    
    # Предлагаем выбрать тип контента
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Фильм"), KeyboardButton(text="Книга")],
            [KeyboardButton(text="Любой")]
        ],
        resize_keyboard=True
    )
    
    await message.answer(f"Выбран жанр: {genre}. Что вы хотите получить в рекомендации?", reply_markup=keyboard)
    await state.set_state(UserState.waiting_for_content_type)

# Обработчик выбора типа контента после выбора жанра
@dp.message(UserState.waiting_for_content_type)
async def process_content_type_with_genre(message: types.Message, state: FSMContext):
    """
    Обработчик выбора типа контента после выбора жанра. 
    Отправляет рекомендацию в зависимости от выбранного жанра и типа.
    """
    content_type = message.text.lower()
    
    # Получаем сохраненный жанр
    data = await state.get_data()
    genre = data.get('genre')
    
    # Сообщаем пользователю, что идет поиск
    await message.answer(f"Ищу {content_type.lower()} в жанре {genre}... 🔍", reply_markup=ReplyKeyboardRemove())
    
    # Преобразование русского выбора в английский для внутренней логики
    if content_type == "фильм":
        content_type = "movie"
    elif content_type == "книга":
        content_type = "book"
    else:
        content_type = None
    
    # Получаем рекомендацию
    recommendation = get_recommendation(genre=genre, content_type=content_type)
    
    # Отправляем рекомендацию пользователю
    if recommendation:
        if recommendation['type'] == 'movie':
            # Формируем сообщение для фильма
            message_text = (
                f"🎬 *Рекомендация фильма*\n\n"
                f"*Название*: {recommendation['title']}\n"
                f"*Жанр*: {recommendation['genre']}\n"
                f"*Описание*: {recommendation['description']}\n"
                f"*Рейтинг*: {recommendation['rating']}/10"
            )
            
            # Если есть постер, отправляем фото с подписью
            if recommendation.get('poster'):
                try:
                    await bot.send_photo(
                        message.chat.id,
                        recommendation['poster'],
                        caption=message_text,
                        parse_mode="Markdown"
                    )
                except Exception:
                    # Если не удалось отправить фото, отправляем только текст
                    await message.answer(message_text, parse_mode="Markdown")
            else:
                await message.answer(message_text, parse_mode="Markdown")
        else:
            # Формируем сообщение для книги
            message_text = (
                f"📚 *Рекомендация книги*\n\n"
                f"*Название*: {recommendation['title']}\n"
                f"*Автор*: {recommendation['author']}\n"
                f"*Жанр*: {recommendation['genre']}\n"
                f"*Описание*: {recommendation['description']}\n"
                f"*Рейтинг*: {recommendation['rating']}/10"
            )
            
            # Если есть обложка, отправляем фото с подписью
            if recommendation.get('thumbnail'):
                try:
                    await bot.send_photo(
                        message.chat.id,
                        recommendation['thumbnail'],
                        caption=message_text,
                        parse_mode="Markdown"
                    )
                except Exception:
                    # Если не удалось отправить фото, отправляем только текст
                    await message.answer(message_text, parse_mode="Markdown")
            else:
                await message.answer(message_text, parse_mode="Markdown")
    else:
        await message.answer(
            f"К сожалению, я не смог найти {content_type if content_type else 'рекомендацию'} в жанре '{genre}'. "
            f"Попробуйте другой жанр или тип контента."
        )
    
    # Сбрасываем состояние
    await state.clear()

# Обработчик для неизвестных команд
@dp.message()
async def unknown_command(message: types.Message):
    """
    Обработчик для неизвестных команд. Отправляет подсказку о доступных командах.
    """
    await message.answer(
        "Я не понимаю эту команду. Пожалуйста, используйте:\n"
        "/recommend - получить рекомендацию\n"
        "/genre - выбрать жанр\n"
        "/help - инструкция по использованию"
    )

# Основная функция запуска бота
async def main():
    # Запускаем бота
    await dp.start_polling(bot)

if __name__ == '__main__':
    # Запускаем бота через asyncio
    asyncio.run(main())