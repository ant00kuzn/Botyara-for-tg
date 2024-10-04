import telebot
import os
import webbrowser
import requests
import platform
import ctypes
import mouse
import PIL.ImageGrab
import sys
import cv2
from PIL import Image, ImageGrab, ImageDraw
from pySmartDL import SmartDL
from telebot import types
from telebot import apihelper

my_id = 111111111
bot_token = '123456789:ABCFJSKVMSDKJSDFOJDSNK'
bot = telebot.TeleBot(bot_token)


##Клавиатура меню
menu_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=False)
btnfiles = types.KeyboardButton('Файлы и процессы')
btnweb = types.KeyboardButton('Перейти по ссылке')
btncmd = types.KeyboardButton('Выполнить команду')
btnoff = types.KeyboardButton('Выключить компьютер')
btnreb = types.KeyboardButton('Перезагрузить компьютер')
btnyved = types.KeyboardButton('Отправка уведомления')
btnmyz = types.KeyboardButton('Включить музыку')
btndota = types.KeyboardButton('Запустить доту')
menu_keyboard.row(btnmyz, btndota)
menu_keyboard.row(btnfiles, btncmd)
menu_keyboard.row(btnoff, btnreb)
menu_keyboard.row(btnyved, btnweb)


#Клавиатура Файлы и Процессы
files_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=False)
btnstart = types.KeyboardButton('Запустить файл')
btnkill = types.KeyboardButton('Убить процесс')
btndown = types.KeyboardButton('Скачать файл')
btnupl = types.KeyboardButton('Загрузить файл')
btnback = types.KeyboardButton('Назад')
files_keyboard.row(btnstart,  btnkill)
files_keyboard.row(btndown, btnupl)
files_keyboard.row(btnback)


MessageBox = ctypes.windll.user32.MessageBoxW
if os.path.exists("msg.pt"):
        pass
else:
        bot.send_message(my_id, "Здарова, чудик", parse_mode = "markdown")
        f = open('msg.pt', 'tw', encoding='utf-8')
        f.close

bot.send_message(my_id, "Я родился", reply_markup = menu_keyboard)


@bot.message_handler(content_types=["text"])
def get_text_messages(message): 
        if message.from_user.id != 1:
                if message.from_user.id == my_id:
                        match message.text:
                                case "Файлы и процессы":
                                        bot.send_message(my_id, "Файлы и процессы", reply_markup = files_keyboard)
                                        bot.register_next_step_handler(message, files_process)
                        
                                case "Перейти по ссылке":
                                        bot.send_message(my_id, "Укажите ссылку: ")
                                        bot.register_next_step_handler(message, web_process)

                                case "Выполнить команду":
                                        bot.send_message(my_id, "Укажите консольную команду: ")
                                        bot.register_next_step_handler(message, cmd_process)

                                case "Выключить компьютер":
                                        bot.send_message(my_id, "Выключение компьютера...")
                                        os.system('shutdown -s /t 0 /f')
                                        bot.register_next_step_handler(message, get_text_messages)

                                case "Перезагрузить компьютер":
                                        bot.send_message(my_id, "Перезагрузка компьютера...")
                                        os.system('shutdown -r /t 0 /f')
                                        bot.register_next_step_handler(message, get_text_messages)
                                        
                                case "Отправка уведомления":
                                        bot.send_message(my_id, "Укажите текст уведомления:")
                                        bot.register_next_step_handler(message, messaga_process)

                                case "Включить музыку":
                                        bot.register_next_step_handler(message, spotify_open)

                                case "Запустить доту":
                                        bot.send_message(my_id, "Запускаю...")
                                        os.startfile(r"Dota 2.url")
                                        bot.register_next_step_handler(message, get_text_messages)

                                case "ты здесь?":
                                        bot.send_message(my_id, "На месте")
                                        back(message)
                                case _:
                                        bot.send_message(my_id, "ты дурак епта")
                                        pass
                else:
                        info_user(message)
        else:
                otvet = input(": ")
                bot.send_message(id, otvet)
                info_user(message)

def files_process(message):
        if message.from_user.id == my_id:
                bot.send_chat_action(my_id, 'typing')
                match message.text:
                        case "Убить процесс": 
                                bot.send_message(my_id, "Укажите название процесса: ")
                                bot.register_next_step_handler(message, kill_process)

                        case "Запустить файл":
                                bot.send_message(my_id, "Укажите путь до файла: ")
                                bot.register_next_step_handler(message, start_process)

                        case "Скачать файл":
                                bot.send_message(my_id, "Укажите путь до файла: ")
                                bot.register_next_step_handler(message, downfile_process)

                        case "Загрузить файл":
                                bot.send_message(my_id, "Отправьте необходимый файл")
                                bot.register_next_step_handler(message, uploadfile_process)

                        case "Назад":
                                back(message)
                        case _:
                                pass
        else:
                info_user(message)


def back(message):
        bot.send_message(my_id, "Возврат", reply_markup=menu_keyboard)

