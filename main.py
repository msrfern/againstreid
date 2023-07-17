#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
from aiogram import Bot
from aiogram import types as t
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from sql import *
from aiogram.utils.deep_linking import get_start_link, decode_payload
import random
import string
import pytz
import datetime
import time
import subprocess

TOKEN = '' #указываете здесь ваш токен бота
ALLOWGROUPS = [1] #можете указать айди группы поддержки. не трогайте этот параметр, если поддержки нет
OWNER = [1, 2] #указываете здесь айди владельца бота (можно несколько владельцом, через запяту.)
CHANNEL = 1 #указываете айди канала, на который нужно подписаться 
CHANNELNAME = 'https://t.me/channel' #указываете ссылку канала, на который нужно подписаться
GROUPP = 1 #укажите айди группы администраторов, в которую добавлен бот. это обязательно.
PROXY_URL = 'http://proxy.server:3128' #Прокси для pythonanywhere
storage = MemoryStorage()
bot = Bot(token=TOKEN, parse_mode='HTML')#, proxy=PROXY_URL) #Прокси
dp = Dispatcher(bot, storage=storage)

class dia(StatesGroup):
    chan = State()
    await_stop = State()
    await_name = State()
    await_desci = State()
    await_category = State()
    await_categorytwo = State()
    await_categorythree = State()

def add_value_to_string(string, value):
    return string + ' ' + str(value)

def string_to_list(string):
    return [int(x) for x in string.split()]

def create_link_refer(idchannel, ownerid):
    characters = '0_1234_56789' + 'ABCDEFGH_IJKLMNOPQRST_UVWXYZabcdefghijklmnop_qrstuvwxyz'
    a = ''.join(random.choice(characters) for i in range(20))
    if can_check_link(a) == 'yes':
        return create_link_refer(idchannel, ownerid)
    sql_create_link(a, ownerid, idchannel)
    return a

def create_id_channel():
    characters = '0123456789' + 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    a = ''.join(random.choice(characters) for i in range(8))
    if check_id_channel(a) == True:
        return create_id_channel()
    return a

@dp.message_handler(content_types=['new_chat_members'])
async def send_welcome(msg: t.Message):
    bot_obj = await bot.get_me()
    bot_id = bot_obj.id

    for chat_member in msg.new_chat_members:
        if chat_member.id == bot_id and not msg.chat.id in ALLOWGROUPS:
            if check_group(msg.chat.id) == False:
                create_group(msg.chat.id)
                await msg.reply(f'''
👠 <b>Спасибо, что добавили меня в группу!</b>

Советую подписаться на мой канал новостей, чтобы не пропустить обновления - @AgainstReid

⚒ Информация как пользоваться нашим ботом — t.me/AgainstReid_Useful/9

🔰 Этот бот поможет вам защитить ваш канал от рейдерства и удаления подписчиков различными способами!

— Проверка пользователя по айди
— Постинг через бота | СКОРО
— Блокировка рейдеров на вашем канале
— Добавление админов через бота и снятие админки на ночь, а после возвращение утром

ℹ️ Все эти функции, и другие которые вы найдете в боте, помогут вам защитить ваш канал от рейдерства.
                    ''', disable_web_page_preview=True)

@dp.message_handler(commands=['группа'], commands_prefix=['.'])
async def group(msg: t.Message):
    if check_group(msg.chat.id) == False:
        create_group(msg.chat.id)
        await msg.reply(f'''
👠 <b>Спасибо, что добавили меня в группу!</b>

Советую подписаться на мой канал новостей, чтобы не пропустить обновления - @AgainstReid

⚒ Информация как пользоваться нашим ботом — t.me/AgainstReid_Useful/9

🔰 Этот бот поможет вам защитить ваш канал от рейдерства и удаления подписчиков различными способами!

— Проверка пользователя по айди
— Постинг через бота | СКОРО
— Блокировка рейдеров на вашем канале
— Добавление админов через бота и снятие админки на ночь, а после возвращение утром

ℹ️ Все эти функции, и другие которые вы найдете в боте, помогут вам защитить ваш канал от рейдерства.
        ''', disable_web_page_preview=True)
    else:
        await msg.reply('Группа уже добавлена! Спасибо!')

@dp.message_handler(state=dia.await_name)
async def name_handler(msg: t.Message, state: FSMContext):
    category_buttons = ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton('Отмена')
    )
    if msg.text == 'Отмена':
        reply_markup = t.ReplyKeyboardRemove()
        await msg.answer('Создание анкеты отменено.', reply_markup=reply_markup)
        await state.finish()
        return
    if len(msg.text) > 32:
        await msg.answer('Имя слишком длинное!')
        return
    await state.update_data(await_name=msg.text)
    await msg.reply('📝 Отлично! Теперь введи описание о себе. Здесь ты можешь рассказать о себе, своих навыках и так далее. Можешь указать, на каких каналах работаешь и тд. Максимум 3000 символов.', reply_markup=category_buttons)
    await dia.await_desci.set()

def create_id():
    characters = '0123456789'
    a = ''.join(random.choice(characters) for i in range(9))
    if is_li_anketa_id(int(a)) == True:
        return create_id()
    else:
        return int(a)

@dp.message_handler(state=dia.await_desci)
async def name_handler(msg: t.Message, state: FSMContext):
    if msg.text == 'Отмена':
        reply_markup = t.ReplyKeyboardRemove()
        await msg.answer('Создание анкеты отменено.', reply_markup=reply_markup)
        await state.finish()
        return
    if len(msg.text) > 3000:
        await msg.answer('Описание слишком длинное!')
        return
    await state.update_data(await_desci=msg.text)
    data = await state.get_data()
    name = data.get('await_name')
    description = data.get('await_desci')
    try:
        create_anketa(msg.from_user.id, create_id(), name, description)
    except:
        pass
    reply_markup = t.ReplyKeyboardRemove()
    await msg.answer('🛡 Ваша анкета отправлена на проверку! Это занимает не более 12-ти часов.', reply_markup=reply_markup)
    await state.finish()
    keyboard = t.InlineKeyboardMarkup(row_width=1)
    buttons = [
        t.InlineKeyboardButton(text="Принять", callback_data=f"AcceptAnket_{msg.from_user.id}"),
        t.InlineKeyboardButton(text="Отклонить", callback_data=f"DeclineAnket_{msg.from_user.id}"),
        t.InlineKeyboardButton(text="Заблокировать", callback_data=f"BanAnketa_{msg.from_user.id}"),
    ]
    keyboard.add(*buttons)
    await bot.send_message(GROUPP, f'''
<b>Новая анкета</b>

Имя: {name}
Описание: {description}

ОТ: <pre>{msg.from_user.id}</pre> @{msg.from_user.username} ({msg.from_user.full_name})
        ''', reply_markup=keyboard)
    return

@dp.message_handler(commands=['тесты'])
async def dfghhfghjhgfgh(msg: t.Message):
    if not msg.from_user.id in OWNER:
        await msg.answer('Нет!')
        return
    keyboard = t.InlineKeyboardMarkup(row_width=1)
    buttons = [
        t.InlineKeyboardButton(text="Принять", callback_data=f"Birza"),
        t.InlineKeyboardButton(text="Отклонить", callback_data=f"Decline_{msg.from_user.id}"),
        t.InlineKeyboardButton(text="Заблокировать", callback_data=f"BanAnketa_{msg.from_user.id}"),
    ]
    keyboard.add(*buttons)
    await msg.answer('1', reply_markup=keyboard)

@dp.message_handler(commands=["нагрузка", "Нагрузка", "актив"], commands_prefix=["/", ".", "!"])
async def ygyguhi(msg: t.Message):
    speedtest_output = subprocess.check_output(['speedtest-cli']).decode('utf-8')
    top_output = subprocess.check_output(['top', '-n', '1', '-b']).decode('utf-8')
    free_output = subprocess.check_output(['free', '-h']).decode('utf-8')
    output = f"<b>Speedtest:</b>n{speedtest_output}nn<b>Top:</b>nn<b>Free:</b>n{free_output}"
    await msg.answer(f'''
Пинг: {(speedtest_output).split(':')[1]}

    ''')
#Скорость интернета: {(speedtest_output).split(':')[2:9]}/{(speedtest_output).split(':')[3:9]}
@dp.message_handler(commands=['getchannels'])
async def hfgh(msg: t.Message):
    if not msg.from_user.id in OWNER:
        await msg.answer('Нет!')
        return
    channel = giveallchannels()
    COL = 0
    for ch in channel:
        try:
            chat = await bot.get_chat(ch[0])
            COL += 1
            await bot.send_message(msg.from_user.id, f'{COL} @{chat["username"]}')
        except:
            pass


@dp.message_handler(commands=['рассылка_каналы'])
async def fghjk(msg: t.Message):
    if not msg.from_user.id in OWNER:
        await msg.answer('Нет!')
        return
    channel = giveallchannels()
    for ch in channel:
        try:
            chat = await bot.get_chat(ch[0])
            await bot.send_message(ch[0], '''
Текст
            ''')
            await msg.answer(f'Отправлено @{chat["username"]}')
        except Exception as e:
            print(e)

@dp.message_handler(commands=['блокпроверка'])
async def admprovban(msg: t.Message):
    if msg.from_user.id in OWNER:
        await msg.reply('Начинаю проверку..')
        COU = 0
        for idd in giveallchannels():
            id = idd[0]
            for iddre in giveallreids():
                idre = iddre[0]
                try:
                    check = await bot.get_chat_member(chat_id=id, user_id=idre)
                    if check["status"] == "member":
                        ownerid = get_owner_id_channel(id)
                        chat = await bot.get_chat(id)
                        await bot.send_message(ownerid, f'''
⚠️ <b>На вашем канале обнаружен рейдер!</b>

На вашем канале, {chat["title"]}, был обнаружен рейдер! Бот успешно его заблокировал и ваш канал в безопасности.
                        ''')
                        await bot.ban_chat_member(chat_id=id, user_id=idre)
                        addreidchannel(int(id))
                        COU += 1
                    if check["status"] == "administrator":
                        ownerid = get_owner_id_channel(id)
                        chat = await bot.get_chat(id)
                        admin = await bot.get_chat_member(id, idre)
                        await bot.send_message(ownerid, f'''
‼️ <b><u>ВНИМАНИЕ!</u></b> ‼️

На вашем канале, {chat["title"]}, в администраторах находится человек РЕЙДЕР!
Не медленно уберите его с админа!

Имя админа: {admin["first_name"]}
Юзернейм: @{admin["username"]}
                        ''')
                except:
                    pass
        await msg.reply(f'✅ Проверка успешно закончена!\n🚫 Было забанено {COU} рейдеров')

    else:
        await msg.reply('Вам это недоступно.')
        return

@dp.message_handler(commands=['рассылка'])
async def рассылкабеать(msg: t.Message):
    if msg.from_user.id in OWNER:
        a = rasulkaforusers()
        for idd in a:
            id = idd[0]
            try:
                await bot.send_message(id, f'{msg.text[9:]}')
            except:
                pass
        await msg.reply('Закончил')
    else:
        await msg.reply('Пошел нахуй')
        return

