import os
import time
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, LabeledPrice
import yt_dlp

TOKEN = "8927197392:8892383697:AAE9QDoXKSHkfdXa_0rrIgmUnVBFrre2bvc"
bot = telebot.TeleBot(TOKEN)
ADMIN_ID = 8520025523

user_states = {}
unlocked_platforms = {} 
user_languages = {} 
pending_links = {}  

ALL_LANGUAGES = [
    ("🇹🇷 Türkçe", "tr"), 
    ("☀️ Kürtçe (Kurmancî)", "ku"), 
    ("🇬🇧 English", "en"), 
    ("🇸🇦 العربية", "ar"), 
    ("🇹🇲 Türkmence (Türkmençe)", "tk")
]

TRANSLATIONS = {
    "tr": {
        "welcome": "🤖 Video İndirici Botuna Hoş Geldin!\n\nİşlem yapmak istediğin seçeneğe tıkla:",
        "admin_active": "\n\n👑 *Admin Paneli Aktif!*",
        "btn_uzun": "🎬 YouTube Uzun Video (40 Yıldız) - 198300 Hak (1596 Gün)",
        "btn_shorts": "📱 YouTube Shorts (40 Yıldız) - 198300 Hak (1596 Gün)",
        "btn_tiktok": "🎵 TikTok Video İndir (70 Yıldız) - 198300 Hak (1596 Gün)",
        "btn_insta": "📸 Instagram Reels (50 Yıldız) - 198300 Hak (1596 Gün)",
        "btn_profile": "👤 Profilim / Kalan Haklarım",
        "btn_lang": "🌐 Dil Seç / Ziman / Language / Dil",
        "lang_select": "🌐 Lütfen kullanmak istediğin dili seç:",
        "back_menu": "🔙 Ana Menüye Dön",
        "admin_prompt": "👑 Admin Özel: Lütfen geçerli bir {p_key} bağlantısı gönder:",
        "user_prompt": "📥 Harika! İlgili platform için bağlantı(ları) gönder.",
        "payment_success": "🎉 Ödeme başarılı! 198300 indirme hakkın tanımlandı.",
        "no_rights": "⚠️ Bu platform için aktif hakkın bulunmuyor.",
        "expired": "⏳ Süren veya indirme hakkın doldu.",
        "err_uzun": "❌ Bu seçenek sadece Normal YouTube Uzun Video içindir!",
        "err_shorts": "❌ Bu seçenek sadece YouTube Shorts içindir!",
        "err_tiktok": "❌ Bu seçenek sadece TikTok içindir!",
        "err_insta": "❌ Bu seçenek sadece Instagram içindir!",
        "choose_format": "📥 Nasıl indirmek istiyorsun?",
        "btn_video": "🎥 Video İndir",
        "btn_audio": "🎵 MP3 (Ses) İndir",
        "downloading": "⏳ İndiriliyor, lütfen bekle...",
        "multi_progress": "🔄 Toplu İndirme: {current}/{total} adet video işleniyor...",
        "success_video": "✅ Videonu galeriye kaydetmeyi unutma dostum!😀",
        "success_audio": "🎵 Ses dosyan hazır!",
        "start_fallback": "Lütfen /start yazıp menüden seçim yap."
    },
    "ku": {
        "welcome": "🤖 Bi xêr hatî Botê Daxistina Vîdyoyan!",
        "admin_active": "\n\n👑 *Panela Admin Çalak e!*",
        "btn_uzun": "🎬 Vîdyoya Dirêj a YouTube (40 Stêrk)",
        "btn_shorts": "📱 YouTube Shorts (40 Stêrk)",
        "btn_tiktok": "🎵 Daxistina TikTok (70 Stêrk)",
        "btn_insta": "📸 Instagram Reels (50 Stêrk)",
        "btn_profile": "👤 Profîla Min / Mafên Mayî",
        "btn_lang": "🌐 Dil Seç / Ziman / Language / Dil",
        "lang_select": "🌐 Ji kerema xwe zimanê xwe hilbijêre:",
        "back_menu": "🔙 Vegere Menuya Sereke",
        "admin_prompt": "👑 Taybet a Admin: Lînka {p_key} bişîne:",
        "user_prompt": "📥 Lînka xwe bişîne:",
        "payment_success": "🎉 Dravdan serketî bû!",
        "no_rights": "⚠️ Mafê te yê vê platformê nîne.",
        "expired": "⏳ Dem an mafê te qediya.",
        "err_uzun": "❌ Tenê ji bo vîdyoyên dirêj ên YouTube!",
        "err_shorts": "❌ Tenê ji bo YouTube Shorts!",
        "err_tiktok": "❌ Tenê ji bo TikTok!",
        "err_insta": "❌ Tenê ji bo Instagram!",
        "choose_format": "📥 Çawa dixwazî daxistinê bikî?",
        "btn_video": "🎥 Vîdyo Daxîne",
        "btn_audio": "🎵 MP3 Daxîne",
        "downloading": "⏳ Tê daxistin...",
        "multi_progress": "🔄 Daxistina berhev: {current}/{total}...",
        "success_video": "✅ Vîdyoya xwe li galeriyê tomar bike!","success_audio": "🎵 Pelê deng amade ye!",
        "start_fallback": "Ji kerema xwe /start binivîse."
    },
    "en": {
        "welcome": "🤖 Welcome to Video Downloader Bot!",
        "admin_active": "\n\n👑 *Admin Panel Active!*",
        "btn_uzun": "🎬 YouTube Long Video (40 Stars)",
        "btn_shorts": "📱 YouTube Shorts (40 Stars)",
        "btn_tiktok": "🎵 TikTok Video (70 Stars)",
        "btn_insta": "📸 Instagram Reels (50 Stars)",
        "btn_profile": "👤 Profile / Remaining Rights",
        "btn_lang": "🌐 Language / Dil",
        "lang_select": "🌐 Please select your language:",
        "back_menu": "🔙 Back to Main Menu",
        "admin_prompt": "👑 Admin Special: Send valid {p_key} links:",
        "user_prompt": "📥 Send your link(s):",
        "payment_success": "🎉 Payment successful!",
        "no_rights": "⚠️ You don't have rights for this platform.",
        "expired": "⏳ Your rights have expired.",
        "err_uzun": "❌ Only for YouTube Long Videos!",
        "err_shorts": "❌ Only for YouTube Shorts!",
        "err_tiktok": "❌ Only for TikTok!",
        "err_insta": "❌ Only for Instagram!",
        "choose_format": "📥 How do you want to download?",
        "btn_video": "🎥 Download Video",
        "btn_audio": "🎵 Download MP3",
        "downloading": "⏳ Downloading...",
        "multi_progress": "🔄 Downloading: {current}/{total}...",
        "success_video": "✅ Video downloaded successfully!",
        "success_audio": "🎵 Audio file is ready!",
        "start_fallback": "Please type /start."
    },
    "ar": {
        "welcome": "🤖 مرحباً بك في بوت تحميل الفيديو!",
        "admin_active": "\n\n👑 *لوحة المشرف نشطة!*",
        "btn_uzun": "🎬 فيديو يوتيوب طويل",
        "btn_shorts": "📱 يوتيوب شورتس",
        "btn_tiktok": "🎵 تيك توك",
        "btn_insta": "📸 إنستغرام ريلز",
        "btn_profile": "👤 ملفي الشخصي / الحقوق المتبقية",
        "btn_lang": "🌐 اللغة",
        "lang_select": "🌐 يرجى اختيار لغتك:",
        "back_menu": "🔙 العودة للقائمة الرئيسية",
        "admin_prompt": "👑 خاص للمشرف: أرسل الروابط:",
        "user_prompt": "📥 أرسل الروابط:",
        "payment_success": "🎉 نجح الدفع!",
        "no_rights": "⚠️ ليس لديك حقوق نشطة.",
        "expired": "⏳ انتهت صلاحية حقوقك.",
        "err_uzun": "❌ لفيديوهات يوتيوب الطويلة فقط!",
        "err_shorts": "❌ ليوتيوب شورتس فقط!",
        "err_tiktok": "❌ لتيك توك فقط!",
        "err_insta": "❌ لإنستغرام فقط!",
        "choose_format": "📥 كيف تريد التنزيل؟",
        "btn_video": "🎥 تنزيل فيديو",
        "btn_audio": "🎵 تنزيل MP3",
        "downloading": "⏳ جاري التحميل...",
        "multi_progress": "🔄 جاري التحميل: {current}/{total}...",
        "success_video": "✅ تم التحميل بنجاح!",
        "success_audio": "🎵 الملف الصوتي جاهز!",
        "start_fallback": "يرجى كتابة /start."
    },
    "tk": {
        "welcome": "🤖 Wideo ýükleýji bota hoş geldiňiz!",
        "admin_active": "\n\n👑 *Admin paneli işjeň!*",
        "btn_uzun": "🎬 YouTube Uzyn Wideo",
        "btn_shorts": "📱 YouTube Shorts",
        "btn_tiktok": "🎵 TikTok Wideo",
        "btn_insta": "📸 Instagram Reels",
        "btn_profile": "👤 Profilim / Galan Haklarym",
        "btn_lang": "🌐 Dil",
        "lang_select": "🌐 Dil saýlaň:",
        "back_menu": "🔙 Yzyna",
        "admin_prompt": "👑 Admin: Salgylary ibăriň:",
        "user_prompt": "📥 Salgylaryňyzy iberiň:",
        "payment_success": "🎉 Töleg üstünlikli!",
        "no_rights": "⚠️ Ygtyýaryňyz ýok.",
        "expired": "⏳ Wagtyňyz gutardy.",
        "err_uzun": "❌ Diňe uzyn wideolar üçin!",
        "err_shorts": "❌ Diňe Shorts üçin!",
        "err_tiktok": "❌ Diňe TikTok üçin!",
        "err_insta": "❌ Diňe Instagram üçin!",
        "choose_format": "📥 Nädip ýükletmeli?","btn_video": "🎥 Wideo",
        "btn_audio": "🎵 MP3",
        "downloading": "⏳ Ýüklenýär...",
        "multi_progress": "🔄 Ýüklenýär: {current}/{total}...",
        "success_video": "✅ Ýüklendi!",
        "success_audio": "🎵 Ses taýýar!",
        "start_fallback": "/start ýazyň."
    }
}

