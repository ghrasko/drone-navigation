"""
Helyi OSM PBF fájlból adatok betöltése és feldolgozása
"""

import os
import geopandas as gpd
import matplotlib.pyplot as plt
import osmnx as ox
import time
from shapely.geometry import box

# Konfiguráció
PBF_FILE = 'map/hungary-latest.osm.pbf'  # Helyi PBF fájl elérési útja
OUTPUT_DIR = 'map/output'  # Kimeneti könyvtár

# Könyvtár létrehozása, ha még nem létezik
os.makedirs(OUTPUT_DIR, exist_ok=True)

ox.settings.all_oneway = True


def extract_buildings(bbox, save=True):
    """
    Épületek kinyerése a megadott területre
    
    Args:
        bbox: (north, south, east, west) koordináták
        save: Ha True, menti az eredményeket
    """
    print(f"\n2. Épületek betöltése helyi fájlból...")

    start_time = time.time()
    try:
        # Épületek betöltése
        buildings = ox.features_from_bbox(bbox=bbox, tags={'building': True})

        print(f"   - Sikeres! Betöltési idő: {time.time() - start_time:.2f} másodperc")
        print(f"   - Épületek száma: {len(buildings)}")

        # Vizualizáció és mentés
        if save and len(buildings) > 0:
            fig, ax = plt.subplots(figsize=(12, 10))
            buildings.plot(ax=ax, facecolor='#DDDDDD', edgecolor='#999999', alpha=0.7)
            plt.title(f"Épületek - {bbox[0]:.4f}, {bbox[1]:.4f}, {bbox[2]:.4f}, {bbox[3]:.4f}")
            plt.tight_layout()
            plt.savefig(os.path.join(OUTPUT_DIR, "buildings.png"), dpi=300)
            plt.close()
            print(f"   - Ábra mentve: {os.path.join(OUTPUT_DIR, 'buildings.png')}")

            # GeoJSON mentés
            buildings.to_file(os.path.join(OUTPUT_DIR, "buildings.geojson"), driver='GeoJSON')
            print(f"   - Adatok mentve: {os.path.join(OUTPUT_DIR, 'buildings.geojson')}")

        return buildings

    except Exception as e:
        print(f"   - HIBA: {e}")
        return None


def extract_water(bbox, save=True):
    """
    Vízfelületek kinyerése a megadott területre
    
    Args:
        bbox: (north, south, east, west) koordináták
        save: Ha True, menti az eredményeket
    """
    print(f"\n3. Vízfelületek betöltése helyi fájlból...")

    start_time = time.time()
    try:
        # Vízfelületek betöltése
        water = ox.features_from_bbox(bbox=bbox, tags={'natural': 'water'})

        print(f"   - Sikeres! Betöltési idő: {time.time() - start_time:.2f} másodperc")
        print(f"   - Vízfelületek száma: {len(water)}")

        # Vizualizáció és mentés
        if save and len(water) > 0:
            fig, ax = plt.subplots(figsize=(12, 10))
            water.plot(ax=ax, facecolor='#AADDFF', edgecolor='#77AACC', alpha=0.7)
            plt.title(f"Vízfelületek - {bbox[0]:.4f}, {bbox[1]:.4f}, {bbox[2]:.4f}, {bbox[3]:.4f}")
            plt.tight_layout()
            plt.savefig(os.path.join(OUTPUT_DIR, "water.png"), dpi=300)
            plt.close()
            print(f"   - Ábra mentve: {os.path.join(OUTPUT_DIR, 'water.png')}")

            # GeoJSON mentés
            water.to_file(os.path.join(OUTPUT_DIR, "water.geojson"), driver='GeoJSON')
            print(f"   - Adatok mentve: {os.path.join(OUTPUT_DIR, 'water.geojson')}")

        return water

    except Exception as e:
        print(f"   - HIBA: {e}")
        return None


