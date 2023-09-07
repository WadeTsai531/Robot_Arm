import os

path = 'pic/'
for num, image in enumerate(os.listdir(path)):
    os.rename(os.path.join(path, image),
              os.path.join(path, 'kaya_' + str(num) + '.jpg'))
