# Dataset

Este proyecto usa el **Sparkov Fraud Dataset** de Kaggle:
https://www.kaggle.com/datasets/kartik2112/fraud-detection

## Descarga manual

1. Descarga `fraudTrain.csv` (y opcionalmente `fraudTest.csv`) desde el link de arriba.
2. Colócalos en esta carpeta (`data/fraudTrain.csv`).
3. Corre `python ml/train.py`.

## Descarga vía Kaggle CLI (alternativa)

```bash
pip install kaggle
# colocar kaggle.json (API token) en ~/.kaggle/kaggle.json
kaggle datasets download -d kartik2112/fraud-detection -p data --unzip
```

Los CSV no se versionan en git (ver `.gitignore`) por tamaño.
