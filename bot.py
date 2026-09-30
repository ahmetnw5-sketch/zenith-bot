import os
import time
import datetime
import random
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, LabeledPrice
import yt_dlp

TOKEN = "8927197392:AAGsATpv90EwcijG2ppvRJJ5QRiz15S_hZc"
bot = telebot.TeleBot(TOKEN)
ADMIN_ID = 8520025523

user_states = {}
unlocked_platforms = {} 
user_languages = {} 
pending_links = {}  
wheel_rights = {}
user_discounts = {}
first_time_users = set()

user_bans = {}
is_maintenance_mode = False

BANNED_WORDS = ["küfür1", "küfür2", "amk", "aq", "orospu", "piç", "sik", "mal", "salak"] 

ALL_LANGUAGES = [
    ("🇹🇷 Türkçe", "tr"), 
    ("☀️ Kürtçe (Kurmancî)", "ku"), 
    ("🇬🇧 English", "en"), 
    ("🇸🇦 العربية", "ar"), 
    ("🇹🇲 Türkmence (Türkmençe)", "tk")
]

TRANSLATIONS = {
    "tr": {
        "welcome": (
            "✨🚀 **Zenith v2.5.0.8 Zirvesine Hoş Geldin Reisim!** 🔥💎\n\n"
            "*Botun motorları son sürat çalışıyor, indirmeye hazır ol!* 👇🤖\n\n"
            "⚠️ **ÖNEMLİ DUYURU & KURALLAR:**\n"
            "Lütfen bot içinde veya bağlı gruplarda **küfür ve hakaret etmeyiniz**. "
            "Alacağınız VIP'lerden veya haklardan sonra küfür ettiğiniz tespit edilirse "
            "**VIP haklarınız tamamen silinir** ve sistem tarafından geçici süreliğine "
            "(1 saat ile 10 gün arası) engellenirsiniz!\n\n"
            "Anlayışınız için teşekkür ederiz... 🙏✨"
        ),
        "admin_active": "\n\n👑 *Zenith v2.5.0.8 Admin Paneli Aktif!*",
        "btn_uzun": "🎬 YouTube Uzun İndir",
        "btn_shorts": "📱 YouTube Shorts İndir",
        "btn_tiktok": "🎵 TikTok İndir",
        "btn_insta": "📸 Instagram Reels İndir",
        "btn_wheel": "🎡 Şans Çarkını Çevir (Günde 3 Hak)",
        "btn_profile": "👤 Profilim / Haklarım",
        "btn_lang": "🌐 Dil Seç / Language",
        "lang_select": "🌐 **Lütfen kullanmak istediğin dili seç:**",
        "back_menu": "🔙 Ana Menüye Dön",
        "choose_format": "📥 **Nasıl indirmek istiyorsun?**",
        "btn_video": "🎥 Video İndir",
        "btn_audio": "🎵 MP3 İndir",
        "success_video": "✅ Videon hazır dostum!😀",
        "success_audio": "🎵 Ses dosyan hazır!",
        "start_fallback": "Lütfen indirmek istediğin video bağlantısını doğrudan gönder reisim!",
        "maintenance_msg": "🛠 **Zenith v2.5.0.8 şu an bakımda reisim!** En kısa sürede döneceğiz."
    },
    "ku": {
        "welcome": "✨🚀 **Bi xêr hatî Qraliyeta Zenith v2.5.0.8!** 🔥💎",
        "btn_uzun": "🎬 Vîdyoya Dirêj a YouTube",
        "btn_shorts": "📱 YouTube Shorts",
        "btn_tiktok": "🎵 Daxistina TikTok",
        "btn_insta": "📸 Instagram Reels",
        "btn_wheel": "🎡 Çerxa Bextê Bivirîne",
        "btn_profile": "👤 Profîla Min",
        "btn_lang": "🌐 Ziman / Dil",
        "lang_select": "🌐 **Ji kerema xwe zimanê xwe hilbijêre:**",
        "back_menu": "🔙 Vegere Menuya Sereke",
        "choose_format": "📥 **Çawa dixwazî daxistinê bikî?**",
        "btn_video": "🎥 Vîdyo Daxîne",
        "btn_audio": "🎵 Pelê deng Daxîne",
        "start_fallback": "Ji kerema xwe lînkê bişîne.",
        "maintenance_msg": "🛠️️ **Zenith di dema bakûr de ye!**"
    },
    "en": {
        "welcome": "✨🚀 **Welcome to Zenith v2.5.0.8!** 🔥💎",
        "btn_uzun": "🎬 YouTube Long Video",
        "btn_shorts": "📱 YouTube Shorts",
        "btn_tiktok": "🎵 TikTok Video",
        "btn_insta": "📸 Instagram Reels",
        "btn_wheel": "🎡 Spin the Lucky Wheel",
        "btn_profile": "👤 Profile",
        "btn_lang": "🌐 Language",
        "lang_select": "🌐 **Please select your language:**",
        "back_menu": "🔙 Back to Main Menu",
        "choose_format": "📥 **How do you want to download?**",
        "btn_video": "🎥 Download Video",
        "btn_audio": "🎵 Download MP3",
        "start_fallback": "Please send the link directly.",
        "maintenance_msg": "🛠️ Zenith is currently under maintenance."
    },
    "ar": {
        "welcome": "✨🚀 **مرحباً بك في Zenith v2.5.0.8!** 🔥💎",
        "btn_uzun": "🎬 فيديو يوتيوب طويل",
        "btn_shorts": "📱 يوتيوب شورتس",
        "btn_tiktok": "🎵 تيك توك",
        "btn_insta": "📸 إنستغرام ريلز",
        "btn_wheel": "🎡 أدار عجلة الحظ",
        "btn_profile": "👤 ملفي الشخصي",
        "btn_lang": "🌐 اللغة",
        "lang_select": "🌐 **يرجى اختيار لغتك:**",
        "back_menu": "🔙 العودة للقائمة الرئيسية",
        "choose_format": "📥 **كيف تريد التنزيل؟**",
        "btn_video": "🎥 تنزيل فيديو",
        "btn_audio": "🎵 تنزيل MP3",
        "start_fallback": "يرجى إرسال الرابط مباشرة.",
        "maintenance_msg": "🛠️ Zenith تحت الصيانة حالياً."
    },
    "tk": {
        "welcome": "✨🚀 **Zenith v2.5.0.8 Hoş geldiňiz!** 🔥💎",
        "btn_uzun": "🎬 YouTube Uzyn Wideo",
        "btn_shorts": "📱 YouTube Shorts",
        "btn_tiktok": "🎵 TikTok Wideo",
        "btn_insta": "Instagram Reels",
        "btn_wheel": "🎡 Bagt Çarhyny Aýla",
        "btn_profile": "👤 Profilim",
        "btn_lang": "🌐 Dil",
        "lang_select": "🌐 **Dil saýlaň:**",
        "back_menu": "🔙 Yzyna",
        "choose_format": "📥 **Nädip ýükletmeli?**",
        "btn_video": "🎥 Wideo",
        "btn_audio": "🎵 MP3",
        "start_fallback": "Salgyny göni ibăriň.",
        "maintenance_msg": "🛠 Zenith tehniki hyzmatda."
    }
}

