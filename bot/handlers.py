from aiogram import types
from aiogram import F
from bot.quiz import new_quiz, update_quiz_state, get_question, get_user_data, clean_stat_player, clean_answers_user
from data.quiz_data import quiz_data
from aiogram.filters.command import Command
from bot.utils import calculate_percentage
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from bot.keyboards import clean_stat_keyboard

def register_handlers(dp):

    # Хэндлер на команду /start
    @dp.message(Command("start"))
    async def cmd_start(message: types.Message):
        builder = ReplyKeyboardBuilder()
        builder.add(types.KeyboardButton(text="Начать игру"))
        builder.add(types.KeyboardButton(text="Статистика"))
        builder.add(types.KeyboardButton(text="Сброс Статистики"))
        builder.adjust(2)
        await message.answer("Добро пожаловать в квиз!", reply_markup=builder.as_markup(resize_keyboard=True))

    # Хэндлер на команду /quiz
    @dp.message(F.text == "Начать игру")
    @dp.message(Command("quiz"))
    async def cmd_quiz(message: types.Message):
        await message.answer(f"Давайте начнем квиз!")
        await message.answer(f"Если вы ответите на 60% вопросов правильно, то вы выйграете")
        await new_quiz(message)

    @dp.message(F.text == "Статистика")
    @dp.message(Command("stat"))
    async def cmd_stat(message: types.Message):
        current_quantity_win_quiz = await get_user_data(message.from_user.id, 'quantity_win_quiz')
        current_quantity_quiz = await get_user_data(message.from_user.id, 'quantity_quiz')

        await message.answer(f"Ваша статистика:")
        await message.answer(f"Количество выйгранных игр - {current_quantity_win_quiz}")
        await message.answer(f"Количество сыгранных игр - {current_quantity_quiz}")

    @dp.message(F.text == "Сброс Статистики")
    @dp.message(Command("cleanstat"))
    async def cmd_stat(message: types.Message):
    
        keyboard = clean_stat_keyboard()
        
        await message.answer("Вы уверены, что хотите сбросить статистику?", reply_markup=keyboard)

        
    @dp.callback_query(F.data.in_(["reset_yes", "reset_no"]))
    async def process_choices(callback_query: types.CallbackQuery):
        user_id = callback_query.from_user.id

        if callback_query.data == "reset_yes":

            await clean_stat_player(user_id, 0, 0)
            await callback_query.message.answer(f"Ваша статистика сброшена")
        else:
            await callback_query.message.answer("Сброс статистики отменен.")

        await callback_query.bot.edit_message_reply_markup(
            chat_id=callback_query.from_user.id,
            message_id=callback_query.message.message_id,
            reply_markup=None
        )

    @dp.callback_query(F.data.startswith("right_answer") | F.data.startswith("wrong_answer"))
    async def handle_answer(callback: types.CallbackQuery):

    # Убираем клавиатуру после выбора ответа
        await callback.bot.edit_message_reply_markup(
            chat_id=callback.from_user.id,
            message_id=callback.message.message_id,
            reply_markup=None
        )

        # Получаем текущий данные
        current_question_index = await get_user_data(callback.from_user.id, 'question_index')
        correct_answer = quiz_data[current_question_index]['options'][quiz_data[current_question_index]['correct_option']]
        current_quantity_win_quiz = await get_user_data(callback.from_user.id, 'quantity_win_quiz')
        current_quantity_quiz = await get_user_data(callback.from_user.id, 'quantity_quiz')
        right_answer_user = await get_user_data(callback.from_user.id, 'right_answer_user')
        wrong_answer_user = await get_user_data(callback.from_user.id, 'wrong_answer_user')

        # Обработка правильного ответа
        if callback.data.startswith("right_answer"):
            right_answer_user += 1
            # Извлекаем текст выбранной кнопки
            selected_answer = callback.data.split("_", maxsplit=2)[-1]

            await callback.message.answer("Верно!")
            await callback.message.answer(f"Ваш ответ: {selected_answer}")

        # Обработка неправильного ответа
        else:           
            wrong_answer_user += 1    
            await callback.message.answer(f"Неправильно. Правильный ответ: {correct_answer}")

        # Обновление номера текущего вопроса
        current_question_index += 1
        await update_quiz_state(callback.from_user.id, 
                                current_question_index, 
                                current_quantity_win_quiz, 
                                current_quantity_quiz,
                                right_answer_user,
                                wrong_answer_user)

        # Проверяем, есть ли еще вопросы
        if current_question_index < len(quiz_data):
            await get_question(callback.message, callback.from_user.id)
        else:
            current_quantity_quiz += 1
            await callback.message.answer("Это был последний вопрос. Квиз завершен!")
            percentage = await calculate_percentage(right_answer_user, wrong_answer_user)

            if percentage == 100:
                current_quantity_win_quiz += 1
                await callback.message.answer("Поздравляем! Вы ответили правильно на все вопросы. Вы выйграли")
                
            elif percentage >= 60:
                current_quantity_win_quiz += 1
                await callback.message.answer("Поздравляем! Вы ответили правильно на 60% или более вопросов. Вы выйграли")
            else:
                await callback.message.answer(f"К сожалению, вы ответили правильно только на {percentage:.2f}% вопросов. Попробуйте еще раз!")
            await clean_answers_user(callback.from_user.id, 0, 0)

        await update_quiz_state(callback.from_user.id, 
                                current_question_index, 
                                current_quantity_win_quiz, 
                                current_quantity_quiz,
                                right_answer_user,
                                wrong_answer_user)