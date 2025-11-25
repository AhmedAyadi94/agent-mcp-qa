import sys
import os
from pathlib import Path

sys.path.append(str(Path(__file__).parent / 'modules'))

def main():
    print("="*60)
    print("    Agent MCP QA - Assistant IA pour Ingénieurs QA")
    print("="*60)
    print("\nFonctionnalités disponibles:")
    print("1. Générer un script de test (Selenium/Appium/Postman)")
    print("2. Analyser un rapport de test")
    print("3. Générer un rapport synthétique")
    print("4. Intégration CI/CD (Jenkins/GitLab)")
    print("5. Créer un ticket Jira")
    print("6. Quitter")
    print("="*60)
    
    choix = input("\nChoisissez une option (1-6): ")
    
    if choix == "1":
        print("\n[Module Générateur de Tests]")
        framework = input("Framework (selenium/appium/postman): ")
        description = input("Décrivez le test à générer: ")
        print(f"\nGénération d'un script {framework}...")
        print("TODO: Implémenter modules/generator.py")
    
    elif choix == "2":
        print("\n[Module Analyseur de Rapports]")
        rapport_path = input("Chemin vers le rapport (XML/JSON): ")
        print(f"\nAnalyse de {rapport_path}...")
        print("TODO: Implémenter modules/analyzer.py")
    
    elif choix == "3":
        print("\n[Module Reporting]")
        print("Génération du rapport synthétique...")
        print("TODO: Implémenter modules/reporter.py")
    
    elif choix == "4":
        print("\n[Module CI/CD]")
        plateforme = input("Plateforme (jenkins/gitlab): ")
        print(f"\nConnexion à {plateforme}...")
        print("TODO: Implémenter modules/ci_cd_connector.py")
    
    elif choix == "5":
        print("\n[Module Jira]")
        titre = input("Titre du ticket: ")
        description = input("Description: ")
        print(f"\nCréation du ticket '{titre}'...")
        print("TODO: Implémenter modules/jira_connector.py")
    
    elif choix == "6":
        print("\nAu revoir!")
        sys.exit(0)
    
    else:
        print("\nOption invalide!")

if __name__ == "__main__":
    main()
