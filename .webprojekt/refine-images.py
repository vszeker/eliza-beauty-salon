from pathlib import Path

root = Path(__file__).resolve().parent.parent
def img(src, alt, cls='', height=500):
    return f'<img class="{cls}" src="images/{src}" alt="{alt}" width="800" height="{height}" loading="lazy">'

p = root/'koncepcio-1-csendes-enido.html'
s = p.read_text(encoding='utf-8')
css = '''
/* Képes irány finomítása: íves fotók és a törődés folytonos vonala. */
main{position:relative;isolation:isolate;overflow:hidden}.care-thread{position:absolute;inset:0;width:100%;height:100%;z-index:-1;pointer-events:none;color:#C9A27E;opacity:.5}.care-thread path{fill:none;stroke:currentColor;stroke-width:1.3;vector-effect:non-scaling-stroke}
.photo-frame{position:relative;margin:0;isolation:isolate}.photo-frame:before{content:'';position:absolute;inset:20px -18px -20px 22px;background:#F1E6DF;border-radius:48% 48% 28px 28px;z-index:-1}.photo-frame:after{content:'';position:absolute;inset:-14px 18px 18px -14px;border:1px solid #C9A27E;border-radius:48% 48% 28px 28px;z-index:-1;opacity:.65}.hero-photo{border-radius:48% 48% 24px 24px;object-position:53% center}.hero{padding-bottom:88px}.detail-frame:before{background:#FAF6F2;inset:24px 24px -20px -20px;border-radius:24px 44% 24px 44%}.detail-frame:after{border-radius:24px 44% 24px 44%;inset:-14px -14px 20px 20px}.detail-photo{border-radius:24px 44% 24px 44%}
.service-photo{margin-top:40px;max-width:360px}.service-photo img{width:100%;height:220px;object-fit:cover;border-radius:100px 16px 100px 16px}.photo-caption{font-size:12px;line-height:1.5;color:var(--color-brand-muted);margin-top:12px}.about-visual{display:grid;gap:28px}.about-photo{width:100%;height:280px;object-fit:cover;border-radius:160px 160px 20px 20px;object-position:center 55%}.about-visual .credentials{padding:16px 32px}.about-visual .credentials>div{display:flex;align-items:center;gap:24px;padding:16px 0}.about-visual .credentials strong{font-size:32px;min-width:94px}.care-gallery{padding:24px 0 96px}.gallery-heading{display:flex;justify-content:space-between;align-items:end;gap:32px;margin-bottom:40px}.gallery-heading p{max-width:400px}.photo-grid{display:grid;grid-template-columns:1.15fr .85fr;gap:64px;align-items:start}.photo-grid figure{margin:0}.photo-grid figure:nth-child(2){padding-top:72px}.photo-grid img{width:100%;height:360px;object-fit:cover;border-radius:24px 140px 24px 24px}.photo-grid figure:nth-child(2) img{height:320px;border-radius:140px 24px 24px 24px}.newsletter-photo{margin-top:28px;width:100%;height:230px;object-fit:cover;object-position:center 65%;border-radius:16px 90px 16px 90px}
@media(max-width:760px){.care-thread{opacity:.28}.hero{padding-bottom:60px}.hero .photo-frame{margin:12px 12px 0 0}.photo-frame:before{inset:16px -12px -14px 16px}.photo-frame:after{inset:-10px 14px 14px -10px}.hero-photo{height:390px;border-radius:48% 48% 20px 20px}.detail-frame{margin:12px 12px 0}.detail-photo{height:370px}.service-photo{max-width:none;margin-top:28px}.service-photo img{height:200px}.about-photo{height:300px}.about-visual .credentials{padding:12px 24px}.care-gallery{padding:0 0 64px}.gallery-heading{display:block;margin-bottom:28px}.gallery-heading p{margin-top:16px}.photo-grid{gap:20px;grid-template-columns:1fr 1fr}.photo-grid figure:nth-child(2){padding-top:48px}.photo-grid img{height:240px;border-radius:16px 70px 16px 16px}.photo-grid figure:nth-child(2) img{height:220px;border-radius:70px 16px 16px 16px}.newsletter-photo{height:200px}.photo-caption{font-size:11px}}
@media(max-width:420px){.hero-photo{height:340px}.photo-grid{grid-template-columns:1fr;gap:28px}.photo-grid figure:nth-child(2){padding-top:0}.photo-grid img,.photo-grid figure:nth-child(2) img{height:260px}.about-visual .credentials>div{gap:12px}}
'''
s=s.replace('</style>',css+'</style>',1)
thread='<svg class="care-thread" viewBox="0 0 1440 6000" preserveAspectRatio="none" aria-hidden="true"><path d="M1210 0 C1510 520 1280 730 1090 880 S80 1150 80 1540 S360 1980 1110 2150 S1460 2700 1290 3000 S90 3260 100 3700 S420 4140 1160 4400 S1420 5000 1230 5300 S140 5580 200 6000"/></svg>'
s=s.replace('<main id="tartalom">','<main id="tartalom">'+thread,1)
start='<img class="hero-photo"'; pos=s.index(start); end=s.index('>',pos)+1
s=s[:pos]+'<figure class="photo-frame">'+s[pos:end]+'</figure>'+s[end:]
pos=s.index('<img class="detail-photo"');end=s.index('>',pos)+1
s=s[:pos]+'<figure class="photo-frame detail-frame">'+s[pos:end]+'</figure>'+s[end:]
anchor='</p></div><div class="service-list">'
s=s.replace(anchor,'</p><figure class="service-photo">'+img('facial-care.jpg','Arcpakolás egy kozmetikai kezelés közben, illusztráció')+'<figcaption class="photo-caption">Személyre szabott ápolás, lépésről lépésre.</figcaption></figure></div><div class="service-list">',1)
s=s.replace('<div class="credentials"><div><strong>14+', '<div class="about-visual">'+img('spa-interior.jpg','Törölközők, virág és ápolási kellékek, hangulatfotó','about-photo')+'<div class="credentials"><div><strong>14+',1)
s=s.replace('kozmetikus, szakmai tréner és oktató</span></div></div></section>','kozmetikus, szakmai tréner és oktató</span></div></div></div></section>',1)
gallery='''<section class="wrap care-gallery" aria-labelledby="care-gallery-title"><div class="gallery-heading"><h2 id="care-gallery-title">Egy kis figyelem.<br>Egy mélyebb lélegzet.</h2><p>A kezelés ideje a bőrödről és a feltöltődésedről szól.</p></div><div class="photo-grid"><figure>'''+img('facial-care.jpg','Arckezelési részlet, illusztráció')+'''<figcaption class="photo-caption">Gondoskodás a bőröd igényei szerint.</figcaption></figure><figure>'''+img('spa-interior.jpg','Puha törölközők és ápolási kellékek természetes fényben')+'''<figcaption class="photo-caption">Apró részletek, nyugodt pillanatok. Hangulatfotók.</figcaption></figure></div></section>'''
s=s.replace('<section class="section wrap" style="padding-top:0">',gallery+'<section class="section wrap" style="padding-top:0">',1)
s=s.replace('Hasznos tippek és szakértői tanácsok a mindennapi ápoláshoz.</p></div><form','Hasznos tippek és szakértői tanácsok a mindennapi ápoláshoz.</p>'+img('skincare.jpg','Bőrápoló üveg természetes fényben, hangulatfotó','newsletter-photo')+'</div><form',1)
p.write_text(s,encoding='utf-8')

