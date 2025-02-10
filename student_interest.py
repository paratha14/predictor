import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, StandardScaler
import joblib
df=pd.read_csv('student_interests_dataset.csv')
df.head()
categorical_columns = ['Club_joined_1', 'Club_joined_2', 'Club_joined_3', 'Activities_interested']
encoder = OneHotEncoder(handle_unknown='ignore')
encoded_features = encoder.fit_transform(df[categorical_columns]).toarray()



scaler = StandardScaler()
X_scaled = scaler.fit_transform(encoded_features)
print(X_scaled.shape)

from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=5, random_state=42)
kmeans.fit(X_scaled)
df['Cluster'] = kmeans.fit_predict(X_scaled)

def topClubs(cluster_group, n=3):
    return cluster_group.value_counts().index[:n].tolist()

df['Recommended_Clubs'] = df.groupby('Cluster')['Club_joined_1'].transform(lambda x: ', '.join(topClubs(x, 3)))
df.head()
# Save models
joblib.dump(kmeans, "kmeans_model.pkl")
joblib.dump(scaler, "scaler.pkl")
joblib.dump(encoder, "encoder.pkl")

print("✅ Model training complete. Files saved successfully!")

print(f"Encoder trained on {len(encoder.categories_)} categories.")
print(f"Scaler trained with {scaler.n_features_in_} features.")
