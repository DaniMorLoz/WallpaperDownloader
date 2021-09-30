from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import urllib3,re,os
from PIL import Image
import shutil
import sys

def Error(ExtraInfo):
    if not os.path.exists("WallpaperDownloaderError"):
        with open("C:\\Users\\dani\\Desktop\\WallpaperDownloaderError","w") as f:
            f.write("El script de los wallpapers no esta funcionando, echale un ojo.\n"+ExtraInfo)
    else:
        with open("C:\\Users\\dani\\Desktop\\WallpaperDownloaderError","a") as f:
            f.write("\n"+ExtraInfo)

out = open("D:\\Development\\AutoWallpaper\\out.txt","w")
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
if len(titles) == 0 or len(links) == 0:
    Error("Los titulos de las fotos o los enlaces no se han encontrado")

#  Create folder
if not os.path.isdir("D:\\Development\\AutoWallpaper\\Images"):
    out.write("Creando carpeta\n")
    os.mkdir("D:\\Development\\AutoWallpaper\\Images")
else:
    shutil.rmtree("D:\\Development\\AutoWallpaper\\Images")
    os.mkdir("D:\\Development\\AutoWallpaper\\Images")
    out.write("La carpeta se ha borrado y creado de nuevo\n")

# Download images
out.write("Descargando imagenes...\n")
for i,link in enumerate(links):
    url = 'https://www.pexels.com' +  link
    if titles[i][-1]  == "/":
        titles[i] = titles[i][:-1]
    with urllib3.PoolManager() as http:
        r = http.request('GET', url)
        with open("D:\\Development\\AutoWallpaper\\Images\\" + titles[i]+".jpg", 'wb') as fout:
            fout.write(r.data)

#  Remove vertical
out.write("Eliminando imagenes verticales...")
for image in os.listdir("D:\\Development\\AutoWallpaper\\Images"):
    im = Image.open("D:\\Development\\AutoWallpaper\\Images\\" + image)
    width, height = im.size
    if height  > width:
        os.remove("D:\\Development\\AutoWallpaper\\Images\\" +  image)

if len(os.listdir("D:\\Development\\AutoWallpaper\\Images")) == 0:
    Error("No se han descargado las imagenes correctamente.")