p=root/'koncepcio-2-a-gondoskodas-tere.html'
s=p.read_text(encoding='utf-8')
css='''
/* Több fotós pillanat, az eredeti szerkezethez igazítva. */
.process-photo{width:100%;height:300px;object-fit:cover;object-position:center 48%;border-radius:16px;margin-top:48px}.image-pair{display:grid;grid-template-columns:1.2fr .8fr;gap:40px;align-items:start;padding-bottom:96px}.image-pair figure{margin:0}.image-pair figure:nth-child(2){padding-top:56px}.image-pair img{width:100%;height:360px;object-fit:cover;border-radius:16px}.image-pair figure:nth-child(2) img{height:304px}.image-pair figcaption{font-size:13px;color:var(--color-brand-muted);margin-top:12px}.newsletter-still{width:100%;height:230px;object-fit:cover;object-position:center 60%;border-radius:16px;margin-top:32px}
@media(max-width:800px){.process-photo{height:220px;margin-top:32px}.image-pair{gap:20px;padding-bottom:64px}.image-pair img{height:250px}.image-pair figure:nth-child(2){padding-top:40px}.image-pair figure:nth-child(2) img{height:210px}.newsletter-still{height:200px}.image-pair figcaption{font-size:12px}}
@media(max-width:480px){.image-pair{grid-template-columns:1fr;gap:28px}.image-pair figure:nth-child(2){padding-top:0}.image-pair img,.image-pair figure:nth-child(2) img{height:260px}}
'''
s=s.replace('</style>',css+'</style>',1)
anchor='</article></div></div></section>\n<section id="kezelesek"'
s=s.replace(anchor,'</article></div>'+img('facial-care.jpg','Arcpakolás felvitele kozmetikai kezelés közben, hangulatfotó','process-photo',400)+'</div></section>\n<section id="kezelesek"',1)
pair='<section class="wrap image-pair" aria-label="A törődés részletei, hangulatfotók"><figure>'+img('spa-interior.jpg','Törölközők, virág és kozmetikai kellékek, hangulatfotó')+'<figcaption>A nyugalom az apró részletekben is ott van.</figcaption></figure><figure>'+img('facial-care.jpg','Arcpakolás egy kezelés során, illusztráció')+'<figcaption>Figyelem és gondoskodás minden lépésben.</figcaption></figure></section>'
s=s.replace('<section class="reviews pad"',pair+'<section class="reviews pad"',1)
s=s.replace('hasznos tippek és szakértői tanácsok a mindennapi bőrápoláshoz.</p></div><form','hasznos tippek és szakértői tanácsok a mindennapi bőrápoláshoz.</p>'+img('spa-interior.jpg','Ápolási kellékek és puha törölközők, hangulatfotó','newsletter-still')+'</div><form',1)
p.write_text(s,encoding='utf-8')
print('Az első és második koncepció képes finomítása elkészült.')
