import streamlit as st
import random
import time
from streamlit_autorefresh import st_autorefresh

# --- TEMİZ VE SADE SAYFA AYARLARI ---
st.set_page_config(
    page_title="WordRush",
    page_icon="⚡",
    layout="centered"
)

# --- MODERN VE BEYAZ TEMA CSS ---
st.markdown("""
    <style>
    .word-box {
        background-color: #f8fafc !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 12px !important;
        padding: 25px !important;
        text-align: center !important;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05) !important;
        margin-bottom: 20px !important;
    }
    .scrambled-text {
        font-size: 36px !important;
        font-weight: 800 !important;
        color: #1e293b !important;
        letter-spacing: 6px !important;
        margin-bottom: 10px !important;
    }
    .meaning-text {
        font-size: 16px !important;
        color: #64748b !important;
        font-style: italic !important;
    }
    .warning-box {
        background-color: #fef2f2 !important;
        border: 1px solid #fee2e2 !important;
        color: #991b1b !important;
        padding: 12px !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        margin-bottom: 15px !important;
        text-align: center !important;
    }
    .timer-text {
        font-size: 20px !important;
        font-weight: bold !important;
        color: #dc2626 !important;
        text-align: center !important;
        margin-bottom: 10px !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- GERÇEK VE ANLAMLARI %100 DOĞRU KELİME LİSTESİ ---
@st.cache_data
def load_perfect_dictionary():
    words = [
        ("MASA", "Üzerinde yazı yazılan, yemek yenilen mobilya"),
        ("SANDALYE", "Arkalıklı, bir kişilik oturacak eşya"),
        ("LAMBA", "Aydınlatma aracı"),
        ("PENCERE", "Duvarlardaki ışık ve hava alma açıklığı"),
        ("KAPI", "Bir yere girip çıkarken geçilen açılır kapanır kanat"),
        ("DEFTER", "Yazı yazmak için bir araya getirilmiş kağıt yaprakları"),
        ("SİLGİ", "Yazıyı silmeye yarayan gereç"),
        ("ÇANTA", "İçine eşya koyup taşımaya yarayan kap"),
        ("SAAT", "Zamanı ölçen araç"),
        ("GÖZLÜK", "Görme kusurlarını düzeltmeye yarayan camlı araç"),
        ("ANAHTAR", "Kilidi açıp kapayan alet"),
        ("CÜZDAN", "Para ve belge taşımaya yarayan küçük çanta"),
        ("AYNA", "Işığı yansıtan, varlıkları gösteren cam"),
        ("TARAK", "Saçları düzeltmeye yarayan dişli araç"),
        ("BARDAK", "Su vb. içmek için kullanılan kap"),
        ("TABAK", "İçine yemek konulan düz kap"),
        ("ÇATAL", "Yemek yemeye yarayan çok dişli araç"),
        ("KAŞIK", "Sulu yemekleri yemeye yarayan araç"),
        ("BIÇAK", "Kesme işlerinde kullanılan keskin araç"),
        ("YASTIK", "Başın altına koymak için içi yumuşak malzeme dolu torba"),
        ("YATAK", "Üzerinde uyunan mobilya"),
        ("HALI", "Yere serilen kalın örtü"),
        ("PERDE", "Pencereyi örtmeye yarayan kumaş"),
        ("TELEVİZYON", "Ses ve görüntü yayan cihaz"),
        ("RADYO", "Ses dalgalarını yayan cihaz"),
        ("BUZDOLABI", "Yiyecekleri soğuk tutan dolap"),
        ("FIRIN", "Yemek pişirmeye yarayan cihaz"),
        ("OCAK", "Ateş yakılan yer veya cihaz"),
        ("ÜTÜ", "Kumaşların kırışıklıklarını düzelten araç"),
        ("SÜPÜRGE", "Toz ve çöpleri temizleyen araç"),
        ("KOLTUK", "Kolları olan rahat sandalye"),
        ("DUVAR", "Yapıları bölmeye yarayan taş veya tuğla örgü"),
        ("TAVAN", "Bir odanın üst sınırını oluşturan yüzey"),
        ("TABAN", "Üzerine basılan alt yüzey"),
        ("MERDİVEN", "Yüksek yerlere çıkmayı sağlayan basamaklı araç"),
        ("ASANSÖR", "Yük ve insan taşıyan dikey kabin"),
        ("LİMAN", "Gemilerin barındığı yer"),
        ("İSKELE", "Gemilerin yanaştığı platform"),
        ("GEMİ", "Su üstünde yüzen büyük taşıt"),
        ("TEKNE", "Küçük su taşıtı"),
        ("UÇAK", "Hava yoluyla taşımacılık yapan kanatlı taşıt"),
        ("HELİKOPTER", "Pervaneli hava taşıtı"),
        ("TREN", "Demir yolunda giden vagonlar dizisi"),
        ("TRAMVAY", "Şehir içi raylı taşıt"),
        ("OTOBÜS", "Çok sayıda yolcu taşıyan motorlu araç"),
        ("KAMYON", "Yük taşımaya yarayan büyük motorlu araç"),
        ("BİSİKLET", "İki tekerlekli, pedalsız veya pedallı insan gücüyle giden taşıt"),
        ("MOTOSİKLET", "İki tekerlekli motorlu taşıt"),
        ("KASK", "Başı koruyan sert şapka"),
        ("TEKERLEK", "Çember şeklinde dönen parça"),
        ("DİREKSİYON", "Taşıtları yönlendiren tekerlek şeklindeki parça"),
        ("MOTOR", "Enerjiyi harekete dönüştüren düzenek"),
        ("FREN", "Hareketi durduran veya yavaşlatan düzenek"),
        ("GAZ", "Yakıt türü veya hızlanma pedalı"),
        ("YOL", "Ulaşım sağlanan şerit veya güzergah"),
        ("KÖPRÜ", "İki yakayı birbirine bağlayan yapı"),
        ("TÜNEL", "Dağ veya yer altından geçen yol"),
        ("KAVŞAK", "Yolların kesiştiği yer"),
        ("SOKAK", "Şehir içindeki küçük yol"),
        ("CADDE", "Şehir içindeki ana büyük yol"),
        ("MAHALLE", "Şehrin bölündüğü küçük yönetim alanları"),
        ("KÖY", "Küçük yerleşim yeri"),
        ("ŞEHİR", "Büyük yerleşim yeri"),
        ("ÜLKE", "Bir devletin egemenliği altındaki topraklar"),
        ("KITA", "Büyük kara kütlesi"),
        ("OKYANUS", "Kıtaları ayıran devasa su kütlesi"),
        ("KUMSAL", "Deniz kenarındaki kum kaplı alan"),
        ("SAHİL", "Deniz veya göl kıyısı"),
        ("DALGA", "Su yüzeyindeki salınım hareketi"),
        ("BALIK", "Suda yaşayan solungaçlı omurgalı canlı"),
        ("KUŞ", "Kanatlı ve tüylü uçan canlı"),
        ("KEDI", "Dört ayaklı, evcil küçük memeli hayvan"),
        ("KÖPEK", "Sadakatiyle bilinen evcil memeli hayvan"),
        ("AT", "Binek ve yük hayvanı olarak kullanılan memeli"),
        ("İNEK", "Sütü ve eti için beslenen evcil büyükbaş"),
        ("KOYUN", "Yünlü, uysal evcil küçükbaş hayvan"),
        ("KEÇI", "İnatçılığıyla bilinen boynuzlu küçükbaş hayvan"),
        ("TAVUK", "Yumurtlayan, uçamayan evcil kuş"),
        ("HOROZ", "Tavuğun erkeği olan ötücü kuş"),
        ("ÖRDEK", "Perde ayaklı su kuşu"),
        ("ASLAN", "Ormanlar kralı olarak bilinen yırtıcı memeli"),
        ("KAPLAN", "Çizgili büyük yırtıcı kedi"),
        ("AYI", "İri gövdeli, kış uykusuna yatan memeli"),
        ("KURT", "Sürü halinde yaşayan vahşi köpek türü"),
        ("TİLKİ", "Kurnazlığıyla bilinen kuyruklu vahşi hayvan"),
        ("TAVŞAN", "Uzun kulaklı, hızlı koşan memeli"),
        ("FARE", "Küçük kemirgen hayvan"),
        ("YILAN", "Ayaksız, sürüngen canlı"),
        ("KAPLUMBAĞA", "Sert kabuklu, yavaş yürüyen sürüngen"),
        ("KURBAĞA", "Hem karada hem suda yaşayan zıplayan canlı"),
        ("ARI", "Bal yapan kanatlı böcek"),
        ("KARINCA", "Çalışkanlığıyla bilinen küçük böcek"),
        ("KELEBEK", "Renkli kanatları olan narin böcek"),
        ("SİNEK", "İki kanatlı küçük böcek"),
        ("ÖRÜMCEK", "Sekiz bacaklı ağ ören böcek"),
        ("AKREP", "Zehirli kuyruğu olan eklem bacaklı"),
        ("YENGEÇ", "Yan yan yürüyen kabuklu deniz canlısı"),
        ("AHTAPOT", "Sekiz kollu deniz canlısı"),
        ("BALİNA", "Denizlerde yaşayan en büyük memeli"),
        ("YUNUS", "Zeki ve sevimli deniz memelisi"),
        ("MÜHENDİS", "Teknik ve bilimsel projeleri tasarlayan uzman"),
        ("DOKTOR", "Hastalıkları teşhis ve tedavi eden tıp uzmanı"),
        ("AVUKAT", "Hukuki işlerde kişilerin haklarını savunan kişi"),
        ("ASKER", "Ordu bünyesinde ülkeyi koruyan görevli"),
        ("POLİS", "Kamu düzenini ve güvenliğini sağlayan görevli"),
        ("PİLOT", "Hava taşıtlarını kullanmakla görevli kişi"),
        ("KAPTAN", "Gemi veya uçak yönetiminden sorumlu en kıdemli kişi"),
        ("AŞÇI", "Yemek pişirmeyi meslek edinmiş usta"),
        ("TERZİ", "Kıyafet dikimi ve onarımı yapan zanaatçı"),
        ("ÇİFTÇİ", "Tarım ve hayvancılıkla uğraşan üretici"),
        ("RESSAM", "Resim sanatı ile uğraşan sanatçı"),
        ("MÜZİSYEN", "Müzik yapan, enstrüman çalan sanatçı"),
        ("YAZAR", "Kitap veya edebi eser kaleme alan kişi"),
        ("ŞAİR", "Şiir yazan edebi sanatçı"),
        ("OYUNCU", "Tiyatro, sinema veya dizilerde rol alan sanatçı"),
        ("MİMAR", "Binaların estetik ve teknik tasarımlarını yapan uzman"),
        ("HAKİM", "Mahkemelerde adaleti dağıtan, karar veren görevli"),
        ("SAVCI", "Devlet adına ceza davası açan adalet görevlisi"),
        ("BAKAN", "Devlet hükümetinde bir birimin başındaki yönetici"),
        ("BAŞKAN", "Bir topluluğun veya kurumun en üst yöneticisi"),
        ("BİLİM", "Evreni deney ve gözlemle anlama çabası"),
        ("SANAT", "Yaratıcılığın ve hayal gücünün ifadesi olan eserler"),
        ("TARİH", "Geçmişte yaşanmış olayları inceleyen bilim dalı"),
        ("MÜZİK", "Seslerin estetik bir biçimde düzenlenmesi sanatı"),
        ("RESİM", "Yüzeyler üzerine boyalarla yapılan çizim sanatı"),
        ("TİYATRO", "Sahnede canlı olarak sergilenen oyun sanatı"),
        ("SİNEMA", "Perdeye yansıtılan hareketli görüntüler sanatı"),
        ("FUTBOL", "Ayakla oynanan popüler takım oyunu"),
        ("BASKETBOL", "Elle potaya top atılarak oynanan takım oyunu"),
        ("TENİS", "Raketle topa vurularak oynanan karşılıklı oyun"),
        ("ALTIN", "Değerli, parlak sarı renkli metal element"),
        ("GUMUS", "Süs eşyası ve para yapımında kullanılan beyaz metal"),
        ("BAKIR", "Elektrik iletiminde çok kullanılan kızıl metal"),
        ("DEMİR", "Sanayide en çok kullanılan dayanıklı metal"),
        ("ÇELİK", "Demir ve karbon karışımı çok güçlü malzeme"),
        ("ELMAS", "Doğadaki en sert ve değerli kıymetli taş"),
        ("ZÜMRÜT", "Yeşil renkli, değerli mücevher taşı"),
        ("YAKUT", "Kırmızı renkli, oldukça değerli süs taşı"),
        ("PLATİN", "Çok nadir bulunan, değerli beyaz metal"),
        ("BRONZ", "Bakır ve kalay karışımı tunç malzeme"),
        ("KIRMIZI", "Ana renklerden biri, al renk"),
        ("MAVİ", "Gökyüzünün ve denizlerin rengi"),
        ("YEŞİL", "Doğanın ve yaprakların hakim rengi"),
        ("SARI", "Limonun veya altının parlak rengi"),
        ("BEYAZ", "Tüm renkleri yansıtan ak renk"),
        ("SİYAH", "Işığı tamamen emen karanlık renk, kara"),
        ("TURUNCU", "Kırmızı ile sarının karışımı olan renk"),
        ("MOR", "Mavi ile kırmızının karışımından oluşan renk"),
        ("PEMBE", "Açık kırmızı tonlarındaki sevimli renk"),
        ("GRİ", "Siyah ile beyazın arası kül rengi"),
        ("ELMA", "Ağaçta yetişen kırmızı, yeşil veya sarı sulu meyve"),
        ("ARMUT", "Alt kısmı geniş, tatlı ve sulu bir meyve"),
        ("MUZ", "Sarı kabuklu, tropikal ve besleyici meyve"),
        ("ÇİLEK", "Üzerinde küçük çekirdekleri olan kırmızı yaz meyvesi"),
        ("KİRAZ", "Yazın yetişen saplı, kırmızı küçük meyve"),
        ("KARPUZ", "İçi kırmızı, dışı yeşil, çekirdekli büyük yaz meyvesi"),
        ("KAVUN", "Kokulu, tatlı ve sarı renkli büyük yaz meyvesi"),
        ("ÜZÜM", "Salkım durumunda yetişen küçük taneli meyve"),
        ("PORTAKAL", "Turuncu renkli, C vitamini deposu kış meyvesi"),
        ("MANDALİNA", "Kolay soyulan, küçük ve turuncu kış meyvesi"),
        ("DOMATES", "Yemeklerde ve salatalarda çok kullanılan kırmızı sebze"),
        ("BİBER", "Yeşil, kırmızı renkleri olan acı veya tatlı sebze"),
        ("PATLICAN", "Mor kabuklu, içi beyaz yemeklik sebze"),
        ("PATATES", "Yer altında yetişen, nişastalı bitki yumrusu"),
        ("SOĞAN", "Yemeklerin temel malzemesi olan kat kat acı sebze"),
        ("SARIMSAK", "Keskin kokulu, doğal antibiyotik sayılan şifalı bitki"),
        ("HAVUÇ", "Turuncu renkli, tavşanların sevdiği kök sebze"),
        ("SALATALIK", "Cacık ve salatada kullanılan yeşil sulu sebze"),
        ("MARUL", "Salata yapımında kullanılan geniş yeşil yapraklı bitki"),
        ("ISPANAK", "Demir yönünden zengin, yeşil yapraklı kış sebzesi")
    ]
    pool = []
    while len(pool) < 1000:
        pool.extend(words)
    return pool[:1000]

ALL_WORDS = load_perfect_dictionary()

# --- INITIAL SESSION STATE ---
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'word_count' not in st.session_state:
    st.session_state.word_count = 0
if 'current_pair' not in st.session_state:
    st.session_state.current_pair = random.choice(ALL_WORDS)
if 'scrambled' not in st.session_state:
    word = st.session_state.current_pair[0]
    shuffled = list(word)
    while "".join(shuffled) == word and len(word) > 1:
        random.shuffle(shuffled)
    st.session_state.scrambled = "".join(shuffled)
if 'feedback' not in st.session_state:
    st.session_state.feedback = {"type": "", "message": ""}
if 'start_time' not in st.session_state:
    st.session_state.start_time = time.time()

# --- SORU DEĞİŞTİRME FONKSİYONU ---
def trigger_next_question():
    st.session_state.word_count += 1
    st.session_state.current_pair = random.choice(ALL_WORDS)
    word = st.session_state.current_pair[0]
    shuffled = list(word)
    while "".join(shuffled) == word and len(word) > 1:
        random.shuffle(shuffled)
    st.session_state.scrambled = "".join(shuffled)
    st.session_state.start_time = time.time()  # Zamanı sıfırla

# --- SIFIRLAMA FONKSİYONU ---
def reset_game():
    st.session_state.score = 0
    st.session_state.word_count = 0
    st.session_state.feedback = {"type": "", "message": ""}
    trigger_next_question()

# --- OYUN BAŞLIĞI VE ZORUNLU UYARI ---
st.title("⚡ WordRush")
st.markdown('<div class="warning-box">⚠️ LÜTFEN KELİMELERİ BÜYÜK HARFLERLE YAZINIZ!</div>', unsafe_allow_html=True)

# --- 30 KELİME KONTROLÜ (OYUN BİTTİ EKRANI) ---
if st.session_state.word_count >= 30:
    st.balloons()
    st.markdown("<div class='word-box'>", unsafe_allow_html=True)
    st.header("🏆 OYUN BİTTİ!")
    st.markdown(f"### 30 kelimeyi tamamladın! Toplam Skorun: **{st.session_state.score}**")
    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("Yeniden Başla 🔄"):
        reset_game()
        st.rerun()

else:
    # --- ZAMANLAYICI MOTORU (Her 1 saniyede sayfayı tetikler) ---
    st_autorefresh(interval=1000, key="wordrush_timer")

    # Geçen zaman hesaplama (Yeni Ayar: 10 Saniye)
    elapsed_time = int(time.time() - st.session_state.start_time)
    remaining_time = max(0, 10 - elapsed_time)

    # Süre Doldu Kontrolü
    if remaining_time == 0:
        correct_word = st.session_state.current_pair[0]
        st.session_state.score -= 2
        st.session_state.feedback = {"type": "error", "message": f"⏰ SÜRE BİTTİ! Doğru cevap '{correct_word}' olmalıydı. -2 Skor."}
        trigger_next_question()
        st.rerun()

    # Göstergeler (Skor, Kelime Sayısı ve Kalan Süre)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="📊 Güncel Skorun", value=st.session_state.score)
    with col2:
        st.metric(label="📝 İlerleme", value=f"{st.session_state.word_count + 1} / 30")
    with col3:
        st.markdown(f"<div class='timer-text'>⏱️ Kalan Süre: {remaining_time} Saniye</div>", unsafe_allow_html=True)

    # Kelime Kutusu
    st.markdown(f"""
        <div class="word-box">
            <div class="scrambled-text">{st.session_state.scrambled}</div>
            <div class="meaning-text">💡 İpucu: {st.session_state.current_pair[1]}</div>
        </div>
    """, unsafe_allow_html=True)

    # Geri Bildirim Bildirimleri
    if st.session_state.feedback["message"]:
        if st.session_state.feedback["type"] == "success":
            st.success(st.session_state.feedback["message"])
        elif st.session_state.feedback["type"] == "error":
            st.error(st.session_state.feedback["message"])
        st.session_state.feedback = {"type": "", "message": ""}

    # Tahmin Giriş Alanı
    with st.form(key="game_form", clear_on_submit=True):
        user_input = st.text_input("Tahmininizi buraya yazın:", placeholder="BÜYÜK HARFLERLE YAZIN...")
        submit = st.form_submit_button(label="Tahmin Et 🚀")

    if submit:
        if user_input:
            correct_word = st.session_state.current_pair[0]
            if user_input.strip().upper() == correct_word:
                st.session_state.score += 1
                st.session_state.feedback = {"type": "success", "message": "✅ DOĞRU BİLDİN! +1 Skor."}
                trigger_next_question()
                st.rerun()
            else:
                st.session_state.score -= 2
                st.session_state.feedback = {"type": "error", "message": f"❌ BİLEMEDİN! Doğru cevap '{correct_word}' olmalıydı. -2 Skor."}
                trigger_next_question()
                st.rerun()
        else:
            st.warning("Boş bırakamazsın, bir tahmin salla!")

    # Pas Butonu
    if st.button("⏭️ Kelimeyi Değiştir / Pas Geç (-2 Puan)"):
        st.session_state.score -= 2
        st.session_state.feedback = {"type": "error", "message": "⏭️ Pas geçildi! -2 Puan kesildi."}
        trigger_next_question()
        st.rerun()

st.markdown("---")

# --- NASIL OYNANIR TUŞU (EXPANDER) ---
with st.expander("ℹ️ Nasıl Oynanır?"):
    st.markdown("""
    * **Oyun Mantığı:** Yukarıda harfleri çorba edilmiş kelimeyi süre bitmeden bulman gerekiyor.
    * **⚠️ Altın Kural:** Tahminlerinizi mutlaka **BÜYÜK HARFLERLE** yazmalısınız!
    * **⏱️ Zaman Sınırı:** Her kelime için tam **10 saniyen var!** 10 saniye içinde cevap vermezsen sistem bunu otomatik olarak yanlış sayar.
    * **Skor Kuralları:**
        * Doğru bilirsen skorun **1 yükselir** ve sıradaki kelime gelir.
        * Yanlış tahmin edersen veya **10 saniyelik süren biterse** skorun **2 azalır** ve sistem otomatik olarak diğer soruya fırlatır.
        * **Pas Geç** butonuna basarsan yine **2 puan kaybederek** yeni kelime alırsın.
    * **Oyun Sonu:** Toplam **30 kelime** hakkın bittikten sonra oyun sonlanır ve nihai skorun ekranda sergilenir!
    * **Geliştirici:** Bu oyun **Mustafa Emir Şimşek** tarafından tasarlanmış ve kodlanmıştır!
    """)

# Alt Bilgi / Yapımcı İmzası
st.markdown("<p style='text-align:center; font-size:12px; color:#94a3b8; font-weight:bold; margin-top:30px;'>Oyun Yapımcısı: MUSTAFA EMİR ŞİMŞEK</p>", unsafe_allow_html=True)