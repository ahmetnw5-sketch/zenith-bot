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
wheel_rights = {}
user_discounts = {}
first_time_users = set()

user_bans = {}
daily_winners = {}  
last_reward_date = ""

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
            "✨🚀 **Zenith v2.5.0.3 Zirvesine Hoş Geldin Reisim!** 🔥💎\n\n"
            "*Botun motorları son sürat çalışıyor, indirmeye hazır ol!* 👇🤖\n\n"
            "⚠️ **ÖNEMLİ DUYURU & KURALLAR:**\n"
            "Lütfen bot içinde veya bağlı gruplarda **küfür ve hakaret etmeyiniz**. "
            "Alacağınız VIP'lerden veya haklardan sonra küfür ettiğiniz tespit edilirse "
            "**VIP haklarınız tamamen silinir** ve sistem tarafından geçici süreliğine "
            "(1 saat ile 10 gün arası) engellenirsiniz!\n\n"
            "Anlayışınız için teşekkür ederiz... 🙏✨"
        ),
        "admin_active": "\n\n👑 *Zenith v2.5.0.3 Admin Paneli Aktif!*",
        "btn_uzun": "🎬 YouTube Uzun",
        "btn_shorts": "📱 YouTube Shorts",
        "btn_tiktok": "🎵 TikTok İndir",
        "btn_insta": "📸 Instagram Reels",
        "btn_wheel": "🎡 Şans Çarkını Çevir (Günde 3 Hak)",
        "btn_profile": "👤 Profilim / Kalan Haklarım",
        "btn_lang": "🌐 Dil Seç / Language",
        "lang_select": "🌐 **Lütfen kullanmak istediğin dili seç:**",
        "back_menu": "🔙 Ana Menüye Dön",
        "admin_prompt": "👑 **Zenith Admin Özel:** Lütfen geçerli bir **{p_key}** bağlantısı gönder:",
        "payment_success": "🎉 Ödeme başarılı! 5200 indirme hakkın tanımlandı.",
        "fast_payment_success": "⚡ Hızlı indirme açıldı! Video hemen indiriliyor...",
        "no_rights": "⚠️ Bu platform için aktif hak veya süren bulunmuyor.",
        "expired": "⏳ Süren veya indirme hakkın doldu.",
        "choose_format": "📥 **Nasıl indirmek istiyorsun?**",
        "btn_video": "🎥 Video İndir",
        "btn_audio": "🎵 MP3 İndir",
        "btn_fast": "⚡ 7 Yıldız ile Anında İndir",
        "success_video": "✅ Videon hazır dostum!😀",
        "success_audio": "🎵 Ses dosyan hazır!",
        "start_fallback": "Lütfen `/start` yazıp menüden seçim yap.",
        "maintenance_msg": "🛠 **Zenith v2.5.0.3 şu an bakımda reisim!** En kısa sürede güncellemelerle döneceğiz, beklemede kal."
    },
    "ku": {
        "welcome": "✨🚀 **Bi xêr hatî Qraliyeta Zenith v2.5.0.3!** 🔥💎",
        "admin_active": "\n\n👑 *Panela Admin Çalak e!*",
        "btn_uzun": "🎬 Vîdyoya Dirêj a YouTube",
        "btn_shorts": "📱 YouTube Shorts",
        "btn_tiktok": "🎵 Daxistina TikTok",
        "btn_insta": "📸 Instagram Reels",
        "btn_wheel": "🎡 Çerxa Bextê Bivirîne",
        "btn_profile": "👤 Profîla Min / Mafên Mayî",
        "btn_lang": "🌐 Ziman / Dil",
        "lang_select": "🌐 **Ji kerema xwe zimanê xwe hilbijêre:**",
        "back_menu": "🔙 Vegere Menuya Sereke",
        "admin_prompt": "👑 **Taybet a Admin:** Lînka **{p_key}** bişîne:",
        "payment_success": "🎉 Dravdan serketî bû!",
        "fast_payment_success": "⚡ Daxistina lezgîn çalak bû!",
        "no_rights": "⚠️ Mafê te yê vê platformê nîne.",
        "expired": "⏳ Dem an mafê te qediya.",
        "choose_format": "📥 **Çawa dixwazî daxistinê bikî?**",
        "btn_video": "🎥 Vîdyo Daxîne",
        "btn_audio": "🎵 Pelê deng Daxîne",
        "btn_fast": "⚡ Bi Stêrkan Tavilê Daxîne",
        "success_video": "✅ Vîdyo amade ye!",
        "success_audio": "🎵 Pelê deng amade ye!",
        "start_fallback": "Ji kerema xwe `/start` binivîse.",
        "maintenance_msg": "🛠️ **Zenith niha di dema bakûr de ye!**"
    },
    "en": {
        "welcome": "✨🚀 **Welcome to Zenith v2.5.0.3!** 🔥💎",
        "admin_active": "\n\n👑 *Admin Panel Active!*",
        "btn_uzun": "🎬 YouTube Long Video",
        "btn_shorts": "📱 YouTube Shorts",
        "btn_tiktok": "🎵 TikTok Video",
        "btn_insta": "📸 Instagram Reels",
        "btn_wheel": "🎡 Spin the Lucky Wheel",
        "btn_profile": "👤 Profile / Remaining Rights",
        "btn_lang": "🌐 Language",
        "lang_select": "🌐 **Please select your language:**",
        "back_menu": "🔙 Back to Main Menu",
        "admin_prompt": "👑 **Admin Special:** Send valid **{p_key}** links:",
        "payment_success": "🎉 Payment successful!",
        "fast_payment_success": "⚡ Fast download activated!",
        "no_rights": "⚠ You don't have rights for this platform.",
        "expired": "⏳ Your rights have expired.",
        "choose_format": "📥 **How do you want to download?**",
        "btn_video": "🎥 Download Video",
        "btn_audio": "🎵 Download MP3",
        "btn_fast": "⚡ Instant Download",
        "success_video": "✅ Video ready!",
        "success_audio": "🎵 Audio file is ready!",
        "start_fallback": "Please type `/start`.",
        "maintenance_msg": "🛠️ Zenith is currently under maintenance."
    },
    "ar": {
        "welcome": "✨🚀 **مرحباً بك في Zenith v2.5.0.3!** 🔥💎",
        "admin_active": "\n\n👑 *لوحة المشرف نشطة!*",
        "btn_uzun": "🎬 فيديو يوتيوب طويل",
        "btn_shorts": "📱 يوتيوب شورتس",
        "btn_tiktok": "🎵 تيك توك",
        "btn_insta": "📸 إنستغرام ريلز",
        "btn_wheel": "🎡 أدار عجلة الحظ",
        "btn_profile": "👤 ملفي الشخصي / الحقوق المتبقية",
        "btn_lang": "🌐 اللغة",
        "lang_select": "🌐 **يرجى اختيار لغتك:**",
        "back_menu": "🔙 العودة للقائمة الرئيسية",
        "admin_prompt": "👑 **خاص للمشرف:** أرسل الروابط:",
        "payment_success": "🎉 نجح الدفع!",
        "fast_payment_success": "⚡ تم تفعيل التنزيل السريع!",
        "no_rights": "⚠️ ليس لديك حقوق نشطة.",
        "expired": "⏳ انتهت صلاحية حقوقك.",
        "choose_format": "📥 **كيف تريد التنزيل؟**",
        "btn_video": "🎥 تنزيل فيديو",
        "btn_audio": "🎵 تنزيل MP3",
        "btn_fast": "⚡ تنزيل فوري",
        "success_video": "✅ الفيديو جاهز!",
        "success_audio": "🎵 الملف الصوتي جاهز!",
        "start_fallback": "يرجى كتابة `/start`.",
        "maintenance_msg": "🛠️ Zenith تحت الصيانة حالياً."
    },
    "tk": {
        "welcome": "✨🚀 **Zenith v2.5.0.3 Hoş geldiňiz!** 🔥💎",
        "admin_active": "\n\n👑 *Admin paneli işjeň!*",
        "btn_uzun": "🎬 YouTube Uzyn Wideo",
        "btn_shorts": "📱 YouTube Shorts",
        "btn_tiktok": "🎵 TikTok Wideo",
        "btn_insta": "Instagram Reels",
        "btn_wheel": "🎡 Bagt Çarhyny Aýla",
        "btn_profile": "👤 Profilim / Galan Haklarym",
        "btn_lang": "🌐 Dil",
        "lang_select": "🌐 **Dil saýlaň:**",
        "back_menu": "🔙 Yzyna",
        "admin_prompt": "👑 **Admin:** Salgylary ibăriň:",
        "payment_success": "🎉 Töleg üstünlikli!",
        "fast_payment_success": "⚡ Çalt ýükleme işjeňleşdirildi!",
        "no_rights": "⚠ Ygtyýaryňyz ýok.",
        "expired": "⏳ Wagtyňyz gutardy.",
        "choose_format": "📥 **Nädip ýükletmeli?**",
        "btn_video": "🎥 Wideo",
        "btn_audio": "🎵 MP3",
        "btn_fast": "⚡ Derrew ýükle",
        "success_video": "✅ Wideo taýýar!",
        "success_audio": "🎵 Ses taýýar!",
        "start_fallback": "`/start` ýazyň.",
        "maintenance_msg": "🛠️️ Zenith tehniki hyzmatda."
    }
}

