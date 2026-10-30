import urllib.request,json,re,concurrent.futures
from pathlib import Path
h=Path('scripts/research-kasbi-komplet.html').read_text(encoding='utf8');urls=re.findall(r'<img[^>]+src="([^"]+)"',h)
lapis=next(x for x in urls if '%252831%2529' in x)
items=[('lapis-tidore',lapis,'https://www.travelerien.com/2017/06/nikmati-kuliner-khas-tidore-ini-di-safira-beach-restaurant.html?m=0','Katerina / Travelerien','Potongan Lapis Tidore dalam dokumentasi kunjungan ke produsen di Tidore.'),('legu-gam','https://eastofwallace.com/fileadmin/_processed_/8/6/csm_gewuerzinsel-ternate-soya-soya-tanz-molukken_60cab60c9e.jpg','https://eastofwallace.com/en/islands/ternate/events-ternate','East of Wallace','Pertunjukan Soya-Soya pada halaman dokumentasi Legu Gam dari East of Wallace.'),('festival-teluk-jailolo','https://biroadpim.malutprov.go.id/public/img/informasi/berita/1781754821_464ac633179346ba444f.jpeg','https://biroadpim.malutprov.go.id/melihat-khazanah-budaya-moloku-kie-raha-lewat-festival-teluk-jailolo-2026','Biro Adpim Provinsi Maluku Utara','Dokumentasi Festival Teluk Jailolo edisi 2026.')]
def get(row):
 k,url,source,credit,caption=row
 try:
  data=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=35).read();assert len(data)>5000
  ext='webp' if data[8:12]==b'WEBP' else 'jpg';Path('public/assets/'+k+'.'+ext).write_bytes(data);print('OK',k);return k,{'src':'/assets/'+k+'.'+ext,'source':source,'credit':credit,'caption':caption,'alt':caption,'license':'Hak foto mengikuti penerbit sumber','remote':url}
 except Exception as e:print(k,str(e));return k,None
p=Path('public/assets/photo-credits.json');d=json.loads(p.read_text())
for k,v in concurrent.futures.ThreadPoolExecutor(max_workers=3).map(get,items):
 if v:d[k]=v
p.write_text(json.dumps(d,indent=2,ensure_ascii=False));Path('lib/photos.mjs').write_text('export const photoCredits='+json.dumps(d,indent=2,ensure_ascii=False)+';\n',encoding='utf8')
