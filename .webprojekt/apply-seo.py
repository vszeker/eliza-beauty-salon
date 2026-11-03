from pathlib import Path
from PIL import Image,ImageOps
from html import escape,unescape
import re,json,shutil
root=Path(__file__).resolve().parent.parent
domain='https://elizaweboldal.netlify.app/'
title='Kozmetikai kezelések Budapesten | Eliza Beauty Salon'
description='Személyre szabott arckezelések, bőrfiatalítás és anti-akné ápolás Budapesten, a Ráday utcában. Ismerd meg az Eliza Beauty Salont, és kérj időpontot!'
image_path='images/website/social-preview.jpg'
with Image.open(root/'images/website/relaxing-facial.webp') as image:
    ImageOps.fit(image.convert('RGB'),(1200,630),Image.Resampling.LANCZOS,centering=(.5,.4)).save(root/image_path,'JPEG',quality=88,optimize=True)
shutil.copy2(root/image_path,root/'public'/image_path)
for relative in ['koncepcio-1-csendes-enido.html','public/index.html']:
    p=root/relative;s=p.read_text(encoding='utf-8')
    s=re.sub(r'<title>.*?</title>',f'<title>{title}</title>',s,count=1,flags=re.S)
    s=re.sub(r'<meta name="description"[^>]*>',f'<meta name="description" content="{escape(description)}">',s,count=1)
    s=re.sub(r'<!-- SEO START -->.*?<!-- SEO END -->\s*','',s,flags=re.S)
    faq=[]
    for question,answer in re.findall(r'<details><summary>(.*?)</summary><p>(.*?)</p></details>',s,re.S):
        clean=lambda x:unescape(re.sub('<[^>]+>','',x)).strip()
        faq.append({'@type':'Question','name':clean(question),'acceptedAnswer':{'@type':'Answer','text':clean(answer)}})
    schema=[{'@context':'https://schema.org','@type':'WebPage','@id':domain+'#webpage','url':domain,'name':title,'description':description,'inLanguage':'hu-HU','primaryImageOfPage':{'@type':'ImageObject','url':domain+image_path,'width':1200,'height':630},'about':{'@type':'BeautySalon','name':'Eliza Beauty Salon','description':'Személyre szabott kozmetikai kezelések bőrfiatalításra és problémás bőr ápolására.'}}, {'@context':'https://schema.org','@type':'FAQPage','@id':domain+'#gyik','mainEntity':faq}]
    meta={'og:title':title,'og:description':description,'og:image':domain+image_path,'og:image:width':'1200','og:image:height':'630','og:image:type':'image/jpeg','og:image:alt':'Relaxáló kozmetikai arckezelés','og:url':domain,'og:type':'website','og:locale':'hu_HU','og:site_name':'Eliza Beauty Salon'}
    block='<!-- SEO START -->\n<link rel="canonical" href="'+domain+'">\n'
    block+='\n'.join(f'<meta property="{k}" content="{escape(v)}">' for k,v in meta.items())
    block+='\n<meta name="twitter:card" content="summary_large_image">\n'+f'<meta name="twitter:title" content="{escape(title)}">\n<meta name="twitter:description" content="{escape(description)}">\n<meta name="twitter:image" content="{domain+image_path}">\n<meta name="twitter:image:alt" content="Relaxáló kozmetikai arckezelés">\n'
    block+='<!-- A tanfolyami minta-elérhetőségek szándékosan nem szerepelnek üzleti schema-adatként. -->\n'
    block+='<script type="application/ld+json">\n'+json.dumps(schema,ensure_ascii=False,indent=2)+'\n</script>\n<!-- SEO END -->\n'
    s=s.replace('</head>',block+'</head>',1)
    # All layout styles are inline custom CSS; no Tailwind utilities are used.
    s=re.sub(r'<script src="https://cdn.tailwindcss.com"></script>\s*<script>if\(window.tailwind\).*?</script>','',s,count=1,flags=re.S)
    p.write_text(s,encoding='utf-8')
(root/'public/robots.txt').write_text('User-agent: *\nAllow: /\n\nSitemap: '+domain+'sitemap.xml\n',encoding='utf-8')
(root/'public/sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n  <url><loc>'+domain+'</loc></url>\n</urlset>\n',encoding='utf-8')
print('SEO metaadatok, WebPage/FAQPage schema, megosztási kép, sitemap és robots elkészült.')
print('Title:',len(title),'karakter; description:',len(description),'karakter.')
