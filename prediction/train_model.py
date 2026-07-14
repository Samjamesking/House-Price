import os
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def train_and_evaluate():
    print("Starting model training and evaluation pipeline...")
    
    # 1. Load dataset
    train_path = os.path.join('datasets', 'train.csv')
    if not os.path.exists(train_path):
        raise FileNotFoundError(f"Training dataset not found at {train_path}. Make sure it is placed in datasets/train.csv")
    
    df = pd.read_csv(train_path)
    print(f"Dataset loaded successfully. Shape: {df.shape}")
    
    # 2. Outlier Handling
    # Deleting outliers recommended by dataset author (GrLivArea > 4000 and SalePrice < 300000)
    outliers = df[(df['GrLivArea'] > 4000) & (df['SalePrice'] < 300000)]
    print(f"Identified {len(outliers)} outliers based on Living Area vs SalePrice. Dropping them.")
    df = df.drop(outliers.index).reset_index(drop=True)
    
    # 3. Feature Engineering
    # Combine FullBath and HalfBath into a single Bathrooms column
    df['Bathrooms'] = df['FullBath'] + 0.5 * df['HalfBath']
    
    # Define features and target
    target = 'SalePrice'
    features = [
        'OverallQual', 'GrLivArea', 'BedroomAbvGr', 'Bathrooms',
        'GarageCars', 'YearBuilt', 'TotRmsAbvGrd', 'LotArea',
        'Neighborhood', 'OverallCond', 'TotalBsmtSF', 'GarageArea', 'Fireplaces'
    ]
    
    X = df[features]
    y = df[target]
    
    # 4. Preprocessing Pipeline
    numeric_features = [
        'OverallQual', 'GrLivArea', 'BedroomAbvGr', 'Bathrooms',
        'GarageCars', 'YearBuilt', 'TotRmsAbvGrd', 'LotArea',
        'OverallCond', 'TotalBsmtSF', 'GarageArea', 'Fireplaces'
    ]
    categorical_features = ['Neighborhood']
    
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])
    
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ])
    
    # 5. Split train/test
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f"Train set size: {X_train.shape[0]}, Validation set size: {X_val.shape[0]}")
    
    # 6. Define candidate models
    models = {
        'Linear Regression': LinearRegression(),
        'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
        'Gradient Boosting': GradientBoostingRegressor(n_estimators=100, learning_rate=0.08, max_depth=4, random_state=42),
        'XGBoost': XGBRegressor(n_estimators=100, learning_rate=0.08, max_depth=6, random_state=42)
    }
    
    results = {}
    best_r2 = -float('inf')
    best_model_name = None
    best_pipeline = None
    
    # Evaluate each model
    for name, model in models.items():
        pipeline = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('regressor', model)
        ])
        
        # Fit
        pipeline.fit(X_train, y_train)
        
        # Predict
        preds = pipeline.predict(X_val)
        
        # Evaluate
        mae = mean_absolute_error(y_val, preds)
        rmse = np.sqrt(mean_squared_error(y_val, preds))
        r2 = r2_score(y_val, preds)
        
        results[name] = {
            'MAE': mae,
            'RMSE': rmse,
            'R2': r2,
            'pipeline': pipeline
        }
        
        print(f"\nModel: {name}")
        print(f"  MAE:  ${mae:,.2f}")
        print(f"  RMSE: ${rmse:,.2f}")
        print(f"  R2:   {r2:.4f}")
        
        if r2 > best_r2:
            best_r2 = r2
            best_model_name = name
            best_pipeline = pipeline
            
    print(f"\n=========================================")
    print(f"Best Model Selected: {best_model_name} with R2: {best_r2:.4f}")
    print(f"=========================================")
    
    # Ensure saved_models directory exists
    os.makedirs('saved_models', exist_ok=True)
    
    # 7. Save the best pipeline and model metadata
    model_save_path = os.path.join('saved_models', 'house_price_model.pkl')
    
    # Save the pipeline
    joblib.dump(best_pipeline, model_save_path)
    print(f"Saved best model pipeline to {model_save_path}")
    
    # Save performance metadata text file for Django dashboard to read
    meta_path = os.path.join('saved_models', 'model_meta.joblib')
    metadata = {
        'model_name': best_model_name,
        'r2_score': best_r2,
        'mae': results[best_model_name]['MAE'],
        'rmse': results[best_model_name]['RMSE'],
        'all_models': {k: {'MAE': v['MAE'], 'RMSE': v['RMSE'], 'R2': v['R2']} for k, v in results.items()}
    }
    joblib.dump(metadata, meta_path)
    print(f"Saved model metadata to {meta_path}")
    
    return metadata

if __name__ == '__main__':
    train_and_evaluate()
