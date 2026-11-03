from pathlib import Path
from PIL import Image, ImageChops, ImageOps
import re, json
from html import escape

root=Path(__file__).resolve().parent.parent
out=root/'images/website'
out.mkdir(exist_ok=True)
assets={
 'relaxing-facial':('4.png','Relaxáló arckezelés puha törölközőkkel'),
 'facial-device':('10.png','Gépi arckezelés a bőr ápolásához'),
 'serum':('2 másolata.png','Aranyszínű szérum cseppentős üvegben'),
 'care-collection':('3 másolata.png','Bőrápolási készítmények meleg bézs környezetben'),
 'mask-treatment':('3.png','Arcpakolás felvitele ecsettel'),
 'skin-detail':('18.png','Arcbőr és krém közeli részlete'),
 'care-guide':('5 másolata.png','Nyitott jegyzetfüzet szárított virágok mellett'),
 'facial-massage':('2.png','Nyugodt arcmasszázs meleg fényben'),
 'facial-care':('19.png','Kozmetikai arckezelés, gondoskodó érintés'),
 'care-products':('4 másolata.png','Bőrápolási termékek természetes bézs tónusokkal'),
 'mask-care':('1.png','Arcpakolás felvitele egy kozmetikai kezelés során'),
 'cream-texture':('6.png','Krém a kézfejen, közeli részlet'),
 'serum-drop':('6 másolata.png','Szérum cseppentése egy üvegbe'),
}
report={}
for slug,(filename,alt) in assets.items():
 with Image.open(root/'images'/filename) as original:
  image=ImageOps.exif_transpose(original).convert('RGB')
  difference=ImageChops.difference(image,Image.new('RGB',image.size,'white')).convert('L')
  bbox=difference.point(lambda p:255 if p>12 else 0).getbbox()
  assert bbox, filename
  image=image.crop(bbox)
  image.thumbnail((1600,1600),Image.Resampling.LANCZOS)
  variants=[]
  for width in [image.width,800,480]:
   if width>image.width or any(v['width']==width for v in variants):continue
   resized=image.resize((width,round(image.height*width/image.width)),Image.Resampling.LANCZOS)
   suffix='' if width==image.width else f'-{width}w'
   file=out/f'{slug}{suffix}.webp'
   resized.save(file,'WEBP',quality=86,method=6)
   variants.append({'path':file.relative_to(root).as_posix(),'width':width,'height':resized.height})
  report[slug]={'source':filename,'crop':bbox,'alt':alt,'variants':variants}

def replacement(tag,slug,sizes):
 data=report[slug]; big=data['variants'][0]
 tag=re.sub(r'\s(?:src|alt|width|height|srcset|sizes|decoding)="[^"]*"','',tag)
 srcset=', '.join(f"{v['path']} {v['width']}w" for v in reversed(data['variants']))
 return tag[:-1]+f' src="{big["path"]}" srcset="{srcset}" sizes="{sizes}" width="{big["width"]}" height="{big["height"]}" alt="{escape(data["alt"])}" decoding="async">'

directions=[('koncepcio-1-csendes-enido.html',[
 ('relaxing-facial','(max-width: 760px) calc(100vw - 52px), 568px'),
 ('facial-device','(max-width: 760px) calc(100vw - 40px), 360px'),
 ('serum','(max-width: 760px) calc(100vw - 64px), 552px'),
 ('care-collection','(max-width: 760px) calc(100vw - 40px), 470px'),
 ('mask-treatment','(max-width: 420px) calc(100vw - 40px), (max-width: 760px) 45vw, 650px'),
 ('skin-detail','(max-width: 420px) calc(100vw - 40px), (max-width: 760px) 45vw, 486px'),
 ('care-guide','(max-width: 760px) calc(100vw - 88px), 470px')]),
 ('koncepcio-2-a-gondoskodas-tere.html',[
 ('facial-massage','calc(100vw - 40px)'),
 ('facial-care','(max-width: 800px) calc(100vw - 40px), 1200px'),
 ('care-products','(max-width: 800px) calc(100vw - 40px), 560px'),
 ('mask-care','(max-width: 480px) calc(100vw - 40px), (max-width: 800px) 55vw, 696px'),
 ('cream-texture','(max-width: 480px) calc(100vw - 40px), (max-width: 800px) 40vw, 464px'),
 ('serum-drop','(max-width: 800px) calc(100vw - 88px), 500px')])]
for filename,choices in directions:
 p=root/filename;s=p.read_text(encoding='utf-8');index=0
 def swap(match):
  global index
  tag=match.group()
  if 'src="images/' not in tag:return tag
  slug,sizes=choices[index];index+=1
  return replacement(tag,slug,sizes)
 s=re.sub(r'<img\b[^>]*>',swap,s)
 assert index==len(choices),(filename,index)
 # The layout already uses object-fit; tune the focal points for the new photos.
 if filename.startswith('koncepcio-1'):
  css='.hero-photo{object-position:52% center}.service-photo img{object-position:center}.detail-photo{object-position:center}.about-photo{object-position:center}.photo-grid figure:nth-child(2) img{object-position:center 42%}.newsletter-photo{object-position:center}'
 else:
  css='.hero-photo{object-position:66% center}.process-photo{object-position:center 48%}.treatment-visual img{object-position:center}.image-pair figure:nth-child(2) img{object-position:center 48%}.newsletter-still{object-position:center 46%}@media(max-width:800px){.hero-photo{object-position:55% center}}'
 s=s.replace('</style>','\n/* A feltöltött fotókhoz igazított fókuszpontok. */\n'+css+'\n</style>',1)
 s=s.replace('Apró részletek, nyugodt pillanatok. Hangulatfotók.','Apró részletek, személyre szabott ápolás.')
 p.write_text(s,encoding='utf-8')
(root/'.webprojekt/website-images.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('13 feltöltött kép, két frissített mintaoldal. A harmadik változatlan.')