@dp.message_handler(commands=['рассылка_важная'])
async def рассылкабеать(msg: t.Message):
    if msg.from_user.id in OWNER:
        a = rasulkaforuser()
        for idd in a:
            id = idd[0]
            try:
                await bot.send_message(id, f'{msg.text[17:]}')
            except:
                pass
        await msg.reply('Закончил')
    else:
        await msg.reply('Пошел нахуй')
        return

@dp.message_handler(commands=['чеканал'])
async def msgfgggh(msg: t.Message):
    if msg.from_user.id in OWNER:
        id = (msg.text).split('анал ')[1]
        print(id)
        chat = await bot.get_chat(id)
        memb = await bot.get_chat_member_count(id)
        await msg.reply(f'{chat["title"]}\n{memb}\n{chat["username"]}')
    else:
        await msg.reply('Ограничено')
        return

@dp.message_handler(commands=['прем'], commands_prefix=['-'])
async def givepremi(msg: t.Message):
    if not msg.from_user.id in OWNER:
        await msg.answer('Вам это недоступно.')
        return
    try:
        iduser = (msg.text).split(' ')[1]
    except IndexError:
        await msg.answer('Вы не указали аргументы')
        return

    a = take_premium(iduser)
    if a == 'have':
        await msg.reply('У пользователя и так нет подписки!')
        return
    if a == 'ok':
        await msg.reply('Подписка успешно снята!')

@dp.message_handler(commands=['прем'], commands_prefix=['+'])
async def givepremi(msg: t.Message):
    if not msg.from_user.id in OWNER:
        await msg.answer('Вам это недоступно.')
        return
    try:
        iduser = (msg.text).split(' ')[1]
    except IndexError:
        await msg.answer('Вы не указали аргументы')
        return

    a = give_premium(iduser)
    if a == 'have':
        await msg.reply('У пользователя уже есть PREMIUM!')
        return
    if a == 'ok':
        await msg.reply('✨ Подписка успешно выдана!')
        await bot.send_message(iduser, '✨ Вам выдали подписку <b><i>AgainstReid Premium</i></b> на месяц!')
        return

def vybar(ch, h):
    t = random.choice(ch)
    if t == h:
        return vybar(ch, h)
    else:
        return t

