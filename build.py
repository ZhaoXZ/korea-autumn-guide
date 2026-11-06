import os, json, base64, io
from PIL import Image

BASE = os.path.dirname(os.path.abspath(__file__))
HR = "/tmp/highres_curated"
TMP = "/tmp"
CAND = "/Users/zhaoxiaozhi/.gemini/antigravity/brain/f131a7ba-2d71-4259-b4fd-ee18428c1268/scratch/cand"
IMG_DIR = os.path.join(BASE, 'img')
os.makedirs(IMG_DIR, exist_ok=True)

MAPPING = {
    # 🍁 Autumn Highlights (High-aesthetic golden ginkgo & vibrant red maples)
    'seoulforest': os.path.join(TMP, 'munmyo_ginkgo.jpg'),        # Golden ginkgo canopy
    'huwon': os.path.join(TMP, 'changdeok_buyong.jpg'),           # Changdeokgung Secret Garden Buyongjeong
    'changgyeong': os.path.join(TMP, 'changgyeong_green.jpg'),    # Greenhouse with vibrant autumn foliage
    'deoksugung': os.path.join(TMP, 'deoksu_autumn.jpg'),         # Deoksugung Palace autumn leaves
    'beomeosa': os.path.join(TMP, 'chiak.jpg'),                   # Mountain temple in autumn foliage
    'citizenspark': os.path.join(TMP, 'nami_17.jpg'),             # Golden tree boulevard
    'dosanpark': os.path.join(CAND, 'dosanpark_0.jpg'),

    # 🛍 Key Non-Standard Commercial & Sceneries
    'seongsu': os.path.join(TMP, 'seongsu_storefronts.jpg'),      # Chic boutique shopfronts
    'shinsegae': os.path.join(HR, 'shinsegae.jpg'),               # Glowing Christmas facade at night
    'lotteworld': os.path.join(HR, 'lotteworld.jpg'),             # Fairytale castle on the lake
    'blueline': os.path.join(TMP, 'test_blueline.jpg'),           # Haeundae Sky Capsule train
    'gamcheon': os.path.join(HR, 'gamcheon.jpg'),                 # Colorful village at golden sunset
    'huinnyeoul': os.path.join(HR, 'huinnyeoul.jpg'),             # White cliff village & ocean
    'gwangalli': os.path.join(HR, 'gwangalli.jpg'),               # Gwangan suspension bridge
    'bukchon': os.path.join(HR, 'bukchon.jpg'),                   # Traditional Hanok roofs at twilight
    'ikseon': os.path.join(HR, 'ikseon.jpg'),                     # Ikseon-dong hanok cafe alley
    'biff': os.path.join(HR, 'biff.jpg'),                         # BIFF square at night
    'bosudong': os.path.join(HR, 'bosudong.jpg'),                 # Bosu-dong bookstore alley
    'gwangjang': os.path.join(HR, 'gwangjang.jpg'),               # Bustling Gwangjang market
    'dongmyo': os.path.join(CAND, 'dongmyo_2.jpg'),               # Dongmyo flea market vintage
    'euljiro': os.path.join(CAND, 'euljiro_0.jpg'),               # Hipjiro retro alley
    'garosu': os.path.join(CAND, 'garosu_1.jpg'),                 # Garosu-gil boutique street
    'gyeongui': os.path.join(CAND, 'gyeongui_1.jpg'),             # Yeontral park green trail
    'haeundae': os.path.join(CAND, 'haeundae_1.jpg'),             # Haeundae beach night view
    'myeongdong': os.path.join(CAND, 'myeongdong_2.jpg'),         # Myeongdong shopping street
    'namsan': os.path.join(CAND, 'namsan_2.jpg'),                 # Namsan Tower sunset Seoul
    'centum': os.path.join(CAND, 'centum_0.jpg'),                 # Shinsegae Centum City
    'haeridan': os.path.join(CAND, 'haeridan_0.jpg'),             # Duplit cafe Haeridan-gil
    'millac': os.path.join(CAND, 'millac_1.jpg'),                 # Millac the Market
    'jeonpo': os.path.join(CAND, 'jeonpo_0.jpg'),                 # Jeonpo cafe street
    'mangwon': os.path.join(CAND, 'mangwon_0.jpg'),               # Mangwon market
    'jagalchi': os.path.join(CAND, 'jagalchi_0.jpg'),             # Jagalchi market
    'kkangtong': os.path.join(CAND, 'kkangtong_0.jpg'),           # Bupyeong night market
    'busanstation': os.path.join(CAND, 'busanstation_1.jpg'),     # KTX at Busan station
    'airport': os.path.join(CAND, 'airport_0.jpg'),               # Gimhae airport
    'f1963': os.path.join(TMP, 'starfield.jpg'),                  # Warm cultural library/cafe space
    'yeongdo': os.path.join(CAND, 'piaq_0.jpg'),                  # Yeongdo Piaq cafe
    'gukje': os.path.join(CAND, 'gukje_2.jpg'),                   # Gukje Market

    # 🍜 Gourmet Foods (warm, crisp, mouth-watering)
    'gukbap': os.path.join(TMP, 'dwaeji_new.jpg'),                # Steaming hot pork soup rice!
    'pajeon': os.path.join(CAND, 'dongnae_0.jpg'),                # Crispy green onion seafood pancake
    'bindaetteok': os.path.join(CAND, 'f_bindaetteok_1.jpg'),     # Golden mung bean pancake
    'yukhoe': os.path.join(CAND, 'f_yukhoe_1.jpg'),               # Fresh beef tartare with egg yolk
    'kalguksu': os.path.join(CAND, 'f_kalguksu_0.jpg'),           # Handmade noodle soup
    'milmyeon': os.path.join(CAND, 'f_milmyeon_0.jpg'),           # Busan spicy cold wheat noodles
    'hotteok': os.path.join(CAND, 'f_hotteok_0.jpg'),             # Ssiat hotteok sweet seed pancake
    'bungeoppang': os.path.join(CAND, 'f_bungeoppang_0.jpg'),     # Fresh golden fish bread
    'samgyeopsal': os.path.join(CAND, 'f_samgyeopsal_0.jpg'),     # Grilled pork belly BBQ
    'eomuk': os.path.join(CAND, 'f_eomuk_2.jpg'),                 # Hot fishcake skewers in broth
}

