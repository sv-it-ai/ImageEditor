import PySimpleGUI as sg
from PIL import Image, ImageFilter, ImageOps
from io import BytesIO

def update_image(original, blur, contrast, emboss, contour, flipx, flipy):
    image = original.convert("RGB")
    if blur:
        image = image.filter(ImageFilter.GaussianBlur(blur))
    if contrast:
        image = image.filter(ImageFilter.UnsharpMask(contrast))
    if emboss:
        image = image.filter(ImageFilter.EMBOSS)
    if contour:
        image = image.filter(ImageFilter.CONTOUR)
    if flipx:
        image = ImageOps.mirror(image)
    if flipy:
        image = ImageOps.flip(image)

    bio = BytesIO()
    image.save(bio, format="PNG")

    window["-IMAGE-"].update(data=bio.getvalue())
    return image

image_path = sg.popup_get_file("Open", no_window=True, file_types=(("Image files", "PNG GIF JPG JPEG"),))
layout = [
    [sg.Column([
        [sg.Frame("Blur", layout=[
            [sg.Slider(range=(1, 10), orientation="horizontal", key="-BLUR-")]
             ])],
        [sg.Frame("Contrast", layout=[
            [sg.Slider(range=(1, 10), orientation="horizontal", key="-CONTRAST-")]
             ])],
        [sg.Checkbox("Emboss", key="-EMBOSS-"), sg.Checkbox("Contour", key="-CONTOUR-")],
        [sg.Checkbox("Flip x", key="-FLIPX-"), sg.Checkbox("Flip y", key="-FLIPY-")],
        [sg.Button("Save Image", key="-SAVE-")]
    ]),
    sg.Column([
        [sg.Image( key="-IMAGE-")]
    ])]
]

original = Image.open(image_path)
window = sg.Window("Image Editor", layout)

while True:
    event, values = window.read(timeout=50)

    if event == sg.WINDOW_CLOSED:
        break

    image = update_image(original, *[values["-" + vname.upper().strip() + "-"] for vname in "blur, contrast, emboss, contour, flipx, flipy".split(",")])
    if event == "-SAVE-":
        file_path = sg.popup_get_file("Save as", save_as=True, no_window=True, file_types=(("files PNG", "png"),), default_extension="png")
        if file_path:
            image.save(file_path, format="PNG")
window.close()