def get_text(user_id, key):
    lang = user_languages.get(user_id, "tr")
    if lang not in TRANSLATIONS: lang = "tr"
    return TRANSLATIONS[lang].get(key, TRANSLATIONS["tr"].get(key, ""))

def get_main_keyboard(user_id):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(get_text(user_id, "btn_uzun"), callback_data="unlock_yt_uzun"),
        InlineKeyboardButton(get_text(user_id, "btn_shorts"), callback_data="unlock_yt_shorts"),
        InlineKeyboardButton(get_text(user_id, "btn_tiktok"), callback_data="unlock_tiktok"),
        InlineKeyboardButton(get_text(user_id, "btn_insta"), callback_data="unlock_insta"),
        InlineKeyboardButton(get_text(user_id, "btn_profile"), callback_data="open_profile"),
        InlineKeyboardButton(get_text(user_id, "btn_lang"), callback_data="open_language_menu")
    )
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    txt = get_text(user_id, "welcome")
    if user_id == ADMIN_ID: txt += get_text(user_id, "admin_active")
    bot.send_message(chat_id, txt, reply_markup=get_main_keyboard(user_id), parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    data = call.data
    
    if data == "open_profile":
        bot.answer_callback_query(call.id)
        user_platforms = unlocked_platforms.get(user_id, {})
        profile_text = f"👤 Senin Profil Bilgilerin:\n\n"
        platforms_list = [("uzun", "🎬 YouTube Uzun"), ("shorts", "📱 YouTube Shorts"), ("tiktok", "🎵 TikTok"), ("insta", "📸 Instagram")]
        
        if user_id == ADMIN_ID:
            profile_text += "👑 Admin Hesabı: Tüm platformlar sınırsız ve aktif!\n\n"
        
        for p_key, p_name in platforms_list:
            if user_id == ADMIN_ID or (p_key in user_platforms and user_platforms[p_key]["hak"] > 0 and time.time() < user_platforms[p_key]["bitis"]):
                if user_id == ADMIN_ID:
                    profile_text += f"✅ {p_name}: Aktif (Sınırsız Admin)\n"
                else:
                    hak = user_platforms[p_key]["hak"]
                    kal_gun = max(0, int((user_platforms[p_key]["bitis"] - time.time()) / 86400))
                    profile_text += f"✅ {p_name}: Aktif | Hak: {hak} | Gün: {kal_gun}\n"
            else:
                profile_text += f"❌ {p_name}: Aktif Değil\n"
                
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
        bot.answer_callback_query(call.id, f"✅ Dil: {lang_code.upper()}")txt = get_text(user_id, "welcome")
        if user_id == ADMIN_ID: txt += get_text(user_id, "admin_active")
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=txt, reply_markup=get_main_keyboard(user_id), parse_mode="Markdown")
        return

    if data == "back_to_main":
        bot.answer_callback_query(call.id)
        txt = get_text(user_id, "welcome")
        if user_id == ADMIN_ID: txt += get_text(user_id, "admin_active")
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=txt, reply_markup=get_main_keyboard(user_id), parse_mode="Markdown")
        return

    if data in ["dl_video", "dl_audio"]:
        bot.answer_callback_query(call.id)
        link_data = pending_links.get(user_id)
        if not link_data:
            bot.send_message(chat_id, get_text(user_id, "start_fallback"))
            return
        
        links = link_data["links"]
        is_audio = (data == "dl_audio")
        total_links = len(links)
        current_state = user_states.get(user_id, "")
        p_type = next((k for k in ["uzun", "shorts", "tiktok", "insta"] if k in current_state), "")

        for index, link in enumerate(links[:999], 1):
            if user_id != ADMIN_ID and p_type:
                if user_id not in unlocked_platforms or p_type not in unlocked_platforms[user_id]:
                    bot.send_message(chat_id, get_text(user_id, "no_rights"))
                    break
                udat = unlocked_platforms[user_id][p_type]
                if time.time() > udat["bitis"] or udat["hak"] <= 0:
                    bot.send_message(chat_id, get_text(user_id, "expired"))
                    break
                udat["hak"] -= 1

            status_msg = bot.send_message(chat_id, get_text(user_id, "multi_progress").format(current=index, total=total_links), parse_mode="Markdown")
            
            output = f"aud_{user_id}_{index}.m4a" if is_audio else f"vid_{user_id}_{index}.mp4"
            ydl_opts = {
                'format': 'bestaudio/best' if is_audio else 'best[height<=720]/best[ext=mp4]/best',
                'outtmpl': output,
                'noplaylist': True,
                'socket_timeout': 60,
                'nocheckcertificate': True,
                'extractor_args': {'youtube': {'player_client': ['android', 'web', 'mweb']}}
            }

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([link])

                with open(output, 'rb') as f:
                    if is_audio:
                        bot.send_audio(chat_id, f, caption=get_text(user_id, "success_audio"), timeout=120)
                    else:
                        bot.send_video(chat_id, f, caption=get_text(user_id, "success_video"), timeout=120)
                if os.path.exists(output): os.remove(output)
            except Exception as e:
                bot.send_message(chat_id, f"❌ Hata ({index}. link): {e}")
                if os.path.exists(output): os.remove(output)
            
            try: bot.delete_message(chat_id, status_msg.message_id)
            except: pass
            
        pending_links.pop(user_id, None)
        user_states[user_id] = None
        return

    if user_id == ADMIN_ID and data.startswith("unlock_"):
        p_key = data.replace("unlock_", "").replace("yt_", "")
        user_states[user_id] = f"waiting_for_{p_key}"
        bot.answer_callback_query(call.id, f"👑 Admin: {p_key} açıldı!")
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=get_text(user_id, "admin_prompt").format(p_key=p_key), parse_mode="Markdown")
        return

    payloads = {"unlock_yt_uzun": "uzun", "unlock_yt_shorts": "shorts", "unlock_tiktok": "tiktok", "unlock_insta": "insta"}if data in payloads:
        bot.answer_callback_query(call.id)
        prices = {"uzun": 40, "shorts": 40, "tiktok": 70, "insta": 50}
        pl = payloads[data]
        bot.send_invoice(chat_id=chat_id, title=pl.capitalize(), description="198300 Hak", invoice_payload=pl, provider_token="", currency="XTR", prices=[LabeledPrice(pl, prices[pl])])

