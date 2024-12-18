from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Ganti dengan kunci rahasia Anda

# Simulasi data pengguna (contoh)
users = {
    "selvi": "111",
    "user2": "password2"
}

# Fungsi Diagnosis Penyakit
def diagnose(gejala):
    if "warna pucat" in gejala and "sirip rusak" in gejala:
        return """<p><strong>Diagnosis:</strong> Ikan terinfeksi bakteri <em>Aeromonas</em>.</p>
<p><strong>Penyebab:</strong> Kualitas air yang buruk atau luka pada ikan yang terinfeksi bakteri.</p>
<p><strong>Solusi:</strong></p>
<ul>
    <li>Pisahkan ikan yang sakit dari ikan lainnya.</li>
    <li>Ganti 30-50% air akuarium dengan air bersih.</li>
    <li>Berikan antibiotik seperti <em>Oxytetracycline</em> atau <em>Chloramphenicol</em>.</li>
    <li>Jaga kebersihan akuarium dan perbaiki sirkulasi air.</li>
</ul>"""
    elif "muncul bintik putih" in gejala and "ikan menggosokkan tubuh ke benda" in gejala:
        return """<p><strong>Diagnosis:</strong> Ikan terkena penyakit <em>White Spot Disease</em> (Ich).</p>
<p><strong>Penyebab:</strong> Infeksi parasit <em>Ichthyophthirius multifiliis</em>.</p>
<p><strong>Solusi:</strong></p>
<ul>
    <li>Naikkan suhu air secara bertahap hingga 28-30°C untuk mempercepat siklus hidup parasit.</li>
    <li>Tambahkan obat anti-parasit seperti <em>Malachite Green</em> atau <em>Formalin</em>.</li>
    <li>Siphon dasar akuarium untuk membersihkan telur parasit.</li>
    <li>Isolasi ikan yang sangat parah dan obati secara terpisah.</li>
</ul>"""
    elif "insang merah atau membengkak" in gejala:
        return """<p><strong>Diagnosis:</strong> Ikan mengalami infeksi insang (Branchiomycosis).</p>
<p><strong>Penyebab:</strong> Jamur atau bakteri yang menyerang insang akibat kualitas air buruk.</p>
<p><strong>Solusi:</strong></p>
<ul>
    <li>Periksa dan stabilkan parameter kualitas air (pH, amonia, nitrat).</li>
    <li>Berikan obat anti-jamur seperti <em>Potassium Permanganate</em>.</li>
    <li>Tambahkan aerasi untuk meningkatkan kadar oksigen dalam air.</li>
    <li>Ganti sebagian air dan bersihkan filter akuarium.</li>
</ul>"""
    elif "berenang tidak seimbang" in gejala:
        return """<p><strong>Diagnosis:</strong> Ikan mengalami gangguan kantung renang (<em>Swim Bladder Disorder</em>).</p>
<p><strong>Penyebab:</strong> Makan berlebihan, sembelit, atau infeksi bakteri.</p>
<p><strong>Solusi:</strong></p>
<ul>
    <li>Puasakan ikan selama 1-2 hari untuk mengurangi tekanan pada kantung renang.</li>
    <li>Berikan pakan yang mudah dicerna seperti kacang polong rebus (tanpa kulit).</li>
    <li>Hindari pemberian pakan berlebihan di masa depan.</li>
    <li>Periksa suhu air agar tetap stabil (sekitar 25-27°C).</li>
</ul>"""
    elif "nafsu makan menurun" in gejala:
        return """<p><strong>Diagnosis:</strong> Ikan mengalami stres.</p>
<p><strong>Penyebab:</strong> Kualitas air buruk, kepadatan ikan terlalu tinggi, atau lingkungan tidak stabil.</p>
<p><strong>Solusi:</strong></p>
<ul>
    <li>Periksa parameter kualitas air (pH, suhu, oksigen).</li>
    <li>Kurangi kepadatan ikan di akuarium atau kolam.</li>
    <li>Tambahkan tanaman air atau tempat persembunyian untuk ikan.</li>
    <li>Pastikan ikan mendapatkan pakan yang sesuai dan bergizi.</li>
</ul>"""
    elif "tubuh ikan berlendir" in gejala or "tumbuh jamur pada tubuh" in gejala:
        return """<p><strong>Diagnosis:</strong> Ikan mengalami infeksi jamur.</p>
<p><strong>Penyebab:</strong> Kualitas air buruk atau luka pada tubuh ikan.</p>
<p><strong>Solusi:</strong></p>
<ul>
    <li>Pisahkan ikan yang terinfeksi dari ikan lainnya.</li>
    <li>Gunakan obat anti-jamur seperti <em>Methylene Blue</em> atau <em>Malachite Green</em>.</li>
    <li>Jaga kualitas air dengan penggantian air secara rutin.</li>
    <li>Tambahkan garam ikan untuk membantu penyembuhan.</li>
</ul>"""
    elif "mata bengkak atau menonjol" in gejala:
        return """<p><strong>Diagnosis:</strong> Ikan mengalami <em>Pop-eye Disease</em>.</p>
<p><strong>Penyebab:</strong> Infeksi bakteri atau cedera fisik.</p>
<p><strong>Solusi:</strong></p>
<ul>
    <li>Ganti sebagian air untuk meningkatkan kualitasnya.</li>
    <li>Gunakan antibiotik seperti <em>Erythromycin</em>.</li>
    <li>Periksa parameter air untuk memastikan kestabilan.</li>
    <li>Pisahkan ikan yang terinfeksi jika diperlukan.</li>
</ul>"""
    elif "ikan sulit bernapas" in gejala:
        return """<p><strong>Diagnosis:</strong> Ikan mengalami kekurangan oksigen atau keracunan amonia.</p>
<p><strong>Penyebab:</strong> Kurangnya aerasi atau kualitas air buruk.</p>
<p><strong>Solusi:</strong></p>
<ul>
    <li>Tambahkan aerasi atau gunakan pompa oksigen.</li>
    <li>Ganti sebagian air untuk mengurangi kadar amonia.</li>
    <li>Periksa dan sesuaikan parameter air.</li>
    <li>Kurangi kepadatan ikan dalam akuarium.</li>
</ul>"""
    elif "tubuh ikan terlihat kaku" in gejala:
        return """<p><strong>Diagnosis:</strong> Ikan mungkin terkena penyakit bakteri atau parasit.</p>
<p><strong>Penyebab:</strong> Infeksi bakteri atau parasit yang menyerang ikan.</p>
<p><strong>Solusi:</strong></p>
<ul>
    <li>Pisahkan ikan yang terinfeksi untuk observasi.</li>
    <li>Gunakan obat anti-bakteri atau anti-parasit sesuai kebutuhan.</li>
    <li>Periksa kualitas air secara menyeluruh.</li>
</ul>"""
    # Additional Symptoms and Diagnoses
    elif "ikan bergerak lambat" in gejala:
        return """<p><strong>Diagnosis:</strong> Ikan mengalami penurunan aktivitas akibat stres atau masalah kesehatan.</p>
<p><strong>Penyebab:</strong> Kualitas air buruk, suhu air terlalu rendah, atau infeksi.</p>
<p><strong>Solusi:</strong></p>
<ul>
    <li>Periksa parameter air (pH, suhu, oksigen).</li>
    <li>Pastikan suhu air sesuai dengan spesies ikan.</li>
    <li>Pisahkan ikan yang tampak lesu untuk pemulihan.</li>
</ul>"""
    elif "ikan cenderung diam di dasar" in gejala:
        return """<p><strong>Diagnosis:</strong> Ikan mengalami stres atau kualitas air buruk.</p>
<p><strong>Penyebab:</strong> Kekurangan oksigen, suhu air tidak stabil, atau infeksi.</p>
<p><strong>Solusi:</strong></p>
<ul>
    <li>Periksa dan stabilkan parameter kualitas air (pH, suhu, oksigen).</li>
    <li>Pastikan aerasi yang cukup di akuarium.</li>
    <li>Berikan lingkungan yang lebih tenang untuk ikan.</li>
</ul>"""
    elif "sirip ikan rusak" in gejala:
        return """<p><strong>Diagnosis:</strong> Ikan terkena luka atau infeksi pada sirip.</p>
<p><strong>Penyebab:</strong> Cedera fisik atau infeksi bakteri.</p>
<p><strong>Solusi:</strong></p>
<ul>
    <li>Pisahkan ikan yang terluka untuk perawatan khusus.</li>
    <li>Gunakan obat anti-bakteri atau antiseptik.</li>
    <li>Periksa dan pastikan kualitas air baik.</li>
</ul>"""
    elif "ekor ikan rusak" in gejala:
        return """<p><strong>Diagnosis:</strong> Ekor ikan rusak akibat infeksi atau cedera.</p>
<p><strong>Penyebab:</strong> Luka fisik atau infeksi bakteri.</p>
<p><strong>Solusi:</strong></p>
<ul>
    <li>Pisahkan ikan yang terinfeksi.</li>
    <li>Gunakan obat yang sesuai untuk infeksi.</li>
    <li>Jaga kebersihan air dan lakukan penggantian rutin.</li>
</ul>"""
    elif "warna tubuh memudar" in gejala:
        return """<p><strong>Diagnosis:</strong> Ikan mengalami stres atau kekurangan nutrisi.</p>
<p><strong>Penyebab:</strong> Kualitas air buruk atau kurangnya pakan yang bergizi.</p>
<p><strong>Solusi:</strong></p>
<ul>
    <li>Periksa kualitas air (pH, suhu, oksigen).</li>
    <li>Pastikan ikan mendapatkan pakan yang sesuai dan bergizi.</li>
    <li>Kurangi kepadatan ikan jika perlu.</li>
</ul>"""
    elif "kerontokan sisik" in gejala:
        return """<p><strong>Diagnosis:</strong> Ikan mengalami infeksi atau masalah dengan kualitas air.</p>
<p><strong>Penyebab:</strong> Infeksi bakteri atau kualitas air yang buruk.</p>
<p><strong>Solusi:</strong></p>
<ul>
    <li>Periksa kualitas air dan lakukan penggantian air jika perlu.</li>
    <li>Gunakan obat anti-bakteri untuk pengobatan.</li>
    <li>Pastikan lingkungan ikan tidak terlalu padat.</li>
</ul>"""
    elif "ikan melompat keluar air" in gejala:
        return """<p><strong>Diagnosis:</strong> Ikan merasa terancam atau kualitas air buruk.</p>
<p><strong>Penyebab:</strong> Stres karena kualitas air yang buruk atau gangguan di lingkungan.</p>
<p><strong>Solusi:</strong></p>
<ul>
    <li>Periksa dan stabilkan kualitas air.</li>
    <li>Jaga lingkungan akuarium agar tetap tenang.</li>
    <li>Kurangi kepadatan ikan untuk mengurangi stres.</li>
</ul>"""
    else:
        return """<p><strong>Diagnosis:</strong> Penyakit tidak terdeteksi.</p>
<p><strong>Solusi:</strong></p>
<ul>
    <li>Periksa gejala lebih lanjut atau konsultasikan ke ahli perikanan.</li>
    <li>Jaga kebersihan air dan lakukan penggantian air rutin.</li>
    <li>Pantau perilaku ikan untuk gejala tambahan.</li>
</ul>"""


