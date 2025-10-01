# In train_model.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error,r2_score
import joblib

print("--- Starting Model Training ---")

# 1. Load the Dataset
print("Step 1: Loading data from training_data.csv...")
df = pd.read_csv('training_data_cleaned.csv')
print(f"Data loaded successfully. Shape: {df.shape}")

# 2. Define Features (X) and Target (y)
print("Step 2: Defining features and target...")
# The 'target_score' is what we want to predict.
y = df['target_score']
# All other columns are the features the model will learn from.
X = df.drop('target_score', axis=1)
print(f"Features defined. Number of features: {len(X.columns)}")

# 3. Split Data into Training and Testing Sets
print("Step 3: Splitting data into training and testing sets...")
# We'll use 80% of the data for training and 20% for testing.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print("Data split complete.")

# 4. Initialize and Train the Model
print("Step 4: Initializing and training the RandomForestRegressor model...")
# A RandomForest is a powerful and versatile model, great for this kind of data.
# n_estimators is the number of "trees" in the forest.
# random_state ensures we get the same result every time we run the script.
model = RandomForestRegressor(n_estimators=100, random_state=42)

# This is the actual training step.
model.fit(X_train, y_train)
print("Model training complete.")

# 5. Evaluate the Model (Optional, but good practice)
print("Step 5: Evaluating model performance on the test set...")
predictions = model.predict(X_test)
mae = mean_absolute_error(y_test, predictions)
print(f"Mean Absolute Error on test data: {mae:.2f}")
# This tells you, on average, how many "points" your model's prediction is off by. A low number is good.

# 6. Save the Trained Model to a File
print("Step 6: Saving the trained model to 'prepscore_ml_model.pkl'...")
# We use joblib to save the model. It's efficient for scikit-learn models.
joblib.dump(model, 'prepscore_ml_model.pkl')
print("--- Model saved successfully! ---")

# --- Feature Importance (Bonus Insight) ---
print("\n--- Feature Importances ---")
# Let's see which features the model found most important.
importances = model.feature_importances_
feature_names = X.columns
# Create a DataFrame for better visualization
feature_importance_df = pd.DataFrame({'feature': feature_names, 'importance': importances})
# Sort by importance
feature_importance_df = feature_importance_df.sort_values('importance', ascending=False).head(10)
print("Top 10 most important features:")
print(feature_importance_df)