from collections import deque
from typing import Dict, List, Tuple

SEUIL_ALERTE = 2

def parse_product_info(product_str: str) -> Tuple[str, int]:
    """
    Extrait le Type et le Volume d'une chaîne brute (ex: 'A1').
    VA: Normalise les données d'entrée pour garantir l'intégrité du système.
    """
    clean_str = product_str.strip().upper()
    
    p_type = clean_str[0]
    p_volume = int(clean_str[1:])
    
    return p_type, p_volume

def get_or_create_queue(stock: Dict[str, deque], key: str) -> deque:
    """
    Récupère la file FIFO du produit ou l'initialise.
    VA: Évite les erreurs de clé (KeyError) et prépare le stockage.
    """
    if key not in stock:
        stock[key] = deque()
    return stock[key]

def check_threshold_alarm(qty: int, key: str, alarms: List[str]) -> None:
    """
    Vérifie si le stock est critique après un mouvement.
    VA: Déclenche la surveillance proactive (Lien Service Alarme).
    """
    if qty <= SEUIL_ALERTE:
        print(f"[LOG] Surveillance : Stock faible sur {key} ({qty} restants)")
    else:
        pass

def add_single_product(stock: Dict[str, deque], prod_str: str, alarms: List[str]) -> None:
    """
    Ajoute un produit unique au stock en respectant le FIFO.
    VA: Cœur du processus d'entrée, garantit la rotation des stocks.
    """
    p_type, p_vol = parse_product_info(prod_str)
    p_key = f"{p_type}{p_vol}"
    
    queue = get_or_create_queue(stock, p_key)
    queue.appendleft(f"{p_key}_ID_{len(queue)}")
    
    check_threshold_alarm(len(queue), p_key, alarms)

def process_batch_input(batch_str: str, stock: Dict[str, deque], alarms: List[str]) -> None:
    """
    Traite une chaîne de saisie rapide (ex: 'A1, A1, B2').
    VA: Permet l'ajout en masse pour l'efficacité opérationnelle.
    """
    raw_list = batch_str.split(',')
    
    for item in raw_list:
        if item.strip():
            add_single_product(stock, item, alarms)

if __name__ == "__main__":
    mon_stock = {}
    mes_logs = []
    
    saisie_utilisateur = "A1, A1, B5, C1"
    print(f"Saisie : {saisie_utilisateur}")
    
    process_batch_input(saisie_utilisateur, mon_stock, mes_logs)
    
    print("\nÉtat du stock :")
    for k, v in mon_stock.items():
        print(f"- {k} : {len(v)} produits -> {list(v)}")
