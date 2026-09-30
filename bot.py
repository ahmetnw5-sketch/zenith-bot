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
fast_downloads = {} 
user_swear_counts = {}

daily_winners = {}  
last_reward_date = ""

PLATFORM_LIMITS = {
    "uzun": 20,
    "shorts": 30,
    "tiktok": 64,  
    "insta": 30
}

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
            "Versiyon **2.8.4.6** sürümüyle karşınızdayız! Bu botumuz tamamen filigransız ve hızlı videolar indirmeniz için tasarlandı.\n\n"
            "🎯 **Nasıl Kullanılır?**\n"
            "İstediğiniz platform butonuna tıklayın, ardından indirmek istediğiniz videonun bağlantısını (linkini) bize gönderin. Saniyeler içinde videonuzu hazırlayalım!\n\n"
            "⚠️ **Önemli Kurallar & Uyarı:**\n"
            "Bota üst üste küfür veya hakaret atıldığı tespit edilirse sistem otomatik olarak sizi engeller ve tüm VIP / indirme haklarınız sıfırlanır. Lütfen saygı çerçevesinde kalın.\n\n"
            "Selam **{name}**, işlem yapmak istediğin seçeneğe tıkla:"
        ),
        "admin_active": "\n\n👑 *Admin Paneli Aktif!*",
        "btn_uzun": "🎬 YouTube Uzun (150 Yıldız) - 5200 Hak",
        "btn_shorts": "📱 YouTube Shorts (150 Yıldız) - 5200 Hak",
        "btn_tiktok": "🎵 TikTok İndir (200 Yıldız) - 5200 Hak",
        "btn_insta": "📸 Instagram Reels (180 Yıldız) - 5200 Hak",
        "btn_profile": "👤 Profilim / Kalan Haklarım",
        "btn_lang": "🌐 Dil Seç / Language",
        "lang_select": "🌐 **Lütfen kullanmak istediğin dili seç:**",
        "back_menu": "🔙 Ana Menüye Dön",
        "admin_prompt": "👑 **Admin Özel:** Lütfen geçerli bir **{p_key}** bağlantısı gönder:",
        "payment_success": "🎉 Ödeme başarılı! 5200 indirme hakkın tanımlandı.",
        "fast_payment_success": "⚡ Hızlı indirme açıldı! Video hemen indiriliyor...",
        "no_rights": "⚠️ Bu platform için aktif hakkın bulunmuyor.",
        "expired": "⏳ Süren veya indirme hakkın doldu.",
        "err_uzun": "❌ Bu seçenek sadece **Normal YouTube Uzun Video** içindir!",
        "err_shorts": "❌ Bu seçenek sadece **YouTube Shorts** içindir!",
        "err_tiktok": "❌ Bu seçenek sadece **TikTok** bağlantısı olmalıdır!",
        "err_insta": "❌ Bu seçenek sadece **Instagram** bağlantısı olmalıdır!",
        "limit_exceeded": "⚠ **Sınır Aşıldı!** Bu platform için tek seferde en fazla **{limit}** adet link gönderebilirsin.",
        "choose_format": "📥 **Nasıl indirmek istiyorsun?**",
        "btn_video": "🎥 Video İndir",
        "btn_audio": "🎵 MP3 İndir",
        "btn_fast": "⚡ 7 Yıldız ile Anında İndir",
        "success_video": "✅ Videon hazır dostum!😀",
        "success_audio": "🎵 Ses dosyan hazır!",
        "start_fallback": "Lütfen `/start` yazıp menüden seçim yap."
    },
    "ku": {
        "welcome": "🤖 **Silav {name}, Bi xêr hatî Botê Daxistina Vîdyoyan (Zenith v2.8.4.6)!**",
        "admin_active": "\n\n👑 *Panela Admin Çalak e!*",
        "btn_uzun": "🎬 Vîdyoya Dirêj a YouTube",
        "btn_shorts": "📱 YouTube Shorts",
        "btn_tiktok": "🎵 Daxistina TikTok",
        "btn_insta": "📸 Instagram Reels",
        "btn_profile": "👤 Profîla Min / Mafên Mayî",
        "btn_lang": "🌐 Ziman / Dil",
        "lang_select": "🌐 **Ji kerema xwe zimanê xwe hilbijêre:**",
        "back_menu": "🔙 Vegere Menuya Sereke",
        "admin_prompt": "👑 **Taybet a Admin:** Lînka **{p_key}** bişîne:",
        "payment_success": "🎉 Dravdan serketî bû!",
        "fast_payment_success": "⚡ Daxistina lezgîn çalak bû!",
        "no_rights": "⚠️ Mafê te yê vê platformê nîne.",
        "expired": "⏳ Dem an mafê te qediya.",
        "err_uzun": "❌ Tenê ji bo vîdyoyên dirêj ên YouTube!",
        "err_shorts": "❌ Tenê ji bo YouTube Shorts!",
        "err_tiktok": "❌ Tenê ji bo TikTok!",
        "err_insta": "❌ Tenê ji bo Instagram!",
        "limit_exceeded": "⚠️ **Sînor derbas bû!**",
        "choose_format": "📥 **Çawa dixwazî daxistinê bikî?**",
        "btn_video": "🎥 Vîdyo Daxîne",
        "btn_audio": "🎵 Pelê deng Daxîne",
        "btn_fast": "⚡ Bi 7 Stêrkan Tavilê Daxîne",
        "success_video": "✅ Vîdyo amade ye!",
        "success_audio": "🎵 Pelê deng amade ye!",
        "start_fallback": "Ji kerema xwe `/start` binivîse."
    },
    "en": {
        "welcome": "⚡ **Hello {name}, Welcome to Zenith Downloader Bot (v2.8.4.6)!**",
        "admin_active": "\n\n👑 *Admin Panel Active!*",
        "btn_uzun": "🎬 YouTube Long Video",
        "btn_shorts": "📱 YouTube Shorts",
        "btn_tiktok": "🎵 TikTok Video",
        "btn_insta": "📸 Instagram Reels",
        "btn_profile": "👤 Profile / Remaining Rights",
        "btn_lang": "🌐 Language",
        "lang_select": "🌐 **Please select your language:**",
        "back_menu": "🔙 Back to Main Menu",
        "admin_prompt": "👑 **Admin Special:** Send valid **{p_key}** links:",
        "payment_success": "🎉 Payment successful!",
        "fast_payment_success": "⚡ Fast download activated!",
        "no_rights": "⚠️ You don't have rights for this platform.",
        "expired": "⏳ Your rights have expired.",
        "err_uzun": "❌ Only for YouTube Long Videos!",
        "err_shorts": "❌ Only for YouTube Shorts!",
        "err_tiktok": "❌ Only for TikTok!",
        "err_insta": "❌ Only for Instagram!",
        "limit_exceeded": "⚠ **Limit Exceeded!**",
        "choose_format": "📥 **How do you want to download?**",
        "btn_video": "🎥 Download Video",
        "btn_audio": "🎵 Download MP3",
        "btn_fast": "⚡ Instant Download (7 Stars)",
        "success_video": "✅ Video ready!",
        "success_audio": "🎵 Audio file is ready!",
        "start_fallback": "Please type `/start`."
    },
    "ar": {
        "welcome": "⚡ **مرحباً {name}، أهلاً بك في بوت تحميل Zenith (v2.8.4.6)!**",
        "admin_active": "\n\n👑 *لوحة المشرف نشطة!*",
        "btn_uzun": "🎬 فيديو يوتيوب طويل",
        "btn_shorts": "📱 يوتيوب شورتس",
        "btn_tiktok": "🎵 تيك توك",
        "btn_insta": "📸 إنستغرام ريلز",
        "btn_profile": "👤 ملفي الشخصي / الحقوق المتبقية",
        "btn_lang": "🌐 اللغة",
        "lang_select": "🌐 **يرجى اختيار لغتك:**",
        "back_menu": "🔙 العودة للقائمة الرئيسية",
        "admin_prompt": "👑 **خاص للمشرف:** أرسل الروابط:",
        "payment_success": "🎉 نجح الدفع!",
        "fast_payment_success": "⚡ تم تفعيل التنزيل السريع!",
        "no_rights": "⚠️️ ليس لديك حقوق نشطة.",
        "expired": "⏳ انتهت صلاحية حقوقك.",
        "err_uzun": "❌ لفيديوهات يوتيوب الطويلة فقط!",
        "err_shorts": "❌ ليوتيوب شورتس فقط!",
        "err_tiktok": "❌ لتيك توك فقط!",
        "err_insta": "❌ لإنستغرام فقط!",
        "limit_exceeded": "⚠ **تم تجاوز الحد!**",
        "choose_format": "📥 **كيف تريد التنزيل؟**",
        "btn_video": "🎥 تنزيل فيديو",
        "btn_audio": "🎵 تنزيل MP3",
        "btn_fast": "⚡ تنزيل فوري (7 نجوم)",
        "success_video": "✅ الفيديو جاهز!",
        "success_audio": "🎵 الملف الصوتي جاهز!",
        "start_fallback": "يرجى كتابة `/start`."
    },
    "tk": {
        "welcome": "⚡ **Salam {name}, Zenith Wideo ýükleýji bota hoş geldiňiz (v2.8.4.6)!**",
        "admin_active": "\n\n👑 *Admin paneli işjeň!*",
        "btn_uzun": "🎬 YouTube Uzyn Wideo",
        "btn_shorts": "📱 YouTube Shorts",
        "btn_tiktok": "🎵 TikTok Wideo",
        "btn_insta": "📸 Instagram Reels",
        "btn_profile": "👤 Profilim / Galan Haklarym",
        "btn_lang": "🌐 Dil",
        "lang_select": "🌐 **Dil saýlaň:**",
        "back_menu": "🔙 Yzyna",
        "admin_prompt": "👑 **Admin:** Salgylary ibăriň:",
        "payment_success": "🎉 Töleg üstünlikli!",
        "fast_payment_success": "⚡ Çalt ýükleme işjeňleşdirildi!",
        "no_rights": "⚠ Ygtyýaryňyz ýok.",
        "expired": "⏳ Wagtyňyz gutardy.",
        "err_uzun": "❌ Diňe uzyn wideolar üçin!",
        "err_shorts": "❌ Diňe Shorts üçin!",
        "err_tiktok": "❌ Diňe TikTok üçin!",
        "err_insta": "❌ Diňe Instagram üçin!",
        "limit_exceeded": "⚠️ **Çäk aşyldy!**",
        "choose_format": "📥 **Nädip ýükletmeli?**",
        "btn_video": "🎥 Wideo",
        "btn_audio": "🎵 MP3",
        "btn_fast": "⚡ 7 Ýyldyz bilen derrew ýükle",
        "success_video": "✅ Wideo taýýar!",
        "success_audio": "🎵 Ses taýýar!",
        "start_fallback": "`/start` ýazyň."
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
        InlineKeyboardButton(get_text(user_id, "btn_uzun"), callback_data="unlock_yt_uzun"),
        InlineKeyboardButton(get_text(user_id, "btn_shorts"), callback_data="unlock_yt_shorts"),
        InlineKeyboardButton(get_text(user_id, "btn_tiktok"), callback_data="unlock_tiktok"),
        InlineKeyboardButton(get_text(user_id, "btn_insta"), callback_data="unlock_insta"),
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
        random_days = random.randint(7, 14)
        random_hak = random.randint(50, 80)
        
        if user_id not in unlocked_platforms: 
            unlocked_platforms[user_id] = {}
            
        unlocked_platforms[user_id][chosen_platform] = {
            "hak": random_hak, 
            "bitis": time.time() + (random_days * 86400)
        }
        
        daily_winners[current_date_str].append(user_id)
        p_names = {"uzun": "🎬 YouTube Uzun", "shorts": "📱 YouTube Shorts", "tiktok": "🎵 TikTok", "insta": "📸 Instagram"}
        
        reward_message = (
            f"\n\n🎁 **Tebrikler! Saat 13:00 Ödülünü Kazandın!**\n"
            f"🏆 Bugün bota erken davranan ilk 3 kişiden biri oldun!\n"
            f"✨ **Hediye Paket:** {p_names[chosen_platform]}\n"
            f"⏳ **Süre:** {random_days} Gün\n"
            f"🎯 **Hak:** {random_hak} Adet\n"
        )

    txt = get_text(user_id, "welcome", name=user_display_name) + reward_message
    if user_id == ADMIN_ID: 
        txt += get_text(user_id, "admin_active")
        
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
                if user_id == ADMIN_ID:
                    profile_text += f"✅ **{p_name}**: Aktif (Sınırsız Admin)\n"
                else:
                    hak = user_platforms[p_key]["hak"]
                    kal_gun = max(0, int((user_platforms[p_key]["bitis"] - time.time()) / 86400))
                    profile_text += f"✅ **{p_name}**: Aktif | Hak: `{hak}` | Gün: `{kal_gun}`\n"
            else:
                profile_text += f"❌ **{p_name}**: Aktif Değil\n"
                
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
        bot.answer_callback_query(call.id, f"✅ Dil: {lang_code.upper()}")
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

    if data == "fast_download_invoice":
        bot.answer_callback_query(call.id)
        bot.send_invoice(
            chat_id=chat_id,
            title="Hızlı İndirme",
            description="7 Yıldız ile Anında İndir",
            invoice_payload="fast_download_boost",
            provider_token="",
            currency="XTR",
            prices=[LabeledPrice("Hızlı İndir", 7)]
        )
        return

    if data in ["dl_video", "dl_audio"]:
        bot.answer_callback_query(call.id)
        link_data = pending_links.get(user_id)
        if not link_data:
            bot.send_message(chat_id, get_text(user_id, "start_fallback"))
            return
        
        links = link_data["links"]
        is_audio = (data == "dl_audio")
        current_state = user_states.get(user_id, "")
        
        p_type = next((k for k in ["uzun", "shorts", "tiktok", "insta"] if k in current_state), "")

        for index, link in enumerate(links, 1):
            if user_id != ADMIN_ID and p_type:
                if user_id not in unlocked_platforms or p_type not in unlocked_platforms[user_id]:
                    bot.send_message(chat_id, get_text(user_id, "no_rights"))
                    break
                udat = unlocked_platforms[user_id][p_type]
                if time.time() > udat["bitis"] or udat["hak"] <= 0:
                    bot.send_message(chat_id, get_text(user_id, "expired"))
                    break
                udat["hak"] -= 1

            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton(get_text(user_id, "btn_fast"), callback_data="fast_download_invoice"))
            
            status_msg = bot.send_message(
                chat_id, 
                f"🔄 İndiriliyor: **%1**\n\n*(Beklemek istemiyorsan aşağıdaki butona basıp anında indirebilirsin!)*", 
                reply_markup=markup, 
                parse_mode="Markdown"
            )
            
            fast_downloads[user_id] = False
            
            for percent in range(5, 101, 20):
                if fast_downloads.get(user_id, False):
                    try:
                        bot.edit_message_text(
                            chat_id=chat_id,
                            message_id=status_msg.message_id,
                            text=f"⚡ İndiriliyor: **%100**\n\n*(Hızlı indirme uygulandı!)*",
                            parse_mode="Markdown"
                        )
                    except:
                        pass
                    break 
                
                time.sleep(1) 
                try:
                    bot.edit_message_text(
                        chat_id=chat_id,
                        message_id=status_msg.message_id,
                        text=f"🔄 İndiriliyor: **%{percent}**\n\n*(Beklemek istemiyorsan aşağıdaki butona basıp anında indirebilirsin!)*",
                        reply_markup=markup,
                        parse_mode="Markdown"
                    )
                except:
                    pass

            if fast_downloads.get(user_id, False):
                time.sleep(3)

            output = f"aud_{user_id}_{index}.m4a" if is_audio else f"vid_{user_id}_{index}.mp4"
            
            ydl_opts = {
                'format': 'bestaudio/best' if is_audio else 'best/bestvideo+bestaudio',
                'outtmpl': output,
                'noplaylist': True,
                'socket_timeout': 60,
                'nocheckcertificate': True
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
                bot.send_message(chat_id, f"❌ Hata ({index}. link): Bu gönderi desteklenmiyor veya dosya çok büyük.")
                if os.path.exists(output): os.remove(output)
            
            try: bot.delete_message(chat_id, status_msg.message_id)
            except: pass
            
        pending_links.pop(user_id, None)
        user_states[user_id] = None
        fast_downloads.pop(user_id, None)
        return

    if user_id == ADMIN_ID and data.startswith("unlock_"):
        p_key = data.replace("unlock_", "").replace("yt_", "")
        user_states[user_id] = f"waiting_for_{p_key}"
        bot.answer_callback_query(call.id)
        m = InlineKeyboardMarkup()
        m.add(InlineKeyboardButton(get_text(user_id, "back_menu"), callback_data="back_to_main"))
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=get_text(user_id, "lang_select"), reply_markup=m, parse_mode="Markdown")
        return

    if data.startswith("set_lang_"):
        lang_code = data.split("_")[2]
        user_languages[user_id] = lang_code
        bot.answer_callback_query(call.id, f"✅ Dil: {lang_code.upper()}")
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

    if data == "fast_download_invoice":
        bot.answer_callback_query(call.id)
        bot.send_invoice(
            chat_id=chat_id,
            title="Hızlı İndirme",
            description="7 Yıldız ile Anında İndir",
            invoice_payload="fast_download_boost",
            provider_token="",
            currency="XTR",
            prices=[LabeledPrice("Hızlı İndir", 7)]
        )
        return

    if data in ["dl_video", "dl_audio"]:
        bot.answer_callback_query(call.id)
        link_data = pending_links.get(user_id)
        if not link_data:
            bot.send_message(chat_id, get_text(user_id, "start_fallback"))
            return
        
        links = link_data["links"]
        is_audio = (data == "dl_audio")
        current_state = user_states.get(user_id, "")
        
        p_type = next((k for k in ["uzun", "shorts", "tiktok", "insta"] if k in current_state), "")

        for index, link in enumerate(links, 1):
            if user_id != ADMIN_ID and p_type:
                if user_id not in unlocked_platforms or p_type not in unlocked_platforms[user_id]:
                    bot.send_message(chat_id, get_text(user_id, "no_rights"))
                    break
                udat = unlocked_platforms[user_id][p_type]
                if time.time() > udat["bitis"] or udat["hak"] <= 0:
                    bot.send_message(chat_id, get_text(user_id, "expired"))
                    break
                udat["hak"] -= 1

            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton(get_text(user_id, "btn_fast"), callback_data="fast_download_invoice"))
            
            status_msg = bot.send_message(
                chat_id, 
                f"🔄 İndiriliyor: **%1**\n\n*(Beklemek istemiyorsan aşağıdaki butona basıp anında indirebilirsin!)*", 
                reply_markup=markup, 
                parse_mode="Markdown"
            )
            
            fast_downloads[user_id] = False
            
            for percent in range(5, 101, 20):
                if fast_downloads.get(user_id, False):
                    try:
                        bot.edit_message_text(
                            chat_id=chat_id,
                            message_id=status_msg.message_id,
                            text=f"⚡ İndiriliyor: **%100**\n\n*(Hızlı indirme uygulandı!)*",
                            parse_mode="Markdown"
                        )
                    except:
                        pass
                    break 
                
                time.sleep(1) 
                try:
                    bot.edit_message_text(
                        chat_id=chat_id,
                        message_id=status_msg.message_id,
                        text=f"🔄 İndiriliyor: **%{percent}**\n\n*(Beklemek istemiyorsan aşağıdaki butona basıp anında indirebilirsin!)*",
                        reply_markup=markup,
                        parse_mode="Markdown"
                    )
                except:
                    pass

            if fast_downloads.get(user_id, False):
                time.sleep(3)

            output = f"aud_{user_id}_{index}.m4a" if is_audio else f"vid_{user_id}_{index}.mp4"
            
            ydl_opts = {
                'format': 'bestaudio/best' if is_audio else 'best/bestvideo+bestaudio',
                'outtmpl': output,
                'noplaylist': True,
                'socket_timeout': 60,
                'nocheckcertificate': True
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
                bot.send_message(chat_id, f"❌ Hata ({index}. link): Bu gönderi desteklenmiyor veya dosya çok büyük.")
                if os.path.exists(output): os.remove(output)
            
            try: bot.delete_message(chat_id, status_msg.message_id)
            except: pass
            
        pending_links.pop(user_id, None)
        user_states[user_id] = None
        fast_downloads.pop(user_id, None)
        return

    if user_id == ADMIN_ID and data.startswith("unlock_"):
        p_key = data.replace("unlock_", "").replace("yt_", "")
        user_states[user_id] = f"waiting_for_{p_key}"
        bot.answer_callback_query(call.id)
        m = InlineKeyboardMarkup()
        m.add(InlineKeyboardButton(get_text(user_id, "back_menu"), callback_data="back_to_main"))
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=get_text(user_id, "admin_prompt", p_key=p_key), reply_markup=m, parse_mode="Markdown")
        return

    payloads = {"unlock_yt_uzun": "uzun", "unlock_yt_shorts": "shorts", "unlock_tiktok": "tiktok", "unlock_insta": "insta"}
    if data in payloads:
        bot.answer_callback_query(call.id)
        prices = {"uzun": 150, "shorts": 150, "tiktok": 200, "insta": 180}
        pl = payloads[data]
        bot.send_invoice(chat_id=chat_id, title=pl.capitalize(), description="5200 Hak", invoice_payload=pl, provider_token="", currency="XTR", prices=[LabeledPrice(pl, prices[pl])])