def get_text(user_id, key):
    lang = user_languages.get(user_id, "tr")
    if lang not in TRANSLATIONS: lang = "tr"
    return TRANSLATIONS[lang].get(key, TRANSLATIONS["tr"].get(key, ""))

def get_main_keyboard(user_id):
    disc = user_discounts.get(user_id, 0)
    base_prices = {"uzun": 150, "shorts": 150, "tiktok": 200, "insta": 180}
    user_platforms = unlocked_platforms.get(user_id, {})
    
    def calc_btn_label(p_key, btn_base_text):
        if user_id != ADMIN_ID and p_key in user_platforms and user_platforms[p_key]["hak"] > 0 and time.time() < user_platforms[p_key]["bitis"]:
            hak = user_platforms[p_key]["hak"]
            kal_gun = max(0, int((user_platforms[p_key]["bitis"] - time.time()) / 86400))
            return f"{btn_base_text} - Aktif ({kal_gun} Gün / {hak} Hak)"
        
        p = base_prices[p_key]
        if disc == 100:
            return f"{btn_base_text} - 0 Yıldız (ÜCRETSİZ 🎁)"
        elif disc > 0:
            discounted = int(p * (100 - disc) / 100)
            return f"{btn_base_text} - %{disc} İndirimli ({discounted} Yıldız)"
        else:
            return f"{btn_base_text} - ({p} Yıldız)"

    m = InlineKeyboardMarkup(row_width=1)
    m.add(
        InlineKeyboardButton(calc_btn_label('uzun', get_text(user_id, 'btn_uzun')), callback_data="unlock_yt_uzun"),
        InlineKeyboardButton(calc_btn_label('shorts', get_text(user_id, 'btn_shorts')), callback_data="unlock_yt_shorts"),
        InlineKeyboardButton(calc_btn_label('tiktok', get_text(user_id, 'btn_tiktok')), callback_data="unlock_tiktok"),
        InlineKeyboardButton(calc_btn_label('insta', get_text(user_id, 'btn_insta')), callback_data="unlock_insta"),
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

@bot.message_handler(commands=['ai'])
def handle_ai_query(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    if user_id in user_bans and time.time() < user_bans[user_id]:
        bot.reply_to(message, "⛔ Engellendiğin için AI kullanamazsın.")
        return
    text_parts = message.text.split(maxsplit=1)
    if len(text_parts) < 2:
        bot.reply_to(message, "💡 Kullanım: `/ai <soru>`")
        return
    query = text_parts[1]
    responses = [
        f"🤖 **Zenith AI:** '{query}' konusunda sistemlerim en iyi optimizasyonun planlı çalışmaktan geçtiğini söylüyor!",
        f"🧠 **Zenith AI:** '{query}' analizi tamamlandı. Adım adım ilerlemen en iyisi.",
        f"⚡ **Zenith AI:** Sorunu aldım reisim! En mantıklı yaklaşım projeyi parçalara bölmektir."
    ]
    bot.reply_to(message, random.choice(responses), parse_mode="Markdown")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    global last_reward_date, daily_winners, is_maintenance_mode
    user_id = message.from_user.id
    chat_id = message.chat.id
    if user_id in user_bans and time.time() < user_bans[user_id]:
        bot.send_message(chat_id, "⛔ Engellisin.")
        return
    if is_maintenance_mode and user_id != ADMIN_ID:
        bot.send_message(chat_id, get_text(user_id, "maintenance_msg"), parse_mode="Markdown")
        return
    user_states[user_id] = None
    now_tr = datetime.datetime.utcnow() + datetime.timedelta(hours=3)
    current_hour, current_minute = now_tr.hour, now_tr.minute
    
    try:
        if user_id not in first_time_users:
            first_time_users.add(user_id)
            if os.path.exists("hosgeldin.ogg"):
                with open("hosgeldin.ogg", "rb") as vf: bot.send_voice(chat_id, vf)
    except: pass

    current_date_str = now_tr.strftime("%Y-%m-%d")
    if last_reward_date != current_date_str:
        last_reward_date = current_date_str
        daily_winners[current_date_str] = []

    reward_message = ""
    today_list = daily_winners.get(current_date_str, [])
    if current_hour == 13 and 0 <= current_minute <= 30 and user_id not in today_list and len(today_list) < 3:
        platforms = ["uzun", "shorts", "tiktok", "insta"]
        chosen_platform = random.choice(platforms)
        random_days, random_hak = random.randint(7, 14), random.randint(50, 80)
        if user_id not in unlocked_platforms: unlocked_platforms[user_id] = {}
        unlocked_platforms[user_id][chosen_platform] = {"hak": random_hak, "bitis": time.time() + (random_days * 86400)}
        daily_winners[current_date_str].append(user_id)
        reward_message = f"\n\n🎁 **Ödül Kazandın!** {chosen_platform} - {random_days} Gün / {random_hak} Hak!"

    txt = get_text(user_id, "welcome") + reward_message
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
        discounts = [50, 80, 89, 98, 99, 100]
        chosen = random.choices(discounts, weights=[40, 25, 15, 10, 8, 2], k=1)[0]
        user_discounts[user_id] = chosen
        m = InlineKeyboardMarkup()
        m.add(InlineKeyboardButton("🔄 Tekrar", callback_data="open_lucky_wheel"))
        m.add(InlineKeyboardButton(get_text(user_id, "back_menu"), callback_data="back_to_main"))
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=f"🎉 Tebrikler! %{chosen} İndirim kazandın!", reply_markup=m, parse_mode="Markdown")
        return

    if data == "open_profile":
        bot.answer_callback_query(call.id)
        user_platforms = unlocked_platforms.get(user_id, {})
        text = "👤 **Profilin:**\n\n"
        for p_key, p_name in [("uzun", "YouTube Uzun"), ("shorts", "YouTube Shorts"), ("tiktok", "TikTok"), ("insta", "Instagram")]:
            if user_id == ADMIN_ID or (p_key in user_platforms and user_platforms[p_key]["hak"] > 0 and time.time() < user_platforms[p_key]["bitis"]):
                text += f"✅ {p_name}: Aktif\n"
            else:
                text += f"❌ {p_name}: Pasif\n"
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

    if data == "fast_download_invoice":
        bot.answer_callback_query(call.id)
        bot.send_invoice(chat_id=chat_id, title="Hızlı İndir", description="Hızlı", invoice_payload="fast_download_boost", provider_token="", currency="XTR", prices=[LabeledPrice("Hızlı", 7)])
        return

    if data in ["dl_video", "dl_audio"]:
        bot.answer_callback_query(call.id)
        link_data = pending_links.get(user_id)
        if not link_data: return
        links = link_data["links"]
        is_audio = (data == "dl_audio")
        
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
        pending_links.pop(user_id, None)
        return

    if user_id == ADMIN_ID and data.startswith("unlock_"):
        p_key = data.replace("unlock_", "").replace("yt_", "")
        user_states[user_id] = f"waiting_for_{p_key}"
        bot.answer_callback_query(call.id, f"Admin: {p_key}")
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=get_text(user_id, "admin_prompt").format(p_key=p_key), parse_mode="Markdown")
        return

    payloads = {"unlock_yt_uzun": "uzun", "unlock_yt_shorts": "shorts", "unlock_tiktok": "tiktok", "unlock_insta": "insta"}
    if data in payloads:
        bot.answer_callback_query(call.id)
        pl = payloads[data]
        base_prices = {"uzun": 150, "shorts": 150, "tiktok": 200, "insta": 180}
        disc = user_discounts.get(user_id, 0)
        if disc == 100:
            if user_id not in unlocked_platforms: unlocked_platforms[user_id] = {}
            unlocked_platforms[user_id][pl] = {"hak": 5200, "bitis": time.time() + (1596 * 86400)}
            user_discounts[user_id] = 0
            bot.send_message(chat_id, "🎉 Ücretsiz hak tanımlandı!")
            return
        final_price = int(base_prices[pl] * (100 - disc) / 100) if disc > 0 else base_prices[pl]
        bot.send_invoice(chat_id=chat_id, title=pl.capitalize(), description="Hak", invoice_payload="fast_download_boost", provider_token="", currency="XTR", prices=[LabeledPrice("Hızlı", 7)])
        return

    if data in ["dl_video", "dl_audio"]:
        bot.answer_callback_query(call.id)
        link_data = pending_links.get(user_id)
        if not link_data: return
        links = link_data["links"]
        is_audio = (data == "dl_audio")
        
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
        pending_links.pop(user_id, None)
        return

    if user_id == ADMIN_ID and data.startswith("unlock_"):
        p_key = data.replace("unlock_", "").replace("yt_", "")
        user_states[user_id] = f"waiting_for_{p_key}"
        bot.answer_callback_query(call.id, f"Admin: {p_key}")
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=get_text(user_id, "admin_prompt").format(p_key=p_key), parse_mode="Markdown")
        return

    payloads = {"unlock_yt_uzun": "uzun", "unlock_yt_shorts": "shorts", "unlock_tiktok": "tiktok", "unlock_insta": "insta"}
    if data in payloads:
        bot.answer_callback_query(call.id)
        pl = payloads[data]
        base_prices = {"uzun": 150, "shorts": 150, "tiktok": 200, "insta": 180}
        disc = user_discounts.get(user_id, 0)
        if disc == 100:
            if user_id not in unlocked_platforms: unlocked_platforms[user_id] = {}
            unlocked_platforms[user_id][pl] = {"hak": 5200, "bitis": time.time() + (1596 * 86400)}
            user_discounts[user_id] = 0
            bot.send_message(chat_id, "🎉 Ücretsiz hak tanımlandı!")
            return
        final_price = int(base_prices[pl] * (100 - disc) / 100) if disc > 0 else base_prices[pl]
        bot.send_invoice(chat_id=chat_id, title=pl.capitalize(), description="Hak", invoice_payload=pl, provider_token="", currency="XTR", prices=[LabeledPrice(pl, final_price)])

@bot.pre_checkout_query_handler(func=lambda q: True)
def checkout(q): bot.answer_pre_checkout_query(q.id, ok=True)

@bot.message_handler(content_types=['successful_payment'])
def payment_success(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    payload = message.successful_payment.invoice_payload
    if payload == "fast_download_boost":
        fast_downloads[user_id] = True
        bot.send_message(chat_id, "⚡ Hızlı indirme aktif!")
        return
    if user_id not in unlocked_platforms: unlocked_platforms[user_id] = {}
    unlocked_platforms[user_id][payload] = {"hak": 5200, "bitis": time.time() + (1596 * 86400)}
    bot.send_message(chat_id, "🎉 Ödeme başarılı!")

@bot.message_handler(func=lambda m: True)
def handle_link_and_security(message):
    global is_maintenance_mode
    user_id = message.from_user.id
    raw_text = message.text.strip()
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
    m.add(InlineKeyboardButton("Video", callback_data="dl_video"), InlineKeyboardButton("MP3", callback_data="dl_audio"))
    bot.send_message(chat_id, f"📥 {len(links)} bağlantı alındı, format seç:", reply_markup=m)

bot.infinity_polling(skip_pending=True)