@dp.callback_query_handler(lambda call: True)
async def handler_call(call: t.CallbackQuery):
    f = await bot.get_chat_member(chat_id=CHANNEL, user_id=call.from_user.id)
    if f["status"] == ('left' or 'kicked'):
        await call.message.answer(f'''
🗣 <b>Чтобы использовать бота, подпишитесь на канал!</b>

Чтобы использовать нашего бота и защищать свой канал - подпишитесь на наш канал {CHANNELNAME}
        ''')
        return
    if (call.data).startswith('Settings'):
        if check_is_channels(call.from_user.id) == 'no':
            keyboard = t.InlineKeyboardMarkup(row_width=1)
            keyboard.add(t.InlineKeyboardButton(text="➕ Добавить канал", callback_data="channelsadd"))
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='💾 <b>У вас пока что нет каналов!</b>\n\nВы можете добавить их с помощью кнопки ниже.', reply_markup=keyboard)
            return
        if check_is_channels(call.from_user.id) == 'yes':
            ch = all_channels_user(call.from_user.id)
            keyboard = t.InlineKeyboardMarkup(row_width=1)
            print(ch)
            try:
                for idd in ch:
                    id = idd[0]
                    try:
                        chat = await bot.get_chat(id)
                    except Exception as e:
                        print(e)
                        await call.message.reply(f'🪫 Произошла ошибка при получении данных канала {id}. Канал  удален из базы данных.\nЕсли у вас есть другие каналы, то вы можете зайти в это меню еще раз.\n\nЕсть вопросы? Обратитесь t.me/AgainstReidChat')
                        remove_channel(id)
                        return
                    title = chat["title"]
                    keyboard.add(t.InlineKeyboardButton(text=f"{title}", callback_data=f"setts_{id}"))
                keyboard.add(t.InlineKeyboardButton(text="➕ Добавить канал", callback_data="channelsadd"))
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='📲 <b>Управление вашими каналами</b>\n\nНажмите на кнопку с названием канала, который хотите настроить.', reply_markup=keyboard)
            except:
                await call.message.answer('Произошла ошибка, попробуйте еще раз!')
                return
 
    if (call.data).startswith('Report'):
        idanket = (call.data).split('_')[1]
        await call.message.answer(f'Чтобы пожаловаться на анкету:\n\n1. Зайдите в чат поддержки бота - @AgainstReidChat\n\n2. Укажите айди анкеты - <pre>{idanket}</pre>\n\n3. Опишите, что не так с этой анкетой\n\n4. Ожидайте ответа агентов')
        await call.answer()

    if (call.data).startswith('AcceptAnket'):
        id = (call.data).split('_')[1]
        accept_anket(id)
        await call.message.reply('Анкета успешно принята!')
        await bot.send_message(id, f'✅ Ваша анкета на бирже админов успешно принята!')

    if (call.data).startswith('DeclineAnket'):
        id = (call.data).split('_')[1]
        await call.message.reply('Анкета успешно отклонята!')
        await bot.send_message(id, '❌ Ваша анкета на бирже админов отклонята! Прочитайте <a href="https://t.me/AgainstReid_Useful/10">правила анкет</a> и можете пересоздать анкету!', disable_web_page_preview=True)

    if (call.data).startswith('BanAnketa'):
        id = (call.data).split('_')[1]
        ban_anket(id)
        await call.message.reply('Анкета успешно забанена!')
        await bot.send_message(id, '🚫 Ваша анкета на бирже админов заблокирована! Вы не сможете больше создать анкету!')

    if (call.data).startswith('DisLikeAnket'):
        idanket = (call.data).split('_')[1]
        set_skiped(add_value_to_string(get_spisok_skip(call.from_user.id)[0], idanket), call.from_user.id)
        if (call.data).split('_')[2] == 'end':
            await call.message.answer('Анкет больше нет. Зайдите на биржу позже.\n\nВАЖНО: Чуть позже обязательно зайдите через команду /start, то есть введите /start, выберите "биржа", далее "поиск админов".')
            return
        a = get_all_ankets()
        o = []
        if a == 0:
            await call.message.answer('Анкет на данный момент нет.')
            await call.answer()
            return
        liked = string_to_list(get_spisok(call.from_user.id)[0])
        skiped = string_to_list(get_spisok_skip(call.from_user.id)[0])

        for ls in a:
            id = ls[0]
            if not id in liked and not id in skiped:
                o.append(id)
            else:
                pass
        try:
            ida = random.choice(o)
        except RecursionError:
            ida = o[0]
        try:
            g = vybar(o, ida)
            keyboard = t.InlineKeyboardMarkup(row_width=3)
            buttons = [
                t.InlineKeyboardButton(text="👍🏻", callback_data=f"LikeAnket_{ida}_no"),
                t.InlineKeyboardButton(text="👎🏻", callback_data=f"DisLikeAnket_{ida}_no"),
                t.InlineKeyboardButton(text="⚠️", callback_data=f"Report_{ida}"),
            ]
            keyboard.add(*buttons)
        except RecursionError:
            keyboard = t.InlineKeyboardMarkup(row_width=3)
            buttons = [
                t.InlineKeyboardButton(text="👍🏻", callback_data=f"LikeAnket_{ida}_end"),
                t.InlineKeyboardButton(text="👎🏻", callback_data=f"DisLikeAnket_{ida}_end"),
                t.InlineKeyboardButton(text="⚠️", callback_data=f"Report_{ida}_end"),
            ]
            keyboard.add(*buttons)
            await call.message.answer('Это последняя анкета:')
        data = get_anketa_id(ida)

        await call.message.answer(f'''
🎊 <b>Найдена следующая анкета:</b>

📍 {data[5]}
📝 {data[2]}
            ''', reply_markup=keyboard)
        await call.answer()


    if (call.data).startswith('LikeAnket'):
        idanket = (call.data).split('_')[1]
        set_liked(add_value_to_string(get_spisok(call.from_user.id)[0], idanket), call.from_user.id)
        dat = get_anketa_id(int(idanket))
        userid = dat[0]
        chat_member = await bot.get_chat_member(chat_id=CHANNEL, user_id=userid)
        username = chat_member.user.username 
        if username == ('None' or None):
            keyboard = t.InlineKeyboardMarkup(row_width=3)
            keyboard.add(t.InlineKeyboardButton(text="Написать", url=f"tg://openmessage?user_id={dat[0]}"))
            await call.message.answer(f'Отлично! Теперь вы можете написать <a href="tg://openmessage?user_id={dat[0]}">{dat[5]}</a>', reply_markup=keyboard)
        else:
            await call.message.answer(f'Отлично! Теперь вы можете написать <b>{dat[5]}</b> - @{username}')
        if (call.data).split('_')[2] == 'end':
            return
        a = get_all_ankets()
        o = []
        if a == 0:
            await call.message.answer('Анкет на данный момент нет.')
            await call.answer()
            return
        liked = string_to_list(get_spisok(call.from_user.id)[0])
        skiped = string_to_list(get_spisok_skip(call.from_user.id)[0])

        for ls in a:
            id = ls[0]
            if not id in liked and not id in skiped:
                o.append(id)
            else:
                pass
        print(o)
        try:
            ida = random.choice(o)
        except RecursionError:
            ida = o[0]
        try:
            g = vybar(o, ida)
            keyboard = t.InlineKeyboardMarkup(row_width=3)
            buttons = [
                t.InlineKeyboardButton(text="👍🏻", callback_data=f"LikeAnket_{ida}_no"),
                t.InlineKeyboardButton(text="👎🏻", callback_data=f"DisLikeAnket_{ida}_no"),
                t.InlineKeyboardButton(text="⚠️", callback_data=f"Report_{ida}"),
            ]
            keyboard.add(*buttons)
        except RecursionError:
            keyboard = t.InlineKeyboardMarkup(row_width=3)
            buttons = [
                t.InlineKeyboardButton(text="👍🏻", callback_data=f"LikeAnket_{ida}_end"),
                t.InlineKeyboardButton(text="👎🏻", callback_data=f"DisLikeAnket_{ida}_end"),
                t.InlineKeyboardButton(text="⚠️", callback_data=f"Report_{ida}_end"),
            ]
            keyboard.add(*buttons)
            await call.message.answer('Это последняя анкета:')
        data = get_anketa_id(ida)

        await call.message.answer(f'''
🎊 <b>Найдена следующая анкета:</b>

📍 {data[5]}
📝 {data[2]}
            ''', reply_markup=keyboard)
        await call.answer()

    if (call.data).startswith('SearchAdm'):
        a = get_all_ankets()
        o = []
        if a == 0:
            await call.message.answer('Анкет на данный момент нет.')
            await call.answer()
            return
        liked = string_to_list(get_spisok(call.from_user.id)[0])
        skiped = string_to_list(get_spisok_skip(call.from_user.id)[0])

        for ls in a:
            id = ls[0]
            if not id in liked and not id in skiped:
                o.append(id)
            else:
                pass
        print(o)
        try:
            ida = random.choice(o)
        except RecursionError:
            ida = o[0]
        try:
            g = vybar(o, ida)
            keyboard = t.InlineKeyboardMarkup(row_width=3)
            buttons = [
                t.InlineKeyboardButton(text="👍🏻", callback_data=f"LikeAnket_{ida}_no"),
                t.InlineKeyboardButton(text="👎🏻", callback_data=f"DisLikeAnket_{ida}_no"),
                t.InlineKeyboardButton(text="⚠️", callback_data=f"Report_{ida}"),
            ]
            keyboard.add(*buttons)
        except RecursionError:
            keyboard = t.InlineKeyboardMarkup(row_width=3)
            buttons = [
                t.InlineKeyboardButton(text="👍🏻", callback_data=f"LikeAnket_{ida}_end"),
                t.InlineKeyboardButton(text="👎🏻", callback_data=f"DisLikeAnket_{ida}_end"),
                t.InlineKeyboardButton(text="⚠️", callback_data=f"Report_{ida}"),
            ]
            keyboard.add(*buttons)
            await call.message.answer('Это последняя анкета:')
        data = get_anketa_id(ida)

        await call.message.answer(f'''
🎊 <b>Найдена следующая анкета:</b>

📍 {data[5]}
📝 {data[2]}
            ''', reply_markup=keyboard)
        await call.answer()
 
    if (call.data).startswith('Birza'):
        if check_ownerbirza(call.from_user.id) == False:
            create_ownerbirza(call.from_user.id)
        keyboard = t.InlineKeyboardMarkup(row_width=1)
        buttons = [
            t.InlineKeyboardButton(text="👨🏼‍💻 Пойти админом", callback_data=f"GoAdmin"),
            t.InlineKeyboardButton(text="🔎 Найти админа", callback_data=f"SearchAdm"),
        ]
        keyboard.add(*buttons)
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'''
🔭 <b>Биржа админов</b>

Это безопасный способ найти админов на свой канал или найти канал, на который можно пойти работать.
Здесь потенциальные админы могут оставить анкету и владельцы каналов могут взять их на свои каналы.

Все анкеты проверяются вручную модераторами бота, а также блокируются подозрительные или нарушающие правила.
            ''', reply_markup=keyboard)

    if (call.data).startswith('CreateAnketa'):
        if yes_li_reid(call.from_user.id) == 'yes':
            await call.message.answer('А что делать рейдерам на бирже админов? Ты рейдер!\n\nСчитаете ошибкой? Пишите @AgainstReidChat')
            return
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Отмена'))
        await bot.send_message(chat_id=call.message.chat.id, text=f'Отлично! Приступим к созданию анкеты!\n\nПервым делом укажи свое имя/псевдоним. Не более 32 символов.', reply_markup=keyboard)
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        await dia.await_name.set()
    if (call.data).startswith('GoAdmin'):
        keyboard = t.InlineKeyboardMarkup(row_width=1)
        if is_li_anketa(call.from_user.id) == False:
            keyboard.add(t.InlineKeyboardButton(text="Создать анкету", callback_data=f"CreateAnketa"))
            await call.answer()
            await call.message.answer('У вас еще нет анкеты! Вы можете её создать, нажав на кнопку ниже.\n\nПравила для анкет: t.me/AgainstReid_Useful/10', reply_markup=keyboard, disable_web_page_preview=True)
        if is_li_anketa(call.from_user.id) == True:
            keyboard.add(t.InlineKeyboardButton(text="Удалить анкету", callback_data=f"ConfirmDeleteAnket"))
            anketa = get_anketa(call.from_user.id, None)
            await call.message.answer(f'''
<b>Твоя анкета выглядит так:</b>

{anketa[5]}
{anketa[2]}
                ''', reply_markup=keyboard)
            await call.answer()

    if (call.data).startswith('ConfirmDeleteAnket'):
        a = get_anketa(call.from_user.id, None)
        if a[1] == 2:
            await call.message.answer('Ошибка! Ваша анкета заблокирована! Вы не можете её удалить или изменить.')
            return
        delete_anket(call.from_user.id)
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'''
🗑 <b>Ваша анкета успешно удалена!</b>

Вы можете создать новую в любой момент.
            ''')

    if (call.data).startswith('channelsadd'):
        keyboard = t.InlineKeyboardMarkup(row_width=1)
        keyboard.add(t.InlineKeyboardButton(text="Отмена", callback_data="CancelFsm"))
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='''
🔧 <b>Добавление канала</b>

Чтобы добавить канал, следуйте инструкции:
1. Добавьте бота в администраторы канала со всеми правами
2. Скиньте ссылку на канал (только публичный канал), если у вас приватный канал, то перешлите любое сообщение из канала
3. Если вы сделали все правильно, то канал добавлен!

Видео-инструкция - https://t.me/AgainstReid/126
        ''')
        await dia.chan.set()
    if (call.data).startswith('setts'):
        id = (call.data).split('_')[1]
        try:
            perms = await bot.get_chat_member(chat_id=id, user_id=bot.id)
            if perms["can_delete_messages"] != True or perms["can_promote_members"] != True or perms["can_change_info"] != True or perms["can_invite_users"] != True or perms["can_post_messages"] != True or perms["can_edit_messages"] != True:
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='''
❌ <b>У бота нет всех необходимых прав!</b>

Похоже, что у бота нет всех прав в канале. Бот покинул канал.
Вы можете добавить канал еще раз.

Есть вопросы? Пишите t.me/AgainstReidChat
                 ''')
                return
        except UnicodeEncodeError as e:
            pass
        except:
            await call.message.answer(f'🪫 Произошла ошибка при получении данных канала {id}. Канал  удален из базы данных.\nЕсли у вас есть другие каналы, то вы можете зайти в это меню еще раз.\n\nЕсть вопросы? Обратитесь t.me/AgainstReidChat')
            try:
                remove_channel(id)
                await bot.leave_chat(id)
            except:
                remove_channel(id)
                pass
            return
        
        chat = await bot.get_chat(id)
        keyboard = t.InlineKeyboardMarkup(row_width=1)
        buttons = [
            t.InlineKeyboardButton(text="📃 Информация о канале", callback_data=f"StatChannel_{id}"),
            t.InlineKeyboardButton(text="🎛 Режим защиты", callback_data=f"CoreChannel_{id}"),
            t.InlineKeyboardButton(text="👨🏼‍💻 Администраторы", callback_data=f"AdminsChannel_{id}"),
            t.InlineKeyboardButton(text="🔬 Личные настройки", callback_data=f"LSett_{id}"),
            t.InlineKeyboardButton(text="🗑 Удалить канал", callback_data=f"DeleteChannel_{id}"),
        ]
        keyboard.add(*buttons)
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'''
🔩 <b>Управление каналом</b> «{chat['title']}»

Используйте кнопки ниже для управлением вашим каналом.

Остались вопросы? Обратитесь t.me/AgainstReidChat
        ''', reply_markup=keyboard, disable_web_page_preview=True)

    if (call.data).startswith('LSett'):
        if get_premium(call.from_user.id) == 0:
            await call.message.answer('✨ Эта функция доступна только <i><b>Premium</b> пользователям</i>!\nПодробнее — /premium')
            await call.answer()
            return
        id = (call.data).split('_')[1]
        try:
            perms = await bot.get_chat_member(chat_id=id, user_id=bot.id)
            if perms["can_delete_messages"] != True or perms["can_promote_members"] != True or perms["can_change_info"] != True or perms["can_invite_users"] != True or perms["can_post_messages"] != True or perms["can_edit_messages"] != True:
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='''
❌ <b>У бота нет всех необходимых прав!</b>

Похоже, что у бота нет всех прав в канале. Бот покинул канал.
Вы можете добавить канал еще раз.

Есть вопросы? Пишите t.me/AgainstReidChat
                 ''')
                return
        except UnicodeEncodeError as e:
            pass
        except Exception as e:
            print(e)
            await call.message.answer(f'🪫 Произошла ошибка при получении данных канала {id}. Канал  удален из базы данных.\nЕсли у вас есть другие каналы, то вы можете зайти в это меню еще раз.\n\nЕсть вопросы? Обратитесь t.me/AgainstReidChat')
            try:
                remove_channel(id)
                await bot.leave_chat(id)
            except:
                remove_channel(id)
                pass
            return

        chat = await bot.get_chat(id)
        keyboard = t.InlineKeyboardMarkup(row_width=1)
        buttons = [
            t.InlineKeyboardButton(text="📨 Уведомления о блокировке", callback_data=f"lnotificationbans_{id}"),
        ]
        keyboard.add(*buttons)
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='''
📫 <b>Личные настройки</b>

<i>Личные настройки — это настройки, которые никак не повлияют на работу защиты вашего канала, а лишь улучшат использование Вами нашего бота.</i>

Уведомления о блокировке — этот пункт означает, что бот будет сообщать вам о блокировке рейдеров на этом канале, если пункт включён. По умолчанию включено.
            ''', reply_markup=keyboard)

    if (call.data).startswith('lnotificationbans'):
        id = (call.data).split('_')[1]
        try:
            perms = await bot.get_chat_member(chat_id=id, user_id=bot.id)
            if perms["can_delete_messages"] != True or perms["can_promote_members"] != True or perms["can_change_info"] != True or perms["can_invite_users"] != True or perms["can_post_messages"] != True or perms["can_edit_messages"] != True:
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='''
❌ <b>У бота нет всех необходимых прав!</b>

Похоже, что у бота нет всех прав в канале. Бот покинул канал.
Вы можете добавить канал еще раз.

Есть вопросы? Пишите t.me/AgainstReidChat
                 ''')
                return
        except UnicodeEncodeError as e:
            pass
        except Exception as e:
            print(e)
            await call.message.answer(f'🪫 Произошла ошибка при получении данных канала {id}. Канал  удален из базы данных.\nЕсли у вас есть другие каналы, то вы можете зайти в это меню еще раз.\n\nЕсть вопросы? Обратитесь t.me/AgainstReidChat')
            try:
                remove_channel(id)
                await bot.leave_chat(id)
            except:
                remove_channel(id)
                pass
            return

        if get_notifi(int(id))[0] == 1:
            set_notifi(int(id), 0)
            await call.answer(text='❎ Уведомления о блокировке рейдеров успешно выключены!', show_alert=True)
            return
        if get_notifi(int(id))[0] == 0:
            set_notifi(int(id), 1)
            await call.answer(text='✅ Уведомления о блокировке рейдеров успешно включены!', show_alert=True)
            return


    if (call.data).startswith('AdminsChannel'):
        id = (call.data).split('_')[1]
        try:
            perms = await bot.get_chat_member(chat_id=id, user_id=bot.id)
            if perms["can_delete_messages"] != True or perms["can_promote_members"] != True or perms["can_change_info"] != True or perms["can_invite_users"] != True or perms["can_post_messages"] != True or perms["can_edit_messages"] != True:
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='''
❌ <b>У бота нет всех необходимых прав!</b>

Похоже, что у бота нет всех прав в канале. Бот покинул канал.
Вы можете добавить канал еще раз.

Есть вопросы? Пишите t.me/AgainstReidChat
                 ''')
                return
        except UnicodeEncodeError as e:
            pass
        except Exception as e:
            print(e)
            await call.message.answer(f'🪫 Произошла ошибка при получении данных канала {id}. Канал  удален из базы данных.\nЕсли у вас есть другие каналы, то вы можете зайти в это меню еще раз.\n\nЕсть вопросы? Обратитесь t.me/AgainstReidChat')
            try:
                remove_channel(id)
                await bot.leave_chat(id)
            except:
                remove_channel(id)
                pass
            return
        chat = await bot.get_chat(id)
        keyboard = t.InlineKeyboardMarkup(row_width=1)
        buttons = [
            t.InlineKeyboardButton(text="🌐 Список администраторов", callback_data=f"ListAdminsChannel_{id}"),
            t.InlineKeyboardButton(text="➕ Добавить администратора", callback_data=f"AddAdminChannel_{id}"),
            t.InlineKeyboardButton(text="🔇 Снятие админа на ночь", callback_data=f"NightAdminsChannel_{id}"),
        ]
        keyboard.add(*buttons)
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'''
👨🏼‍💻 <b>Администраторы канала</b> «{chat["title"]}»

🔰 Администраторы канала в боте — это один из самых надежных способов защиты вашего канала!

ℹ️ На данный момент, вы можете включить функцию <b>Снятие админов на ночь</b> и бот будет снимать админов на ночь, а утром возвращать права, которые были у пользователя.

💤 В следующих обновлениях планируется добавить функцию отправки сообщений в канал через бота без админки на самом канале.
        ''', reply_markup=keyboard) 

    if (call.data).startswith('NightAdminsChannel'):
        id = (call.data).split('_')[1]
        try:
            perms = await bot.get_chat_member(chat_id=id, user_id=bot.id)
            if perms["can_delete_messages"] != True or perms["can_promote_members"] != True or perms["can_change_info"] != True or perms["can_invite_users"] != True or perms["can_post_messages"] != True or perms["can_edit_messages"] != True:
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='''
❌ <b>У бота нет всех необходимых прав!</b>

Похоже, что у бота нет всех прав в канале. Бот покинул канал.
Вы можете добавить канал еще раз.

Есть вопросы? Пишите t.me/AgainstReidChat
                 ''')
                return
        except UnicodeEncodeError as e:
            pass
        except Exception as e:
            print(e)
            await call.message.answer(f'🪫 Произошла ошибка при получении данных канала {id}. Канал  удален из базы данных.\nЕсли у вас есть другие каналы, то вы можете зайти в это меню еще раз.\n\nЕсть вопросы? Обратитесь t.me/AgainstReidChat')
            try:
                remove_channel(id)
                await bot.leave_chat(id)
            except:
                remove_channel(id)
                pass
            return
        
        if get_night(id) == 1:
            await call.answer(text='❌ Снятие админов на ночь успешно выключено!', show_alert=True)
            set_night(id, 0)
            return
        if get_night(id) == 0:
            await call.answer(text='✅ Снятие админов на ночь успешно включено!', show_alert=True)
            set_night(id, 1)
            return


    if (call.data).startswith('AddAdminChannel'):
        id = (call.data).split('_')[1]
        try:
            perms = await bot.get_chat_member(chat_id=id, user_id=bot.id)
            if perms["can_delete_messages"] != True or perms["can_promote_members"] != True or perms["can_change_info"] != True or perms["can_invite_users"] != True or perms["can_post_messages"] != True or perms["can_edit_messages"] != True:
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='''
❌ <b>У бота нет всех необходимых прав!</b>

Похоже, что у бота нет всех прав в канале. Бот покинул канал.
Вы можете добавить канал еще раз.

Есть вопросы? Пишите t.me/AgainstReidChat
                 ''')
                return
        except UnicodeEncodeError as e:
            pass
        except Exception as e:
            print(e)
            await call.message.answer(f'🪫 Произошла ошибка при получении данных канала {id}. Канал  удален из базы данных.\nЕсли у вас есть другие каналы, то вы можете зайти в это меню еще раз.\n\nЕсть вопросы? Обратитесь t.me/AgainstReidChat')
            try:
                remove_channel(id)
                await bot.leave_chat(id)
            except:
                remove_channel(id)
                pass
            return
        linked = await get_start_link(str(create_link_refer(id, call.from_user.id)), encode=True)
        keyboard = t.InlineKeyboardMarkup(row_width=1)
        keyboard.add(t.InlineKeyboardButton(text=f"Сбросить ссылку-приглашение", callback_data=f"Reset_{id}_{(linked).split('=')[1]}"))

        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'''
➕ <b>Добавление администратора в канал</b>

📒 Чтобы добавить пользователя как администратора в ваш канал, скопируйте (для этого просто нажмите на текст) ссылку ниже и отправьте её человеку, которого хотите назначить.

📎 Пригласительная ссылка (Нажмите, чтобы скопировать):
<pre>{linked}</pre>

⚠️ <u>Будьте осторожны и не давайте эту ссылку кому-попало!</u>

ℹ️ Когда человек перейдет по ссылке, то бот добавить его в администраторы канала (человек сможет даже удалить подписчиков) с правами <b>создавать пригласительные ссылки</b>, <b>публиковать сообщения</b> и <b>изменять сообщения</b>.
Вы сможете также в любой момент времени изменить права человека через бота. Бот сообщит вам о том, что человек назначен администратором.

🗑 Вы можете сбросить ссылку с помощью кнопки ниже.

💬 Остались вопросы? Наш чат поддержки — t.me/AgainstReidChat
        ''', disable_web_page_preview=True, reply_markup=keyboard)

    if (call.data).startswith('Reset'):
        id = (call.data).split('_')[1]

        try:
            perms = await bot.get_chat_member(chat_id=id, user_id=bot.id)
            if perms["can_delete_messages"] != True or perms["can_promote_members"] != True or perms["can_change_info"] != True or perms["can_invite_users"] != True or perms["can_post_messages"] != True or perms["can_edit_messages"] != True:
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='''
❌ <b>У бота нет всех необходимых прав!</b>

Похоже, что у бота нет всех прав в канале. Бот покинул канал.
Вы можете добавить канал еще раз.

Есть вопросы? Пишите t.me/AgainstReidChat
                 ''')
                return
        except UnicodeEncodeError as e:
            pass
        except Exception as e:
            print(e)
            await call.message.answer(f'🪫 Произошла ошибка при получении данных канала {id}. Канал  удален из базы данных.\nЕсли у вас есть другие каналы, то вы можете зайти в это меню еще раз.\n\nЕсть вопросы? Обратитесь t.me/AgainstReidChat')
            try:
                remove_channel(id)
                await bot.leave_chat(id)
            except:
                remove_channel(id)
                pass
            return
        
        lin = (call.data).split('_')[2]
        link = decode_payload(lin)
        reset_link(link)

        linked = await get_start_link(str(create_link_refer(id, call.from_user.id)), encode=True)
        keyboard = t.InlineKeyboardMarkup(row_width=1)
        keyboard.add(t.InlineKeyboardButton(text=f"Сбросить ссылку-приглашение", callback_data=f"Reset_{id}_{(linked).split('=')[1]}"))

        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'''
➕ <b>Добавление администратора в канал</b>

📒 Чтобы добавить пользователя как администратора в ваш канал, скопируйте (для этого просто нажмите на текст) ссылку ниже и отправьте её человеку, которого хотите назначить.
🎥 Видео-инструкция — t.me/AgainstReid_Useful/7

📎 Пригласительная ссылка (Нажмите, чтобы скопировать):
<pre>{linked}</pre>

⚠️ <u>Будьте осторожны и не давайте эту ссылку кому-попало!</u>

ℹ️ Когда человек перейдет по ссылке, то бот добавить его в администраторы канала (человек сможет даже удалить подписчиков) с правами <b>создавать пригласительные ссылки</b>, <b>публиковать сообщения</b> и <b>изменять сообщения</b>.
Вы сможете также в любой момент времени изменить права человека через бота. Бот сообщит вам о том, что человек назначен администратором.

🗑 Вы можете сбросить ссылку с помощью кнопки ниже.

💬 Остались вопросы? Наш чат поддержки — t.me/AgainstReidChat
        ''', disable_web_page_preview=True, reply_markup=keyboard)

    if (call.data).startswith('ListAdminsChannel'):
        id = (call.data).split('_')[1]
        try:
            perms = await bot.get_chat_member(chat_id=id, user_id=bot.id)
            if perms["can_delete_messages"] != True or perms["can_promote_members"] != True or perms["can_change_info"] != True or perms["can_invite_users"] != True or perms["can_post_messages"] != True or perms["can_edit_messages"] != True:
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='''
❌ <b>У бота нет всех необходимых прав!</b>

Похоже, что у бота нет всех прав в канале. Бот покинул канал.
Вы можете добавить канал еще раз.

Есть вопросы? Пишите t.me/AgainstReidChat
                 ''')
                return
        except UnicodeEncodeError as e:
            pass
        except Exception as e:
            print(e)
            await call.message.answer(f'🪫 Произошла ошибка при получении данных канала {id}. Канал  удален из базы данных.\nЕсли у вас есть другие каналы, то вы можете зайти в это меню еще раз.\n\nЕсть вопросы? Обратитесь t.me/AgainstReidChat')
            try:
                remove_channel(id)
                await bot.leave_chat(id)
            except:
                remove_channel(id)
                pass
            return
        try:
            if get_all_admins(id) == None or len(get_all_admins(id)) == 0:
                await call.answer(text='❎ У вас нет администраторов!', show_alert=True)
                return
        except:
            await call.answer(text='❎ У вас нет администраторов!', show_alert=True)
            return

        keyboard = t.InlineKeyboardMarkup(row_width=1)
        for g in get_all_admins(id):
            user = await bot.get_chat_member(id, g[0])
            keyboard.add(t.InlineKeyboardButton(text=f"{user.user.full_name}", callback_data=f"UserAdmin_{id}_{g[0]}"))

        await call.message.answer('🌐 <b>Список всех администраторов, добавленных через бота</b>\n\nℹ️ <i>Нажмите на администратора, чтобы управлять им: снять, изменить права или заблокировать.</i>', reply_markup=keyboard)

    if (call.data).startswith('UserAdmin'):
        id = (call.data).split('_')[1]
        user_id = (call.data).split('_')[2]
        try:
            perms = await bot.get_chat_member(chat_id=id, user_id=bot.id)
            if perms["can_delete_messages"] != True or perms["can_promote_members"] != True or perms["can_change_info"] != True or perms["can_invite_users"] != True or perms["can_post_messages"] != True or perms["can_edit_messages"] != True:
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='''
❌ <b>У бота нет всех необходимых прав!</b>

Похоже, что у бота нет всех прав в канале. Бот покинул канал.
Вы можете добавить канал еще раз.

Есть вопросы? Пишите t.me/AgainstReidChat
                 ''')
                return
        except UnicodeEncodeError as e:
            pass
        except Exception as e:
            print(e)
            await call.message.answer(f'🪫 Произошла ошибка при получении данных канала {id}. Канал  удален из базы данных.\nЕсли у вас есть другие каналы, то вы можете зайти в это меню еще раз.\n\nЕсть вопросы? Обратитесь t.me/AgainstReidChat')
            try:
                remove_channel(id)
                await bot.leave_chat(id)
            except:
                remove_channel(id)
                pass
            return

        try:
            user_check = await bot.get_chat_member(chat_id=id, user_id=user_id)
        except:
            await call.message.answer('Пользователь отписался от канала, бот не может получить информацию.\nПользователь удален из базы админов вашего канала.')
            remove_admin(user_id, id)
            return
        
        if user_check.status == ('administrator' or 'creator'):
            statusvkanale = '🚀 У этого пользователя есть права администратора в канале'
        if user_check.status == 'member':
            statusvkanale = '🌧 У этого пользователя нет прав администратора в канале'
        if user_check.status == 'left':
            statusvkanale = '❗️ Пользователь не подписан на канал'
        if user_check.status == 'kicked':
            statusvkanale = '‼️ Пользователь заблокирован в канале'

        data = get_info_admin(int(id), int(user_id))
        if data[2] == True:
            permsdelete = '✅ Удаление сообщений'
        if data[2] == False:
            permsdelete = '❌ Удаление сообщений'

        if data[3] == True:
            permspromote = '✅ Назначение новых администраторов'
        if data[3] == False:
            permspromote = '❌ Назначение новых администраторов'

        if data[4] == True:
            permschange = '✅ Изменение информации о канале'
        if data[4] == False:
            permschange = '❌ Изменение информации о канале'

        if data[5] == True:
            permsinvite = '✅ Приглашение пользователей'
        if data[5] == False:
            permsinvite = '❌ Приглашение пользователей'

        if data[6] == True:
            permssend = '✅ Публикация сообщений'
        if data[6] == False:
            permssend = '❌ Публикация сообщений'

        if data[7] == True:
            permsedit = '✅ Изменение сообщений'
        if data[7] == False:
            permsedit = '❌ Изменение сообщений'

        if check_agent(int(user_id)) == 'yes':
            agent = '\n\n👨🏼‍💻 <i>Пользователь является агентом <a href="https://t.me/AgainstReidChat">поддержки бота.</a></i>'
        if check_agent(int(user_id)) == 'no':
            agent = ' '
        keyboard = t.InlineKeyboardMarkup(row_width=1)
        buttons = [
            t.InlineKeyboardButton(text="➖ Снять пользователя", callback_data=f"UnPromote_{id}_{user_id}"),
            t.InlineKeyboardButton(text="🔨 Заблокировать пользователя", callback_data=f"banuser_{id}_{user_id}"),
        ]
        keyboard.add(*buttons)

        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'''
🗃 <b>Информация и управление админом</b> «{user_check.user.full_name} (@{user_check.user.username})»{agent}

{statusvkanale}

🍸 Пользователь назначен администратором <b>{data[10]}</b>
🔰 <u><b>Права пользователя (установленные в боте):</b></u>
{permschange}
{permsinvite}
{permspromote}
{permsdelete}
{permssend}
{permsedit}

ℹ️ Используйте кнопки ниже для управления пользователем.
        ''', reply_markup=keyboard, disable_web_page_preview=True)

    if (call.data).startswith('banuser'):
        id = (call.data).split('_')[1]
        user_id = (call.data).split('_')[2]
        try:
            perms = await bot.get_chat_member(chat_id=id, user_id=bot.id)
            if perms["can_delete_messages"] != True or perms["can_promote_members"] != True or perms["can_change_info"] != True or perms["can_invite_users"] != True or perms["can_post_messages"] != True or perms["can_edit_messages"] != True:
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='''
❌ <b>У бота нет всех необходимых прав!</b>

Похоже, что у бота нет всех прав в канале. Бот покинул канал.
Вы можете добавить канал еще раз.

Есть вопросы? Пишите t.me/AgainstReidChat
                 ''')
                return
        except UnicodeEncodeError as e:
            pass
        except Exception as e:
            print(e)
            await call.message.answer(f'🪫 Произошла ошибка при получении данных канала {id}. Канал  удален из базы данных.\nЕсли у вас есть другие каналы, то вы можете зайти в это меню еще раз.\n\nЕсть вопросы? Обратитесь t.me/AgainstReidChat')
            try:
                remove_channel(id)
                await bot.leave_chat(id)
            except:
                remove_channel(id)
                pass
            return

        try:
            user_check = await bot.get_chat_member(chat_id=id, user_id=user_id)
        except:
            await call.message.answer('Пользователь отписался от канала, бот не может получить информацию.\nПользователь удален из базы админов вашего канала.')
            remove_admin(user_id, id)
            return

        if user_check.status == 'administrator':
            remove_admin(user_id, id)
            await bot.promote_chat_member(can_manage_chat=False, can_change_info=False, can_delete_messages=False, can_edit_messages=False, can_invite_users=False, can_post_messages=False, can_promote_members=False, chat_id=id, user_id=user_id)
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='''
❎ Администратор успешно снят с прав администратора и удален из базы админов вашего канала, а также заблокирован!
            ''')
            await bot.ban_chat_member(chat_id=id, user_id=user_id)
            return
        if user_check.status != 'administrator':
            remove_admin(user_id, id)
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='''
❎ Администратор успешно удален из базы админов вашего канала и заблокирован!
            ''')
            await bot.ban_chat_member(chat_id=id, user_id=user_id)
            return


    if (call.data).startswith('UnPromote'):
        id = (call.data).split('_')[1]
        user_id = (call.data).split('_')[2]
        try:
            perms = await bot.get_chat_member(chat_id=id, user_id=bot.id)
            if perms["can_delete_messages"] != True or perms["can_promote_members"] != True or perms["can_change_info"] != True or perms["can_invite_users"] != True or perms["can_post_messages"] != True or perms["can_edit_messages"] != True:
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='''
❌ <b>У бота нет всех необходимых прав!</b>

Похоже, что у бота нет всех прав в канале. Бот покинул канал.
Вы можете добавить канал еще раз.

Есть вопросы? Пишите t.me/AgainstReidChat
                 ''')
                return
        except UnicodeEncodeError as e:
            pass
        except Exception as e:
            print(e)
            await call.message.answer(f'🪫 Произошла ошибка при получении данных канала {id}. Канал  удален из базы данных.\nЕсли у вас есть другие каналы, то вы можете зайти в это меню еще раз.\n\nЕсть вопросы? Обратитесь t.me/AgainstReidChat')
            try:
                remove_channel(id)
                await bot.leave_chat(id)
            except:
                remove_channel(id)
                pass
            return

        try:
            user_check = await bot.get_chat_member(chat_id=id, user_id=user_id)
        except:
            await call.message.answer('Пользователь отписался от канала, бот не может получить информацию.\nПользователь удален из базы админов вашего канала.')
            remove_admin(user_id, id)
            return

        if user_check.status == 'administrator':
            remove_admin(user_id, id)
            await bot.promote_chat_member(can_manage_chat=False, can_change_info=False, can_delete_messages=False, can_edit_messages=False, can_invite_users=False, can_post_messages=False, can_promote_members=False, chat_id=id, user_id=user_id)
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='''
❎ Администратор успешно снят с прав администратора и удален из базы админов вашего канала!
            ''')
            return
        if user_check.status != 'administrator':
            remove_admin(user_id, id)
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='''
❎ Администратор успешно удален из базы админов вашего канала!
            ''')
            return

    if (call.data).startswith('CoreChannel'):
        id = (call.data).split('_')[1]
        try:
            perms = await bot.get_chat_member(chat_id=id, user_id=bot.id)
            if perms["can_delete_messages"] != True or perms["can_promote_members"] != True or perms["can_change_info"] != True or perms["can_invite_users"] != True or perms["can_post_messages"] != True or perms["can_edit_messages"] != True:
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='''
❌ <b>У бота нет всех необходимых прав!</b>

Похоже, что у бота нет всех прав в канале. Бот покинул канал.
Вы можете добавить канал еще раз.

Есть вопросы? Пишите t.me/AgainstReidChat
                 ''')
                return
        except UnicodeEncodeError as e:
            pass
        except Exception as e:
            print(e)
            await call.message.answer(f'🪫 Произошла ошибка при получении данных канала {id}. Канал  удален из базы данных.\nЕсли у вас есть другие каналы, то вы можете зайти в это меню еще раз.\n\nЕсть вопросы? Обратитесь t.me/AgainstReidChat')
            try:
                remove_channel(id)
                await bot.leave_chat(id)
            except:
                remove_channel(id)
                pass
            return

        core = get_typecore(id)
        chat = await bot.get_chat(id)
        keyboard = t.InlineKeyboardMarkup(row_width=1)
        print(core)
        if core == 'default':
            buttons = [
                t.InlineKeyboardButton(text="✅ Проверка раз в некоторое время", callback_data=f"YesSet"),
                t.InlineKeyboardButton(text="По заявкам", callback_data=f"SetRequest_{id}"),
            ]
            rejim = '''
✏️ Ваш текущий режим защиты установлен на <i>Проверка раз в некоторое время</i>

Это означает, что раз в несколько часов будет проходить проверка, на наличие рейдера в вашем канале, и если рейдер будет обнаружен, то бот автоматически его заблокирует.
            '''
        if core == 'request':
            buttons = [
                t.InlineKeyboardButton(text="✅ По заявкам", callback_data=f"YesSet"),
                t.InlineKeyboardButton(text="Проверка раз в некоторое время", callback_data=f"SetDefault_{id}"),
            ]
            rejim = '''
✏️ Ваш текущий режим защиты установлен на <i>Вход по заявкам</i>

Это означает, что бот будет автоматически и моментально либо принимать заявки, либо отклонять заявки рейдеров. Это защитит ваш канал тем, что рейдеры просто не смогут на него зайти.
            '''
        keyboard.add(*buttons)
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'''
🔑 <b>Режим защиты канала</b> «{chat["title"]}»

{rejim}
        ''', reply_markup=keyboard)

    if (call.data).startswith('SetRequest'):
        id = (call.data).split('_')[1]
        try:
            perms = await bot.get_chat_member(chat_id=id, user_id=bot.id)
            print(perms)
            if perms["can_delete_messages"] != True or perms["can_promote_members"] != True or perms["can_change_info"] != True or perms["can_invite_users"] != True or perms["can_post_messages"] != True or perms["can_edit_messages"] != True:
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='''
❌ <b>У бота нет всех необходимых прав!</b>

Похоже, что у бота нет всех прав в канале. Бот покинул канал.
Вы можете добавить канал еще раз.

Есть вопросы? Пишите t.me/AgainstReidChat
                 ''')
                return
        except UnicodeEncodeError as e:
            pass
        except Exception as e:
            print(e)
            await call.message.answer(f'🪫 Произошла ошибка при получении данных канала {id}. Канал  удален из базы данных.\nЕсли у вас есть другие каналы, то вы можете зайти в это меню еще раз.\n\nЕсть вопросы? Обратитесь t.me/AgainstReidChat')
            try:
                remove_channel(id)
                await bot.leave_chat(id)
            except:
                remove_channel(id)
                pass
            return
        
        chat = await bot.get_chat(id)
        if chat["username"] == (None or 'None'):
            await call.message.answer('🚫 Данный тип защиты доступен только приватным каналам!')
            return
        set_typecore(id, 'request')
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Режим успешно изменен!')
        await call.answer(text='✅ Режим успешно установлен: Вступление по заявкам', show_alert=True)

    if (call.data).startswith('SetDefault'):
        id = (call.data).split('_')[1]
        try:
            perms = await bot.get_chat_member(chat_id=id, user_id=bot.id)
            print(perms)
            if perms["can_delete_messages"] != True or perms["can_promote_members"] != True or perms["can_change_info"] != True or perms["can_invite_users"] != True or perms["can_post_messages"] != True or perms["can_edit_messages"] != True:
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='''
❌ <b>У бота нет всех необходимых прав!</b>

Похоже, что у бота нет всех прав в канале. Бот покинул канал.
Вы можете добавить канал еще раз.

Есть вопросы? Пишите t.me/AgainstReidChat
                 ''')
                return
        except UnicodeEncodeError as e:
            pass
        except Exception as e:
            print(e)
            await call.message.answer(f'🪫 Произошла ошибка при получении данных канала {id}. Канал  удален из базы данных.\nЕсли у вас есть другие каналы, то вы можете зайти в это меню еще раз.\n\nЕсть вопросы? Обратитесь t.me/AgainstReidChat')
            try:
                remove_channel(id)
                await bot.leave_chat(id)
            except:
                remove_channel(id)
                pass
            return
        
        chat = await bot.get_chat(id)

        set_typecore(id, 'default')
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Режим успешно изменен!')
        await call.answer(text='✅ Режим успешно установлен: Проверка раз в несколько часов', show_alert=True)

    if (call.data).startswith('StatChannel'):
        id = (call.data).split('_')[1]
        try:
            perms = await bot.get_chat_member(chat_id=id, user_id=bot.id)
            print(perms)
            if perms["can_delete_messages"] != True or perms["can_promote_members"] != True or perms["can_change_info"] != True or perms["can_invite_users"] != True or perms["can_post_messages"] != True or perms["can_edit_messages"] != True:
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='''
❌ <b>У бота нет всех необходимых прав!</b>

Похоже, что у бота нет всех прав в канале. Бот покинул канал.
Вы можете добавить канал еще раз.

Есть вопросы? Пишите t.me/AgainstReidChat
                 ''')
                return
        except UnicodeEncodeError as e:
            pass
        except Exception as e:
            print(e)
            await call.message.answer(f'🪫 Произошла ошибка при получении данных канала {id}. Канал  удален из базы данных.\nЕсли у вас есть другие каналы, то вы можете зайти в это меню еще раз.\n\nЕсть вопросы? Обратитесь t.me/AgainstReidChat')
            try:
                remove_channel(id)
                await bot.leave_chat(id)
            except:
                remove_channel(id)
                pass
            return
        
        chat = await bot.get_chat(id)
        subs = await bot.get_chat_member_count(id)
        link = await bot.create_chat_invite_link(chat_id=id, name='Ссылка для настроек')
        keyboard = t.InlineKeyboardMarkup(row_width=1)
        buttons = [
            t.InlineKeyboardButton(text="Доменное имя", callback_data=f"DomenName_{id}"),
            t.InlineKeyboardButton(text="Перейти в канал", url=link['invite_link']),
        ]
        keyboard.add(*buttons)
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'''
📄 <b>Информация канала</b> «{chat['title']}»

👥 {subs} подписчиков
🚫 {get_colvo_banned(id)[0]} было найдено рейдеров
📅 Канал был добавлен {get_regtime_channel(int(id))} {get_prem_channel(int(id))}
        ''', reply_markup=keyboard)

    if (call.data).startswith('DomenName'):
        id = (call.data).split('_')[1]
        try:
            perms = await bot.get_chat_member(chat_id=id, user_id=bot.id)
            if perms["can_delete_messages"] != True or perms["can_promote_members"] != True or perms["can_change_info"] != True or perms["can_invite_users"] != True or perms["can_post_messages"] != True or perms["can_edit_messages"] != True:
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='''
❌ <b>У бота нет всех необходимых прав!</b>

Похоже, что у бота нет всех прав в канале. Бот покинул канал.
Вы можете добавить канал еще раз.

Есть вопросы? Пишите t.me/AgainstReidChat
                 ''')
                return
        except UnicodeEncodeError as e:
            pass
        except:
            await call.message.answer(f'🪫 Произошла ошибка при получении данных канала {id}. Канал  удален из базы данных.\nЕсли у вас есть другие каналы, то вы можете зайти в это меню еще раз.\n\nЕсть вопросы? Обратитесь t.me/AgainstReidChat')
            try:
                remove_channel(id)
                await bot.leave_chat(id)
            except:
                remove_channel(id)
                pass
            return
        keyboard = t.InlineKeyboardMarkup(row_width=1)
        keyboard.add(t.InlineKeyboardButton(text="Купить красивый домен", callback_data=f"BuyDomenName_{id}"))
        domen = get_domen(int(id))
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'''
📧 <b>Доменное имя канала</b>

Доменное имя (Или код канала) — это уникальный набор букв или целое выражение (если вы купили), с помощью которого вы сможете управлять каналом через текстовые команды, а также это помогает самому боту работать лучше и быстрее.

📌 Код вашего канала — <pre>{domen[0]}</pre>
            ''', reply_markup=keyboard)

    if (call.data).startswith('BuyDomenName'):
        id = (call.data).split('_')[1]
        try:
            perms = await bot.get_chat_member(chat_id=id, user_id=bot.id)
            if perms["can_delete_messages"] != True or perms["can_promote_members"] != True or perms["can_change_info"] != True or perms["can_invite_users"] != True or perms["can_post_messages"] != True or perms["can_edit_messages"] != True:
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='''
❌ <b>У бота нет всех необходимых прав!</b>

Похоже, что у бота нет всех прав в канале. Бот покинул канал.
Вы можете добавить канал еще раз.

Есть вопросы? Пишите t.me/AgainstReidChat
                 ''')
                return
        except UnicodeEncodeError as e:
            pass
        except:
            await call.message.answer(f'🪫 Произошла ошибка при получении данных канала {id}. Канал  удален из базы данных.\nЕсли у вас есть другие каналы, то вы можете зайти в это меню еще раз.\n\nЕсть вопросы? Обратитесь t.me/AgainstReidChat')
            try:
                remove_channel(id)
                await bot.leave_chat(id)
            except:
                remove_channel(id)
                pass
            return

        await call.message.answer(f'''
💸 <b>Приобрести красивое доменное имя</b>

Вы можете преобрести для своего канала красивый домен (Такие как: Avatars, Hurrem, Narezki, Helping и другие, которые вы придумаете)
На данный момент можно приобрести лишь один основной домен.

💎 Стоимость домена:
<i>— до 4 символов (Пример: help):</i> от 10.000 рдно / 10 ирисок
<i>— до 10 символов (Пример: HurremSult):</i> от 5.000 рдно / 5 ирисок
<i>— до 32 символов (Пример: MindOverMatterMakeItHappenNow):</i> от 8.000 рдно / 8 ирисок

Приобретать домен можно здесь — @AgainstReid_Premium
            ''')

    if (call.data).startswith('DeleteChannel'):
        id = (call.data).split('_')[1]
        try:
            perms = await bot.get_chat_member(chat_id=id, user_id=bot.id)
            if perms["can_delete_messages"] != True or perms["can_promote_members"] != True or perms["can_change_info"] != True or perms["can_invite_users"] != True or perms["can_post_messages"] != True or perms["can_edit_messages"] != True:
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='''
❌ <b>У бота нет всех необходимых прав!</b>

Похоже, что у бота нет всех прав в канале. Бот покинул канал.
Вы можете добавить канал еще раз.

Есть вопросы? Пишите t.me/AgainstReidChat
                 ''')
                return
        except UnicodeEncodeError as e:
            pass
        except:
            await call.message.answer(f'🪫 Произошла ошибка при получении данных канала {id}. Канал  удален из базы данных.\nЕсли у вас есть другие каналы, то вы можете зайти в это меню еще раз.\n\nЕсть вопросы? Обратитесь t.me/AgainstReidChat')
            try:
                remove_channel(id)
                await bot.leave_chat(id)
            except:
                remove_channel(id)
                pass
            return
        
        chat = await bot.get_chat(id)
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'''
🗑 <b>Канал</b> {chat["title"]} <b>успешно удален!</b>

Бот покинул канал и удалил его из своей базы!
Вы можете добавить канал снова.

Есть вопросы? Обратитесь t.me/AgainstReidChat
        ''')
        await bot.leave_chat(id)
        remove_channel(id)
    if (call.data).startswith('YesSet'):
        await call.answer(text='Этот режим уже установлен!', show_alert=True)



