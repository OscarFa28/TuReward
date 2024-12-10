import qrcode
import os
import io
from django.conf import settings
from PIL import Image, ImageDraw
from io import BytesIO
from django.core.files import File
from rest_framework.response import Response
from rest_framework import status

def generate_qr(folio):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(folio)
    qr.make(fit=True)
            
    qr_img = qr.make_image(fill='black', back_color='white').convert('RGB')

    logo_path_bottom = os.path.join(settings.BASE_DIR, 'publicPanel/static/publicPanel/img/qr_bottom_logo.png')
    try:
        logo_bottom = Image.open(logo_path_bottom)
    except FileNotFoundError:
        return None
    
    total_height = qr_img.size[1] + logo_bottom.size[1]
    new_img = Image.new('RGB', (qr_img.size[0], total_height), color=(255, 255, 255))
    new_img.paste(qr_img, (0, 0))
    new_img.paste(logo_bottom, ((new_img.size[0] - logo_bottom.size[0]) // 2, qr_img.size[1]))
    
    buffer = BytesIO()
    new_img.save(buffer, format='PNG')
    buffer.seek(0)

    return File(buffer, name=f'QR_code_{folio}.png')  