def get_text(user_id, key):
    lang = user_languages.get(user_id, "tr")
    if lang not in TRANSLATIONS: lang = "tr"
    return TRANSLATIONS[lang].get(key, TRANSLATIONS["tr"].get(key, ""))

def get_main_keyboard(user_id):
    m = InlineKeyboardMarkup(row_width=1)
    m.add(
        InlineKeyboardButton(get_text(user_id, 'btn_uzun'), callback_data="menu_uzun"),
        InlineKeyboardButton(get_text(user_id, 'btn_shorts'), callback_data="menu_shorts"),
        InlineKeyboardButton(get_text(user_id, 'btn_tiktok'), callback_data="menu_tiktok"),
        InlineKeyboardButton(get_text(user_id, 'btn_insta'), callback_data="menu_insta"),
        InlineKeyboardButton("⚡ 7 Yıldız ile Anında İndir", callback_data="buy_instant_vip"),
        InlineKeyboardButton(get_text(user_id, "btn_wheel"), callback_data="open_lucky_wheel"),
        InlineKeyboardButton(get_text(user_id, "btn_profile"), callback_data="open_profile"),
        InlineKeyboardButton(get_text(user_id, "btn_lang"), callback_data="open_language_menu")
    )
    return m

@bot.message_handler(commands=['bakim'])
def toggle_maintenance(message):
    global is_maintenance_mode
    user_id = message.from_user.id
    if user_id != ADMIN_ID: return
    is_maintenance_mode = not is_maintenance_mode
    status_text = "🟢 Açıldı" if not is_maintenance_mode else "🔴 Kapatıldı (Bakım)"
    bot.reply_to(message, f"🛠️ Bakım Modu: {status_text}")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    global is_maintenance_mode
    user_id = message.from_user.id
    chat_id = message.chat.id
    if user_id in user_bans and time.time() < user_bans[user_id]:
        bot.send_message(chat_id, "⛔ Engellisin.")
        return
    if is_maintenance_mode and user_id != ADMIN_ID:
        bot.send_message(chat_id, get_text(user_id, "maintenance_msg"), parse_mode="Markdown")
        return
    user_states[user_id] = None
    
    try:
        if user_id not in first_time_users:
            first_time_users.add(user_id)
            if os.path.exists("hosgeldin.ogg"):
                with open("hosgeldin.ogg", "rb") as vf: bot.send_voice(chat_id, vf)
    except: pass

    txt = get_text(user_id, "welcome")
    if user_id == ADMIN_ID: txt += get_text(user_id, "admin_active")
    bot.send_message(chat_id, txt, reply_markup=get_main_keyboard(user_id), parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    data = call.data
    
    if user_id in user_bans and time.time() < user_bans[user_id]:
        bot.answer_callback_query(call.id, "⛔ Engellisin!", show_alert=True)
        return

    if data.startswith("menu_"):
        bot.answer_callback_query(call.id)
        user_states[user_id] = "waiting_for_link"
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text="🔗 Lütfen indirmek istediğin bağlantıyı (linki) gönder reisim:", reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(get_text(user_id, "back_menu"), callback_data="back_to_main")), parse_mode="Markdown")
        return

    if data == "buy_instant_vip":
        bot.answer_callback_query(call.id)
        bot.send_invoice(chat_id=chat_id, title="Anında Sınırsız İndir", description="7 Yıldız ile tüm indirmeler anında ve sınırsız olsun!", invoice_payload="instant_vip", provider_token="", currency="XTR", prices=[LabeledPrice("Anında VIP", 7)])
        return

    if data == "open_lucky_wheel":
        bot.answer_callback_query(call.id)
        now_date = (datetime.datetime.utcnow() + datetime.timedelta(hours=3)).strftime("%Y-%m-%d")
        if user_id not in wheel_rights or wheel_rights[user_id]["date"] != now_date:
            wheel_rights[user_id] = {"date": now_date, "count": 3}
        kalan = wheel_rights[user_id]["count"]
        m = InlineKeyboardMarkup(row_width=1)
        if kalan > 0: m.add(InlineKeyboardButton("🎲 Çevir", callback_data="spin_wheel_action"))
        m.add(InlineKeyboardButton(get_text(user_id, "back_menu"), callback_data="back_to_main"))
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=f"🎡 Kalan Hak: {kalan}/3", reply_markup=m, parse_mode="Markdown")
        return

    if data == "spin_wheel_action":
        now_date = (datetime.datetime.utcnow() + datetime.timedelta(hours=3)).strftime("%Y-%m-%d")
        if user_id not in wheel_rights or wheel_rights[user_id]["date"] != now_date:
            wheel_rights[user_id] = {"date": now_date, "count": 3}
        if wheel_rights[user_id]["count"] <= 0:
            bot.answer_callback_query(call.id, "⚠️ Hak bitti!", show_alert=True)
            return
        wheel_rights[user_id]["count"] -= 1
        discounts = [50, 80, 90, 100]
        chosen = random.choice(discounts)
        user_discounts[user_id] = chosen
        m = InlineKeyboardMarkup()
        m.add(InlineKeyboardButton("🔄 Tekrar", callback_data="open_lucky_wheel"))
        m.add(InlineKeyboardButton(get_text(user_id, "back_menu"), callback_data="back_to_main"))
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=f"🎉 Tebrikler! %{chosen} İndirim kazandın!", reply_markup=m, parse_mode="Markdown")
        return

    if data == "open_profile":
        bot.answer_callback_query(call.id)
        is_vip = (user_id == ADMIN_ID) or (user_id in unlocked_platforms and time.time() < unlocked_platforms[user_id].get("bitis", 0))
        status_str = "Aktif (Sınırsız / Anında ⚡)" if is_vip else "Standart Kullanıcı (1'er 1'er İndirme)"
        text = f"👤 **Profilin:**\n\nDurum: {status_str}\n"
        m = InlineKeyboardMarkup()
        m.add(InlineKeyboardButton(get_text(user_id, "back_menu"), callback_data="back_to_main"))
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=text, reply_markup=m, parse_mode="Markdown")
        return

    if data == "open_language_menu":
        bot.answer_callback_query(call.id)
        m = InlineKeyboardMarkup(row_width=1)
        m.add(*(InlineKeyboardButton(name, callback_data=f"set_lang_{code}") for name, code in ALL_LANGUAGES))
        m.add(InlineKeyboardButton(get_text(user_id, "back_menu"), callback_data="back_to_main"))
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=get_text(user_id, "lang_select"), reply_markup=m, parse_mode="Markdown")
        return

    if data.startswith("set_lang_"):
        lang_code = data.split("_")[2]
        user_languages[user_id] = lang_code
        bot.answer_callback_query(call.id, f"✅ {lang_code}")
        txt = get_text(user_id, "welcome")
        if user_id == ADMIN_ID: txt += get_text(user_id, "admin_active")
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=txt, reply_markup=get_main_keyboard(user_id), parse_mode="Markdown")
        return

    if data == "back_to_main":
        bot.answer_callback_query(call.id)
        user_states[user_id] = None
        txt = get_text(user_id, "welcome")
        if user_id == ADMIN_ID: txt += get_text(user_id, "admin_active")
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=txt, reply_markup=get_main_keyboard(user_id), parse_mode="Markdown")
        return

    if data in ["dl_video", "dl_audio"]:
        bot.answer_callback_query(call.id)
        link_data = pending_links.get(user_id)
        if not link_data: return
        links = link_data["links"]
        is_audio = (data == "dl_audio")
        
        is_vip = (user_id == ADMIN_ID) or (user_id in unlocked_platforms and time.time() < unlocked_platforms[user_id].get("bitis", 0))
        
        msg_progress = bot.send_message(chat_id, "📥 İndirme hazırlanıyor... %0")
        
        if is_vip:
            bot.edit_message_text("📥 İndiriliyor... %100", chat_id, msg_progress.message_id)
            for index, link in enumerate(links[:999], 1):
                output = f"aud_{user_id}_{index}.m4a" if is_audio else f"vid_{user_id}_{index}.mp4"
                ydl_opts = {'format': 'bestaudio/best' if is_audio else 'best', 'outtmpl': output, 'noplaylist': True}
                try:
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl: ydl.download([link])
                    with open(output, 'rb') as f:
                        if is_audio: bot.send_audio(chat_id, f)
                        else: bot.send_video(chat_id, f)
                    if os.path.exists(output): os.remove(output)
                except:
                    if os.path.exists(output): os.remove(output)
            bot.delete_message(chat_id, msg_progress.message_id)
            pending_links.pop(user_id, None)
            return

        for percent in range(1, 101, 2):
            try:
                bot.edit_message_text(f"📥 İndiriliyor... %{percent}", chat_id, msg_progress.message_id)
            except:
                pass
            time.sleep(0.08)

        for index, link in enumerate(links[:999], 1):
            output = f"aud_{user_id}_{index}.m4a" if is_audio else f"vid_{user_id}_{index}.mp4"
            ydl_opts = {'format': 'bestaudio/best' if is_audio else 'best', 'outtmpl': output, 'noplaylist': True}
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl: ydl.download([link])
                with open(output, 'rb') as f:
                    if is_audio: bot.send_audio(chat_id, f)
                    else: bot.send_video(chat_id, f)
                if os.path.exists(output): os.remove(output)
            except:
                if os.path.exists(output): os.remove(output)
        
        bot.delete_message(chat_id, msg_progress.message_id)
        pending_links.pop(user_id, None)
        return