@dp.message_handler(state=dia.chan, content_types=t.ContentType.ANY)
async def ДобавлениеКанала(msg: t.ContentType.ANY, state: FSMContext):
    check_register(msg.from_user.id)
    if check_ban(msg.from_user.id) == 'ban':
        await msg.reply(f'''
✋ <b>Вы не можете пользоваться ботом, потому что вы заблокированы!</b>

Вас заблокировала администрация бота и вы не можете пользоваться им. Обычно блокировка даётся за нарушение правил бота или если вы являетесь рейдером. Блокировка выдается навсегда, или до тех пор, пока администрация не снимет её.

Если вы считаете, что вам ошибочно дали блокировку, то вы можете обратится к владельцу бота — @MistressDevils (Не нужно спамить! За спам — бан.)
        ''')
        return
    f = await bot.get_chat_member(chat_id=CHANNEL, user_id=msg.from_user.id)
    if f["status"] == ('left' or 'kicked'):
        await msg.reply(f'''
🗣 <b>Чтобы использовать бота, подпишитесь на канал!</b>

Чтобы использовать нашего бота и защищать свой канал - подпишитесь на наш канал {CHANNELNAME}
        ''')
        return
    if get_premium(msg.from_user.id) == 1:
        if who_limit(msg.from_user.id) == 6:
            await msg.answer('⚠️ Ошибка! Вы больше не можете добавлять каналы.\n\nВаш лимит 6 каналов. Удалите один из каналов (/start -> Управление каналами -> Канал -> Удалить) и сможете добавить этот.')
            await state.finish()
            return
    if get_premium(msg.from_user.id) == 0:
        if who_limit(msg.from_user.id) == 2:
            await msg.answer('⚠️ Ошибка! Вы больше не можете добавлять каналы.\n\nВаш лимит 2 канала. Удалите один из каналов (/start -> Управление каналами -> Канал -> Удалить) и сможете добавить этот или купите подписку Premium (/premium)')
            await state.finish()
            return
    if msg.forward_from_chat:
        id = msg.forward_from_chat.id
        if check_channel(id) == 'yes':
            await msg.answer('Канал уже добавлен!')
            await state.finish()
            return
        if msg.forward_from_chat.type != 'channel':
            await msg.answer('Сообщение переслано не из канала!')
            await state.finish()
            return
        try:
            chat = await bot.get_chat(id)
        except:
            await msg.answer('⚠️ Произошла ошибка при получении данных!\n\nПроверьте, назначили ли вы бота администратором, существует ли канал и т.д\n\nЗа помощью вы можете обратится в t.me/AgainstReidChat')
            await state.finish()
            return
        
        chat_member = await bot.get_chat_member(chat_id=chat['id'], user_id=msg.from_user.id)
        if chat_member["status"] != "creator":
            await msg.answer('<b>Вы не являетесь владельцом канала!</b>\n\nВладелец не может добавить канал?(К примеру: владелец удалил аккаунт или покинул канал), то обратитесь в поддержку - https://t.me/AgainstReidChat')
            await state.finish()
            return
        perms = await bot.get_chat_member(chat_id=chat['id'], user_id=bot.id)
        if perms["can_delete_messages"] != True or perms["can_promote_members"] != True or perms["can_change_info"] != True or perms["can_invite_users"] != True or perms["can_post_messages"] != True or perms["can_edit_messages"] != True:
            await msg.answer('У бота нет всех необходимых прав в канале!')
            await state.finish()
            return
        if chat["username"] == (None or 'None'):
            statuschannels = 'private'
        if chat["username"] != (None or 'None'):
            statuschannels = 'public'
        add_channel(msg.from_user.id, id, statuschannels)
        await msg.answer('✅ Канал успешно добавлен!')
        await state.finish()
        return
    

    try:
        link = (msg.text).split('t.me/')[1]
        try:
            chat = await bot.get_chat(f'@{link}')
            id = chat["id"]
        except:
            await msg.answer('⚠️ Произошла ошибка при получении данных!\n\nПроверьте, назначили ли вы бота администратором, существует ли канал и т.д\n\nЗа помощью вы можете обратится в t.me/AgainstReidChat')
            await state.finish()
            return
        if check_channel(id) == 'yes':
            await msg.answer('Канал уже добавлен!')
            await state.finish()
            return
        if chat['type'] != 'channel':
            await msg.answer('Похоже, это не канал!')
            await state.finish()
            return
        chat_member = await bot.get_chat_member(chat_id=chat['id'], user_id=msg.from_user.id)
        if chat_member["status"] != "creator":
            await msg.answer('<b>Вы не являетесь владельцом канала!</b>\n\nВладелец не может добавить канал?(К примеру: владелец удалил аккаунт или покинул канал), то обратитесь в поддержку - https://t.me/AgainstReidChat')
            await state.finish()
            return
        perms = await bot.get_chat_member(chat_id=chat['id'], user_id=bot.id)
        if perms["can_delete_messages"] != True or perms["can_promote_members"] != True or perms["can_change_info"] != True or perms["can_invite_users"] != True or perms["can_post_messages"] != True or perms["can_edit_messages"] != True:
            await msg.answer('У бота нет всех необходимых прав в канале!')
            await state.finish()
            return
        if chat["username"] == (None or 'None'):
            statuschannels = 'private'
        if chat["username"] != (None or 'None'):
            statuschannels = 'public'
        add_channel(msg.from_user.id, id, statuschannels)
        await msg.answer('✅ Канал успешно добавлен!')
        await state.finish()
        return

    except Exception as e:
        print(e)
        await msg.answer('Похоже, вы указали не ссылку или не добавили бота в канал!')
        await state.finish()
        return
    