@bot.pre_checkout_query_handler(func=lambda q: True)
def checkout(q):
    bot.answer_pre_checkout_query(q.id, ok=True)

@bot.message_handler(content_types=['successful_payment'])
def payment_success(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    payload = message.successful_payment.invoice_payload
    
    if payload == "fast_download_boost":
        fast_downloads[user_id] = True
        bot.send_message(chat_id, get_text(user_id, "fast_payment_success"))
        return

    if user_id not in unlocked_platforms: unlocked_platforms[user_id] = {}
    unlocked_platforms[user_id][payload] = {"hak": 5200, "bitis": time.time() + (1596 * 86400)}
    user_states[user_id] = f"waiting_for_{payload}"
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
        if user_id not in user_swear_counts:
            user_swear_counts[user_id] = 0
        user_swear_counts[user_id] += 1
        
        if user_swear_counts[user_id] >= 3:
            if user_id in unlocked_platforms:
                unlocked_platforms[user_id] = {}
            bot.reply_to(message, "🚨 **Cezalandırıldınız!** 3 kez küfür/hakaret ettiğiniz tespit edildi. Tüm VIP haklarınız sıfırlandı ve sisteme mesaj atmanız kısıtlandı!")
            return
        else:
            bot.reply_to(message, f"⚠️ **Küfür Uyarısı ({user_swear_counts[user_id]}/3):** Botumuzda küfür etmek yasaktır! 3'e ulaşırsanız VIP haklarınız tamamen silinecektir.")
            return
        
    links = [line.strip() for line in raw_text.splitlines() if line.strip().startswith("http")]
    
    if not links:
        bot.reply_to(message, get_text(user_id, "start_fallback"))
        return

    current_state = user_states.get(user_id)
    
    detected_platform = ""
    if current_state:
        for p in ["uzun", "shorts", "tiktok", "insta"]:
            if p in current_state:
                detected_platform = p
                break

    if detected_platform and detected_platform in PLATFORM_LIMITS:
        max_limit = PLATFORM_LIMITS[detected_platform]
        if len(links) > max_limit:
            bot.send_message(chat_id, get_text(user_id, "limit_exceeded", limit=max_limit), parse_mode="Markdown")
            return

    for text in links:
        t_lower = text.lower()
        is_valid, error_msg = True, ""
        
        if current_state == "waiting_for_uzun":
            if "youtube.com/shorts" in t_lower or ("youtube.com" not in t_lower and "youtu.be" not in t_lower):
                is_valid, error_msg = False, get_text(user_id, "err_uzun")
        elif current_state == "waiting_for_shorts":
            if "youtube.com/shorts" not in t_lower:
                is_valid, error_msg = False, get_text(user_id, "err_shorts")
        elif current_state == "waiting_for_tiktok":
            if "tiktok.com" not in t_lower:
                is_valid, error_msg = False, get_text(user_id, "err_tiktok")
        elif current_state == "waiting_for_insta":
            if "instagram.com" not in t_lower:
                is_valid, error_msg = False, get_text(user_id, "err_insta")
        
        if not is_valid and current_state:
            bot.send_message(chat_id, error_msg, parse_mode="Markdown")
            return

    pending_links[user_id] = {"links": links}
    format_markup = InlineKeyboardMarkup(row_width=2)
    format_markup.add(
        InlineKeyboardButton(get_text(user_id, "btn_video"), callback_data="dl_video"),
        InlineKeyboardButton(get_text(user_id, "btn_audio"), callback_data="dl_audio")
    )
    bot.send_message(chat_id, f"📥 {len(links)} adet bağlantı alındı!\n\n" + get_text(user_id, "choose_format"), reply_markup=format_markup, parse_mode="Markdown")

bot.infinity_polling()
