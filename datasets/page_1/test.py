import pickle
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor

# Load df
df = pd.read_pickle("df.pkl")

# Add synthetic price column (in lakhs or crores)
df['price'] = np.random.uniform(50, 250, size=len(df))  # 50 lakhs to 2.5 crores

# Categorical and numerical features
categorical_cols = ['location', 'floor_category', 'luxury_category',
                    'furnishing_status', 'flooring_type', 'parking_space',
                    'age_of_property', 'balconies']  # Moved 'balconies' here

numerical_cols = ['bedrooms', 'bathrooms',
                  'built_up_area', 'storage_room', 'pooja_room']


# X and y
X = df.drop(columns=['price'])
y = np.log(df['price'])

# Preprocessing
preprocessor = ColumnTransformer(transformers=[
    ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols),
    ('num', StandardScaler(), numerical_cols)
])

# Full pipeline
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', XGBRegressor())
])

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
pipeline.fit(X_train, y_train)

# Save model
with open("xgbmodel.pkl", "wb") as f:
    pickle.dump(pipeline, f)

print("✅ Model trained and saved successfully with synthetic price data.")
