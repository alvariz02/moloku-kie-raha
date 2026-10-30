import urllib.request,urllib.parse,json,re,concurrent.futures
from pathlib import Path
pages={
'kedaton-ternate':('https://www.indonesia.travel/id/id/travel-ideas/heritage/kedaton-sultan-ternate','Indonesia Travel'),
'gohu-ikan':('https://www.indonesia.travel/id/id/travel-ideas/culinary/gohu-ikan','Indonesia Travel'),
'hibualamo':('https://kikomunal-indonesia.dgip.go.id/home/explore/traditional/31498','DJKI / Dinas Pendidikan dan Kebudayaan Halmahera Utara'),
'coka-iba':('https://infopublik.id/galeri/foto/212844','G. Juna / MC Tidore / InfoPublik'),
'kololi-kie':('https://ternatekota.go.id/berita/ritual-kololi-kie-awali-peringatan-hari-jadi-ternate-ke-775-tahun-2025','Pemerintah Kota Ternate'),
'musik-bambu-tada':('https://iwip.co.id/bambu-tada-tetap-hidup/','PT IWIP'),
'batik-tubo':('https://www.iwarebatik.org/tubo-kelapa-eng/','iWareBatik'),
'bambu-gila':('https://referensi.data.kemdikbud.go.id/budayakita/wbtb/objek/AA000224','Pangkalan Data WBTb'),
"tide-tide":('https://referensi.data.kemdikbud.go.id/budayakita/wbtb/objek/AA000182','Pangkalan Data WBTb')}
def fetch(item):
 key,(url,credit)=item
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
  h=urllib.request.urlopen(req,timeout=25).read().decode('utf-8',errors='replace')
  Path('scripts/photo-'+key+'.html').write_text(h,encoding='utf8')
  tags=re.findall(r'<meta\b[^>]+>',h,re.I)
  image=''
  for tag in tags:
   if re.search(r'(?:og:image|twitter:image)["\s]',tag,re.I):
    m=re.search(r'content=[\"\x27]([^\"\x27]+)',tag,re.I)
    if m:image=urllib.parse.urljoin(url,m.group(1).replace('&amp;','&'));break
  imgs=re.findall(r'<img[^>]+src=[\"\x27]([^\"\x27]+)',h,re.I)
  return key,{'page':url,'credit':credit,'image':image,'candidates':imgs[:25]}
 except Exception as e:return key,{'error':str(e),'page':url}
result=dict(concurrent.futures.ThreadPoolExecutor(max_workers=7).map(fetch,pages.items()))
Path('scripts/photo-candidates.json').write_text(json.dumps(result,indent=2))
for key,value in result.items(): print(key,json.dumps(value))