@bot.pre_checkout_query_handler(func=lambda q: True)
def checkout(q): bot.answer_pre_checkout_query(q.id, ok=True)

@bot.message_handler(content_types=['successful_payment'])
def payment_success(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    unlocked_platforms[user_id] = {"bitis": time.time() + (365 * 86400)}
    bot.send_message(chat_id, "🎉 7 Yıldız ile anında ve sınırsız indirme hakkın tanımlandı!")

@bot.message_handler(func=lambda m: True)
def handle_link_and_security(message):
    global is_maintenance_mode
    user_id = message.from_user.id
    raw_text = message.text.strip() if message.text else ""
    chat_id = message.chat.id
    
    if user_id in user_bans and time.time() < user_bans[user_id]: return
    if is_maintenance_mode and user_id != ADMIN_ID: return
    if raw_text.startswith("/"): return

    if any(w in raw_text.lower() for w in BANNED_WORDS) and user_id != ADMIN_ID:
        if user_id in unlocked_platforms: unlocked_platforms.pop(user_id, None)
        ban_sec = random.randint(3600, 864000)
        user_bans[user_id] = time.time() + ban_sec
        try: bot.delete_message(chat_id, message.message_id)
        except: pass
        bot.send_message(chat_id, f"🚫 Küfür tespit edildi! VIP hakların silindi ve {int(ban_sec/3600)} saat engellendin.")
        return

    links = [l.strip() for l in raw_text.splitlines() if l.strip().startswith("http")]
    if not links:
        bot.reply_to(message, get_text(user_id, "start_fallback"))
        return

    pending_links[user_id] = {"links": links}
    m = InlineKeyboardMarkup(row_width=2)
    m.add(InlineKeyboardButton(get_text(user_id, "btn_video"), callback_data="dl_video"), InlineKeyboardButton(get_text(user_id, "btn_audio"), callback_data="dl_audio"))
    bot.send_message(chat_id, f"📥 {len(links)} bağlantı alındı, format seç:", reply_markup=m)

bot.infinity_polling(skip_pending=True)
        
