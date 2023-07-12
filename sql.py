import sqlite3
import datetime
import pytz

conn = sqlite3.connect('base.db', check_same_thread=False)
cur = conn.cursor()

def regtime():
    tz = pytz.timezone('Europe/Moscow')
    now = datetime.datetime.now(tz)
    formatted_date = now.strftime("%d.%m.%Y в %H:%M")
    return formatted_date

def colvo_reids(id):
    s = cur.execute('select colvobanned from channels where id=?', [id]).fetchone()
    return s[0]

def remove_channel(channel):
    s = cur.execute('select ownerid from channels where id=?', [int(channel)]).fetchone()
    ss = s[0]
    a = cur.execute('select limchannel from users where id=?', [ss]).fetchone()
    aa = a[0] - 1
    cur.execute('UPDATE users SET limchannel = ? where id = ?', [aa, ss])
    cur.execute('delete from channels where id=?', [int(channel)])
    conn.commit()

def colvoadmins(channel):
    a = cur.execute('select * from admins where channelid = ?', [int(channel)]).fetchall()
    return len(a)

def rasulkaforusers():
    a = cur.execute('select id from users where prem = ?', [0]).fetchall()
    return a

def get_notifi(channel):
    a = cur.execute('select noti from channels where id = ?', [int(channel)]).fetchall()
    print(a[0])
    return a[0]

def rasulkaforuser():
    a = cur.execute('select id from users').fetchall()
    return a

def get_colvo_banned(channel):
    a = cur.execute('select colvobanned from channels where id = ?', [int(channel)]).fetchall()
    return a[0]

def giveallchannels():
    a = cur.execute('select id from channels').fetchall()
    return a

def set_notifi(channel, noti):
    print('xe')
    cur.execute('UPDATE channels SET noti = ? where id = ?', [int(noti), int(channel)])
    conn.commit()

def set_typecore(channel, type):
    cur.execute('UPDATE channels SET typecore = ? where id = ?', [type, int(channel)])
    conn.commit()

def get_all_admins(id):
    s = cur.execute('select userid from admins where channelid=?', [int(id)]).fetchall()
    return s

def can_check_link(link):
    if bool(cur.execute('select * from links where link=?', [link]).fetchone()) == True:
        return 'yes'
    else:
        return 'no'

def remove_admin(user, channel):
    cur.execute('delete from admins where userid=? AND channelid=?', [int(user), int(channel)])
    conn.commit()

def is_admin_channel(channel, user):
    if bool(cur.execute('select * from admins where channelid=? AND userid=?', [int(channel), user]).fetchone()) == True:
        return True
    else:
        return False

def delete_anket(id):
    cur.execute('delete from birza where id=?', [id])
    conn.commit()

def accept_anket(id):
    cur.execute('UPDATE birza SET st = ? where id = ?', [1, int(id)])
    conn.commit()

def ban_anket(id):
    cur.execute('UPDATE birza SET st = ? where id = ?', [2, int(id)])
    conn.commit()

def set_liked(liked, id):
    cur.execute('UPDATE birzaowners SET liked = ? where id = ?', [liked, id])
    conn.commit()

def check_ownerbirza(id):
    if bool(cur.execute('select * from birzaowners where id = ?', [id]).fetchone()) == True:
        return True 
    else:
        return False 

def check_group(id):
    if bool(cur.execute('select * from chats where id = ?', [id]).fetchone()) == True:
        return True 
    else:
        return False 

def check_id_channel(id):
    if bool(cur.execute('select * from channels where domen = ?', [id]).fetchone()) == True:
        return True 
    else:
        return False 

def get_regtime_channel(id):
    a = cur.execute('select regtime from channels where id = ?', [id]).fetchone()
    return a[0]

def get_prem_channel(id):
    a = cur.execute('select prem from channels where id = ?', [id]).fetchone()
    if a[0] == 1:
        return '\n\n⭐️ Канал имеет Premium статус'
    if a[0] == 0:
        return ' '

def create_group(id):
    cur.execute('INSERT INTO chats(id, regtime, st) VALUES(?, ?, ?)', [id, regtime(), 0])
    conn.commit()

def create_ownerbirza(id):
    cur.execute('INSERT INTO birzaowners(id, liked, skiped) VALUES(?, ?, ?)', [id, '1 ', '1 '])
    conn.commit()

def set_skiped(skiped, id):
    cur.execute('UPDATE birzaowners SET skiped = ? where id = ?', [skiped, id])
    conn.commit()

