import os
import time
import datetime
import random
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import yt_dlp

TOKEN = "8927197392:AAE9QDoXKSHkfdXa_0rrIgmUnVBFrre2bvc"
bot = telebot.TeleBot(TOKEN)
ADMIN_ID = 8520025523

user_states = {}
user_languages = {} 
pending_links = {}  
user_swear_counts = {}

SWEAR_WORDS = ["amk", "aq", "orospu", "piç", "sik", "anan", "amina", "amcık", "mal", "salak"]

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
            "⚡ **Zenith İndirme Botuna Hoş Geldin Reisim!**\n\n"
            "Tamamen **Ücretsiz** ve Hızlı İndirme Modu Aktif!\n\n"
            "🎯 **Nasıl Kullanılır?**\n"
            "Önce aşağıdan indirmek istediğin platform butonuna tıkla, ardından linkini gönder.\n\n"
            "Selam **{name}**, işlem yapmak istediğin seçeneğe tıkla:"
        ),
        "admin_active": "\n\n👑 *Admin Paneli Aktif!*",
        "btn_uzun": "🎬 YouTube Uzun Video (Ücretsiz)",
        "btn_shorts": "📱 YouTube Shorts (Ücretsiz)",
        "btn_tiktok": "🎵 TikTok İndir (Ücretsiz)",
        "btn_insta": "📸 Instagram Reels (Ücretsiz)",
        "btn_profile": "👤 Profilim / Haklarım",
        "btn_lang": "🌐 Dil Seç / Language",
        "lang_select": "🌐 **Lütfen kullanmak istediğin dili seç:**",
        "back_menu": "🔙 Ana Menüye Dön",
        "admin_prompt": "👑 **{p_key}** menüsündesin. Şimdi bu platforma ait bağlantıyı gönder:",
        "err_platform": "❌ **HATA: Yanlış Platform Linki!**\n\nŞu an **{current_menu}** menüsündesin ama farklı bir platformun bağlantısını attın. Lütfen menüye uygun link gönder!",
        "err_no_menu": "⚠️ **Önce Menü Seçmelisin!**\n\nDoğrudan link atamazsın reisim. Önce ana menüden ilgili platform butonuna tıkla, ardından linki gönder.",
        "choose_format": "📥 **Nasıl indirmek istiyorsun?**",
        "btn_video": "🎥 Video İndir",
        "btn_audio": "🎵 MP3 İndir",
        "downloading": "⏳ **Video indiriliyor ve hazırlanıyor, lütfen bekle reisim...**",
    },
    "ku": {
        "welcome": "🤖 **Silav {name}, Bi xêr hatî Botê Daxistina Vîdyoyan! (Belaş)**",
        "admin_active": "\n\n👑 *Panela Admin Çalak e!*",
        "btn_uzun": "🎬 Vîdyoya Dirêj a YouTube",
        "btn_shorts": "📱 YouTube Shorts",
        "btn_tiktok": "🎵 Daxistina TikTok",
        "btn_insta": "📸 Instagram Reels",
        "btn_profile": "👤 Profîla Min",
        "btn_lang": "🌐 Ziman / Dil",
        "lang_select": "🌐 **Ji kerema xwe zimanê xwe hilbijêre:**",
        "back_menu": "🔙 Vegere Menuya Sereke",
        "admin_prompt": "👑 Lînka **{p_key}** bişîne:",
        "err_platform": "❌ **Platforma Çewt!**",
        "err_no_menu": "⚠️ Pêşî menu hilbijêre!",
        "choose_format": "📥 **Çawa dixwazî daxistinê bikî?**",
        "btn_video": "🎥 Vîdyo Daxîne",
        "btn_audio": "🎵 Pelê deng Daxîne",
        "downloading": "⏳ **Tê daxistin, ji kerema xwe bisekinîne...**",
    },
    "en": {
        "welcome": "⚡ **Hello {name}, Welcome to Zenith Downloader Bot! (Free)**",
        "admin_active": "\n\n👑 *Admin Panel Active!*",
        "btn_uzun": "🎬 YouTube Long Video",
        "btn_shorts": "📱 YouTube Shorts",
        "btn_tiktok": "🎵 TikTok Video",
        "btn_insta": "📸 Instagram Reels",
        "btn_profile": "👤 Profile",
        "btn_lang": "🌐 Language",
        "lang_select": "🌐 **Please select your language:**",
        "back_menu": "🔙 Back to Main Menu",
        "admin_prompt": "👑 Send valid **{p_key}** link:",
        "err_platform": "❌ **Wrong Platform!**",
        "err_no_menu": "⚠️ Please select a menu first!",
        "choose_format": "📥 **How do you want to download?**",
        "btn_video": "🎥 Download Video",
        "btn_audio": "🎵 Download MP3",
        "downloading": "⏳ **Downloading and preparing, please wait...**",
    },
    "ar": {
        "welcome": "⚡ **مرحباً {name}، أهلاً بك في بوت تحميل Zenith! (مجاني)**",
        "admin_active": "\n\n👑 *لوحة المشرف نشطة!*",
        "btn_uzun": "🎬 فيديو يوتيوب طويل",
        "btn_shorts": "📱 يوتيوب شورتس",
        "btn_tiktok": "🎵 تيك توك",
        "btn_insta": "📸 إنستغرام ريلز",
        "btn_profile": "👤 ملفي الشخصي",
        "btn_lang": "🌐 اللغة",
        "lang_select": "🌐 **يرجى اختيار لغتك:**",
        "back_menu": "🔙 العودة للقائمة الرئيسية",
        "admin_prompt": "👑 أرسل رابط **{p_key}** صحيح:",
        "err_platform": "❌ **منصة خاطئة!**",
        "err_no_menu": "⚠️ اختر القائمة أولاً!",
        "choose_format": "📥 **كيف تريد التنزيل؟**",
        "btn_video": "🎥 تنزيل فيديو",
        "btn_audio": "🎵 تنزيل MP3",
        "downloading": "⏳ **جاري التنزيل، يرجى الانتظار...**",
    },
    "tk": {
        "welcome": "⚡ **Salam {name}, Zenith Wideo ýükleýji bota hoş geldiňiz! (Mugt)**",
        "admin_active": "\n\n👑 *Admin paneli işjeň!*",
        "btn_uzun": "🎬 YouTube Uzyn Wideo",
        "btn_shorts": "📱 YouTube Shorts",
        "btn_tiktok": "🎵 TikTok Wideo",
        "btn_insta": "Instagram Reels",
        "btn_profile": "👤 Profilim",
        "btn_lang": "🌐 Dil",
        "lang_select": "🌐 **Dil saýlaň:**",
        "back_menu": "🔙 Yzyna",
        "admin_prompt": "👑 Salgyny ibăriň:",
        "err_platform": "❌ Ýalňyş platforma!",
        "err_no_menu": "⚠️ Ilki menu saýlaň!",
        "choose_format": "📥 **Nädip ýükletmeli?**",
        "btn_video": "🎥 Wideo",
        "btn_audio": "🎵 MP3",
        "downloading": "⏳ **Ýüklenýär, garaşyň...**",
    }
}

