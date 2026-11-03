from pathlib import Path
from PIL import Image, ImageOps, ImageCms
import io,json
root=Path(__file__).resolve().parent.parent
manifest=root/'.webprojekt/image-optimization.json'
report=json.loads(manifest.read_text(encoding='utf-8'))
known={r['source'] for r in report}
added=[]
for source in sorted((root/'images').iterdir()):
    relative=source.relative_to(root).as_posix()
    if not source.is_file() or source.suffix.lower() not in {'.png','.jpg','.jpeg'} or relative in known:
        continue
    with Image.open(source) as original:
        image=ImageOps.exif_transpose(original)
        profile=image.info.get('icc_profile')
        if profile:
            image=ImageCms.profileToProfile(image,ImageCms.ImageCmsProfile(io.BytesIO(profile)),ImageCms.createProfile('sRGB'),outputMode='RGBA' if 'A' in image.getbands() else 'RGB')
        else:
            image=image.convert('RGBA' if 'A' in image.getbands() else 'RGB')
        dimensions=image.size
        image.thumbnail((1600,1600),Image.Resampling.LANCZOS)
        variants=[]
        for width in [None,800,480]:
            if width and width>=image.width:continue
            resized=image.copy() if width is None else image.resize((width,round(image.height*width/image.width)),Image.Resampling.LANCZOS)
            suffix=f'-{width}w' if width else ''
            output=root/'images/optimized'/f'{source.stem}{suffix}.webp'
            resized.save(output,'WEBP',quality=84,method=6,exact=True)
            with Image.open(output) as verify:
                verify.load()
                assert verify.size==resized.size
            variants.append({'file':output.relative_to(root).as_posix(),'width':resized.width,'height':resized.height,'bytes':output.stat().st_size})
        added.append({'source':relative,'original_width':dimensions[0],'original_height':dimensions[1],'original_bytes':source.stat().st_size,'variants':variants})
report.extend(added)
manifest.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(added,ensure_ascii=False,indent=2))
if added:
    before=sum(r['original_bytes'] for r in added);after=sum(r['variants'][0]['bytes'] for r in added)
    print(f'New originals: {before} bytes; primary WebP: {after} bytes; saving: {100*(1-after/before):.1f}%')
