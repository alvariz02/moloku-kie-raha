import urllib.request,re,json,concurrent.futures,urllib.parse
from pathlib import Path
candidate=json.loads(Path('scripts/expansion-candidates.json').read_text())
# Resolve publishers' current canonical photo pages and additional event/food imagery.
urls={'kabata':'https://infopublik.id/galeri/foto/7592','togal':'https://infopublik.id/galeri/foto/204154','lapis-tidore':'https://megapolitan.antaranews.com/berita/464429/kemenkum-sebut-kue-lapis-tidore-masuk-kekayaan-intelektual-dilindungi','festival-teluk-jailolo':'https://biroadpim.malutprov.go.id/melihat-khazanah-budaya-moloku-kie-raha-lewat-festival-teluk-jailolo-2026','sagu-kasbi':'https://annienugraha.com/sagu-singkong-roti-ala-tidore/','kasbi-komplet':'https://www.travelerien.com/2017/06/nikmati-kuliner-khas-tidore-ini-di-safira-beach-restaurant.html?m=0'}
def read(pair):
 k,url=pair
 try:
  h=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=20).read().decode('utf8',errors='replace');Path('scripts/research-'+k+'.html').write_text(h,encoding='utf8');tags=re.findall(r'<meta\b[^>]+>',h,re.I);image=''
  for t in tags:
   if 'og:image' in t:
    m=re.search(r'content=[\"\x27]([^\"\x27]+)',t)
    if m:image=urllib.parse.urljoin(url,m.group(1).replace('&amp;','&'));break
  imgs=re.findall(r'<img[^>]+(?:src|data-src)=[\"\x27]([^\"\x27]+)',h,re.I)
  return k,{'source':url,'image':image,'candidates':imgs[:35]}
 except Exception as e:return k,{'error':str(e),'source':url}
candidate.update(dict(concurrent.futures.ThreadPoolExecutor(max_workers=6).map(read,urls.items())))
Path('scripts/expansion-candidates-final.json').write_text(json.dumps(candidate,indent=2));print(json.dumps({k:v for k,v in candidate.items() if k in urls}))
