"""
Module Analyseur de Rapports de Test
Ce module analyse les rapports de tests automatisés dans différents formats :
- JUnit XML
- JSON
- Allure
- TestNG
"""

import xml.etree.ElementTree as ET
import json
import os
from typing import Dict, List

def analyze_junit_xml(report_path: str) -> Dict:
    """
    Analyse un rapport JUnit XML et extrait les statistiques
    
    Args:
        report_path (str): Chemin vers le fichier XML
        
    Returns:
        Dict: Statistiques du rapport (tests, failures, errors, skipped, time)
    """
    try:
        tree = ET.parse(report_path)
        root = tree.getroot()
        
        stats = {
            "total_tests": int(root.attrib.get('tests', 0)),
            "failures": int(root.attrib.get('failures', 0)),
            "errors": int(root.attrib.get('errors', 0)),
            "skipped": int(root.attrib.get('skipped', 0)),
            "time": float(root.attrib.get('time', 0)),
            "test_cases": []
        }
        
        # Analyser chaque test case
        for testcase in root.findall('.//testcase'):
            case_info = {
                "name": testcase.attrib.get('name', 'Unknown'),
                "classname": testcase.attrib.get('classname', ''),
                "time": float(testcase.attrib.get('time', 0)),
                "status": "passed"
            }
            
            # Vérifier si le test a échoué
            if testcase.find('failure') is not None:
                case_info["status"] = "failed"
                failure = testcase.find('failure')
                case_info["failure_message"] = failure.attrib.get('message', '')
                case_info["failure_type"] = failure.attrib.get('type', '')
            
            # Vérifier si le test a des erreurs
            if testcase.find('error') is not None:
                case_info["status"] = "error"
                error = testcase.find('error')
                case_info["error_message"] = error.attrib.get('message', '')
            
            # Vérifier si le test a été skip
            if testcase.find('skipped') is not None:
                case_info["status"] = "skipped"
            
            stats["test_cases"].append(case_info)
        
        # Calculer le taux de réussite
        if stats["total_tests"] > 0:
            passed = stats["total_tests"] - stats["failures"] - stats["errors"] - stats["skipped"]
            stats["success_rate"] = (passed / stats["total_tests"]) * 100
        else:
            stats["success_rate"] = 0
        
        return stats
    
    except Exception as e:
        return {"error": f"Erreur lors de l'analyse du rapport JUnit: {str(e)}"}

def analyze_json_report(report_path: str) -> Dict:
    """
    Analyse un rapport JSON (format Postman, Newman, etc.)
    
    Args:
        report_path (str): Chemin vers le fichier JSON
        
    Returns:
        Dict: Statistiques du rapport
    """
    try:
        with open(report_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Support pour le format Newman/Postman
        if 'run' in data:
            stats = data['run'].get('stats', {})
            return {
                "total_tests": stats.get('tests', {}).get('total', 0),
                "failures": stats.get('tests', {}).get('failed', 0),
                "passed": stats.get('tests', {}).get('passed', 0),
                "skipped": stats.get('tests', {}).get('pending', 0),
                "assertions": stats.get('assertions', {}),
                "requests": stats.get('requests', {})
            }
        
        # Format JSON générique
        return data
    
    except Exception as e:
        return {"error": f"Erreur lors de l'analyse du rapport JSON: {str(e)}"}

def detect_anomalies(stats: Dict) -> List[str]:
    """
    Détecte les anomalies dans les résultats de test
    
    Args:
        stats (Dict): Statistiques du rapport
        
    Returns:
        List[str]: Liste des anomalies détectées
    """
    anomalies = []
    
    # Vérifier le taux de réussite
    if stats.get("success_rate", 100) < 80:
        anomalies.append(f"⚠️ Taux de réussite faible: {stats.get('success_rate', 0):.1f}%")
    
    # Vérifier les erreurs
    if stats.get("errors", 0) > 0:
        anomalies.append(f"❌ {stats['errors']} erreur(s) détectée(s)")
    
    # Vérifier les échecs
    if stats.get("failures", 0) > 0:
        anomalies.append(f"❌ {stats['failures']} test(s) échoué(s)")
    
    # Vérifier les tests ignorés
    if stats.get("skipped", 0) > stats.get("total_tests", 0) * 0.2:
        anomalies.append(f"⚠️ Trop de tests ignorés: {stats.get('skipped', 0)}")
    
    # Vérifier le temps d'exécution
    if stats.get("time", 0) > 300:  # Plus de 5 minutes
        anomalies.append(f"⏱️ Temps d'exécution long: {stats['time']:.2f}s")
    
    return anomalies

def generate_summary(stats: Dict) -> str:
    """
    Génère un résumé textuel des statistiques
    
    Args:
        stats (Dict): Statistiques du rapport
        
    Returns:
        str: Résumé formaté
    """
    summary = []
    summary.append("\n" + "="*60)
    summary.append("    RÉSUMÉ DES TESTS AUTOMATISÉS")
    summary.append("="*60)
    
    if "error" in stats:
        summary.append(f"\nErreur: {stats['error']}")
        return "\n".join(summary)
    
    summary.append(f"\nTests totaux     : {stats.get('total_tests', 0)}")
    summary.append(f"✅ Réussis          : {stats.get('total_tests', 0) - stats.get('failures', 0) - stats.get('errors', 0) - stats.get('skipped', 0)}")
    summary.append(f"❌ Échoués          : {stats.get('failures', 0)}")
    summary.append(f"⚠️ Erreurs          : {stats.get('errors', 0)}")
    summary.append(f"⏭️ Ignorés          : {stats.get('skipped', 0)}")
    summary.append(f"\nTaux de réussite : {stats.get('success_rate', 0):.1f}%")
    summary.append(f"Temps total      : {stats.get('time', 0):.2f}s")
    
    # Ajouter les anomalies
    anomalies = detect_anomalies(stats)
    if anomalies:
        summary.append("\n" + "="*60)
        summary.append("ANOMALIES DÉTECTÉES:")
        summary.append("="*60)
        for anomaly in anomalies:
            summary.append(f"  {anomaly}")
    
    summary.append("="*60 + "\n")
    
    return "\n".join(summary)

def analyze_report(report_path: str) -> Dict:
    """
    Fonction principale pour analyser un rapport (détecte le format automatiquement)
    
    Args:
        report_path (str): Chemin vers le fichier de rapport
        
    Returns:
        Dict: Statistiques et résumé
    """
    if not os.path.exists(report_path):
        return {"error": f"Fichier introuvable: {report_path}"}
    
    # Détecter le format
    if report_path.endswith('.xml'):
        stats = analyze_junit_xml(report_path)
    elif report_path.endswith('.json'):
        stats = analyze_json_report(report_path)
    else:
        return {"error": "Format de rapport non supporté. Utilisez .xml ou .json"}
    
    # Générer le résumé
    if "error" not in stats:
        stats["summary"] = generate_summary(stats)
        stats["anomalies"] = detect_anomalies(stats)
    
    return stats
