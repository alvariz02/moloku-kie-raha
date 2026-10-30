import urllib.request,urllib.parse,re,json,concurrent.futures
from pathlib import Path
pages={
'kabata':'https://infopublik.id/galeri/foto/detail/7592',
'togal':'https://infopublik.id/galeri/foto/detail/204154',
'bahasa-map':'https://petabahasa.kemendikdasmen.go.id/provinsi.php?idp=Maluku+Utara',
'papeda':'https://www.indonesia.travel/id/id/travel-ideas/gastronomy/papeda-ikan-kuah-kuning',
'bagea':'https://www.indonesia.travel/gb/en/travel-ideas/gastronomy/kue-bagea-sagu',
'lapis-tidore':'https://rri.co.id/ternate/berita-lain/2289519/kue-lapis-tidore-jadi-favorit-lebaran-kini-dilindungi-negara',
'legu-gam':'https://www.indonesia.travel/id/id/news-update/legu-gam-festival-2016-on-ternate',
'manteren-lamo':'https://www.indonesia.travel/id/id/travel-ideas/culture/manteren-lamo-maluku',
'sagu-kasbi':'https://malut.brmp.pertanian.go.id/berita/mengulik-peluang-sni-sagu-kasbi',
'halua-kenari':'https://saloi.id/2025/07/12/menengok-sentra-usaha-halua-kenari-desa-suma-halmahera-selatan/'
}
def read(item):
 key,url=item
 try:
  html=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=20).read().decode('utf8',errors='replace')
  Path('scripts/research-'+key+'.html').write_text(html,encoding='utf8')
  image=''
  for tag in re.findall(r'<meta\b[^>]+>',html,re.I):
   if 'og:image' in tag:
    m=re.search(r'content=[\"\x27]([^\"\x27]+)',tag,re.I)
    if m:image=urllib.parse.urljoin(url,m.group(1).replace('&amp;','&'));break
  imgs=[urllib.parse.urljoin(url,x.replace('&amp;','&')) for x in re.findall(r'<img[^>]+src=[\"\x27]([^\"\x27]+)',html,re.I)]
  return key,{'source':url,'image':image,'candidates':imgs[:18]}
 except Exception as e:return key,{'source':url,'error':str(e)}
d=dict(concurrent.futures.ThreadPoolExecutor(max_workers=8).map(read,pages.items()));Path('scripts/expansion-candidates.json').write_text(json.dumps(d,indent=2));print(json.dumps(d))
