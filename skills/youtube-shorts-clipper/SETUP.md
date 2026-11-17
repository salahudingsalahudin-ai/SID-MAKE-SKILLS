# Setup — YouTube Shorts Clipper (Sid's PC)

Ek dafa setup karo, phir har dafa sirf aik command chalani hai.
Sab kuch terminal mein hota hai, koi download link nahi.

## 1. Tools install karo (aik dafa)

```bash
sudo apt update && sudo apt install -y ffmpeg python3-venv
```

Check karo — teeno ka version ana chahiye:

```bash
ffmpeg -version | head -1
python3 --version
node --version
```

(Node pehle se hai tumhare PC par — YouTube download ke liye
chahiye hota hai. Agar `node` nahi milta to Node.js install karo,
phir dobara try karo.)

## 2. Skill folder mein jao, venv banao, packages install karo

```bash
cd ~/youtube-shorts-clipper
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Har nayi terminal mein pehle ye chalana hai:

```bash
cd ~/youtube-shorts-clipper
source .venv/bin/activate
```

(`.venv` ka matlab: aik alag dabba jismein sirf is project ke
packages hain — tumhare baaki Python ko kuch nahi hota.)

## 3. Pehla test — bina upload, apni video se

```bash
python3 scripts/clip.py ~/Videos/my-video.mp4 --clips 3
```

Ye karega: video parhna → bolna likhna → achay moments dhoondna →
3 vertical clips banana. Clips yahan milen ge:

```
work/my-video/clips/clip_01.mp4
work/my-video/clips/clip_02.mp4
work/my-video/clips/clip_03.mp4
```

Pehli dafa `faster-whisper` ka chhota model download hoga (~75 MB),
aik dafa hi. Video lambi ho to thora waqt lage ga — chhoti video se
shuru karo.

## 4. YouTube link se test

```bash
python3 scripts/clip.py "https://www.youtube.com/watch?v=VIDEO_ID" --clips 3
```

Link ke gird quotes lagana mat bhoolna. Sirf apni video ya jis ki
ijazat ho, us ka link use karo — doosron ki video upload karne se
copyright strike lag sakti hai.

## 5. Upload chahiye to — Google Cloud setup (aik dafa)

Upload ke liye YouTube ko batana parta hai ke "ye mera hi channel
hai". Is ke liye Google Cloud mein aik chhoti si setting karni hai:

1. Browser mein jao: https://console.cloud.google.com/
   Apne Google account se sign in karo (wohi jis se YouTube channel hai).
2. Upar "New Project" banao, naam kuch bhi — jaise `shorts-clipper`.
3. Left menu → "APIs & Services" → "Library" → search karo
   `YouTube Data API v3` → Enable dabao.
4. Left menu → "APIs & Services" → "Credentials" →
   "Create Credentials" → "OAuth client ID" →
   Application type: **Desktop app** → Create.
5. Download ka button dabao — file ka naam `client_secrets.json`
   rakho aur skill folder mein daal do:
   `~/youtube-shorts-clipper/client_secrets.json`
6. Pehli dafa upload karte waqt browser khule ga — Google se sign in
   karo aur "Allow" dabao. Us ke baad token save ho jaye ga, dobara
   browser nahi khule ga.

Phir upload karo:

```bash
python3 scripts/clip.py "https://www.youtube.com/watch?v=VIDEO_ID" --clips 3 --upload
```

Upload **private** hota hai. YouTube Studio mein ja kar Short dekho,
phir khud Public karo.

## 6. Options jo kaam aati hain

```bash
# Zyada clips
python3 scripts/clip.py LINK --clips 5

# Bolne wali video (face camera mein) — beech wala hissa kaato
python3 scripts/clip.py LINK --clips 3 --mode crop

# Gameplay (GTA 6) — poori screen rakho, side blur karo (default)
python3 scripts/clip.py LINK --clips 3 --mode blur

# Bina captions ke
python3 scripts/clip.py LINK --clips 3 --captions off

# Gemini se behtar ranking (agar tumhare paas key hai)
cp .env.example .env
# .env mein likho: GEMINI_API_KEY=tumhari-key
python3 scripts/clip.py LINK --clips 3 --llm gemini

# Seedha public upload (sirf tab jab tum khud dekh chuke ho)
python3 scripts/clip.py LINK --clips 3 --upload --privacy public

# Apna brand + speed tweak (clip aur transformative lage)
python3 scripts/clip.py LINK --clips 3 --brand "RotiAI" --speed 1.1

# Apni commentary mila kar
python3 scripts/clip.py LINK --clips 3 --voiceover ~/commentary.mp3

# Transform band karna ho to (sirf apni video par, warna mat karo)
python3 scripts/clip.py LINK --clips 3 --transform off
```

## 7. Safe rules — clip transformative kaise bane

Har clip mein ye sab **khud-ba-khud** hota hai — tumhe kuch nahi karna:

1. **3-second rule:** koi shot 3 sec se zyada same nahi rehta —
   har 3 sec mein zoom ya pan badal jata hai.
2. **Transformative changes:** 9:16 reframe, dynamic zoom, burned
   captions, apna brand, apni commentary, speed tweak.
3. **Short clip, chhota hissa:** 15–60 sec ka clip, source ka chhota
   hissa. Agar clips 15% se zyada ho jayen to warning milti hai.

**Yaad rakho:** ye risk boht kam karte hain, lekin 100% guarantee
nahi — Content ID phir bhi claim kar sakta hai. Sab se safe apni
video, apni gameplay, apni commentary hai.

## 8. Agar kuch ghalat ho

| Masla | Hal |
|---|---|
| `yt-dlp` download fail | Dobara try karo; YouTube kabhi kabhi rokta hai. Ya video khud download kar ke local file do. |
| `ffmpeg: command not found` | Step 1 dobara karo: `sudo apt install -y ffmpeg` |
| `faster-whisper` slow hai | `--model tiny` hi rakho (default). Lamba video = zyada waqt, normal hai. |
| Upload: `client_secrets.json not found` | Step 5 dekho — file skill folder mein honi chahiye. |
| Upload: quota error | YouTube Data API ki free limit 10,000 units rozana hai — aik upload ~1600 units. Agle din phir try karo. |
| Koi step 2 dafa fail ho | Wohi tareeqa dobara mat chalao — error parho, wo batata hai kya kami hai. |

## 9. Keys kahan rakhtay hain

- `.env` file mein (`.env.example` copy karo). Kabhi chat mein,
  screenshot mein ya GitHub par mat bhejo.
- `client_secrets.json` aur `token.json` sirf tumhare PC par rehte
  hain — `~/.config/youtube-shorts-clipper/token.json`.
