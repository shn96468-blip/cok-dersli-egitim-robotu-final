import streamlit as st
import time

# --- YÖNETİCİ GİRİŞİ AYARLARI VE OTURUM BAŞLATMA ---
ADMIN_PASSWORD = "123"
MOCK_USERS = [
    {"username": "ali", "email": "ali@okul.com", "password_hash": "a123"},
    {"username": "ayse", "email": "ayse@okul.com", "password_hash": "a456"},
]

# OTURUM DURUMU BAŞLANGIÇ DEĞERLERİ
if 'admin_mode' not in st.session_state:
    st.session_state['admin_mode'] = False
if 'user_logged_in' not in st.session_state:
    st.session_state['user_logged_in'] = False
if 'current_user' not in st.session_state:
    st.session_state['current_user'] = None
if 'show_admin_login' not in st.session_state:
    st.session_state['show_admin_login'] = False
if 'show_user_login' not in st.session_state:
    st.session_state['show_user_login'] = False
if 'show_user_register' not in st.session_state:
    st.session_state['show_user_register'] = False
if 'app_color' not in st.session_state:
    st.session_state['app_color'] = '#1E90FF' # Varsayılan Tema Rengi
if 'announcement' not in st.session_state:
    st.session_state['announcement'] = "🤖 Eğitim robotu aktif! Yeni konuları keşfetmeye başlayın."
if 'announcement_color' not in st.session_state:
    st.session_state['announcement_color'] = 'warning'
if 'registration_allowed' not in st.session_state:
    st.session_state['registration_allowed'] = True
if 'user_login_allowed' not in st.session_state:
    st.session_state['user_login_allowed'] = True
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []
if 'secilen_ders' not in st.session_state:
    st.session_state['secilen_ders'] = None
if 'music_enabled' not in st.session_state:
    st.session_state['music_enabled'] = False
if 'music_url' not in st.session_state:
    st.session_state['music_url'] = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"


# --- DERS FONKSİYONLARI YEDEK TANIMLARI (SIMÜLASYON) ---
def konuyu_bul_yedek(ders, konu): 
    return f"🤖 İçerik dosyaları yüklenmediği için {ders} dersi **'{konu}'** konusu hakkında genel bilgi veriyorum: Bu bir simülasyon cevabıdır. Gerçek bir AI, burada detaylı konu anlatımı yapacaktır."
    
def soru_cozumu_yap_yedek(ders, soru): 
    return f"🤖 İçerik dosyaları yüklenmediği için {ders} dersi **'{soru}'** sorusu çözülemiyor. Bu bir simülasyon cevabıdır. Gerçek bir AI, burada adım adım çözüm sunacaktır."

konuyu_bul_tr = lambda konu: konuyu_bul_yedek("Türkçe", konu)
soru_cozumu_yap_tr = lambda soru: soru_cozumu_yap_yedek("Türkçe", soru)
konuyu_bul_eng = lambda konu: konuyu_bul_yedek("İngilizce", konu)
soru_cozumu_yap_eng = lambda soru: soru_cozumu_yap_yedek("İngilizce", soru)
konuyu_bul_math = lambda konu: konuyu_bul_yedek("Matematik", konu)
soru_cozumu_yap_math = lambda soru: soru_cozumu_yap_yedek("Matematik", soru)
konuyu_bul_history = lambda konu: konuyu_bul_yedek("Tarih", konu)
soru_cozumu_yap_history = lambda soru: soru_cozumu_yap_yedek("Tarih", soru)
konuyu_bul_religion = lambda konu: konuyu_bul_yedek("Din K.", konu)
soru_cozumu_yap_religion = lambda soru: soru_cozumu_yap_yedek("Din K.", soru)


# --- SAYFA VE SİMGE AYARLARI ---
st.set_page_config(
    page_title="Eğitim Robotu | Yusuf Efe Şahin",
    layout="wide",
    page_icon="🤖" # Projenizi profesyonel gösteren simge!
)

# --- GİRİŞ/ÇIKIŞ VE YÖNETİCİ FONKSİYONLARI ---
def attempt_admin_login(password):
    if password == ADMIN_PASSWORD:
        st.session_state['admin_mode'] = True
        st.session_state['show_admin_login'] = False
        st.rerun()
    else:
        st.error("Hatalı yönetici şifresi.")

def admin_logout():
    st.session_state['admin_mode'] = False
    st.rerun()