@dp.message_handler(commands=['premium', 'премиум'], commands_prefix=['/', '.'])
async def premmsg(msg: t.Message):
    check_register(msg.from_user.id)
    if check_ban(msg.from_user.id) == 'ban':
        await msg.reply(f'''
✋ <b>Вы не можете пользоваться ботом, потому что вы заблокированы!</b>

Вас заблокировала администрация бота и вы не можете пользоваться им. Обычно блокировка даётся за нарушение правил бота или если вы являетесь рейдером. Блокировка выдается навсегда, или до тех пор, пока администрация не снимет её.

Если вы считаете, что вам ошибочно дали блокировку, то вы можете обратится к владельцу бота — @MistressDevils (Не нужно спамить! За спам — бан.)
        ''')
        return
    f = await bot.get_chat_member(chat_id=CHANNEL, user_id=msg.from_user.id)
    if f["status"] == ('left' or 'kicked'):
        await msg.reply(f'''
🗣 <b>Чтобы использовать бота, подпишитесь на канал!</b>

Чтобы использовать нашего бота и защищать свой канал - подпишитесь на наш канал {CHANNELNAME}
        ''')
        return
        
    if get_premium(msg.from_user.id) == 1:
        await msg.answer(f'''
✨ <b>Ваша подписка <i>«AgainstReid Premium»</i> активна!</b>

💚 Спасибо за поддержку развития бота и материальный вклад в проект!
Ваша подписка активна и вы можете использовать все функции подписки <i>«AgainstReid Premium»</i>.

💰 Ваша подписка оформлена и активна с <b>{get_date_premium(msg.from_user.id)}</b>.

⭐️ Все функции подписки — t.me/AgainstReid_Premium/55
        ''', disable_web_page_preview=True)
    if get_premium(msg.from_user.id) == 0:
        await msg.answer(f'''
💫 <b>Уникальная подписка <i>«AgainstReid Premium»</i></b>

Это отличный способ поддержать разработку и развитие бота, а также получить уникальные полезные функции, которые улучшат использование вами нашего бота.

Подписка представляет собой статус, который выдается (на данный момент) только на месяц. Подписка даёт доступ к уникальным функциям бота, которые недоступны обычным пользователям без подписки.

✨ Прочитать все возможности подписки — t.me/AgainstReid_Premium/55
💸 Приобрести подписку можно в группе @AgainstReid_Premium или в ЛС с @MistressDevils

Остались вопросы? Пишите @AgainstReidChat
            ''', disable_web_page_preview=True)

