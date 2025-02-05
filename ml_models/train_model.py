import numpy as np
import joblib
from sklearn.linear_model import LinearRegression

# Mock training data
complexities = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]).reshape(-1, 1)
times = np.array([5, 8, 12, 18, 25, 35, 48, 60, 75, 90])  # Saat
costs = np.array([200, 400, 700, 1000, 1400, 1900, 2500, 3200, 4000, 4900])  # Maliyet

# Train models
time_model = LinearRegression().fit(complexities, times)
cost_model = LinearRegression().fit(complexities, costs)

# Save trained models
joblib.dump(time_model, 'ml_models/time_model.pkl')
joblib.dump(cost_model, 'ml_models/cost_model.pkl')

print("Models trained and saved successfully!")