def is_li_anketa_id(id):
    if bool(cur.execute('select * from birza where idankety = ?', [id]).fetchone()) == True:
        return True 
    else:
        return False 

def get_spisok(id):
    ankets = cur.execute('select liked from birzaowners where id = ?', [id]).fetchone()
    return ankets

def get_anketa_id(id):
    ankets = cur.execute('select * from birza where idankety = ?', [id]).fetchone()
    return ankets

def get_spisok_skip(id):
    ankets = cur.execute('select skiped from birzaowners where id = ?', [id]).fetchone()
    return ankets

def get_all_ankets():
    ankets = cur.execute('select idankety from birza where st = ?', [1]).fetchall()
    try:
        if ankets[0] == '':
            return 0
    except Exception as e:
        print(e)
        return 0
    return ankets

def is_li_anketa(user):
    if bool(cur.execute('select * from birza where id = ?', [user]).fetchone()) == True:
        return True 
    else:
        return False 

def get_anketa(user : None, idanketa : None):
    if user != None:
        s = cur.execute('select * from birza where id = ?', [user]).fetchone()
        return s
    if idanketa != None:
        s = cur.execute('select * from birza where idankety = ?', [idanketa]).fetchone()
        return s

def create_anketa(user, idanket, name, desc):
    cur.execute('INSERT INTO birza(id, st, descr, idankety, psevdoname) VALUES(?, ?, ?, ?, ?)', [user, 0, desc, idanket, name])
    conn.commit()

def reset_link(link):
    cur.execute('UPDATE links SET st = ? where link = ?', [1, link])
    conn.commit()

def add_admin_channel(channel, user):
    cur.execute('INSERT INTO admins(channelid, userid, regtime) VALUES(?, ?, ?)', [channel, user, regtime()])
    conn.commit()

def get_info_admin(channel, user):
    s = cur.execute('select * from admins where channelid=? AND userid=?', [channel, user]).fetchone()
    return s

def get_info_link(link):
    s = cur.execute('select * from links where link=?', [link]).fetchone()
    return s

def sql_create_link(link, ownerid, channelid):
        cur.execute('INSERT INTO links(link, ownerid, regtime, channelid) VALUES(?, ?, ?, ?)', [link, ownerid, regtime(), channelid])
        conn.commit()

def get_date_premium(user):
    s = cur.execute('select premdate from users where id=?', [int(user)]).fetchone()
    return s[0]

def get_premium(user):
    s = cur.execute('select prem from users where id=?', [int(user)]).fetchone()
    return s[0]

def get_night(channel):
    s = cur.execute('select night from channels where id=?', [int(channel)]).fetchone()
    print(s)
    return s[0]

def give_premium(user):
    if get_premium(int(user)) == 1:
        return 'have'
    if get_premium(int(user)) == 0:
        cur.execute('UPDATE users SET prem = ? where id = ?', [1, int(user)])
        cur.execute('UPDATE users SET premdate = ? where id = ?', [regtime(), int(user)])

        for channel in cur.execute('select * from channels where ownerid=?', [int(user)]).fetchall():
            idchannel = channel[0]
            cur.execute('UPDATE channels SET prem = ? where id = ?', [1, int(idchannel)])
        conn.commit()
        return 'ok'

def take_premium(user):
    if get_premium(int(user)) == 0:
        return 'have'
    if get_premium(int(user)) == 1:
        cur.execute('UPDATE users SET prem = ? where id = ?', [0, int(user)])

        for channel in cur.execute('select * from channels where ownerid=?', [int(user)]).fetchall():
            idchannel = channel[0]
            cur.execute('UPDATE channels SET prem = ? where id = ?', [0, int(idchannel)])
        conn.commit()
        return 'ok'

def set_night(channel, rejim):
    cur.execute('UPDATE channels SET night = ? where id = ?', [int(rejim), int(channel)])
    conn.commit()

def get_typecore(channel):
    print(channel)
    s = cur.execute('select typecore from channels where id=?', [int(channel)]).fetchone()
    return s[0]

def get_all_channel_nights():
    s = cur.execute('select id from channels where night=?', [1]).fetchall()
    return s

def get_all_perms_admin(id):
    s = cur.execute('select * from admins where channelid=?', [id]).fetchall()
    return s

def get_all_admins_channel(id):
    s = cur.execute('select userid from admins where channelid=?', [id]).fetchall()
    return s

