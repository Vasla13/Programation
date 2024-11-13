import time
import concurrent.futures
import requests

# Liste des URL des images à télécharger
img_urls = [
    'https://cdn.pixabay.com/photo/2016/04/04/14/12/monitor-1307227_1280.jpg',
    'https://cdn.pixabay.com/photo/2018/07/14/11/33/earth-3537401_1280.jpg',
    'https://cdn.pixabay.com/photo/2016/06/09/20/38/woman-1446557_1280.jpg',
]

def download_image(img_url):
    try:
        # Télécharger l'image
        img_bytes = requests.get(img_url).content
        # Générer le nom du fichier à partir de l'URL
        img_name = img_url.split('/')[-1]
        # Enregistrer l'image dans un fichier
        with open(img_name, 'wb') as img_file:
            img_file.write(img_bytes)
        print(f"{img_name} a été téléchargée")
    except Exception as e:
        print(f"Échec du téléchargement de {img_url} : {e}")

if __name__ == '__main__':
    start = time.perf_counter()
    # Utiliser ThreadPoolExecutor pour télécharger les images en parallèle
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(download_image, img_urls)
    end = time.perf_counter()
    print(f"Tâches terminées en {round(end - start, 2)} seconde(s)")