def user_login(username, password):
    if not st.session_state['user_login_allowed']:
        st.error("Üye girişi şu anda bakımdadır. Lütfen daha sonra tekrar deneyin.")
        return

    for user in MOCK_USERS:
        if user["username"] == username and user["password_hash"] == password:
            st.session_state['user_logged_in'] = True
            st.session_state['current_user'] = username
            st.session_state['show_user_login'] = False
            st.success(f"Hoş geldiniz, {username.upper()}!")
            time.sleep(1)
            st.rerun()
            return
    st.error("Kullanıcı adı veya şifre yanlış.")

def user_logout():
    st.session_state['user_logged_in'] = False
    st.session_state['current_user'] = None
    st.rerun()

def toggle_admin_login_panel():
    st.session_state['show_admin_login'] = not st.session_state['show_admin_login']
    st.session_state['show_user_login'] = False
    st.session_state['show_user_register'] = False

def toggle_user_login_panel():
    if st.session_state['user_login_allowed']:
        st.session_state['show_user_login'] = not st.session_state['show_user_login']
        st.session_state['show_admin_login'] = False
        st.session_state['show_user_register'] = False
    else:
        st.sidebar.error("Üye girişi şu anda bakımdadır.")

def toggle_user_register_panel():
    if st.session_state['registration_allowed']:
        st.session_state['show_user_register'] = not st.session_state['show_user_register']
        st.session_state['show_admin_login'] = False
        st.session_state['show_user_login'] = False
    else:
        st.sidebar.error("Yeni kayıtlar şu anda kapalıdır.")

def forgot_password_simulation(email_or_username, is_admin=False):
    st.sidebar.warning("Sistemimiz simülasyon modunda olduğundan, şifre sıfırlama linki kayıtlı e-posta adresinize gönderilmiştir.")
    time.sleep(1)
    if is_admin:
        st.sidebar.success(f" Yönetici Şifresi sıfırlama maili 'admin@robot.com' adresine gönderildi.")
    else:
        user_email = "kayıtlı_eposta_adresi"
        for user in MOCK_USERS:
            if user["username"] == email_or_username:
                user_email = user["email"]
                break

        st.sidebar.success(f" Kullanıcı şifresi sıfırlama linki '{user_email}' adresine gönderildi.")


# --- METİN OKUMA FONKSİYONU (SESLENDİRME) ---
def metin_oku(text):
    clean_text = text.replace('"', '').replace('\n', ' ')
    js_code = f"""
    <script>
        var utterance = new SpeechSynthesisUtterance("{clean_text}");
        window.speechSynthesis.speak(utterance);
    </script>
    """
    st.markdown(js_code, unsafe_allow_html=True)


# --- SOHBET VE ÇEVİRİ MANTIKLARI ---
basit_sozluk = {
    "merhaba": "Hello", "selam": "Hi", "teşekkürler": "Thanks", "sağol": "Thanks",
    "elma": "Apple", "armut": "Pear", "kedi": "Cat", "köpek": "Dog",
    "apple": "Elma", "pear": "Armut", "cat": "Kedi", "dog": "Köpek",
    "again": "Tekrar / Yine",
    "teach": "Öğretmek", "study": "Çalışmak", "kitap": "Book", "kalem": "Pen"
}

def instant_translate(kelime_veya_cumle):
    mesaj_lower = kelime_veya_cumle.lower().strip()

    if mesaj_lower in basit_sozluk: # Türkçe'den İngilizce'ye
         return f"'{kelime_veya_cumle.title()}' kelimesinin İngilizce karşılığı: **{basit_sozluk[mesaj_lower]}**."
    elif mesaj_lower in [v.lower() for v in basit_sozluk.values()]: # İngilizce'den Türkçe'ye
        tr_karsilik = next(k for k, v in basit_sozluk.items() if v.lower() == mesaj_lower)
        return f"'{kelime_veya_cumle.title()}' kelimesinin Türkçe karşılığı: **{tr_karsilik}**."
    else:
        # Google Translate Simülasyonu
        return f"'{kelime_veya_cumle}' ifadesi için hazır çeviri bulamadım. Bu uzunluğu çevirmek için gerçek bir dil modeline ihtiyacım var. (Simülasyon)"

def general_chat_kanka(kullanici_mesaji):
    mesaj_lower = kullanici_mesaji.lower().strip()
    kelimeler = mesaj_lower.split()

    # 1. ÇEVİRİ KONTROLÜ (Tek kelime ise veya kelime 'çevir' ile başlıyorsa)
    
    # 'çevir elma' veya sadece 'elma' gibi durumlarda çeviri yap

    if len(kelimeler) == 1 and (kelimeler[0] in basit_sozluk or kelimeler[0] in [v.lower() for v in basit_soz
