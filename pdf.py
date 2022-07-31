#-*-coding:utf-8-*-

from PIL import Image

def imgs_to_pdf(img_id, down_id,lists):
    png_files = []
    sources = []
    for li in lists:
        for file in li:
            if 'png' in file or 'jpg' in file:
                png_files.append(img_id + file)
    output = Image.open(png_files[0])
    png_files.pop(0)
    for file in png_files:
        png_file = Image.open(file)
        if png_file.mode == "RGB":
            png_file = png_file.convert("RGB")
        sources.append(png_file)
    output.save(down_id, "pdf", save_all=True, append_images=sources)

def to_pdf(IMG_ID,DOWN_ID,LISTS):
    print("开始转换···")
    imgs_to_pdf(IMG_ID,f'pdf/{DOWN_ID}.pdf',LISTS)
    print('转换完毕！')