@bot.pre_checkout_query_handler(func=lambda q: True)
def checkout(q):
    bot.answer_pre_checkout_query(q.id, ok=True)

@bot.message_handler(content_types=['successful_payment'])
def payment_success(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    payload = message.successful_payment.invoice_payload
    if user_id not in unlocked_platforms: unlocked_platforms[user_id] = {}
    unlocked_platforms[user_id][payload] = {"hak": 198300, "bitis": time.time() + (1596 * 86400)}
    user_states[user_id] = f"waiting_for_{payload}"
    bot.send_message(chat_id, get_text(user_id, "payment_success"))

@bot.message_handler(func=lambda m: True)
def handle_link(message):
    user_id = message.from_user.id
    raw_text = message.text.strip()
    chat_id = message.chat.id
    links = [line.strip() for line in raw_text.splitlines() if line.strip().startswith("http")]
    
    if not links:
        bot.reply_to(message, get_text(user_id, "start_fallback"))
        return

    current_state = user_states.get(user_id)
    for text in links[:999]:
        text_lower = text.lower()
        is_valid, error_msg = True, ""
        
        if current_state == "waiting_for_uzun":
            if "youtube.com/shorts" in text_lower or ("youtube.com" not in text_lower and "youtu.be" not in text_lower):
                is_valid, error_msg = False, get_text(user_id, "err_uzun")
        elif current_state == "waiting_for_shorts":
            if "youtube.com/shorts" not in text_lower:
                is_valid, error_msg = False, get_text(user_id, "err_shorts")
        elif current_state == "waiting_for_tiktok":
            if "tiktok.com" not in text_lower:
                is_valid, error_msg = False, get_text(user_id, "err_tiktok")
        elif current_state == "waiting_for_insta":
            if "instagram.com" not in text_lower:
                is_valid, error_msg = False, get_text(user_id, "err_insta")
        
        if not is_valid and current_state:
            bot.send_message(chat_id, error_msg, parse_mode="Markdown")
            return

    pending_links[user_id] = {"links": links[:999]}
    format_markup = InlineKeyboardMarkup(row_width=2)
    format_markup.add(
        InlineKeyboardButton(get_text(user_id, "btn_video"), callback_data="dl_video"),
        InlineKeyboardButton(get_text(user_id, "btn_audio"), callback_data="dl_audio")
    )
    bot.send_message(chat_id, f"📥 {len(links[:999])} adet bağlantı alındı!\n\n" + get_text(user_id, "choose_format"), reply_markup=format_markup, parse_mode="Markdown")

bot.infinity_polling(skip_pending=True)
