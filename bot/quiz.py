from bot.keyboards import generate_options_keyboard
import aiosqlite
from data.quiz_data import quiz_data

DB_NAME = 'quiz_bot.db'


async def get_question(message, user_id):
    current_question_index = await get_user_data(user_id, 'question_index')
    correct_index = quiz_data[current_question_index]['correct_option']
    opts = quiz_data[current_question_index]['options']
    kb = generate_options_keyboard(opts, opts[correct_index])
    await message.answer(f"{quiz_data[current_question_index]['question']}", reply_markup=kb)

async def new_quiz(message):
    user_id = message.from_user.id
    current_question_index = 0
    current_quantity_win_quiz = await get_user_data(user_id, 'quantity_win_quiz')
    current_quantity_quiz = await get_user_data(user_id, 'quantity_quiz')
    right_answer_user = await get_user_data(user_id, 'right_answer_user')
    wrong_answer_user = await get_user_data(user_id, 'wrong_answer_user')
    await update_quiz_state(user_id, 
                            current_question_index, 
                            current_quantity_win_quiz, 
                            current_quantity_quiz, 
                            right_answer_user, 
                            wrong_answer_user)
    await get_question(message, user_id)

async def get_user_data(user_id, column):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(f'SELECT {column} FROM quiz_state WHERE user_id = (?)', (user_id, )) as cursor:
            results = await cursor.fetchone()
            if results is not None:
                return results[0]
            else:
                return 0


async def update_quiz_state(user_id, index, quantity_win_quiz, quantity_quiz, right_answer_user, wrong_answer_user):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''INSERT OR REPLACE 
                         INTO quiz_state (user_id, question_index, quantity_win_quiz, quantity_quiz, right_answer_user, wrong_answer_user) 
                         VALUES (?, ?, ?, ?, ?, ?)''', 
                         (user_id, index, quantity_win_quiz, quantity_quiz, right_answer_user, wrong_answer_user))
        await db.commit()


async def clean_stat_player(user_id, quantity_win_quiz, quantity_quiz):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''UPDATE quiz_state 
                         SET quantity_win_quiz = ?, quantity_quiz = ? WHERE user_id = ?''', 
                         (quantity_win_quiz, quantity_quiz, user_id))
        await db.commit()

async def clean_answers_user(user_id, right_answer_user, wrong_answer_user):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''UPDATE quiz_state 
                         SET right_answer_user = ?, wrong_answer_user = ? WHERE user_id = ?''', 
                         (right_answer_user, wrong_answer_user, user_id))
        await db.commit()

async def create_table():
    # Создаем соединение с базой данных (если она не существует, она будет создана)
    async with aiosqlite.connect(DB_NAME) as db:
        # Создаем таблицу
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_state (user_id INTEGER PRIMARY KEY, 
                         question_index INTEGER, 
                         quantity_win_quiz INTEGER, 
                         quantity_quiz INTEGER, 
                         right_answer_user INTEGER, 
                         wrong_answer_user INTEGER)''')
        # Сохраняем изменения
        await db.commit()