def get_text(user_id, key, **kwargs):
    lang = user_languages.get(user_id, "tr")
    if lang not in TRANSLATIONS: lang = "tr"
    text = TRANSLATIONS[lang].get(key, TRANSLATIONS["tr"].get(key, ""))
    if kwargs:
        return text.format(**kwargs)
    return text

def get_main_keyboard(user_id):
    m = InlineKeyboardMarkup(row_width=1)
    m.add(
        InlineKeyboardButton(get_text(user_id, "btn_uzun"), callback_data="menu_uzun"),
        InlineKeyboardButton(get_text(user_id, "btn_shorts"), callback_data="menu_shorts"),
        InlineKeyboardButton(get_text(user_id, "btn_tiktok"), callback_data="menu_tiktok"),
        InlineKeyboardButton(get_text(user_id, "btn_insta"), callback_data="menu_insta"),
        InlineKeyboardButton(get_text(user_id, "btn_profile"), callback_data="open_profile"),
        InlineKeyboardButton(get_text(user_id, "btn_lang"), callback_data="open_language_menu")
    )
    return m

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    user_states[user_id] = None  
    user_display_name = message.from_user.first_name or message.from_user.username or "Dostum"
    
    txt = get_text(user_id, "welcome", name=user_display_name)
    if user_id == ADMIN_ID: txt += get_text(user_id, "admin_active")
    bot.send_message(chat_id, txt, reply_markup=get_main_keyboard(user_id), parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    data = call.data
    user_display_name = call.from_user.first_name or call.from_user.username or "Dostum"
    
    if data == "open_profile":
        bot.answer_callback_query(call.id)
        profile_text = (
            f"👤 **Senin Profil Bilgilerin:**\n\n"
            f"👑 **Durum:** Tüm Platformlar Tamamen Sınırsız ve **Ücretsiz**! ✅\n"
            f"📥 Dilediğin kadar video ve MP3 indirebilirsin reisim."
        )
        m = InlineKeyboardMarkup()
        m.add(InlineKeyboardButton(get_text(user_id, "back_menu"), callback_data="back_to_main"))
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=profile_text, reply_markup=m, parse_mode="Markdown")
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
        bot.answer_callback_query(call.id, f"✅ Dil seçildi: {lang_code.upper()}")
        txt = get_text(user_id, "welcome", name=user_display_name)
        if user_id == ADMIN_ID: txt += get_text(user_id, "admin_active")
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=txt, reply_markup=get_main_keyboard(user_id), parse_mode="Markdown")
        return

    if data == "back_to_main":
        bot.answer_callback_query(call.id)
        user_states[user_id] = None
        txt = get_text(user_id, "welcome", name=user_display_name)
        if user_id == ADMIN_ID: txt += get_text(user_id, "admin_active")
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=txt, reply_markup=get_main_keyboard(user_id), parse_mode="Markdown")
        return

    if data in ["dl_video", "dl_audio"]:
        bot.answer_callback_query(call.id)
        link_data = pending_links.get(user_id)
        if not link_data:
            bot.send_message(chat_id, "⚠️ Bağlantı bulunamadı veya zaman aşımına uğradı.")
            return
        
        link = link_data["link"]
        is_audio = (data == "dl_audio")
        
        rand_id = random.randint(1000, 9999)
        output = f"aud_{user_id}_{rand_id}.m4a" if is_audio else f"vid_{user_id}_{rand_id}.mp4"
        
        status_msg = bot.send_message(chat_id, get_text(user_id, "downloading"))

        ydl_opts = {
            'format': 'bestaudio/best' if is_audio else 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': output,
            'noplaylist': True,
            'socket_timeout': 120,
            'nocheckcertificate': True,
            'geo_bypass': True,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            },
            'extractor_args': {'tiktok': {'web_app': True}}
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([link])

            actual_file = output
            if not os.path.exists(actual_file):
                for file in os.listdir('.'):
                    if file.startswith(f"aud_{user_id}_{rand_id}") or file.startswith(f"vid_{user_id}_{rand_id}"):
                        actual_file = file
                        break

            if os.path.exists(actual_file):
                with open(actual_file, 'rb') as f:
                    if is_audio:
                        bot.send_audio(chat_id, f, timeout=300)
                    else:
                        bot.send_video(chat_id, f, timeout=300)
                try:
                    bot.delete_message(chat_id, status_msg.message_id)
                except:
                    pass
                os.remove(actual_file)
            else:
                bot.edit_message_text("❌ Dosya oluşturulamadı, bağlantıyı kontrol et reisim.", chat_id, status_msg.message_id)

        except Exception as e:
            try:
                bot.edit_message_text(f"❌ İndirme hatası: {str(e)[:60]}", chat_id, status_msg.message_id)
            except:
                bot.send_message(chat_id, f"❌ İndirme hatası: {str(e)[:60]}")
            
            for file in os.listdir('.'):
                if f"{user_id}_{rand_id}" in file:
                    try:
                        os.remove(file)
                    except:
                        pass
            
        pending_links.pop(user_id, None)
        user_states[user_id] = None
        return

    if data.startswith("menu_"):
        p_key = data.replace("menu_", "")
        user_states[user_id] = f"active_{p_key}"
        bot.answer_callback_query(call.id)
        m = InlineKeyboardMarkup()
        m.add(InlineKeyboardButton(get_text(user_id, "back_menu"), callback_data="back_to_main"))
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=get_text(user_id, "admin_prompt", p_key=p_key.upper()), reply_markup=m, parse_mode="Markdown")
        return

