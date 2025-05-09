import cv2
import sys
import os
import subprocess

# Überprüfen und Installieren der erforderlichen Bibliotheken
try:
    from ultralytics import YOLO
except ImportError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'ultralytics'])
    from ultralytics import YOLO

def predict_and_save(image_path, output_dir):
    # Überprüfen, ob das Bild existiert
    if not os.path.exists(image_path):
        print(f"Fehler: Das Bild {image_path} existiert nicht.")
        return
    
    # Falls der Ausgabeordner nicht existiert, erstellen
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Modell laden (das Modell muss sich im aktuellen Verzeichnis befinden)
    model = YOLO('./best.pt')
    results = model(image_path)
    detections = results[0].boxes
    
    # Extrahieren der Bounding-Box-Koordinaten, Klassen und Konfidenzwerte
    boxes = detections.xyxy
    classes = detections.cls
    scores = detections.conf
    
    # Originalbild laden
    image = cv2.imread(image_path)
    colors = {0: (255, 0, 0), 1: (0, 255, 0)}  # Blau für "edge", Grün für "node"
    
    # Zeichnen der Bounding-Boxen mit Beschriftung
    for box, cls, score in zip(boxes, classes, scores):
        x_min, y_min, x_max, y_max = map(int, box)
        if cls == 1 or (cls == 0 and score >= 0.5):
            label = f"{'edge' if cls == 0 else 'node'} {score:.2f}"
            cv2.rectangle(image, (x_min, y_min), (x_max, y_max), colors[int(cls)], 2)
            cv2.putText(image, label, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, colors[int(cls)], 2)
    
    # Speichern des Bildes mit den Bounding-Boxen
    base_name, ext = os.path.splitext(os.path.basename(image_path))
    output_filename = f"{base_name}_detections{ext}"
    output_path = os.path.join(output_dir, output_filename)
    cv2.imwrite(output_path, image)
    print(f"Bild gespeichert unter: {output_path}")

# Hauptfunktion zur Befehlszeilenausführung
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Verwendung: python predict.py <bildpfad> <ausgabeordner>")
    else:
        image_path = sys.argv[1]
        output_dir = sys.argv[2]
        predict_and_save(image_path, output_dir)
