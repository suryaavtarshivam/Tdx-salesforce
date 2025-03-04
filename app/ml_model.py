import numpy as np
from sklearn.ensemble import RandomForestClassifier

class FraudDetectionModel:
    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self._train_initial_model()
    
    def _train_initial_model(self):
        # Training with dummy data for demonstration
        X = np.random.rand(1000, 4)  # 4 features
        # Generate synthetic fraud labels (0: normal, 1: fraud)
        y = (X[:, 0] * X[:, 1] + X[:, 2] - X[:, 3] > 1).astype(int)
        self.model.fit(X, y)
    
    def predict(self, features):
        try:
            # Make prediction
            fraud_score = self.model.predict_proba([features])[0][1]
            return {
                "fraud_score": float(fraud_score),
                "risk_level": self._get_risk_level(fraud_score),
                "flags": self._generate_flags(features, fraud_score)
            }
        except Exception as e:
            print(f"Prediction error: {str(e)}")
            return {"error": "Prediction failed"}

    @staticmethod
    def _get_risk_level(score):
        if score > 0.7:
            return "High"
        elif score > 0.3:
            return "Medium"
        return "Low"

    def _generate_flags(self, features, score):
        flags = []
        if score > 0.7:
            flags.append("High risk transaction detected")
        if features[0] > 10000:  # Amount threshold
            flags.append("Large transaction amount")
        if features[1] < 1:  # Number of items
            flags.append("Suspicious item count")
        return flags
