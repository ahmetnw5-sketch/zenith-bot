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

daily_winners = {}  
last_reward_date = ""

ALL_LANGUAGES = [
    ("🇹🇷 Türkçe", "tr"), 
    ("☀️ Kürtçe (Kurmancî)", "ku"), 
    ("🇬🇧 English", "en"), 
    ("🇸🇦 العربية", "ar"), 
    ("🇹🇲 Türkmence (Türkmençe)", "tk")
]

TRANSLATIONS = {
    "tr": {
        "welcome": "✨🚀 **Yoğooov! Hoş geldin NEYOM Krallığına!** 🔥💎\n\n*Botun motorları son sürat çalışıyor, indirmeye hazır ol!* 👇🤖",
        "admin_active": "\n\n👑 *Admin Paneli Aktif!*",
        "btn_uzun": "🎬 YouTube Uzun",
        "btn_shorts": "📱 YouTube Shorts",
        "btn_tiktok": "🎵 TikTok İndir",
        "btn_insta": "📸 Instagram Reels",
        "btn_wheel": "🎡 Şans Çarkını Çevir (Günde 3 Hak)",
        "btn_profile": "👤 Profilim / Kalan Haklarım",
        "btn_lang": "🌐 Dil Seç / Language",
        "lang_select": "🌐 **Lütfen kullanmak istediğin dili seç:**",
        "back_menu": "🔙 Ana Menüye Dön",
        "admin_prompt": "👑 **Admin Özel:** Lütfen geçerli bir **{p_key}** bağlantısı gönder:",
        "payment_success": "🎉 Ödeme başarılı! 5200 indirme hakkın tanımlandı.",
        "fast_payment_success": "⚡ Hızlı indirme açıldı! Video hemen indiriliyor...",
        "no_rights": "⚠️ Bu platform için aktif hakkın bulunmuyor.",
        "expired": "⏳ Süren veya indirme hakkın doldu.",
        "choose_format": "📥 **Nasıl indirmek istiyorsun?**",
        "btn_video": "🎥 Video İndir",
        "btn_audio": "🎵 MP3 İndir",
        "btn_fast": "⚡ 7 Yıldız ile Anında İndir",
        "success_video": "✅ Videon hazır dostum!😀",
        "success_audio": "🎵 Ses dosyan hazır!",
        "start_fallback": "Lütfen `/start` yazıp menüden seçim yap."
    },
    "ku": {
        "welcome": "✨🚀 **Bi xêr hatî Qraliyeta NEYOM!** 🔥💎",
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
        "btn_fast": "⚡ Bi 7 Stêrkan Tavilê Daxîne",
        "success_video": "✅ Vîdyo amade ye!",
        "success_audio": "🎵 Pelê deng amade ye!",
        "start_fallback": "Ji kerema xwe `/start` binivîse."
    },
    "en": {
        "welcome": "✨🚀 **Welcome to NEYOM Kingdom!** 🔥💎",
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
        "no_rights": "⚠️ You don't have rights for this platform.",
        "expired": "⏳ Your rights have expired.",
        "choose_format": "📥 **How do you want to download?**",
        "btn_video": "🎥 Download Video",
        "btn_audio": "🎵 Download MP3",
        "btn_fast": "⚡ Instant Download (7 Stars)",
        "success_video": "✅ Video ready!",
        "success_audio": "🎵 Audio file is ready!",
        "start_fallback": "Please type `/start`."
    },
    "ar": {
        "welcome": "✨🚀 **مرحباً بك في مملكة NEYOM!** 🔥💎",
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
        "btn_fast": "⚡ تنزيل فوري (7 نجوم)",
        "success_video": "✅ الفيديو جاهز!",
        "success_audio": "🎵 الملف الصوتي جاهز!",
        "start_fallback": "يرجى كتابة `/start`."
    },
    "tk": {
        "welcome": "✨🚀 **NEYOM Patyşalygyna Hoş geldiňiz!** 🔥💎",
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
        "btn_fast": "⚡ 7 Ýyldyz bilen derrew ýükle",
        "success_video": "✅ Wideo taýýar!",
        "success_audio": "🎵 Ses taýýar!",
        "start_fallback": "`/start` ýazyň."
    }
}

def get_text(user_id, key):
    lang = user_languages.get(user_id, "tr")
    if lang not in TRANSLATIONS: lang = "tr"
    return TRANSLATIONS[lang].get(key, TRANSLATIONS["tr"].get(key, ""))

