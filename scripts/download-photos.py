import json,urllib.request,urllib.parse,re,concurrent.futures
from pathlib import Path
root=Path('public/assets')
a=json.loads(Path('scripts/photo-candidates.json').read_text());b=json.loads(Path('scripts/photo-candidates-2.json').read_text());a.update({k:v for k,v in b.items() if not v.get('error')})
a['kedaton-ternate']['image']='https://upload.wikimedia.org/wikipedia/commons/a/a3/Bagian_depan_Kedaton_Ternate.jpg';a['kedaton-ternate']['credit']='Oceanmuse / Wikimedia Commons';a['kedaton-ternate']['license']='CC BY 4.0';a['kedaton-ternate']['licenseUrl']='https://creativecommons.org/licenses/by/4.0/'
a['batik-tubo']['image']='https://www.iwarebatik.org/wp-content/uploads/2020/01/3-3.png';a['batik-tubo']['license']='Penggunaan dengan rujukan sumber sesuai ketentuan iWareBatik'
a['tide-tide']['image']='https://wonderful.pulaumorotaikab.go.id/gambar/budaya/budaya-tarian-tide-tide-1-l.jpg'
a['musik-bambu-tada']['image']='https://iwip.co.id/wp-content/uploads/2025/11/DSC03178-768x512.jpg'
a['hibualamo']['image']='https://web.halmaherautarakab.go.id/component/media/upload-gambar-artikel/1000019130.jpg'
# Use culture-specific publisher pages, never their generic site preview.
for key,url,credit in [('gohu-ikan','https://www.indonesia.travel/gb/en/travel-ideas/gastronomy/gohu-ikan','Indonesia Travel'),('arababu','https://indonesiakaya.com/pustaka-indonesia/uniknya-arababu-dalam-lantunan-musik-tradisional-ternate/','Indonesia Kaya'),('air-guraka','https://www.indonesia.travel/id/id/travel-ideas/gastronomy/air-guraka','Indonesia Travel')]:
 try:
  h=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=20).read().decode()
  m=re.search(r'<meta[^>]+property="og:image"[^>]+content="([^"]+)',h) or re.search(r'<meta[^>]+content="([^"]+)"[^>]+property="og:image"',h)
  if m:a[key]={'page':url,'credit':credit,'image':urllib.parse.urljoin(url,m.group(1))}
 except Exception as e:print(key,str(e))
keys=['kedaton-ternate','gohu-ikan','arababu','air-guraka','coka-iba','kololi-kie','musik-bambu-tada','batik-tubo','tide-tide','hibualamo']
def download(key):
 v=a.get(key,{})
 if not v.get('image'):return key,None
 try:
  data=urllib.request.urlopen(urllib.request.Request(v['image'],headers={'User-Agent':'Mozilla/5.0'}),timeout=25).read()
  if len(data)<5000:raise Exception('Image too small')
  ext='png' if data.startswith(b'\x89PNG') else 'webp' if data[8:12]==b'WEBP' else 'jpg'
  path=root/(key+'.'+ext);path.write_bytes(data)
  return key,{'src':'/assets/'+path.name,'source':v['page'],'credit':v['credit'],'license':v.get('license','Hak foto mengikuti penerbit sumber'),'licenseUrl':v.get('licenseUrl'),'remote':v['image']}
 except Exception as e:print(key,str(e));return key,None
out={k:v for k,v in concurrent.futures.ThreadPoolExecutor(max_workers=6).map(download,keys) if v}
Path('public/assets/photo-credits.json').write_text(json.dumps(out,indent=2,ensure_ascii=False))
print(json.dumps(out,ensure_ascii=False))
