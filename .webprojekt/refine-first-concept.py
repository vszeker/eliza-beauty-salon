from pathlib import Path
import re,json
from html import escape
root=Path(__file__).resolve().parent.parent
p=root/'koncepcio-1-csendes-enido.html'
s=p.read_text(encoding='utf-8')
assets=json.loads((root/'.webprojekt/website-images.json').read_text(encoding='utf-8'))
def photo(slug,cls='',sizes='(max-width:760px) calc(100vw - 40px), 560px',hero=False):
 d=assets[slug];v=d['variants'][0]
 srcset=', '.join(f"{x['path']} {x['width']}w" for x in reversed(d['variants']))
 return f'<img class="{cls}" src="{v["path"]}" srcset="{srcset}" sizes="{sizes}" width="{v["width"]}" height="{v["height"]}" alt="{escape(d["alt"])}" decoding="async" '+('fetchpriority="high"' if hero else 'loading="lazy"')+'>'
s=re.sub(r'<svg class="care-thread".*?</svg>','',s,flags=re.S)
# Remove obsolete guide-line rules as well as its SVG.
s=re.sub(r'\.care-thread(?: path)?\{[^}]*\}','',s)
s=re.sub(r'<img class="hero-photo"[^>]*>',photo('mask-care','hero-photo',hero=True),s,count=1)
s=re.sub(r'<img class="about-photo"[^>]*>',photo('facial-care','about-photo'),s,count=1)
gallery='<div class="photo-grid staggered-gallery">'
for slug,caption in [('mask-treatment','A törődés itt kezdődik.'),('skin-detail','Figyelem a bőröd igényeire.'),('cream-texture','Ápolás a mindennapokban is.')]:
 gallery+='<figure>'+photo(slug,sizes='(max-width:600px) 75vw, (max-width:760px) 29vw, 380px')+'<figcaption class="photo-caption">'+caption+'</figcaption></figure>'
