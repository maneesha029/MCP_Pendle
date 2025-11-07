import numpy as np
from pathlib import Path
import joblib

MODEL_DIR = Path("models")
MODEL_DIR.mkdir(exist_ok=True)

class PricePredictor:
    def __init__(self, model_file="models/price_predictor.joblib"):
        self.model_file=Path(model_file)
        self.model=None
    def load_or_train(self):
        if self.model_file.exists():
            self.model = joblib.load(self.model_file)
        else:
            from sklearn.ensemble import RandomForestRegressor
            X=np.random.rand(1000,31)
            y=np.random.rand(1000)
            m=RandomForestRegressor(n_estimators=50,random_state=42)
            m.fit(X,y)
            joblib.dump(m,self.model_file)
            self.model=m
    def predict(self,symbol,days_ahead=1,lookback_days=90):
        history = np.cumsum(np.random.randn(lookback_days)+1.0)
        feats = np.concatenate([[0],history[-30:]]).reshape(1,-1)
        pred=self.model.predict(feats)[0]
        return float(pred*(1+0.001*(days_ahead-1)))
