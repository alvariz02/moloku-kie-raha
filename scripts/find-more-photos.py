import urllib.request,urllib.parse,json,re,concurrent.futures
from pathlib import Path
pages={
'arababu':('https://infopublik.id/galeri/foto/detail/204960','MC Tidore / InfoPublik'),
'kedaton-ternate':('https://commons.wikimedia.org/wiki/File:Bagian_depan_Kedaton_Ternate.jpg','Wikimedia Commons'),
'gohu-ikan':('https://www.indonesia.travel/id/id/travel-ideas/food/gohu-ikan','Indonesia Travel'),
'tide-tide':('https://www.wonderful.pulaumorotaikab.go.id/budaya/tarian-tide-tide','Dinas Pariwisata Pulau Morotai'),
'hibualamo':('https://web.halmaherautarakab.go.id/publikasi/562-festival-pijar-hibualmo-2024-resmi-dibuka-bupati-halmahera-utara','Pemerintah Kabupaten Halmahera Utara'),
'gerabah-mare':('https://ciptamedia.gitlab.io/hibahcme/248','Arlinah Madjid / Cipta Media'),
'kabata':('https://pasiar.ternatekota.go.id/','PASIAR Kota Ternate')}

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
Path('scripts/photo-candidates-2.json').write_text(json.dumps(result,indent=2))
for key,value in result.items(): print(key,json.dumps(value))
