import os
import sys
from PIL import Image, ImageEnhance
import numpy as np
from skimage import filters

def preprocess_images(input_directory, resize_images=True):
    # Überprüfen Sie, ob das Eingabeverzeichnis existiert
    if not os.path.isdir(input_directory):
        print(f"Das Verzeichnis {input_directory} ist nicht vorhanden.")
        return
    
    # Durchsuchen aller Dateien im Verzeichnis
    for image_file in os.listdir(input_directory):
        if image_file.lower().endswith(('.jpg', '.png')):  # Filterung von nur JPG-Dateien oder PNG-Dateien
            try:
                # Vollständiger Pfad des Bildes
                image_path = os.path.join(input_directory, image_file)

                # Laden des Bildes und Konvertieren in Graustufen
                image = Image.open(image_path).convert('L')

                # Kontrast erhöhen
                image = ImageEnhance.Contrast(image).enhance(2.0)

                #Konvertieren in ein NumPy-Array zum Filtern
                image_np = np.array(image)

                # Gaußsche Filterung mit scikit-image
                image_filtered = filters.gaussian(image_np, sigma=1)

                # Konvertierung in ein PIL-Bild nach der Filterung
                image_filtered_pil = Image.fromarray((image_filtered * 255).astype('uint8'))

                # Redimensionnement si nécessaire
                if resize_images:
                    image_filtered_pil = image_filtered_pil.resize((416, 416))

                # Speichern des Endergebnisses (ersetzt das Originalbild)
                image_filtered_pil.save(image_path)
                #print(f"Image bearbeitet und gespeichert : {image_path}")

            except Exception as e:
                print(f"Fehler bei der Bildvorverarbeitung {image_file}: {e}")

if __name__ == "__main__":
    # Vérifiez les arguments
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Benutzung : python image_preprocessing.py <Pfad_des_Verzeichnis> [resize]")
        print("  <Pfad_des_Verzeichnis> : Verzeichnis mit den Bildern")
        print("  [resize] : true (standardmäßig) oder false, gibt an, ob die Größe von Bildern geändert werden soll")
        sys.exit(1)
    
    # Verzeichnis mit den Bildern
    input_directory = sys.argv[1]
    
    # Bestimmen Sie, ob die Größe von Bildern geändert werden muss
    resize_flag = True  # Standardmäßig die Größe von Bildern ändern
    if len(sys.argv) == 3:
        resize_flag = sys.argv[2].lower() == "true"
    
    preprocess_images(input_directory, resize_images=resize_flag)
