import urllib.request,json,concurrent.futures
from pathlib import Path
p=Path('public/assets/photo-credits.json');d=json.loads(p.read_text())
items=[('air-guraka','https://upload.wikimedia.org/wikipedia/commons/4/48/Air_Guraka_minuman_herbal_tradisional_Maluku_Utara.jpg','https://commons.wikimedia.org/wiki/File:Air_Guraka_minuman_herbal_tradisional_Maluku_Utara.jpg','Muhammad Arifin Hasanuddin / Wikimedia Commons','CC BY 4.0','https://creativecommons.org/licenses/by/4.0/'),('hibualamo','https://jaringnusa.id/wp-content/uploads/2022/08/herli-1024x682.jpg','https://jaringnusa.id/hibua-lamo-simbolis-persatuan-masyarakat-pesisir-halmahera-utara/','Jaring Nusa KTI','Hak foto mengikuti penerbit sumber',None),('gerabah-mare','https://djpb.kemenkeu.go.id/kanwil/malut/images/sinergi-kemenkeu-4.jpeg','https://djpb.kemenkeu.go.id/kanwil/malut/id/data-publikasi/berita-terbaru/2896-sinergi-kanwil-ditjen-perbendaharaan-provinsi-maluku-utara-dengan-bank-indonesia-dan-pemda-dalam-memajukan-usaha-kerajinan-gerabah-di-pulau-mare.html','DJPb Kemenkeu Maluku Utara','Hak foto mengikuti penerbit sumber',None)]
def fetch(item):
 key,url,source,credit,license,licenseUrl=item
 try:
  data=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=25).read();assert len(data)>5000
  Path('public/assets/'+key+'.jpg').write_bytes(data)
  return key,{'src':'/assets/'+key+'.jpg','source':source,'credit':credit,'license':license,'licenseUrl':licenseUrl,'remote':url}
 except Exception as e:print(key,str(e));return key,None
# Omit mismatched event group photo until a building photo is downloaded.
d.pop('hibualamo',None)
for k,v in concurrent.futures.ThreadPoolExecutor(max_workers=3).map(fetch,items):
 if v:d[k]=v
p.write_text(json.dumps(d,indent=2,ensure_ascii=False))
print('Downloaded matching photos:',len(d))
