from pathlib import Path
from PIL import Image, ImageOps, ImageCms, features
import io, json

root = Path(__file__).resolve().parent.parent
source_dir = root/'images'
target_dir = source_dir/'optimized'
target_dir.mkdir(exist_ok=True)
assert features.check('webp'), 'A WebP kódoló nem elérhető.'
report=[]
for source in sorted(source_dir.iterdir()):
    if not source.is_file() or source.suffix.lower() not in {'.png','.jpg','.jpeg'}:
        continue
    with Image.open(source) as original:
        image=ImageOps.exif_transpose(original)
        # Convert embedded color profiles to sRGB before dropping metadata.
        profile=image.info.get('icc_profile')
        if profile:
            image=ImageCms.profileToProfile(image,ImageCms.ImageCmsProfile(io.BytesIO(profile)),ImageCms.createProfile('sRGB'),outputMode='RGBA' if 'A' in image.getbands() else 'RGB')
        else:
            image=image.convert('RGBA' if 'A' in image.getbands() else 'RGB')
        original_dimensions=image.size
        image.thumbnail((1600,1600),Image.Resampling.LANCZOS)
        variants=[]
        for width in [None,800,480]:
            if width is not None and width>=image.width:
                continue
            resized=image.copy()
            if width:
                resized=resized.resize((width,round(image.height*width/image.width)),Image.Resampling.LANCZOS)
            suffix=f'-{width}w' if width else ''
            destination=target_dir/f'{source.stem}{suffix}.webp'
            resized.save(destination,'WEBP',quality=84,method=6,exact=True)
            with Image.open(destination) as verify:
                verify.load()
                assert verify.size==resized.size
            variants.append({'file':str(destination.relative_to(root)).replace('\\','/'),'width':resized.width,'height':resized.height,'bytes':destination.stat().st_size})
        report.append({'source':str(source.relative_to(root)).replace('\\','/'),'original_width':original_dimensions[0],'original_height':original_dimensions[1],'original_bytes':source.stat().st_size,'variants':variants})
(root/'.webprojekt/image-optimization.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
before=sum(r['original_bytes'] for r in report)
after=sum(r['variants'][0]['bytes'] for r in report)
print(json.dumps({'sources':len(report),'webp_files':sum(len(r['variants']) for r in report),'original_bytes':before,'primary_webp_bytes':after,'primary_saving_percent':round(100*(1-after/before),1),'all_variants_bytes':sum(v['bytes'] for r in report for v in r['variants'])},indent=2))