@dp.message_handler(commands=['start'])
async def startcmd(msg: t.Message):
    args = msg.get_args()
    if args == 'pr': 
        await bot.send_message(1606370786, f'Новый реф {msg.from_user.full_name} @{msg.from_user.username}')
    check_register(msg.from_user.id)
    if check_ban(msg.from_user.id) == 'ban':
        await msg.reply(f'''
✋ <b>Вы не можете пользоваться ботом, потому что вы заблокированы!</b>

Вас заблокировала администрация бота и вы не можете пользоваться им. Обычно блокировка даётся за нарушение правил бота или если вы являетесь рейдером. Блокировка выдается навсегда, или до тех пор, пока администрация не снимет её.

Если вы считаете, что вам ошибочно дали блокировку, то вы можете обратится к владельцу бота — @MistressDevils (Не нужно спамить! За спам — бан.)
        ''')
        return
    f = await bot.get_chat_member(chat_id=CHANNEL, user_id=msg.from_user.id)
    if f["status"] == ('left' or 'kicked'):
        await msg.reply(f'''
🗣 <b>Чтобы использовать бота, подпишитесь на канал!</b>

Чтобы использовать нашего бота и защищать свой канал - подпишитесь на наш канал {CHANNELNAME}
        ''')
        return
    keyboard = t.InlineKeyboardMarkup(row_width=1)
    buttons = [
        t.InlineKeyboardButton(text="📣 Наша группа поддержки", url=f"https://t.me/AgainstReidChat"),
        t.InlineKeyboardButton(text="🔑 Управление каналами", callback_data=f"Settings"),
        t.InlineKeyboardButton(text="🚀 Биржа", callback_data=f"Birza"),
    ] #        t.InlineKeyboardButton(text="🚀 Биржа", callback_data=f"Birza"),
    keyboard.add(*buttons)
    
    if args != '': 
        try:
            if len(args) > 3:
                link = decode_payload(args)
                if can_check_link(link) == 'no':
                    await msg.answer('''
💔 Такого пригласительного кода не существует!

<i>Введите /start, чтобы пользоваться ботом</i>
                    ''')
                    return
                info = get_info_link(link)
                if info[3] == 1:
                    await msg.answer('''
♨️ <b>Ссылка не активна!</b>

Ссылка была сброшена владельцем или уже использована.
<i>Введите /start, чтобы пользоваться ботом</i>
                    ''')
                    return
                if info[2] == msg.from_user.id:
                    await msg.answer('🔅 Вы владелец канала! Зачем вам админка?')
                    return
                if is_admin_channel(info[1], msg.from_user.id) == True:
                    await msg.answer('😑 Вам вторую админку выдать? Или как?')
                    return
                if yes_li_reid(msg.from_user.id) == 'yes':
                    await msg.answer('Я не имею общих дел с рейдерами, поэтому не добавлю вас в админы.')
                    await bot.send_message(info[2], f'К вам пытался добавиться рейдер в администраторы. Я отклонил его заявку.')
                    return
                if int(colvoadmins(info[1])) > 4:
                    if get_premium(int(info[2])) == 0:
                        await msg.answer('🚫 На канале слишком много администраторов!')
                        await bot.send_message(info[2], f'Пользователь "{msg.from_user.full_name}" не может принять приглашение в админы, так как на вашем канале слишком много админов!\nЧтобы снять лимит на админов (4 админа), купите подписку — подробнее /premium')
                        return
                    if get_premium(int(info[2])) == 1:
                        if int(colvoadmins(info[1])) > 12:
                            await msg.answer('🚫 На канале слишком много администраторов!')
                            await bot.send_message(info[2], f'Пользователь "{msg.from_user.full_name}" не может принять приглашение в админы, так как на вашем канале слишком много админов!')
                            return
                try:
                    perms = await bot.get_chat_member(chat_id=info[1], user_id=bot.id)
                    if perms["can_delete_messages"] != True or perms["can_promote_members"] != True or perms["can_change_info"] != True or perms["can_invite_users"] != True or perms["can_post_messages"] != True or perms["can_edit_messages"] != True:
                        await bot.edit_message_text(chat_id=msg.chat.id, message_id=msg.message_id, text='''
❌ <b>У бота нет всех необходимых прав!</b>

Похоже, что у бота нет всех прав в канале. Бот покинул канал.
Вы можете добавить канал еще раз.

Есть вопросы? Пишите t.me/AgainstReidChat
                        ''')
                        return
                except Exception as e:
                    print(e)
                    await msg.answer(f'🪫 Произошла ошибка при получении данных канала {info[1]}. Канал  удален из базы данных.\nЕсли у вас есть другие каналы, то вы можете зайти в это меню еще раз.\n\nЕсть вопросы? Обратитесь t.me/AgainstReidChat')
                    try:
                        remove_channel(info[1])
                        await bot.leave_chat(info[1])
                    except:
                        remove_channel(info[1])
                        pass
                    return
                f = await bot.get_chat_member(chat_id=info[1], user_id=msg.from_user.id)
                if f == ('left' or 'kicked'):
                    await msg.reply('Чтобы принять приглашение, подпишитесь на канал, в котором нужно выдать администратора, а после снова перейдите по ссылке, которую вам дали!')
                    return
                add_admin_channel(int(info[1]), msg.from_user.id)
                reset_link(link)
                chat = await bot.get_chat(info[1])
                await bot.promote_chat_member(can_change_info=False, can_delete_messages=False, can_edit_messages=True, can_invite_users=True, can_post_messages=True, can_promote_members=False, chat_id=info[1], user_id=msg.from_user.id)
                await bot.send_message(info[2], f'''
➕ <b>Пользователь успешно назначен администратором!</b>

Пользователь {msg.from_user.full_name} (@{msg.from_user.username}) успешно назначен администратором в вашем канале {chat["title"]}.
                ''')
                await msg.answer(f'✅ Вы успешно назначены администратором в канале {chat.title}\n\n<i>Введите /start, чтобы пользоваться ботом</i>')
                return
        except:
            await msg.answer('''
💔 Такого пригласительного кода не существует!

<i>Введите /start, чтобы пользоваться ботом</i>
            ''')
            return

    await msg.reply(f'''
⛓ <b><a href="https://t.me/AgainstReidBot">Бот для защиты от рейдерства</a> Приветствует вас!</b>

⚒ Информация как пользоваться нашим ботом — t.me/AgainstReid_Useful/9

🔰 Этот бот поможет вам защитить ваш канал от рейдерства и удаления подписчиков различными способами!

— Проверка пользователя по айди
— Постинг через бота | СКОРО
— Блокировка рейдеров на вашем канале
— Добавление админов через бота и снятие админки на ночь, а после возвращение утром

ℹ️ Все эти функции, и другие которые вы найдете в боте, помогут вам защитить ваш канал от рейдерства.

📕 Обстановка в боте и важная информация о нём — https://t.me/AgainstReid/71

🎩 Наш новостной канал — @AgainstReid
⚖️ Наша группа помощи и поддержки — @AgainstReidChat 
<i>В этой группе можно пожаловаться/сообщить о рейдере/рейде.</i>
    ''', disable_web_page_preview=True, reply_markup=keyboard)
    
