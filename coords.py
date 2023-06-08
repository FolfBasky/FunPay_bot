import random

class Desktop:
    home = (1365,767)
    tor = (714,767)
    windows = (108,767)
    last_window = (373,203)
    turn_tor = (1140,63)
    close_Tor = (1232, 64)

class Tor:
    funpay = 'https://funpay.com'
    new_persona = (1170,110)

    profile_link = "https://funpay.com/lots/699/trade"
    chat_link = "https://funpay.com/chat/"
    link_coordinates = (580,116)
    button_coordinates = (950,242) 
    chat_new = (450,300)
    window_coordinates_high = (540,295)
    window_coordinates_low = (985,655)
    nick_start = (610,235)
    nick_end = (800,235)
    chat_write_coordinates = (650, 679)
    enter = (810, 155)

    login_coordinates = (600,500)
    password_coordinates = (600,540)
    number_coordinates = (830, 300)

    class slots:
        link = 'https://funpay.com/lots/699/trade'
        create = (600, 330)
        create_again = (1157,229)
        subscribers_coordinates = (695, 373+20)
        subscribers = int()
        themes_coordinates = (686, 287+30)
        smallDiscribe_coordinates = (670, 500)
        ds_list = [['❤💛🧡💚💙💜 ПЕРЕДАЧА ПРАВ ВЛАДЕЛЬЦА ГРУППЫ |', 'ПОДПИСЧИКОВ ❤💛🧡💚💙💜'],
                   ['🈴🈵🈲🈴🈵🈲 ПЕРЕДАЮ ПРАВА ВЛАДЕЛЬЦА |','УЧАСТНИКОВ 🈴🈵🈲🈴🈵🈲'], 
                   ['🈶🈚🈸🈺🈶🈚 ПЕРЕДАЧА ПРАВА ВЛАДЕЛЬЦА |','ПОДПИСЧИКОВ 🈶🈚🈶🈚🈸🈺'],
                   ['✅✅✅ Группа с', 'подписчиками. Передача владельца. Полная смена тематики. ✅✅✅'],
                   ['🟣 𝐕𝐊𝐎𝐍𝐓𝐀𝐊𝐓𝐄 🟣 ','ПОДПИСЧИКОВ 🟣 СООБЩЕСТВО ДЛЯ СТАРТА 🟣 БЕЗ БЛОКИРОВКИ 🟣']]

        Des_list = random.choice(ds_list)
        smallDiscribe_text = ''
        Discribe_coordinates = (640, 606+30)
        Discribe_text = 'ПЕРЕДАЮ ПРАВА ВЛАДЕЛЬЦА\n'
        price_coordinates = (545,514)
        price = str()
        save = (585,672+30)
        slot = (633, 332+30)
        delete = (750,640)
        confirm_delete = (750,600)