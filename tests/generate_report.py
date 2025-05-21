import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from jinja2 import Environment, FileSystemLoader
import os

# 📥 Lecture du fichier JTL
jtl_file = "results.jtl"
df = pd.read_csv(jtl_file)

# 🧹 Nettoyage & conversions
df['timeStamp'] = pd.to_datetime(df['timeStamp'], unit='ms')
df['elapsed'] = df['elapsed'].astype(float)

# 📊 Statistiques
summary = {
    "Total samples": len(df),
    "Average response time (ms)": round(df["elapsed"].mean(), 2),
    "Median response time (ms)": round(df["elapsed"].median(), 2),
    "Max response time (ms)": round(df["elapsed"].max(), 2),
    "Min response time (ms)": round(df["elapsed"].min(), 2),
    "Success rate (%)": round(df['success'].mean() * 100, 2),
    "Error count": len(df[df['success'] == False])
}

# 📈 Générer un graphique de la performance dans le temps
sns.set(style="darkgrid")
plt.figure(figsize=(12, 6))
sns.lineplot(data=df, x="timeStamp", y="elapsed", hue="label", legend=False)
plt.title("Temps de réponse dans le temps")
plt.xlabel("Temps")
plt.ylabel("Durée (ms)")
plt.tight_layout()

graph_path = "response_times.png"
plt.savefig(graph_path)
plt.close()

# 📄 Préparer le template HTML
env = Environment(loader=FileSystemLoader("."))

template_str = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Rapport JMeter</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 2em; background: #f9f9f9; }
    h1 { color: #333; }
    table { border-collapse: collapse; width: 60%; margin: 1em 0; }
    th, td { border: 1px solid #ccc; padding: 0.5em; text-align: left; }
    th { background: #eee; }
    img { max-width: 100%; margin-top: 2em; }
  </style>
</head>
<body>
  <h1>🧪 Rapport de test JMeter</h1>
  <h2>📊 Statistiques principales</h2>
  <table>
    {% for key, value in summary.items() %}
      <tr><th>{{ key }}</th><td>{{ value }}</td></tr>
    {% endfor %}
  </table>
  <h2>📈 Temps de réponse dans le temps</h2>
  <img src="{{ graph_path }}" alt="Graphique des temps de réponse">
</body>
</html>
"""

template = env.from_string(template_str)
html_out = template.render(summary=summary, graph_path=graph_path)

# 💾 Sauvegarder le fichier HTML
output_file = "jmeter_custom_report.html"
with open(output_file, "w", encoding="utf-8") as f:
    f.write(html_out)

print(f"✅ Rapport généré : {output_file}")