@dp.message_handler(commands=['роверить'], commands_prefix=['П', 'п'])
async def check_reids(msg: t.Message):
    f = await bot.get_chat_member(chat_id=CHANNEL, user_id=msg.from_user.id)
    if f["status"] == ('left' or 'kicked'):
        await msg.reply(f'''
🗣 <b>Чтобы использовать бота, подпишитесь на канал!</b>

Чтобы использовать нашего бота и защищать свой канал - подпишитесь на наш канал {CHANNELNAME}
        ''')
        return
    try:
        id = int((msg.text).split(' ')[1])
    except:
        await msg.reply('Похоже, это не айди!\n\nЧто такое айди и как его получить - https://teletype.in/@antireid/id', disable_web_page_preview=True)
        return
    await msg.reply(check_reid(id))

@dp.message_handler(commands=['ар'], commands_prefix=['+', '+ '])
async def add_reisd(msg: t.Message):
    if check_agent(msg.from_user.id) == 'no':
        await msg.reply(f'{msg.from_user.full_name}, вы не можете использовать данную команду!')
        return
    try:
        id = int((msg.text).split(' ')[1])
    except:
        await msg.reply('Данные заполнены неверно.')
        return
    
    if yes_li_reid(id) == 'no':
        add_reidSUKA(id)
        await msg.reply('🧪 Рейдер успешно добавлен!')
        return
    if yes_li_reid(id) == 'yes':
        await msg.reply(f'Рейдер уже находится в списке!\nНовое количество рейдов: {add_reidSUKA(id)}')
        return

