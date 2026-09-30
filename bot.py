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
user_swear_counts = {}

daily_winners = {}  
last_reward_date = ""

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
            "⚡ **Zenith İndirme Botuna Hoş Geldiniz!**\n\n"
            "Versiyon **2.8.4.7** sürümüyle karşınızdayız! Bu botumuz tamamen filigransız ve hızlı videolar indirmeniz için tasarlandı.\n\n"
            "🎯 **Nasıl Kullanılır?**\n"
            "İstediğiniz platform butonuna tıklayın, ardından indirmek istediğiniz videonun bağlantısını (linkini) bize gönderin. Saniyeler içinde videonuzu hazırlayalım!\n\n"
            "⚠️ **Önemli Kurallar & Uyarı:**\n"
            "Bota üst üste küfür veya hakaret atıldığı tespit edilirse sistem otomatik olarak sizi engeller ve tüm VIP / indirme haklarınız sıfırlanır. Lütfen saygı çerçevesinde kalın.\n\n"
            "Selam **{name}**, işlem yapmak istediğin seçeneğe tıkla:"
        ),
        "admin_active": "\n\n👑 *Admin Paneli Aktif!*",
        "btn_uzun": "🎬 YouTube Uzun (120 Yıldız) - 18753 Hak",
        "btn_shorts": "📱 YouTube Shorts (120 Yıldız) - 18753 Hak",
        "btn_tiktok": "🎵 TikTok İndir (120 Yıldız) - 18753 Hak",
        "btn_insta": "📸 Instagram Reels (120 Yıldız) - 18753 Hak",
        "btn_profile": "👤 Profilim / Haklarım",
        "btn_lang": "🌐 Dil Seç / Language",
        "lang_select": "🌐 **Lütfen kullanmak istediğin dili seç:**",
        "back_menu": "🔙 Ana Menüye Dön",
        "admin_prompt": "👑 **{p_key}** menüsündesin. Lütfen indirmek istediğin bağlantıyı gönder:",
        "payment_success": "🎉 Ödeme başarılı! 18.753 indirme hakkın tanımlandı.",
        "choose_format": "📥 **Nasıl indirmek istiyorsun?**",
        "btn_video": "🎥 Video İndir",
        "btn_audio": "🎵 MP3 İndir",
    },
    "ku": {
        "welcome": "🤖 **Silav {name}, Bi xêr hatî Botê Daxistina Vîdyoyan!**",
        "admin_active": "\n\n👑 *Panela Admin Çalak e!*",
        "btn_uzun": "🎬 Vîdyoya Dirêj a YouTube",
        "btn_shorts": "📱 YouTube Shorts",
        "btn_tiktok": "🎵 Daxistina TikTok",
        "btn_insta": "📸 Instagram Reels",
        "btn_profile": "👤 Profîla Min",
        "btn_lang": "🌐 Ziman / Dil",
        "lang_select": "🌐 **Ji kerema xwe zimanê xwe hilbijêre:**",
        "back_menu": "🔙 Vegere Menuya Sereke",
        "admin_prompt": "👑 Lînka xwe bişîne:",
        "payment_success": "🎉 Dravdan serketî bû!",
        "choose_format": "📥 **Çawa dixwazî daxistinê bikî?**",
        "btn_video": "🎥 Vîdyo Daxîne",
        "btn_audio": "🎵 Pelê deng Daxîne",
    },
    "en": {
        "welcome": "⚡ **Hello {name}, Welcome to Zenith Downloader Bot!**",
        "admin_active": "\n\n👑 *Admin Panel Active!*",
        "btn_uzun": "🎬 YouTube Long Video",
        "btn_shorts": "📱 YouTube Shorts",
        "btn_tiktok": "🎵 TikTok Video",
        "btn_insta": "📸 Instagram Reels",
        "btn_profile": "👤 Profile",
        "btn_lang": "🌐 Language",
        "lang_select": "🌐 **Please select your language:**",
        "back_menu": "🔙 Back to Main Menu",
        "admin_prompt": "👑 Send your link:",
        "payment_success": "🎉 Payment successful!",
        "choose_format": "📥 **How do you want to download?**",
        "btn_video": "🎥 Download Video",
        "btn_audio": "🎵 Download MP3",
    },
    "ar": {
        "welcome": "⚡ **مرحباً {name}، أهلاً بك في بوت تحميل Zenith!**",
        "admin_active": "\n\n👑 *لوحة المشرف نشطة!*",
        "btn_uzun": "🎬 فيديو يوتيوب طويل",
        "btn_shorts": "📱 يوتيوب شورتس",
        "btn_tiktok": "🎵 تيك توك",
        "btn_insta": "📸 إنستغرام ريلز",
        "btn_profile": "👤 ملفي الشخصي",
        "btn_lang": "🌐 اللغة",
        "lang_select": "🌐 **يرجى اختيار لغتك:**",
        "back_menu": "🔙 العودة للقائمة الرئيسية",
        "admin_prompt": "👑 أرسل الرابط:",
        "payment_success": "🎉 نجح الدفع!",
        "choose_format": "📥 **كيف تريد التنزيل؟**",
        "btn_video": "🎥 تنزيل فيديو",
        "btn_audio": "🎵 تنزيل MP3",
    },
    "tk": {
        "welcome": "⚡ **Salam {name}, Zenith Wideo ýükleýji bota hoş geldiňiz!**",
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
        "payment_success": "🎉 Töleg üstünlikli!",
        "choose_format": "📥 **Nädip ýükletmeli?**",
        "btn_video": "🎥 Wideo",
        "btn_audio": "🎵 MP3",
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
    global last_reward_date, daily_winners
    user_id = message.from_user.id
    chat_id = message.chat.id
    user_states[user_id] = None
    user_display_name = message.from_user.first_name or message.from_user.username or "Dostum"
    
    now_tr = datetime.datetime.utcnow() + datetime.timedelta(hours=3)
    current_date_str = now_tr.strftime("%Y-%m-%d")
    current_hour = now_tr.hour
    current_minute = now_tr.minute

    if last_reward_date != current_date_str:
        last_reward_date = current_date_str
        daily_winners[current_date_str] = []

    reward_message = ""
    today_list = daily_winners.get(current_date_str, [])
    
    if current_hour == 13 and 0 <= current_minute <= 5 and user_id not in today_list and len(today_list) < 3:
        platforms = ["uzun", "shorts", "tiktok", "insta"]
        chosen_platform = random.choice(platforms)
        if user_id not in unlocked_platforms: unlocked_platforms[user_id] = {}
        unlocked_platforms[user_id][chosen_platform] = {"hak": 18753, "bitis": time.time() + (365 * 86400)}
        daily_winners[current_date_str].append(user_id)
        reward_message = f"\n\n🎁 **Tebrikler! Günlük Ödülünü Kazandın!**\n"

    txt = get_text(user_id, "welcome", name=user_display_name) + reward_message
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
        user_platforms = unlocked_platforms.get(user_id, {})
        profile_text = f"👤 **Senin Profil Bilgilerin:**\n\n"
        platforms_list = [("uzun", "🎬 YouTube Uzun"), ("shorts", "📱 YouTube Shorts"), ("tiktok", "🎵 TikTok"), ("insta", "📸 Instagram")]
        
        if user_id == ADMIN_ID:
            profile_text += "👑 **Admin Hesabı:** Tüm platformlar sınırsız ve aktif!\n\n"
        
        for p_key, p_name in platforms_list:
            if user_id == ADMIN_ID or (p_key in user_platforms and user_platforms[p_key]["hak"] > 0 and time.time() < user_platforms[p_key]["bitis"]):
                hak = user_platforms[p_key]["hak"]
                profile_text += f"✅ **{p_name}**: Aktif | Kalan Hak: `{hak}`\n"
            else:
                profile_text += f"❌ **{p_name}**: Kilitli (120 Yıldız)\n"
                
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
        output = f"aud_{user_id}.m4a" if is_audio else f"vid_{user_id}.mp4"
        
        ydl_opts = {
            'format': 'bestaudio/best' if is_audio else 'bestvideo+bestaudio/best',
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

            with open(output, 'rb') as f:
                if is_audio:
                    bot.send_audio(chat_id, f, timeout=300)
                else:
                    bot.send_video(chat_id, f, timeout=300)
            if os.path.exists(output): os.remove(output)
        except Exception as e:
            if os.path.exists(output): os.remove(output)
            bot.send_message(chat_id, f"❌ İndirme sırasında hata oluştu: {str(e)[:50]}")
            
        pending_links.pop(user_id, None)
        user_states[user_id] = None
        return

    if data.startswith("menu_"):
        p_key = data.replace("menu_", "")
        user_platforms = unlocked_platforms.get(user_id, {})
        
        if user_id != ADMIN_ID and (p_key not in user_platforms or user_platforms[p_key]["hak"] <= 0 or time.time() > user_platforms[p_key]["bitis"]):
            bot.answer_callback_query(call.id, "💳 Bu platform kilitli, 120 Yıldız ödeme ekranı açılıyor!")
            bot.send_invoice(
                chat_id=chat_id, 
                title=f"{p_key.upper()} Sınırsız Erişim", 
                description="Sadece bu platform için geçerli 18.753 indirme hakkı", 
                invoice_payload=p_key, 
                provider_token="", 
                currency="XTR", 
                prices=[LabeledPrice(p_key, 120)]
            )
            return

        user_states[user_id] = f"active_{p_key}"
        bot.answer_callback_query(call.id)
        m = InlineKeyboardMarkup()
        m.add(InlineKeyboardButton(get_text(user_id, "back_menu"), callback_data="back_to_main"))
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=get_text(user_id, "admin_prompt", p_key=p_key.upper()), reply_markup=m, parse_mode="Markdown")
        return

@bot.pre_checkout_query_handler(func=lambda q: True)
def checkout(q):
    bot.answer_pre_checkout_query(q.id, ok=True)

@bot.message_handler(content_types=['successful_payment'])
def payment_success(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    payload = message.successful_payment.invoice_payload
    
    if user_id not in unlocked_platforms: unlocked_platforms[user_id] = {}
    unlocked_platforms[user_id][payload] = {"hak": 18753, "bitis": time.time() + (365 * 86400)}
    user_states[user_id] = f"active_{payload}"
    bot.send_message(chat_id, get_text(user_id, "payment_success"))

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
        
    link = next((line.strip() for line in raw_text.splitlines() if line.strip().startswith("http")), None)
    if not link:
        bot.reply_to(message, "⚠️ Lütfen geçerli bir video bağlantısı (linki) gönderin.")
        return

    # KANAL ZORUNLULUĞU VEYA PLATFORM HATASI TAMAMEN KALdirILDI:
    # Hangi menüde olursan ol veya hangi linki atarsan at doğrudan format seçimine yönlendirilir.
    pending_links[user_id] = {"link": link}
    format_markup = InlineKeyboardMarkup(row_width=2)
    format_markup.add(
        InlineKeyboardButton(get_text(user_id, "btn_video"), callback_data="dl_video"),
        InlineKeyboardButton(get_text(user_id, "btn_audio"), callback_data="dl_audio")
    )
    bot.send_message(chat_id, get_text(user_id, "choose_format"), reply_markup=format_markup, parse_mode="Markdown")

bot.infinity_polling()
