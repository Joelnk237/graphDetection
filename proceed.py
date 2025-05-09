import os
import sys
import subprocess
import cv2
import numpy as np
from sklearn.cluster import DBSCAN
from graph import Graph, plot_graph
from houghLineDetect import proceed, find_hough_lines
from ultralytics import YOLO

def install_missing_packages():
    packages = ['numpy', 'opencv-python', 'matplotlib', 'scikit-learn', 'ultralytics']
    for package in packages:
        try:
            __import__(package)
        except ImportError:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

install_missing_packages()

def extract_edges_from_yolo(detections, class_edge=0, confidence_threshold=0.5):
    """
    Extrahiert Kanten aus den YOLO-Detektionen.
    """
    edges = []
    boxes = detections.xyxy.cpu().numpy()
    classes = detections.cls.cpu().numpy()
    scores = detections.conf.cpu().numpy()
    
    for box, cls, conf in zip(boxes, classes, scores):
        if cls == class_edge and conf >= confidence_threshold:
            edges.append(tuple(map(int, box[:4])))
    
    return edges

def process_edge_roi(img, roi):
    """
    Verarbeitet den Bereich der erkannten Kante.
    """
    x_min, y_min, x_max, y_max = roi
    roi_img = img[y_min:y_max, x_min:x_max]
    img_height = img.shape[0]
    (x1, y1), (x2, y2) = proceed(roi_img, roi)
    return (x1, img_height - y1), (x2, img_height - y2)

def reconstruct_nodes_and_edges(edges_detected, image, eps=80):
    """
    Rekonstruiert Knoten und Kanten aus den erkannten Kantenregionen.
    """
    points = []
    for roi in edges_detected:
        roi_points = process_edge_roi(image, roi)
        points.extend(roi_points)
    
    points = np.array(points)
    clustering = DBSCAN(eps=eps, min_samples=1).fit(points)
    node_labels = clustering.labels_
    
    nodes = {}
    for label in np.unique(node_labels):
        cluster_points = points[node_labels == label]
        cluster_center = cluster_points.mean(axis=0)
        nodes[label] = tuple(cluster_center)
    
    edges = []
    for roi in edges_detected:
        roi_points = process_edge_roi(image, roi)
        if len(roi_points) < 2:
            continue
        point1, point2 = roi_points[:2]
        node1 = clustering.labels_[np.argmin(np.linalg.norm(points - np.array(point1), axis=1))]
        node2 = clustering.labels_[np.argmin(np.linalg.norm(points - np.array(point2), axis=1))]
        edges.append((node1, node2))
    
    return nodes, edges

def main(image_path, eps=35):
    """
    Hauptfunktion zur Erkennung von Kanten und Knoten aus einem Bild.
    """
    if not os.path.exists(image_path):
        print(f"Fehler: Datei {image_path} nicht gefunden!")
        return
    
    image = cv2.imread(image_path)
    model = YOLO('./best.pt')
    test = model(image_path)
    detections = test[0].boxes
    
    edges_detected = extract_edges_from_yolo(detections, class_edge=0, confidence_threshold=0.4)
    nodes, edges = reconstruct_nodes_and_edges(edges_detected, image, eps)
    
    graphe = Graph()
    for node_id, (x, y) in nodes.items():
        graphe.add_node(node_id, x, y)
    for node1, node2 in edges:
        graphe.add_edge(node1, node2)
    
    print("Knoten:", graphe.nodes)
    print("Kanten:", graphe.edges)
    plot_graph(graphe, output_dir="./output")

if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Verwendung: python proceed.py <Pfad_zum_Bild> [eps]")
    else:
        image_path = sys.argv[1]
        eps = int(sys.argv[2]) if len(sys.argv) == 3 else 35
        main(image_path, eps)
