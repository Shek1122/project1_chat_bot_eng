import telebot
import random
import json

TOKEN = "7460844917:AAG7lMZpNW6TnZQSz7s2l_4_8uJTtJOPVcY"  # это спец-ый ключ

bot = telebot.TeleBot(TOKEN)  # инициалируем бота т.е. создаем экземпляр

# Урок 78. Т. 1
user_data = {}  # это словарь в котором хранятся все слова пользователя по ИД


# Обработай исключение при открытии файла в начале бота. FileNotFoundError — исключение, которое возникает, когда файл не найден.
# try:
#     with open("user_data.json", "r", encoding="utf-8") as file:
#         user_data = json.load(file)
# except FileNotFoundError:
#     user_data = {}


# Теория 1
# декоратор , обертка над функцией. Будет срабатывать тогда, когда мы нажмем Старт. Может быть много таких декораторов
@bot.message_handler(commands=["start"])
def handle_start(message):  # обработка после того, как бот  запущен. message - сообщение пользователя
    bot.send_message(message.chat.id,
                     "Привет. Это твой чат бот. Скоро я буду уметь много всего.")  # ответное сообщщениею chat.id - id чата. Собеседников может быт  много


# что бы бот постоянно прослушивал все чаты


@bot.message_handler(commands=["learn"])  # /learn 5
# обработчик сообщений handle - обработка
def handle_learn(message):  # обработка после того, как бот запущен. message - сообщение пользователя
    # bot.send_message(message.chat.id, "Обучение сейчас начнется")  #Урок 77. Теория 2. Ответное сообщение chat.id - id чата. Собеседников может быт  много
    # bot.send_message(message.chat.id, user_data)  # ответное сообщщениею chat.id - id чата. Собеседников может быт  много
    user_words = user_data.get(str(message.chat.id), {})  # берёт выборку слов пользователя

    # Проверяем, есть ли у пользователя слова для изучения
    if not user_words:
        bot.send_message(message.chat.id, "Твой словарь пуст! Добавь слова с помощью команды /addword.")
        return

    # В функции handle_learn() добавь обработку этих исключений на этих строчках:
    try:
        words_number = int(message.text.split()[1])  # берёт количество слов для повторения
        # Начинаем процесс изучения
        ask_translation(message.chat.id, user_words, words_number)
    except ValueError:  # ValueError — исключение, которое возникает, когда функция получает аргумент правильного типа, но с недопустимым значением.
        bot.send_message(message.chat.id, "Используй команду /learn <количество> для изучения слов.")
    except IndexError:  # IndexError — исключение, которое возникает, когда происходит попытка обращения к элементу последовательности (например, строке, списку или кортежу) по индексу, который находится вне допустимого диапазона индексов этой последовательности. (Например, в списке пять элементов, а пытаются обратиться к шестому).
        bot.send_message(message.chat.id, "Используй команду /learn <количество> для изучения слов.")


# Урок 78. Т. 2
def ask_translation(chat_id, user_words,
                    words_left):  # спрашивает перевод chat_id - с какого чата,user_words - из каких слов нам спрашивать,words_left - сколько слов у нас еще остплось
    if words_left > 0:  # если осталось спросить слов больше 0
        word = random.choice(list(user_words.keys()))  # превращаем в список наш словарь
        translation = user_words[word]  # берем его перевод
        bot.send_message(chat_id, f"Напиши перевод слова '{word}'.")

        bot.register_next_step_handler_by_chat_id(chat_id, check_translation, translation,
                                                  words_left - 1)  # обрабатываем то, что введ пользователь. Назначить следующему шагу по чату обработку
    else:
        bot.send_message(chat_id, "Урок закончен.")


def check_translation(message, expected_translation, words_left):  # проверяет перевод
    user_translation = message.text.strip().lower()  # strip()  -убирает ненужные пробелы в начале и конце
    if user_translation == expected_translation.lower():
        bot.send_message(message.chat.id, "Правильно, молодец!")
    else:
        bot.send_message(message.chat.id, f"Неправильно. Правильный перевод: {expected_translation}")
    ask_translation(message.chat.id, user_data[str(message.chat.id)], words_left - 1)


# Урок 78. Т. 1
@bot.message_handler(
    commands=["addword"])  # /addword apple яблоко добавлять слово с переводом в специальный словарь words
def handle_addword(message):  #
    # global user_data
    chat_id = message.chat.id
    # Получаем словарь пользователя
    user_dict = user_data.get(str(chat_id), {})

    # Получаем слово и его перевод от пользователя
    # Обработай исключение Exception в функции handle_addword()
    try:
        words = message.text.split()[1:]
        if len(words) == 2:
            word, translation = words[0].lower(), words[1].lower()
            # Добавляем слово и перевод в словарь пользователя
            user_dict[word] = translation
            # Сохраняем обновленные данные в файл
            user_data[str(chat_id)] = user_dict
            with open("user_data.json", "w", encoding="utf-8") as file:
                json.dump(user_data, file, ensure_ascii=False, indent=4)
            bot.send_message(chat_id, f"Слово '{word}' добавлено в словарь.")
        else:
            bot.send_message(chat_id, "Используй команду /addword <слово> <перевод> для добавления слова.")
    except Exception as e:
        bot.send_message(chat_id,
                         "Произошла ошибка при обработке команды. Попробуйте ещё раз использовать команду /addword <слово> <перевод> для добавления слова.")


# Урок 77.Задание 9
@bot.message_handler(commands=["help"])
def handle_help(message):
    bot.send_message(message.chat.id, "Добро пожаловать! Я бот для изучения английского языка.")
    bot.send_message(message.chat.id, "Вот список доступных команд:")
    bot.send_message(message.chat.id, "/start - Начало работы с ботом")
    bot.send_message(message.chat.id, "/learn - Начать обучение")
    bot.send_message(message.chat.id, "/help - Посмотреть справку")
    bot.send_message(message.chat.id, "Автор бота: Шекер")


@bot.message_handler(func=lambda message: True)  # обрабатываем все сообщения, которые к нам поступают и мы его повторим
def handle_all(message):
    # bot.send_message(message.chat.id, message.text)  #Урок 76. Теория 2
    if message.text.lower() == "Как тебя зовут?":  # Урок 77. Т. 1. Бот-болталка
        bot.send_message(message.chat.id, "У меня нет пока имени")  # message.text - текст нашего же сообщения
    elif message.text.lower() == "расскажи о себе?":
        bot.send_message(message.chat.id,
                         " Я бот для изучения английского языка")  # message.text - текст нашего же сообщения
    elif message.text.lower() == "расскажи шутку?":
        bot.send_message(message.chat.id, " У меня плохое чувство юмора. Об этом лучше спросить в инете")


if __name__ == "__main__":
    bot.polling(none_stop=True)  # none_stop =True - если ошибка, то бот не вылетает, продолжает работать



