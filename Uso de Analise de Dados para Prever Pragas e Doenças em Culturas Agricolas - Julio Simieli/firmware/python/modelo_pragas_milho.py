# modelo_pragas_milho.py
"""Treino de modelo para previsão de risco de pragas na cultura do milho."""
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
from pathlib import Path

DATA_PATH = Path(__file__).parent.parent / "data" / "dados_milho_exemplo.csv"

def main():
    df = pd.read_csv(DATA_PATH)

    X = df[["temperatura", "umidade_ar", "umidade_solo"]]
    y = df["risco_praga"]

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=None,
        random_state=42
    )
    model.fit(X, y)

    # Salva modelo
    joblib.dump(model, "modelo_pragas_milho.pkl")

    # Previsão de exemplo
    sample = pd.DataFrame([[29.5, 85.0, 50.0]],
                          columns=["temperatura", "umidade_ar", "umidade_solo"])
    pred = model.predict(sample)[0]
    risco_str = "ALTO" if pred == 1 else "BAIXO"
    print(f"Risco de praga para a amostra: {risco_str}")

if __name__ == "__main__":
    main()