photos_dict = {}
total_b64_len = 0

for k, p in MAPPING.items():
    if not os.path.exists(p):
        webp_path = os.path.join(IMG_DIR, f"{k}.webp")
        if os.path.exists(webp_path):
            with open(webp_path, 'rb') as rf:
                webp_bytes = rf.read()
            b64 = base64.b64encode(webp_bytes).decode('ascii')
            photos_dict[k] = f"data:image/webp;base64,{b64}"
            total_b64_len += len(b64)
            continue
        print(f"Warning: file {p} does not exist!")
        continue
    im = Image.open(p).convert('RGB')
    im.thumbnail((800, 600), Image.Resampling.LANCZOS)
    
    buf = io.BytesIO()
    im.save(buf, format='WEBP', quality=82, method=6)
    webp_bytes = buf.getvalue()
    
    with open(os.path.join(IMG_DIR, f"{k}.webp"), 'wb') as wf:
        wf.write(webp_bytes)
        
    b64 = base64.b64encode(webp_bytes).decode('ascii')
    photos_dict[k] = f"data:image/webp;base64,{b64}"
    total_b64_len += len(b64)

# Build credits list
cands_file = os.path.join(CAND, 'candidates.json')
cands = json.load(open(cands_file)) if os.path.exists(cands_file) else {}

credits_list = []
for k in sorted(MAPPING.keys()):
    fn = os.path.basename(MAPPING[k])
    found = False
    for cand_list in cands.values():
        for item in cand_list:
            if item.get('file') == fn:
                credits_list.append({
                    'k': k,
                    'title': item.get('title', k),
                    'page': item.get('page', 'https://commons.wikimedia.org'),
                    'artist': item.get('artist', 'Wikimedia Commons'),
                    'license': item.get('license', 'CC BY-SA')
                })
                found = True
                break
        if found:
            break
    if not found:
        credits_list.append({
            'k': k,
            'title': k,
            'page': 'https://commons.wikimedia.org',
            'artist': 'Wikimedia Commons',
            'license': 'CC BY-SA'
        })

tpl = open(os.path.join(BASE, 'src', 'template.html')).read()
l_css = open(os.path.join(BASE, 'lib', 'leaflet.css')).read()
l_js = open(os.path.join(BASE, 'lib', 'leaflet.js')).read()

# Load couple avatar for inline header image
avatar_path = os.path.join(IMG_DIR, 'couple_avatar_circle.png')
if os.path.exists(avatar_path):
    av_im = Image.open(avatar_path)
    av_im = av_im.resize((128, 128), Image.Resampling.LANCZOS)
    av_buf = io.BytesIO()
    av_im.save(av_buf, format='PNG', optimize=True)
    av_b64 = base64.b64encode(av_buf.getvalue()).decode('ascii')
    avatar_src = f"data:image/png;base64,{av_b64}"
else:
    avatar_src = "favicon-32x32.png"

out = tpl.replace('/*LEAFLET_CSS*/', l_css)
out = out.replace('/*LEAFLET_JS*/', l_js)
out = out.replace('/*PHOTOS*/', f"const PHOTOS = {json.dumps(photos_dict)};")
out = out.replace('/*CREDITS*/', f"const CREDITS = {json.dumps(credits_list, ensure_ascii=False)};")
out = out.replace('/*COUPLE_AVATAR_SRC*/', avatar_src)

dest = os.path.join(BASE, 'index.html')
with open(dest, 'w') as f:
    f.write(out)

print(f"Generated {dest} ({os.path.getsize(dest)/1024/1024:.2f} MB)")