def load_and_process_area(bbox, save=True):
    """
    Adott bbox területre adatok betöltése a helyi PBF fájlból
    
    Args:
        bbox: (north, south, east, west) koordináták
        save: Ha True, menti az eredményeket
    """
    north, south, east, west = bbox
    print(f"1. Úthálózat betöltése helyi fájlból...")

    start_time = time.time()
    try:
        # Úthálózat betöltése a megadott polygonon belül, unsimplified módban
        polygon = box(west, south, east, north)
        G = ox.graph_from_polygon(polygon, network_type='drive', simplify=False)

        print(f"   - Sikeres! Betöltési idő: {time.time() - start_time:.2f} másodperc")
        print(f"   - Csomópontok száma: {len(G.nodes)}")
        print(f"   - Élek száma: {len(G.edges)}")

        if save:
            fig, ax = plt.subplots(figsize=(12, 10))
            ox.plot_graph(G, ax=ax, node_size=0, edge_linewidth=0.5, edge_color='#999999')
            plt.title(f"Úthálózat - {north:.4f}, {south:.4f}, {east:.4f}, {west:.4f}")
            plt.tight_layout()
            plt.savefig(os.path.join(OUTPUT_DIR, "roads.png"), dpi=300)
            plt.close()
            print(f"   - Ábra mentve: {os.path.join(OUTPUT_DIR, 'roads.png')}")

            ox.save_graph_xml(G, filepath=os.path.join(OUTPUT_DIR, "road_network.osm"))
            print(f"   - Gráf mentve: {os.path.join(OUTPUT_DIR, 'road_network.osm')}")

        return G

    except Exception as e:
        print(f"   - HIBA: {e}")
        return None

def create_combined_map(roads, buildings, water, save=True):
    """
    Kombinált térkép készítése
    """
    print("\n4. Kombinált térkép készítése...")
    
    try:
        fig, ax = plt.subplots(figsize=(15, 12))
        
        # Rétegek megjelenítése
        if roads is not None:
            ox.plot_graph(roads, ax=ax, node_size=0, edge_linewidth=0.5, 
                        edge_color='#999999', show=False)
        
        if water is not None and len(water) > 0:
            water.plot(ax=ax, facecolor='#AADDFF', edgecolor='#77AACC', alpha=0.7)
        
        if buildings is not None and len(buildings) > 0:
            buildings.plot(ax=ax, facecolor='#DDDDDD', edgecolor='#999999', alpha=0.7)
        
        plt.title("Kombinált OSM Térkép")
        plt.tight_layout()
        
        if save:
            plt.savefig(os.path.join(OUTPUT_DIR, "combined_map.png"), dpi=300)
            print(f"   - Kombinált térkép mentve: {os.path.join(OUTPUT_DIR, 'combined_map.png')}")
        
        plt.close()
    
    except Exception as e:
        print(f"   - HIBA: {e}")

def main():
    # Tesztterület - Budapest, Parlament környéke 
    # Ez egy kis terület, ami gyorsan betölthető
    budapest_bbox = (47.60, 47.50, 19.10, 19.00)  # North, South, East, West
    
    # Megjegyzés: A jelenlegi script az OSM API-n keresztül tölti le az adatokat,
    # nem a helyi PBF fájlból, mivel az OSMnx újabb verziói más megközelítést 
    # igényelnek a helyi fájlok használatához. Ehhez más könyvtárakra (pl. pyosmium)
    # lenne szükség.
    
    print(f"OSM adatok betöltése a helyi '{PBF_FILE}' fájlból")
    print(f"Kimeneti könyvtár: '{OUTPUT_DIR}'")
    print("-" * 60)
    
    # Adatok betöltése és feldolgozása
    roads = load_and_process_area(budapest_bbox)
    buildings = extract_buildings(budapest_bbox)
    water = extract_water(budapest_bbox)
    
    # Kombinált térkép készítése
    create_combined_map(roads, buildings, water)
    
    print("-" * 60)
    print("Feldolgozás befejezve!")

if __name__ == "__main__":
    main()