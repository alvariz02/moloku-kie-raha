import urllib.request,json,concurrent.futures
from pathlib import Path
c=json.loads(Path('scripts/expansion-candidates-final.json').read_text())
items=[]
for key,credit,caption in [('papeda','Shutterstock / Hendra Kashva via Indonesia Travel','Papeda ikan kuah kuning dalam dokumentasi Indonesia Travel; sajian juga dikenal di Maluku dan Papua.'),('bagea','Indonesia Travel','Bagea sagu dalam dokumentasi Indonesia Travel.'),('halua-kenari','Saloi.id','Dokumentasi halua kenari dalam laporan tentang produksi di Desa Suma, Makian.')]:
 items.append((key,c[key]['image'],c[key]['source'],credit,caption))
items += [
('togal','https://infopublik.id/resources/album/seni-budaya/TARI_LALAYON1.jpeg','https://infopublik.id/galeri/foto/detail/204154','InfoPublik / MC Tidore','Penampilan yang diberi judul Tari Togal oleh InfoPublik; nama berkas sumber berbeda dari judul halaman.'),
('bambu-gila','https://awsimages.detik.net.id/community/media/visual/2023/08/07/atraksi-bambu-gila-di-pantai-tobololo-ternate_169.jpeg?q=90&w=700','https://travel.detik.com/fototravel/d-6862419/melihat-atraksi-bambu-gila-di-pantai-tobololo-ternate','ANTARA FOTO / Andri Saputra via detikTravel','Atraksi Bambu Gila di Pantai Tobololo, Ternate, 6 Agustus 2023.'),
('sagu-kasbi','https://annienugraha.com/wp-content/uploads/2017/01/Sagu-Singkong-09.jpg','https://annienugraha.com/sagu-singkong-roti-ala-tidore/','Annie Nugraha','Sagu singkong dalam dokumentasi perjalanan Annie Nugraha di Tidore.'),
('pisang-mulu-bebek','https://static.republika.co.id/uploads/images/inpicture_slide/pisang-mulu-bebek-_180125134746-610.jpg','https://ameera.republika.co.id/berita/p33mvv328/gurihnya-pisang-mulu-bebek-bercocol-sambal','Republika / Christiyaningsih','Pisang mulu bebek dengan sambal dalam dokumentasi sajian di Ternate.'),
('festival-teluk-jailolo','https://biroadpim.malutprov.go.id/public/img/informasi/berita/1781754821_464ac633179346ba444f.jpeg','https://biroadpim.malutprov.go.id/melihat-khazanah-budaya-moloku-kie-raha-lewat-festival-teluk-jailolo-2026','Biro Adpim Provinsi Maluku Utara','Dokumentasi Festival Teluk Jailolo 2026, bukan jadwal acara mendatang.'),
('kasbi-komplet','https://c.inilah.com/reborn/2024/07/Kasbi_Komplet_11zon_8e31fd8d69.jpg','https://www.inilah.com/makanan-khas-maluku','Inilah.com','Foto rujukan sajian kasbi komplet dari artikel kuliner Maluku; tidak diklaim sebagai satu resep baku.')]
def get(item):
 k,url,source,credit,caption=item
 try:
  data=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=20).read();assert len(data)>5000
  ext='webp' if data[8:12]==b'WEBP' else 'png' if data.startswith(b'\x89PNG') else 'jpg';Path('public/assets/'+k+'.'+ext).write_bytes(data)
  return k,{'src':'/assets/'+k+'.'+ext,'source':source,'credit':credit,'caption':caption,'alt':caption,'remote':url,'license':'Hak foto mengikuti penerbit sumber'}
 except Exception as e:print(k,str(e));return k,None
p=Path('public/assets/photo-credits.json');d=json.loads(p.read_text())
for k,v in concurrent.futures.ThreadPoolExecutor(max_workers=7).map(get,items):
 if v:d[k]=v;print('OK',k)
p.write_text(json.dumps(d,indent=2,ensure_ascii=False));Path('lib/photos.mjs').write_text('export const photoCredits='+json.dumps(d,indent=2,ensure_ascii=False)+';\n',encoding='utf8')