# Route Halaman Diagnosis
@app.route("/", methods=["GET", "POST"])
def index():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    hasil = ""
    gejala_list = [
        "warna pucat", "sirip rusak", "muncul bintik putih", "ikan menggosokkan tubuh ke benda",
        "insang merah atau membengkak", "berenang tidak seimbang", "nafsu makan menurun",
        "tubuh ikan berlendir", "tumbuh jamur pada tubuh", "ikan melompat keluar air",
        "mata bengkak atau menonjol", "warna tubuh memudar", "ikan cenderung diam di dasar",
        "ikan sulit bernapas", "tubuh ikan terlihat kaku", "kerontokan sisik",
        "perut ikan membengkak", "ikan bergerak lambat", "ikan terlihat gelisah",
        "ekor ikan rusak", "sirip ikan berlubang", "lapisan lendir berlebihan",
        "ikan lemah dan tidak aktif", "kulit ikan mengelupas", "mata ikan tampak kabur",
        "ikan terlihat goyah", "ikan mengalami pendarahan di tubuh", "ikan memuntahkan pakan",
        "insang ikan tampak putih", "ikan melompat ke permukaan air", "kulit ikan menghitam",
        "perut ikan kembung", "sirip ikan mengalami kerusakan parah", "ikan mati mendadak",
        "ekor ikan terlihat kaku", "ikan menggigit tubuhnya sendiri", "kuku ikan rusak", "sirip ikan pecah",
        "ikan mengalami kerusakan pada mulut", "ikan tertular penyakit bakteri"
    ]
    if request.method == "POST":
        gejala = request.form.getlist("gejala")
        hasil = diagnose(gejala)
    return render_template("diagnosis.html", hasil=hasil, gejala_list=gejala_list)

# Route Halaman Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # Cek kredensial pengguna
        if username in users and users[username] == password:
            session["logged_in"] = True  # Tandai sebagai login
            session["username"] = username
            flash(f"Selamat datang, {username}!", "success")
            return redirect(url_for("index"))  # Arahkan ke halaman diagnosis
        else:
            flash("Username atau password salah.", "danger")
            return redirect(url_for("login"))
    return render_template("login.html")

# Route Halaman Register
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        users[username] = password
        flash(f"Pengguna {username} berhasil didaftarkan!", "success")
        return redirect(url_for("login"))
    return render_template("register.html")

if __name__ == "__main__":
    app.run(debug=True)
