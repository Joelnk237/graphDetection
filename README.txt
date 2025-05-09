Das trainiertes Modell ist die Dateien best.pt gespeichert. Es muss immer bei Erkenunng , Entfernung von Knoten et Konstruktion des Graphen in Verzeichnis vorhanden sein

- Bildvorverarbeitung 
Wir haben ein Shell Skript geschrieben: prepare.sh
Bei der Ausführung des Shell muss man als Argument das Verzeichnis, wo sich die Bilder befinden, übergeben. Und dann werden alle JPG und PNG-Bildateien verarbeitet

Bsp: ./prepare.sh meineBilder/

- Graph Erkennung
Der Code hier zu verwenden ist predict.py
python predict.py <bildpfad> <ausgabeordner>

- Entfernung von Knoten
Der Code hier ist DeleteNodes.py
Verwendung: python deleteNodes.py <bildpfad> <ausgabeordner>

- Konstruktion der Graphen
Verwendung: python proceed.py <Pfad_zum_Bild> [eps]
[eps] ist Maximale Distanz zwischen zwei Punkten, damit sie als Teil desselben Clusters (Knotens) betrachtet werden

- Man kann auch unsere Implementierun auf JupyterLab ausführen lassen. Verwendung der Datei main.ipynb


