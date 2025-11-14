# Module de generation de rapports de test
# Ce module genere des rapports HTML a partir des statistiques

import os
from datetime import datetime

def generate_html_report(stats, output_path="reports/test_report.html"):
    """
    Genere un rapport HTML a partir des statistiques de test
    
    Args:
        stats: Dictionnaire contenant les statistiques
        output_path: Chemin du fichier de sortie
    
    Returns:
        str: Chemin du fichier genere
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    html_content = f"""
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rapport de Tests - {datetime.now().strftime('%Y-%m-%d')}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            border-bottom: 3px solid #4CAF50;
            padding-bottom: 10px;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
            margin: 30px 0;
        }}
        .stat-card {{
            background: #f9f9f9;
            padding: 20px;
            border-radius: 5px;
            border-left: 4px solid #2196F3;
        }}
        .stat-label {{
            font-size: 14px;
            color: #666;
            margin-bottom: 5px;
        }}
        .stat-value {{
            font-size: 28px;
            font-weight: bold;
            color: #333;
        }}
        .success {{ border-left-color: #4CAF50; }}
        .failure {{ border-left-color: #f44336; }}
        .warning {{ border-left-color: #ff9800; }}
        .info {{ border-left-color: #2196F3; }}
        .footer {{
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            color: #666;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Rapport de Tests Automatises</h1>
        <p><strong>Date:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
        
        <div class="stats">
            <div class="stat-card info">
                <div class="stat-label">Tests Totaux</div>
                <div class="stat-value">{stats.get('total_tests', 0)}</div>
            </div>
            <div class="stat-card success">
                <div class="stat-label">Reussis</div>
                <div class="stat-value">{stats.get('total_tests', 0) - stats.get('failures', 0) - stats.get('errors', 0) - stats.get('skipped', 0)}</div>
            </div>
            <div class="stat-card failure">
                <div class="stat-label">Echecs</div>
                <div class="stat-value">{stats.get('failures', 0)}</div>
            </div>
            <div class="stat-card warning">
                <div class="stat-label">Erreurs</div>
                <div class="stat-value">{stats.get('errors', 0)}</div>
            </div>
        </div>
        
        <div class="stat-card info" style="margin-top: 20px;">
            <div class="stat-label">Taux de Reussite</div>
            <div class="stat-value">{stats.get('success_rate', 0):.1f}%</div>
        </div>
        
        <div class="footer">
            <p>Genere par Agent MCP QA</p>
        </div>
    </div>
</body>
</html>
    """
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Rapport genere: {output_path}")
    return output_path

def generate_text_report(stats, output_path="reports/test_report.txt"):
    """
    Genere un rapport texte simple
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    content = f"""
RAPPORT DE TESTS AUTOMATISES
Date: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

STATISTIQUES:
- Tests totaux: {stats.get('total_tests', 0)}
- Reussis: {stats.get('total_tests', 0) - stats.get('failures', 0) - stats.get('errors', 0) - stats.get('skipped', 0)}
- Echecs: {stats.get('failures', 0)}
- Erreurs: {stats.get('errors', 0)}
- Ignores: {stats.get('skipped', 0)}

Taux de reussite: {stats.get('success_rate', 0):.1f}%
Temps d'execution: {stats.get('time', 0):.2f}s
    """
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Rapport genere: {output_path}")
    return output_path