def addreidchannel(channel):
    s = cur.execute('select colvobanned from channels where id=?', [channel]).fetchone()
    ss = s[0]
    res = ss + 1
    cur.execute('UPDATE channels SET colvobanned = ? where id = ?', [res, channel])
    conn.commit()

def get_owner_id_channel(channel):
    s = cur.execute('select ownerid from channels where id=?', [channel]).fetchone()
    return s[0]

def giveallreids():
    a = cur.execute('select id from reids').fetchall()
    return a

def giveallchannels():
    a = cur.execute('select * from channels where prem = ?', [0]).fetchall()
    return a

def givealchannels():
    a = cur.execute('select * from channels').fetchall()
    return a

def set_domen(id, domen):
    cur.execute('UPDATE channels SET domen = ? where id = ?', [domen, id])
    conn.commit()

def set_domen_d(id, domen):
    cur.execute('UPDATE channels SET domen = ? where domen = ?', [domen, id])
    conn.commit()

def get_domen(id):
    a = cur.execute('select domen from channels where id = ?', [id]).fetchall()
    return a[0]

def add_channel(user, channel, types):
    cur.execute('INSERT INTO channels(id, ownerid, regtime, type) VALUES(?, ?, ?, ?)', [channel, user, regtime(), types])
    conn.commit()
    s = cur.execute('select limchannel from users where id=?', [user]).fetchone()
    ss = s[0] + 1
    cur.execute('UPDATE users SET limchannel = ? where id = ?', [ss, user])
    conn.commit()

def check_channel(id):
    if bool(cur.execute('select * from channels where id=?', [id]).fetchone()) == True:
        return 'yes'
    else:
        return 'no'

def who_limit(user):
    s = cur.execute('select limchannel from users where id=?', [user]).fetchone()
    return s[0]

def check_is_channels(user):
    if bool(cur.execute('select * from channels where ownerid=?', [user]).fetchone()) == True:
        return 'yes'
    else:
        return 'no'

def all_channels_user(user):
    s = cur.execute('select id from channels where ownerid=?', [user]).fetchall()
    return s

def check_register(user):
    if bool(cur.execute('select * from users where id=?', [user]).fetchone()) == False:
        cur.execute('INSERT INTO users(id, regtime) VALUES(?, ?)', [user, regtime()])
        conn.commit()
    else:
        pass

def check_ban(user):
    s = cur.execute('select st from users where id=?', [user]).fetchone()
    if s[0] == 1:
        return 'ban'
    else:
        return 'none'
    
def check_agent(user):
    s = cur.execute('select st from users where id=?', [user]).fetchone()
    if s[0] in [2, 3]:
        return 'yes'
    else:
        return 'no'

def yes_li_reid(user):
    if bool(cur.execute('select * from reids where id=?', [user]).fetchone()) == True:
        return 'yes'
    else:
        return 'no'

def add_agent(user):
    cur.execute('UPDATE users SET st = ? where id = ?', [2, user])
    conn.commit()

def rem_agent(user):
    cur.execute('UPDATE users SET st = ? where id = ?', [0, user])
    conn.commit()

def removereider(user):
    cur.execute('delete from reids where id=?', [user])
    conn.commit()

def add_reidSUKA(user):
    if yes_li_reid(user) == 'yes':
        s = cur.execute('select colvo from reids where id=?', [user]).fetchone()
        ss = s[0] + 1
        cur.execute('UPDATE reids SET colvo = ? where id = ?', [ss, user])
        conn.commit()
        print(2)
        return ss
    if yes_li_reid(user) == 'no':
        cur.execute('INSERT INTO reids(id) VALUES(?)', [user])
        conn.commit()

def check_reid(user):
    if bool(cur.execute('select * from reids where id=?', [user]).fetchone()) == True:
        s = cur.execute('select colvo from reids where id=?', [user]).fetchone()
        return f'''
📛 <b>Данный пользователь рейдер!</b>

Мы настоятельно не рекомендуем брать данного человека в админы вашего канала. За ним замечены случаи рейдерства.

📃 Случаев рейда от этого человека: <pre>{s[0]}</pre>

Считаете ошибкой? Обратитесь t.me/AgainstReidChat
        '''
    else:
        return f'''
💚 <b>Этот человек не рейдер и его можно брать в админы!</b>

За этим человеком не было замечено случаев рейда и его можно брать в админы!

Считаете ошибкой? Обратитесь t.me/AgainstReidChat
        '''

