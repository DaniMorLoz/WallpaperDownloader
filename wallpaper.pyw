#pip install Pillow,selenium,webdriver-manager

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import urllib3,re,os
from PIL import Image
import shutil

folder = os.path.realpath(__file__).rsplit("\\",1)[0]+"\\"

# Chromedriver
out = open(folder + "out.txt","w")
out.write("Lanzando el chromedriver...\n")
chrome_options = Options()  
#chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)
driver.get("https://www.pexels.com/search/Wallpaper/")
data = driver.page_source
driver.close()
driver.quit()
out.write("Chromedriver terminado...\n")

# Get links and titles
out.write("Recopilando las fotos...\n")
title_key='<a class="js-photo-link photo-item__link".+href="/photo/(.+)"><img'
titles = re.findall(title_key, data)
links = []
for i in range(len(titles)):
    links.append("/photo/"+titles[i].split("-")[-1]+"download/")

out.write("Numero de fotos: "+str(len(titles))+"\n")

#  Create folder
if not os.path.isdir(folder + "Images"):
    out.write("Creando carpeta\n")
    os.mkdir(folder + "Images")
else:
    shutil.rmtree(folder + "Images")
    os.mkdir(folder + "Images")
    out.write("La carpeta se ha borrado y creado de nuevo\n")

# Download images
out.write("Descargando imagenes...\n")
for i,link in enumerate(links):
    url = 'https://www.pexels.com' +  link
    if titles[i][-1]  == "/":
        titles[i] = titles[i][:-1]
    with urllib3.PoolManager() as http:
        r = http.request('GET', url)
        with open(folder + "Images\\" + titles[i]+".jpg", 'wb') as fout:
            fout.write(r.data)

#  Remove vertical
out.write("Eliminando imagenes verticales...")
for image in os.listdir(folder + "Images"):
    im = Image.open(folder + "Images\\" + image)
    width, height = im.size
    if height  > width:
        os.remove(folder + "Images\\" +  image)