"""
Module Générateur de Scripts de Test
Ce module utilise l'IA (OpenAI) pour générer automatiquement des scripts de test
pour différents frameworks : Selenium, Appium, Postman, JUnit, TestNG, etc.
"""

import openai
import os

# Configuration OpenAI (utilisez une variable d'environnement pour la clé API)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY

def generate_selenium_test(description):
    """
    Génère un script de test Selenium Python à partir d'une description
    
    Args:
        description (str): Description du test à générer
        
    Returns:
        str: Code Python du script Selenium généré
    """
    if not OPENAI_API_KEY:
        return "# Erreur: Clé API OpenAI manquante. Définissez OPENAI_API_KEY dans vos variables d'environnement."
    
    prompt = f"""
Génère un script de test Selenium Python complet et fonctionnel pour le scénario suivant:
{description}

Le script doit :
- Utiliser selenium webdriver
- Inclure des imports nécessaires
- Gérer les exceptions
- Inclure des assertions
- Fermer proprement le navigateur
"""
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Tu es un expert en automatisation QA Selenium."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=800,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"# Erreur lors de la génération: {str(e)}"

def generate_appium_test(description):
    """
    Génère un script de test Appium Python pour mobile
    
    Args:
        description (str): Description du test mobile
        
    Returns:
        str: Code Python du script Appium
    """
    if not OPENAI_API_KEY:
        return "# Erreur: Clé API OpenAI manquante."
    
    prompt = f"""
Génère un script de test Appium Python pour application mobile:
{description}

Inclure:
- Configuration des capabilities
- Initialisation du driver Appium
- Actions de test
- Assertions
"""
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Tu es un expert en tests mobiles Appium."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=800
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"# Erreur: {str(e)}"

def generate_postman_test(description):
    """
    Génère une collection Postman pour tests d'API
    
    Args:
        description (str): Description du test API
        
    Returns:
        str: JSON de la collection Postman
    """
    if not OPENAI_API_KEY:
        return "# Erreur: Clé API OpenAI manquante."
    
    prompt = f"""
Génère une collection Postman (format JSON) pour tester:
{description}

Inclure:
- Requests avec méthodes HTTP appropriées
- Tests automatiques dans les scripts
- Variables d'environnement si nécessaire
"""
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Tu es un expert en tests d'API REST avec Postman."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"# Erreur: {str(e)}"

def save_test_script(script_content, filename, output_dir="generated_tests"):
    """
    Sauvegarde le script généré dans un fichier
    
    Args:
        script_content (str): Contenu du script
        filename (str): Nom du fichier de sortie
        output_dir (str): Répertoire de sortie
    """
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print(f"Script sauvegardé: {filepath}")
    return filepath