@bot.message_handler(func=lambda m: True)
def handle_link(message):
    user_id = message.from_user.id
    raw_text = message.text.strip()
    chat_id = message.chat.id
    
    if raw_text.startswith("/"):
        return

    text_lower = raw_text.lower()
    if any(swear in text_lower for swear in SWEAR_WORDS):
        if user_id not in user_swear_counts: user_swear_counts[user_id] = 0
        user_swear_counts[user_id] += 1
        bot.reply_to(message, f"⚠️ **Küfür Uyarısı ({user_swear_counts[user_id]}/3)**")
        return
        
    current_state = user_states.get(user_id)
    
    if not current_state or not current_state.startswith("active_"):
        bot.reply_to(message, get_text(user_id, "err_no_menu"))
        return

    p_type = current_state.replace("active_", "")
    
    link = next((line.strip() for line in raw_text.splitlines() if line.strip().startswith("http")), None)
    if not link:
        bot.reply_to(message, "⚠️ Lütfen geçerli bir video bağlantısı (linki) gönderin.")
        return

    is_tiktok = "tiktok.com" in link or "vm.tiktok.com" in link or "vt.tiktok.com" in link
    is_insta = "instagram.com" in link or "instagr.am" in link
    is_yt = "youtube.com" in link or "youtu.be" in link

    target_match = True
    if p_type == "tiktok" and not is_tiktok: target_match = False
    if p_type == "insta" and not is_insta: target_match = False
    if (p_type == "uzun" or p_type == "shorts") and not is_yt: target_match = False

    if not target_match:
        bot.reply_to(message, get_text(user_id, "err_platform", current_menu=p_type.upper()))
        return

    pending_links[user_id] = {"link": link}
    
    format_markup = InlineKeyboardMarkup(row_width=2)
    format_markup.add(
        InlineKeyboardButton(get_text(user_id, "btn_video"), callback_data="dl_video"),
        InlineKeyboardButton(get_text(user_id, "btn_audio"), callback_data="dl_audio")
    )
    bot.send_message(chat_id, get_text(user_id, "choose_format"), reply_markup=format_markup, parse_mode="Markdown")

bot.infinity_polling()
    