def info_user(message):
        bot.send_chat_action(my_id, 'typing')
        alert = f"Кто-то пытался отправить команду: \"{message.text}\"\n\n"
        alert += f"user id: {str(message.from_user.id)}\n"
        alert += f"first name: {str(message.from_user.first_name)}\n"
        alert += f"last name: {str(message.from_user.last_name)}\n" 
        alert += f"username: @{str(message.from_user.username)}"
        bot.send_message(my_id, alert, reply_markup = menu_keyboard)

def kill_process (message):
        bot.send_chat_action(my_id, 'typing')
        try:
                os.system("taskkill /IM " + message.text + " -F")
                bot.send_message(my_id, f"Процесс \"{message.text}\" убит", reply_markup = files_keyboard)
                bot.register_next_step_handler(message, files_process)
        except:
                bot.send_message(my_id, "Ошибка! Процесс не найден", reply_markup = files_keyboard)
                bot.register_next_step_handler(message, files_process)

def start_process (message):
        bot.send_chat_action(my_id, 'typing')
        try:
                os.startfile(r'' + message.text)
                bot.send_message(my_id, f"Файл по пути \"{message.text}\" запустился", reply_markup = files_keyboard)
                bot.register_next_step_handler(message, files_process)
        except:
                bot.send_message(my_id, "Ошибка! Указан неверный файл", reply_markup = files_keyboard)
                bot.register_next_step_handler(message, files_process)

def web_process (message):
        bot.send_chat_action(my_id, 'typing')
        try:
                webbrowser.open(message.text, new=0)
                bot.send_message(my_id, f"Переход по ссылке \"{message.text}\" осуществлён", reply_markup = additionals_keyboard)
                bot.register_next_step_handler(message, get_text_messages)
        except:
                bot.send_message(my_id, "Ошибка! ссылка введена неверно")
                bot.register_next_step_handler(message, get_text_messages)

def spotify_open (message):
        bot.send_chat_action(my_id, 'typing')
        try:
                webbrowser.open("https://open.spotify.com/playlist/7CEPji1Vco829FF2Qbjvjo", new=0)
                bot.send_message(my_id, f"Спотифу запущен", reply_markup = additionals_keyboard)
                bot.register_next_step_handler(message, get_text_messages)
        except:
                bot.register_next_step_handler(message, get_text_messages)

def cmd_process (message):
        bot.send_chat_action(my_id, 'typing')
        try:
                os.system(message.text)
                bot.send_message(my_id, f"Команда \"{message.text}\" выполнена", reply_markup = additionals_keyboard)
                bot.register_next_step_handler(message, get_text_messages)
        except:
                bot.send_message(my_id, "Ошибка! Неизвестная команда")
                bot.register_next_step_handler(message, get_text_messages)

def downfile_process(message):
        bot.send_chat_action(my_id, 'typing')
        try:
                file_path = message.text
                if os.path.exists(file_path):
                        bot.send_message(my_id, "Файл загружается, подождите...")
                        bot.send_chat_action(my_id, 'upload_document')
                        file_doc = open(file_path, 'rb')
                        bot.send_document(my_id, file_doc)
                        bot.register_next_step_handler(message, files_process)
                else:
                        bot.send_message(my_id, "Файл не найден или указан неверный путь")
                        bot.register_next_step_handler(message, files_process)
        except:
                bot.send_message(my_id, "Ошибка! Файл не найден или указан неверный путь")
                bot.register_next_step_handler(message, files_process)

def uploadfile_process(message):
        bot.send_chat_action(my_id, 'typing')
        try:
                file_info = bot.get_file(message.document.file_id)
                downloaded_file = bot.download_file(file_info.file_path)
                src = message.document.file_name
                with open(src, 'wb') as new_file:
                        new_file.write(downloaded_file)
                bot.send_message(my_id, "Файл успешно загружен")
                bot.register_next_step_handler(message, files_process)
        except:
                bot.send_message(my_id, "Ошибка! Отправьте файл как документ")
                bot.register_next_step_handler(message, files_process)

def uploadurl_process(message):
        bot.send_chat_action(my_id, 'typing')
        User.urldown = message.text
        bot.send_message(my_id, "Укажите путь сохранения файла:")
        bot.register_next_step_handler(message, uploadurl_2process)     

def uploadurl_2process(message):
        bot.send_chat_action(my_id, 'typing')
        try:
                User.fin = message.text
                obj = SmartDL(User.urldown, User.fin, progress_bar=False)
                obj.start()
                bot.send_message(my_id, f"Файл успешно сохранён по пути \"{User.fin}\"")
                bot.register_next_step_handler(message, files_process)
        except:
                bot.send_message(my_id, "Указаны неверная ссылка или путь")
                bot.register_next_step_handler(message, get_text_messages)

def messaga_process(message):
        bot.send_chat_action(my_id, 'typing')
        try:
                MessageBox(None, message.text, 'Ботяра', 0)
        except:
                bot.send_message(my_id, "Ошибка")

bot.polling(none_stop=True, interval=0, timeout=20)
