import json,urllib.request,concurrent.futures
from pathlib import Path
items=[('bahasa-map','https://upload.wikimedia.org/wikipedia/commons/b/b3/82_Maluku_Utara.png','https://commons.wikimedia.org/wiki/File:82_Maluku_Utara.png','Badan Pengembangan dan Pembinaan Bahasa via Wikimedia Commons','Peta persebaran bahasa Maluku Utara dari Badan Bahasa. Ini peta rujukan, bukan foto penutur.','Public domain'),('togal','https://blue.kumparan.com/image/upload/fl_progressive%2Cfl_lossy%2Cc_fill%2Cf_auto%2Cq_auto%3Abest%2Cw_640/v1567434996/gm81c5p95pnghjfcgb3h.jpg','https://kumparan.com/ceritamalukuutara/tarian-togal-desa-talimau-hipnotis-pengunjung-iccf-2019-1rmrP6gWQhA','Cermat / kumparan','Penampilan Togal dari Desa Talimau dalam dokumentasi ICCF 2019.','Hak foto mengikuti penerbit sumber')]
def get(row):
 k,url,source,credit,caption,license=row
 try:
  data=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=25).read();assert len(data)>5000
  ext='png' if data.startswith(b'\x89PNG') else 'webp' if data[8:12]==b'WEBP' else 'jpg';Path('public/assets/'+k+'.'+ext).write_bytes(data);return k,{'src':'/assets/'+k+'.'+ext,'source':source,'credit':credit,'caption':caption,'alt':caption,'license':license,'remote':url}
 except Exception as e:print(k,str(e));return k,None
p=Path('public/assets/photo-credits.json');d=json.loads(p.read_text())
for k,v in concurrent.futures.ThreadPoolExecutor(max_workers=2).map(get,items):
 if not v:continue
 if k=='bahasa-map':
  for id in ['bahasa-sula','bahasa-taliabu','bahasa-tobelo','bahasa-ternate']:d[id]=dict(v,kind='map')
 else:d[k]=v
p.write_text(json.dumps(d,indent=2,ensure_ascii=False));Path('lib/photos.mjs').write_text('export const photoCredits='+json.dumps(d,indent=2,ensure_ascii=False)+';\n',encoding='utf8')