gallery+='</div>'
s=re.sub(r'<div class="photo-grid">.*?</div></section><section class="section wrap" style="padding-top:0">',gallery+'</section><section class="section wrap" style="padding-top:0">',s,count=1,flags=re.S)
contact='''<div class="opening-panel"><div class="opening-heading"><span class="opening-dot" aria-hidden="true"></span><h3>Amikor szeretettel várlak</h3></div><div class="opening-main"><span>Hétfőtől péntekig</span><strong>9:00–16:00</strong></div><div class="opening-weekend"><span>Szombat és vasárnap</span><span>Zárva</span></div><p>Kizárólag előre egyeztetett időpontra.</p></div><address class="contact-details"><div class="contact-location"><span class="contact-icon" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M19 10c0 5-7 11-7 11S5 15 5 10a7 7 0 1 1 14 0Z"/><circle cx="12" cy="10" r="2.5"/></svg></span><div><span class="contact-label">Itt találsz meg</span><span>1092 Budapest, Ráday u. 1.</span></div></div><div class="contact-channels"><a href="tel:+36203449272"><span class="contact-label">Beszéljünk telefonon</span><span class="contact-value">+36 20 344 9272</span></a><a href="mailto:hello.elizabeauty@gmail.com"><span class="contact-label">Vagy írj nekem</span><span class="contact-value contact-email">hello.elizabeauty@gmail.com</span></a></div></address>'''
s=re.sub(r'<address>.*?</address><p class="hours">.*?</p>',contact,s,count=1,flags=re.S)
css='''
/* Első koncepció: a kiválasztott irány további finomítása. */
.hero-photo{object-position:55% center}.about-photo{height:340px;object-position:center 50%;border-radius:24px 120px 24px 24px}
.staggered-gallery{grid-template-columns:repeat(3,minmax(0,1fr));gap:32px;align-items:start;padding-bottom:12px}.staggered-gallery figure:nth-child(1){padding-top:0}.staggered-gallery figure:nth-child(2){padding-top:88px}.staggered-gallery figure:nth-child(3){padding-top:32px}.staggered-gallery img,.staggered-gallery figure:nth-child(2) img{height:370px;width:100%;border-radius:140px 140px 24px 24px;object-fit:cover}.staggered-gallery figure:nth-child(2) img{border-radius:24px 24px 140px 140px;object-position:center 45%}.staggered-gallery figure:nth-child(3) img{border-radius:100px 24px 100px 24px}
.opening-panel{background:var(--color-brand-surface);border-radius:20px;margin-top:32px;padding:28px 32px}.opening-heading{display:flex;align-items:center;gap:12px}.opening-heading h3{font:500 16px/1.4 var(--font-body)}.opening-dot{width:8px;height:8px;border-radius:50%;background:var(--color-brand-primary);flex-shrink:0}.opening-main{display:flex;justify-content:space-between;align-items:center;gap:16px;margin-top:20px}.opening-main>span{font-size:16px}.opening-main strong{font:500 clamp(30px,3vw,40px)/1.2 var(--font-heading);color:var(--color-brand-primary);white-space:nowrap}.opening-weekend{display:flex;justify-content:space-between;gap:16px;border-top:1px solid #d8c5ba;margin-top:20px;padding-top:16px;font-size:15px;color:var(--color-brand-muted)}.contact .opening-panel p{font-size:14px;margin-top:16px}.contact .contact-details{margin-top:28px;display:block;font-size:16px}.contact-location{display:flex;gap:16px;align-items:center;padding-bottom:24px;border-bottom:1px solid var(--line)}.contact-icon{width:44px;height:44px;border:1px solid var(--line);border-radius:50%;display:grid;place-items:center;flex-shrink:0;color:var(--color-brand-primary)}.contact-icon svg{width:22px;height:22px;fill:none;stroke:currentColor;stroke-width:1.4}.contact-label{display:block;font-size:13px;color:var(--color-brand-muted);margin-bottom:5px}.contact-channels{display:grid;grid-template-columns:1fr;gap:20px;margin-top:24px}.contact address .contact-channels a{text-decoration:none;display:block}.contact-value{font-size:21px;color:var(--color-brand-primary);border-bottom:1px solid transparent;transition:border-color .2s}.contact-channels a:hover .contact-value{border-color:var(--color-brand-primary)}.contact-value.contact-email{font-size:17px;overflow-wrap:anywhere}.contact form{position:sticky;top:140px}
@media(max-width:1000px){.opening-main{display:block}.opening-main strong{display:block;margin-top:8px}.staggered-gallery{gap:24px}.staggered-gallery img,.staggered-gallery figure:nth-child(2) img{height:310px}}
@media(max-width:760px){.about-photo{height:300px}.staggered-gallery{gap:20px}.staggered-gallery figure:nth-child(2){padding-top:48px}.staggered-gallery figure:nth-child(3){padding-top:16px}.staggered-gallery img,.staggered-gallery figure:nth-child(2) img{height:240px}.opening-panel{padding:24px}.opening-main{display:flex}.opening-main strong{margin:0;font-size:34px}.contact form{position:static}}
@media(max-width:600px){.staggered-gallery{display:flex;gap:20px;overflow-x:auto;scroll-snap-type:x proximity;padding:0 0 20px;align-items:flex-start}.staggered-gallery figure{flex:0 0 76%;scroll-snap-align:start}.staggered-gallery img,.staggered-gallery figure:nth-child(2) img{height:330px}.staggered-gallery figure:nth-child(2){padding-top:40px}.staggered-gallery figure:nth-child(3){padding-top:16px}.opening-main{display:block}.opening-main strong{margin-top:8px;font-size:38px}.opening-weekend{font-size:14px}}
'''
s=s.replace('</style>',css+'</style>',1)
p.write_text(s,encoding='utf-8')
print('Az első változat öt kért módosítása elkészült.')
