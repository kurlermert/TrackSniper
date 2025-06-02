import socket
import time
import tkinter as tk
import threading
import requests

calisiyor = False
hedef_kullanici = ""

def telegram_bildirim(token, chat_id, mesaj):
    try:
        requests.get(
            f"https://api.telegram.org/bot{token}/sendMessage",
            params={"chat_id": chat_id, "text": mesaj}
        )
    except Exception as e:
        print("Telegram Hatası:", e)

def check_user_in_chat(host, port, nick, password, channel, user):
    try:
        s = socket.socket()
        s.connect((host, port))
        s.send(f"PASS {password}\r\n".encode("utf-8"))
        s.send(f"NICK {nick}\r\n".encode("utf-8"))
        s.send(f"JOIN #{channel}\r\n".encode("utf-8"))
        time.sleep(2)
        s.send(f"NAMES #{channel}\r\n".encode("utf-8"))
        time.sleep(2)
        resp = s.recv(4096).decode("utf-8")
        s.close()
        return user.lower() in resp.lower()
    except Exception:
        return False

def dongulu_kontrol():
    global calisiyor
    token = entry_token.get().strip()
    chat_id = entry_chat_id.get().strip()
    host = entry_host.get().strip()
    port = int(entry_port.get().strip())
    nick = entry_nick.get().strip()
    password = entry_password.get().strip()
    user_list = entry_kanallar.get("1.0", tk.END).strip().splitlines()
    while calisiyor:
        for kanal in user_list:
            if not calisiyor:
                break
            bulundu = check_user_in_chat(host, port, nick, password, kanal, hedef_kullanici)
            sonuc = f"{kanal} -> {'✅ VAR' if bulundu else '❌ YOK'}\n"
            result_box.insert(tk.END, sonuc)
            result_box.see(tk.END)
            if bulundu:
                telegram_bildirim(token, chat_id, f"🎯 {hedef_kullanici} {kanal} kanalında bulundu!")
            time.sleep(1)
        result_box.insert(tk.END, "--- Başlangıca dönülüyor ---\n")
        result_box.see(tk.END)
        time.sleep(3)

def baslat():
    global calisiyor, hedef_kullanici
    hedef_kullanici = entry_kullanici.get().strip()
    if not hedef_kullanici:
        result_box.insert(tk.END, "❗ Lütfen bir kullanıcı adı girin.\n")
        return
    calisiyor = True
    threading.Thread(target=dongulu_kontrol).start()
    telegram_bildirim(entry_token.get().strip(), entry_chat_id.get().strip(), f"🎯 TrackSniper başladı: {hedef_kullanici}")
    result_box.insert(tk.END, f"Takip başlatıldı: {hedef_kullanici}\n")

def durdur():
    global calisiyor
    calisiyor = False
    result_box.insert(tk.END, "🛑 Takip durduruldu.\n")
    telegram_bildirim(entry_token.get().strip(), entry_chat_id.get().strip(), "🛑 TrackSniper durduruldu.")

pencere = tk.Tk()
pencere.title("TrackSniper")
pencere.geometry("500x800")

tk.Label(pencere, text="Telegram Bot Token:").pack(pady=3)
entry_token = tk.Entry(pencere, font=("Arial", 10))
entry_token.pack(pady=3)

tk.Label(pencere, text="Telegram Chat ID:").pack(pady=3)
entry_chat_id = tk.Entry(pencere, font=("Arial", 10))
entry_chat_id.pack(pady=3)

tk.Label(pencere, text="IRC Host (örn: irc.chat.twitch.tv):").pack(pady=3)
entry_host = tk.Entry(pencere, font=("Arial", 10))
entry_host.pack(pady=3)

tk.Label(pencere, text="IRC Port (örn: 6667):").pack(pady=3)
entry_port = tk.Entry(pencere, font=("Arial", 10))
entry_port.pack(pady=3)

tk.Label(pencere, text="IRC Nick (örn: justinfan12345):").pack(pady=3)
entry_nick = tk.Entry(pencere, font=("Arial", 10))
entry_nick.pack(pady=3)

tk.Label(pencere, text="IRC Password (örn: oauth:anonymous):").pack(pady=3)
entry_password = tk.Entry(pencere, font=("Arial", 10))
entry_password.pack(pady=3)

tk.Label(pencere, text="Takip Edilecek Kanallar (her satıra bir kanal):").pack(pady=3)
entry_kanallar = tk.Text(pencere, height=10, width=40)
entry_kanallar.pack(pady=3)

tk.Label(pencere, text="Takip Edilecek Kullanıcı Adı:").pack(pady=3)
entry_kullanici = tk.Entry(pencere, font=("Arial", 12))
entry_kullanici.pack(pady=5)

tk.Button(pencere, text="Başlat", command=baslat, bg="lightgreen", width=20).pack(pady=5)
tk.Button(pencere, text="Durdur", command=durdur, bg="tomato", width=20).pack(pady=5)

result_box = tk.Text(pencere, height=20, width=60)
result_box.pack(pady=10)

pencere.mainloop()