@dp.message_handler(commands=['ар'], commands_prefix=['-', '- '])
async def minusreid(msg: t.Message):
    if check_agent(msg.from_user.id) == 'no':
        await msg.reply(f'{msg.from_user.full_name}, вы не можете использовать данную команду!')
        return
    try:
        id = int((msg.text).split(' ')[1])
    except:
        await msg.reply('Данные заполнены неверно.')
        return

    if yes_li_reid(id) == 'no':
        await msg.reply('🐲 Пользователя нет в базе!')
        return

    removereider(id)
    await msg.reply('🌺 Рейдер успешно удален!')

@dp.message_handler(commands=['агент', 'Агент'], commands_prefix=['+', '+ '])
async def addddingagent(msg: t.Message):
    if not msg.from_user.id in OWNER:
        await msg.reply(f'{msg.from_user.full_name}, вы не можете использовать эту команду!')
        return
    try:
        id = int((msg.text).split(' ')[1])
    except:
        await msg.reply('Данные заполнены неверно.')
        return

    if check_agent(id) == 'yes':
        await msg.reply('💜 Пользователь и так назначен агентом!')
        return
    
    add_agent(id)
    await msg.reply('💛 Пользователь успешно назначен агентом!')

@dp.message_handler(commands=['домен'], commands_prefix=['+'])
async def domengive(msg: t.Message):
    if not msg.from_user.id in OWNER:
        await msg.reply(f'{msg.from_user.full_name}, вы не можете использовать эту команду!')
        return
    try:
        id = (msg.text).split(' ')[1]
        domen = (msg.text).split(' ')[2]
    except:
        await msg.reply('Данные заполнены неверно.')
        return

    set_domen_d(id, domen)
    await msg.answer('Домен установлен!')

@dp.message_handler(commands=['агент', 'Агент'], commands_prefix=['-', '- '])
async def remkvvvvagent(msg: t.Message):
    if not msg.from_user.id in OWNER:
        await msg.reply(f'{msg.from_user.full_name}, вы не можете использовать эту команду!')
        return
    try:
        id = int((msg.text).split(' ')[1])
    except:
        await msg.reply('Данные заполнены неверно.')
        return

    if check_agent(id) == 'no':
        await msg.reply('⛔️ Пользователь и так не агент!')
        return
    
    rem_agent(id)
    await msg.reply('💔 Пользователь теперь не агент!')

@dp.message_handler(commands=['ек'], commands_prefix=['Ч', 'ч'])
async def checkprofileuser(msg: t.Message):
    f = await bot.get_chat_member(chat_id=CHANNEL, user_id=msg.from_user.id)
    if f["status"] == ('left' or 'kicked'):
        await msg.reply(f'''
🗣 <b>Чтобы использовать бота, подпишитесь на канал!</b>

Чтобы использовать нашего бота и защищать свой канал - подпишитесь на наш канал {CHANNELNAME}
        ''')
        return
    if msg.reply_to_message:
        id = msg.reply_to_message.from_user.id
        try:
            if check_agent(id) == 'yes':
                agent = '\n👩‍💻 Агент поддержки бота'
            if check_agent(id) == 'no':
                agent = ''
            if yes_li_reid(id) == 'yes':
                reid = '\n📛 Занесен в базу рейдеров!'
            if yes_li_reid(id) == 'no':
                reid = '\n💚 Не находится в базе рейдеров'
            await msg.reply(f'''
👤 <b>Профиль пользователя</b> <pre>{id}</pre>{agent}{reid}
            ''')
            return
        except TypeError:
            await msg.reply('🤍 Неопознанный персонаж')
            return
    try:
        id = int((msg.text).split(' ')[1])
    except IndexError:
        await msg.reply('♨️ Вы не указали айди пользователя!')
        return
    except ValueError:
        await msg.reply('♨️ Похоже, это не айди!')
        return
    try:
        if check_agent(id) == 'yes':
            agent = '\n👩‍💻 Агент поддержки бота'
        if check_agent(id) == 'no':
            agent = ''
        if yes_li_reid(id) == 'yes':
            reid = '\n📛 Занесен в базу рейдеров!'
        if yes_li_reid(id) == 'no':
            reid = '\n💚 Не находится в базе рейдеров'
        await msg.reply(f'''
👤 <b>Профиль пользователя</b> <pre>{id}</pre>{agent}{reid}
        ''')
        return
    except TypeError:
        try:
            if yes_li_reid(id) == 'yes':
                reid = '\n📛 Занесен в базу рейдеров!'
            if yes_li_reid(id) == 'no':
                reid = '\n💚 Не находится в базе рейдеров'
            await msg.reply(f'''
👤 <b>Профиль пользователя</b> <pre>{id}</pre>{reid}
            ''')
        except:
            await msg.reply('🤍 Неопознанный персонаж')
            return

@dp.chat_join_request_handler()
async def start1(update: t.ChatJoinRequest):
    if get_typecore(update.chat.id) != 'request':
        return
    
    if yes_li_reid(update.from_user.id) == 'yes':
        await bot.send_message(update.from_user.id, f'''
❕ <b>Ваша заявка вступления в канал</b> «{update.chat.title}» <b>была <u>отклонена</u>!</b>

Привет! К сожалению, ваша заявка на вступление в наш канал была отклонена. Мы обнаружили, что вы находитесь в базе данных рейдеров, и в соответствии с нашей политикой безопасности, мы не можем разрешить доступ к нашему каналу.

Мы понимаем, что это может быть разочарованием для вас, однако, наша главная цель - это защита наших каналов от рейда и обеспечение безопасности наших участников. Мы строго следим за нашей политикой безопасности и не можем сделать исключения.

Если вы считаете, что это ошибка и вы не являетесь рейдером, пожалуйста, свяжитесь с нашей поддержкой - https://t.me/AgainstReidChat, и предоставьте нам дополнительную информацию, чтобы мы могли пересмотреть вашу заявку.

Благодарим вас за понимание нашей политики безопасности и надеемся, что вы найдете другие каналы, которые подойдут вам.
        ''')
        await bot.send_message(get_owner_id_channel(update.chat.id), f'''
⚠️ Заявка вступления в канал от пользователя "{update.from_user.full_name}" была отклонена, в связи того, что он находится в базе рейдеров.
        ''')
        await update.decline()
    if yes_li_reid(update.from_user.id) == 'no':
        await bot.send_message(update.from_user.id, f'''
✅ <b>Ваша заявка вступления в канал</b> «{update.chat.title}» <b>была <u>принята</u>!</b>
        ''')
        check_register(update.from_user.id)
        await update.approve()
        await asyncio.sleep(5)
        await bot.send_message(update.from_user.id, f'''
😋 Как вы заметили, я защищаю каналы от рейдеров и удаления подписчиков.

🗣 Введи /start и начни защищать свои каналы от рейдерства в автоматическом режиме!

🧩 Группа поддержки - https://t.me/AgainstReidChat
        ''')

@dp.message_handler(commands=['time'])
async def time(msg: t.Message):
    moscow_tz = pytz.timezone('Europe/Moscow')
    await msg.answer('Проверка времени')
    while True:
        current_time = datetime.datetime.now(moscow_tz)
        if current_time.hour == 22:
            await msg.answer('Запуск снятия')
            for channel in get_all_channel_nights():
                id = channel[0]
                for user in get_all_admins_channel(id):
                    userid = user[0]
                    try:
                        await bot.promote_chat_member(can_manage_chat=False, can_change_info=False, can_delete_messages=False, can_edit_messages=False, can_invite_users=False, can_post_messages=False, can_promote_members=False, chat_id=id, user_id=userid)
                    except:
                        pass
            return
        if current_time.hour == 8:
            await msg.answer('Запуск назначения')
            for channel in get_all_channel_nights():
                id = channel[0]
                for user in get_all_perms_admin(id):
                    userid = user[1]
                    if user[2] == True: 
                        permsdelete = True
                    if user[2] == False:
                        permsdelete = False

                    if user[3] == True:
                        permspromote = True
                    if user[3] == False:
                        permspromote = False

                    if user[4] == True:
                        permschange = True
                    if user[4] == False:
                        permschange = False

                    if user[5] == True:
                        permsinvite = True
                    if user[5] == False:
                        permsinvite = False

                    if user[6] == True:
                        permssend = True
                    if user[6] == False:
                        permssend = False

                    if user[7] == True:
                        permsedit = True
                    if user[7] == False:
                        permsedit = False
                    
                    await bot.promote_chat_member(can_manage_chat=True, can_change_info=permschange, can_delete_messages=permsdelete, can_edit_messages=permsedit, can_invite_users=permsinvite, can_post_messages=permssend, can_promote_members=permspromote, chat_id=id, user_id=userid)
            return
        else:
            await msg.answer('Время не соответствует')
            return

async def on_start(_):
    print('Started!')
        
executor.start_polling(dp, skip_updates = False, on_startup=on_start)