def get_main_keyboard(user_id):
    disc = user_discounts.get(user_id, 0)
    base_prices = {"uzun": 150, "shorts": 150, "tiktok": 200, "insta": 180}
    
    def calc_price(p_key):
        p = base_prices[p_key]
        if disc == 100:
            return "0 Yıldız (ÜCRETSİZ 🎁)"
        elif disc > 0:
            discounted = int(p * (100 - disc) / 100)
            return f"%{disc} İndirimli ({discounted} Yıldız)"
        else:
            return f"({p} Yıldız)"

    m = InlineKeyboardMarkup(row_width=1)
    m.add(
        InlineKeyboardButton(f"{get_text(user_id, 'btn_uzun')} - {calc_price('uzun')}", callback_data="unlock_yt_uzun"),
        InlineKeyboardButton(f"{get_text(user_id, 'btn_shorts')} - {calc_price('shorts')}", callback_data="unlock_yt_shorts"),
        InlineKeyboardButton(f"{get_text(user_id, 'btn_tiktok')} - {calc_price('tiktok')}", callback_data="unlock_tiktok"),
        InlineKeyboardButton(f"{get_text(user_id, 'btn_insta')} - {calc_price('insta')}", callback_data="unlock_insta"),
        InlineKeyboardButton(get_text(user_id, "btn_wheel"), callback_data="open_lucky_wheel"),
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
    
    now_tr = datetime.datetime.utcnow() + datetime.timedelta(hours=3)
    current_hour = now_tr.hour
    
    try:
        if user_id not in first_time_users:
            first_time_users.add(user_id)
            if os.path.exists("hosgeldin.ogg"):
                with open("hosgeldin.ogg", "rb") as voice_file:
                    bot.send_voice(chat_id, voice_file, caption="👑 Hoş geldin kral!")
        elif 8 <= current_hour < 10:
            if os.path.exists("gunaydin.ogg"):
                with open("gunaydin.ogg", "rb") as voice_file:
                    bot.send_voice(chat_id, voice_file, caption="☀️ Günaydın reis nasılsın iyisin?")
    except Exception:
        pass

    current_date_str = now_tr.strftime("%Y-%m-%d")
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

    txt = get_text(user_id, "welcome") + reward_message
    if user_id == ADMIN_ID: 
        txt += get_text(user_id, "admin_active")
        
    bot.send_message(chat_id, txt, reply_markup=get_main_keyboard(user_id), parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    data = call.data
    
    if data == "open_lucky_wheel":
        bot.answer_callback_query(call.id)
        now_date = (datetime.datetime.utcnow() + datetime.timedelta(hours=3)).strftime("%Y-%m-%d")
        
        if user_id not in wheel_rights:
            wheel_rights[user_id] = {"date": now_date, "count": 3}
        elif wheel_rights[user_id]["date"] != now_date:
            wheel_rights[user_id] = {"date": now_date, "count": 3}
            
        kalan_hak = wheel_rights[user_id]["count"]
        
        wheel_text = (
            f"🎡 **Şans Çarkı Odasına Hoş Geldin NEYOM!**\n\n"
            f"Bugünkü kalan çevirme hakkın: `{kalan_hak} / 3`\n\n"
            f"Çarkı çevirerek **%50, %80, %89, %98, %99 veya %100** indirim kazanabilirsin!\n"
            f"*(Eğer %100 gelirse seçtiğin paket tamamen ücretsiz / 0 Yıldız olur!)*"
        )
        
        m = InlineKeyboardMarkup(row_width=1)
        if kalan_hak > 0:
            m.add(InlineKeyboardButton("🎲 Çarkı Hemen Çevir!", callback_data="spin_wheel_action"))
        m.add(InlineKeyboardButton(get_text(user_id, "back_menu"), callback_data="back_to_main"))
        
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=wheel_text, reply_markup=m, parse_mode="Markdown")
        return

    if data == "spin_wheel_action":
        now_date = (datetime.datetime.utcnow() + datetime.timedelta(hours=3)).strftime("%Y-%m-%d")
        if user_id not in wheel_rights or wheel_rights[user_id]["date"] != now_date:
            wheel_rights[user_id] = {"date": now_date, "count": 3}
            
        if wheel_rights[user_id]["count"] <= 0:
            bot.answer_callback_query(call.id, "⚠️ Bugünkü çevirme hakkın bitti!", show_alert=True)
            return
            
        wheel_rights[user_id]["count"] -= 1
        
        try:
            bot.send_dice(chat_id, emoji="🎯")
        except:
            pass
            
        discounts = [50, 80, 89, 98, 99, 100]
        weights = [40, 25, 15, 10, 8, 2]
        chosen_discount = random.choices(discounts, weights=weights, k=1)[0]
        
        user_discounts[user_id] = chosen_discount
        
        res_text = f"🎡 **Çark Döndü ve Durdu!**\n\n✨ **Tebrikler!** Çarktan **%{chosen_discount} İndirim** kazandın!\n\n"
        
        if chosen_discount == 100:
            res_text += "🏆 İnanılmaz! **%100 İndirim** kazandın! Butonlardaki paketler tamamen **0 Yıldız (Ücretsiz)** oldu reisim!"
        else:
            res_text += f"Bu indirimle paketlerin fiyatı düştü reisim!"

        m = InlineKeyboardMarkup()
        m.add(InlineKeyboardButton("🔄 Tekrar Çevir", callback_data="open_lucky_wheel"))
        m.add(InlineKeyboardButton(get_text(user_id, "back_menu"), callback_data="back_to_main"))
        
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=res_text, reply_markup=m, parse_mode="Markdown")
        return

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

            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton(get_text(user_id, "btn_fast"), callback_data="fast_download_invoice"))
            
            status_msg = bot.send_message(chat_id, f"🔄 İndiriliyor: **%1**", reply_markup=markup, parse_mode="Markdown")
            fast_downloads[user_id] = False
            
            for percent in range(5, 101, 20):
                if fast_downloads.get(user_id, False):
                    break 
                time.sleep(1) 
                try:
                    bot.edit_message_text(chat_id=chat_id, message_id=status_msg.message_id, text=f"🔄 İndiriliyor: **%{percent}**", reply_markup=markup, parse_mode="Markdown")
                except:
                    pass

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
                if os.path.exists(output): 
                    os.remove(output)
            except Exception as e:
                bot.send_message(chat_id, f"❌ Hata: Bu gönderi desteklenmiyor.")
                if os.path.exists(output): 
                    os.remove(output)
            except Exception as e:
                bot.send_message(chat_id, f"❌ Hata: Bu gönderi desteklenmiyor.")
                if os.path.exists(output): 
                    os.remove(output)
            
            try: bot.delete_message(chat_id, status_msg.message_id)
            except: pass
            
        pending_links.pop(user_id, None)
        user_states[user_id] = None
        fast_downloads.pop(user_id, None)
        return

    if user_id == ADMIN_ID and data.startswith("unlock_"):
        p_key = data.replace("unlock_", "").replace("yt_", "")
        user_states[user_id] = f"waiting_for_{p_key}"
        bot.answer_callback_query(call.id, f"👑 Admin: {p_key} açıldı!")
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
            user_states[user_id] = f"waiting_for_{pl}"
            user_discounts[user_id] = 0  
            bot.send_message(chat_id, f"🎉 Çark İndirimi Kullanıldı! 5200 indirme hakkın ücretsiz tanımlandı reisim!")
            return
            
        final_price = base_prices[pl]
        if disc > 0:
            final_price = int(final_price * (100 - disc) / 100)
            
        bot.send_invoice(
            chat_id=chat_id, 
            title=pl.capitalize(), 
            description="5200 Hak", 
            invoice_payload=pl, 
            provider_token="", 
            currency="XTR", 
            prices=[LabeledPrice(pl, final_price)]
        )

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

    links = [line.strip() for line in raw_text.splitlines() if line.strip().startswith("http")]
    if not links:
        bot.reply_to(message, get_text(user_id, "start_fallback"))
        return

    pending_links[user_id] = {"links": links[:999]}
    format_markup = InlineKeyboardMarkup(row_width=2)
    format_markup.add(
        InlineKeyboardButton(get_text(user_id, "btn_video"), callback_data="dl_video"),
        InlineKeyboardButton(get_text(user_id, "btn_audio"), callback_data="dl_audio")
    )
    bot.send_message(chat_id, f"📥 {len(links[:999])} adet bağlantı alındı!\n\n" + get_text(user_id, "choose_format"), reply_markup=format_markup, parse_mode="Markdown")

bot.infinity_polling(skip_pending=True)
