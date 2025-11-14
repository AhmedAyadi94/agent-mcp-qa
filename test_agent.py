#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour l'Agent MCP QA
Ce fichier permet de tester toutes les fonctionnalites de l'agent
"""

import os
import sys
from datetime import datetime

def print_header(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def test_imports():
    print_header("Test 1: Verification des imports")
    try:
        from modules.generator import generate_selenium_script, generate_appium_script
        from modules.analyzer import parse_junit_xml, detect_anomalies
        from modules.reporter import generate_html_report, generate_text_report
        from modules.ci_cd_connector import JenkinsConnector, GitLabConnector
        from modules.jira_connector import JiraConnector
        print("✅ Tous les modules sont importes avec succes")
        return True
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        return False

def test_generator():
    print_header("Test 2: Generation de scripts de test")
    try:
        from modules.generator import generate_selenium_script
        
        print("\n📝 Generation d'un script Selenium...")
        description = "Script pour tester la connexion a LinkedIn"
        script = generate_selenium_script(description)
        
        if script and len(script) > 50:
            print(f"✅ Script genere: {len(script)} caracteres")
            print(f"   Apercu: {script[:100]}...")
            
            os.makedirs('generated_scripts', exist_ok=True)
            filename = 'generated_scripts/test_linkedin.py'
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(script)
            print(f"   Fichier sauvegarde: {filename}")
            return True
        else:
            print("❌ Script genere invalide ou trop court")
            return False
    except Exception as e:
        print(f"❌ Erreur lors de la generation: {e}")
        return False

def test_analyzer():
    print_header("Test 3: Analyse de rapports")
    try:
        from modules.analyzer import detect_anomalies
        
        print("\n🔍 Test de detection d'anomalies...")
        
        # Test avec stats normales
        normal_stats = {
            'total_tests': 100,
            'success_rate': 0.95,
            'failures': 5,
            'errors': 0,
            'skipped': 0,
            'time': 120.5
        }
        anomalies_normal = detect_anomalies(normal_stats)
        print(f"   Stats normales: {len(anomalies_normal)} anomalie(s) detectee(s)")
        
        # Test avec stats anormales
        bad_stats = {
            'total_tests': 100,
            'success_rate': 0.45,
            'failures': 55,
            'errors': 0,
            'skipped': 0,
            'time': 500.0
        }
        anomalies_bad = detect_anomalies(bad_stats)
        print(f"   Stats anormales: {len(anomalies_bad)} anomalie(s) detectee(s)")
        
        if len(anomalies_bad) > len(anomalies_normal):
            print("✅ Detection d'anomalies fonctionnelle")
            for anomaly in anomalies_bad:
                print(f"      - {anomaly}")
            return True
        else:
            print("❌ Detection d'anomalies non fonctionnelle")
            return False
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse: {e}")
        return False

def test_reporter():
    print_header("Test 4: Generation de rapports")
    try:
        from modules.reporter import generate_html_report, generate_text_report
        
        print("\n📊 Generation de rapports...")
        
        stats = {
            'total_tests': 100,
            'success_rate': 0.92,
            'failures': 6,
            'errors': 2,
            'skipped': 0,
            'time': 145.3
        }
        
        # Generer rapport HTML
        html_path = generate_html_report(stats, output_path="reports/test_report.html")
        if os.path.exists(html_path):
            print(f"✅ Rapport HTML genere: {html_path}")
            html_success = True
        else:
            print(f"❌ Echec generation rapport HTML")
            html_success = False
        
        # Generer rapport texte
        text_path = generate_text_report(stats, output_path="reports/test_report.txt")
        if os.path.exists(text_path):
            print(f"✅ Rapport texte genere: {text_path}")
            text_success = True
        else:
            print(f"❌ Echec generation rapport texte")
            text_success = False
        
        return html_success and text_success
    except Exception as e:
        print(f"❌ Erreur lors de la generation de rapports: {e}")
        return False

def test_connectors():
    print_header("Test 5: Verification des connecteurs")
    try:
        from modules.ci_cd_connector import JenkinsConnector, GitLabConnector
        from modules.jira_connector import JiraConnector
        
        print("\n🔌 Verification des classes de connecteurs...")
        
        # Test Jenkins
        jenkins = JenkinsConnector(
            base_url="http://localhost:8080",
            username="test",
            api_token="token"
        )
        print("   ✅ JenkinsConnector initialise")
        
        # Test GitLab
        gitlab = GitLabConnector(
            base_url="https://gitlab.com",
            private_token="token"
        )
        print("   ✅ GitLabConnector initialise")
        
        # Test Jira
        jira = JiraConnector(
            base_url="https://example.atlassian.net",
            email="test@example.com",
            api_token="token"
        )
        print("   ✅ JiraConnector initialise")
        
        print("\n✅ Tous les connecteurs sont operationnels")
        print("   Note: Tests reels necessitent des credentials valides")
        return True
    except Exception as e:
        print(f"❌ Erreur lors du test des connecteurs: {e}")
        return False

def run_all_tests():
    print("\n" + "#"*60)
    print("#  AGENT MCP QA - SUITE DE TESTS")
    print(f"#  Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("#"*60)
    
    results = {}
    
    results['imports'] = test_imports()
    results['generator'] = test_generator()
    results['analyzer'] = test_analyzer()
    results['reporter'] = test_reporter()
    results['connectors'] = test_connectors()
    
    # Resume
    print_header("RESUME DES TESTS")
    total = len(results)
    passed = sum(results.values())
    
    print(f"\nTests executes: {total}")
    print(f"Tests reussis:  {passed}")
    print(f"Tests echoues:  {total - passed}")
    print(f"\nTaux de reussite: {(passed/total)*100:.1f}%\n")
    
    if passed == total:
        print("🎉 TOUS LES TESTS SONT PASSES! 🎉\n")
        return 0
    else:
        print("⚠️  CERTAINS TESTS ONT ECHOUE\n")
        return 1

if __name__ == "__main__":
    sys.exit(run_all_tests())
