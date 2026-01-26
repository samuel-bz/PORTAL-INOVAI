import random
import string

random_secret = ''.join(random.choices(string.ascii_letters + string.digits, k=64))
allowed_hosts = '127.0.0.1,localhost'

with open('.env','w') as file:
    file.write(f'SECRET_KEY={random_secret}\n')
    file.write(f'ALLOWED_HOSTS={allowed_hosts}\n')
    file.write('DEBUG=True\n')
    print('Arquivo .env gerado!')
