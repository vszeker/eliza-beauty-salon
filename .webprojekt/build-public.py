from pathlib import Path
import re, shutil, json
root=Path(__file__).resolve().parent.parent
target=root/'public'
assert not target.exists(), 'A public mappa már létezik.'
target.mkdir()
source=root/'koncepcio-1-csendes-enido.html'
html=source.read_text(encoding='utf-8')
html=re.sub(r'<a class="preview-back"[^>]*>.*?</a>','',html)
html=html.replace('Csendes énidő | Eliza Beauty Salon','Eliza Beauty Salon | Személyre szabott kozmetikai kezelések')
refs=set(re.findall(r'(?:src|href)="([^"#]+)"',html))
for value in re.findall(r'srcset="([^"]+)"',html):
    refs.update(part.strip().rsplit(' ',1)[0] for part in value.split(','))
refs.update(re.findall(r'url\([\"\']?([^\)\"\']+)',html))
copied=[]
for ref in sorted(refs):
    if re.match(r'^(?:https?:|mailto:|tel:|data:|#)',ref) or ref.startswith('var('):continue
    path=(root/ref).resolve()
    assert path.is_relative_to(root),ref
    assert path.is_file(),ref
    destination=target/ref
    destination.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(path,destination)
    copied.append(ref)
(target/'index.html').write_text(html,encoding='utf-8')
(root/'.webprojekt/deploy-manifest.json').write_text(json.dumps({'entry':'public/index.html','assets':copied,'note':'Prototípus bemutató űrlapokkal; az éles űrlap, PDF és végleges adatkezelés még hiányzik.'},ensure_ascii=False,indent=2),encoding='utf-8')
print(f'public/index.html és {len(copied)} szükséges asset előkészítve.')
