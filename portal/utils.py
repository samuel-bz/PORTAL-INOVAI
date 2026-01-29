import os

def upload_image_path(instance, filename):
    if os.path.exists(f'{filename}'):
       os.remove(f'{filename}')

    return f'{filename}'
    
    