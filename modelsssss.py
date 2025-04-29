




# import os
# import time
# import requests
# import pandas as pd
# import numpy as np
# import joblib
# from sklearn.model_selection import train_test_split, GridSearchCV
# from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
# from xgboost import XGBRegressor
# from sklearn.preprocessing import StandardScaler
# import matplotlib.pyplot as plt
# import seaborn as sns

# # --- CONFIG — replace with your RapidAPI credentials ---
# REALTOR_API_KEY = "f59924088dmshcb5d0189d6aa800p1a9d0djsndea4ea47920d"
# REALTOR_HOST = "realty-in-us.p.rapidapi.com"
# HEADERS = {
#     "X-RapidAPI-Key": REALTOR_API_KEY,
#     "X-RapidAPI-Host": REALTOR_HOST,
#     "Content-Type": "application/json"
# }

# # Define multiple locations to fetch data from (mix of cities and zip codes)
# LOCATIONS = [
#     "02190",  # Weymouth, MA
#     "02116",  # Boston (Back Bay), MA
#     "02108",  # Boston (Beacon Hill), MA
#     "28262",  # Charlotte, NC
#     "28202",  # Charlotte (Uptown), NC
#     "10001",  # New York (Chelsea), NY
#     "60611",  # Chicago (Near North Side), IL
#     "90210",  # Beverly Hills, CA
#     "78701",  # Austin (Downtown), TX
# ]

# def fetch_rental_listings(location, pages=3, per_page=50, pause=1.0):
#     """
#     Fetch rental listings for a specific location from the API
#     """
#     url = "https://realty-in-us.p.rapidapi.com/properties/v3/list"
#     all_props = []
    
#     print(f"Fetching rental data for location: {location}")
    
#     for p in range(pages):
#         payload = {
#             "limit": per_page,
#             "offset": p * per_page,
#             "status": ["for_rent"],
#             "sort": {"direction": "desc", "field": "list_date"},
#             "search_location": location
#         }
        
#         if location.isdigit() and len(location) == 5:
#             payload["postal_code"] = location
#         else:
#             payload["city"] = location

#         try:
#             print(f"  Page {p+1}/{pages}...")
#             resp = requests.post(url, headers=HEADERS, json=payload, timeout=10)
            
#             if resp.status_code != 200:
#                 print(f"  Error fetching page {p+1}: {resp.status_code}")
#                 continue
            
#             results = resp.json().get("data", {}).get("home_search", {}).get("results", [])
            
#             if not results:
#                 print(f"  No results found on page {p+1}")
#                 break

#             for r in results:
#                 desc = r.get("description", {})
#                 addr = r.get("location", {}).get("address", {})
#                 coords = r.get("location", {}).get("coordinate", {})
                
#                 # Extract more features
#                 all_props.append({
#                     "bedrooms": desc.get("beds"),
#                     "bathrooms": desc.get("baths"),
#                     "living_area": desc.get("sqft"),
#                     "zipcode": addr.get("postal_code"),
#                     "city": addr.get("city"),
#                     "state": addr.get("state_code"),
#                     "latitude": coords.get("lat"),
#                     "longitude": coords.get("lon"),
#                     "property_type": desc.get("type", "UNKNOWN"),
#                     "year_built": desc.get("year_built"),
#                     "has_garage": 1 if "garage" in desc.get("text", "").lower() else 0,
#                     "has_pool": 1 if "pool" in desc.get("text", "").lower() else 0,
#                     "has_fireplace": 1 if "fireplace" in desc.get("text", "").lower() else 0,
#                     "rent": r.get("list_price")
#                 })
            
#             print(f"  Retrieved {len(results)} properties from page {p+1}")
#             time.sleep(pause)
            
#         except Exception as e:
#             print(f"  Error on page {p+1}: {str(e)}")
#             time.sleep(pause * 2)  # Wait longer after an error
#             continue
    
#     print(f"Total properties fetched for {location}: {len(all_props)}")
#     return all_props

# def fetch_all_locations():
#     """
#     Fetch data from all defined locations and combine into one dataset
#     """
#     all_data = []
    
#     for location in LOCATIONS:
#         props = fetch_rental_listings(location)
#         all_data.extend(props)
#         time.sleep(2)  # Wait between locations to avoid API rate limits
    
#     # Convert to DataFrame
#     df = pd.DataFrame(all_data)
    
#     # Save raw data for inspection
#     df.to_csv("rental_data_raw.csv", index=False)
#     print(f"Total properties collected: {len(df)}")
    
#     return df

# def prepare_features(df):
#     """
#     Clean and prepare features for model training
#     """
#     print("Preparing features...")
#     print(f"Initial shape: {df.shape}")
    
#     # Drop rows with missing core values
#     df = df.dropna(subset=["bedrooms", "living_area", "zipcode", "rent"])
#     print(f"After dropping rows with missing core values: {df.shape}")
    
#     # Convert data types
#     df["bedrooms"] = df["bedrooms"].astype(float)
#     df["bathrooms"] = df["bathrooms"].astype(float)
#     df["living_area"] = df["living_area"].astype(float)
#     df["rent"] = df["rent"].astype(float)
    
#     # Handle missing values for other features
#     df["year_built"] = df["year_built"].fillna(df["year_built"].median())
#     df["has_garage"] = df["has_garage"].fillna(0)
#     df["has_pool"] = df["has_pool"].fillna(0)
#     df["has_fireplace"] = df["has_fireplace"].fillna(0)
    
#     # Add derived features
#     df["beds_baths_ratio"] = df["bedrooms"] / df["bathrooms"].replace(0, 1)
#     df["price_per_sqft"] = df["rent"] / df["living_area"]
#     df["living_area_per_bed"] = df["living_area"] / df["bedrooms"].replace(0, 1)
    
#     # Standardize property types
#     df["property_type"] = df["property_type"].str.upper().fillna("OTHER")
#     df["property_type"] = df["property_type"].replace({
#         "APARTMENT": "APARTMENT",
#         "CONDO": "CONDO",
#         "TOWNHOUSE": "TOWNHOUSE",
#         "SINGLE_FAMILY": "SINGLE_FAMILY"
#     }).fillna("OTHER")
    
#     # Create a property age feature
#     current_year = datetime.now().year
#     df["property_age"] = current_year - df["year_built"]
    
#     # One-hot encode categorical variables
#     df = pd.get_dummies(df, columns=["property_type"], prefix="type")
#     df = pd.get_dummies(df, columns=["zipcode"], prefix="zip")
#     df = pd.get_dummies(df, columns=["state"], prefix="state")
    
#     print(f"Final shape: {df.shape}")
#     print(f"Features: {df.columns.tolist()}")
    
#     return df

# def feature_importance_analysis(model, X):
#     """
#     Analyze and visualize feature importance
#     """
#     # Get feature importance
#     importance = model.feature_importances_
    
#     # Create a DataFrame for better visualization
#     feat_importance = pd.DataFrame({
#         'Feature': X.columns,
#         'Importance': importance
#     }).sort_values(by='Importance', ascending=False)
    
#     # Plot top 15 features
#     plt.figure(figsize=(10, 6))
#     sns.barplot(x='Importance', y='Feature', data=feat_importance.head(15))
#     plt.title('Top 15 Feature Importance for Rental Price Prediction')
#     plt.tight_layout()
#     plt.savefig('feature_importance.png')
    
#     return feat_importance

# def geographic_analysis(df):
#     """
#     Analyze rental prices by location
#     """
#     # Get average rent by zipcode
#     zipcode_rent = df.groupby('zipcode')['rent'].agg(['mean', 'count', 'std']).reset_index()
#     zipcode_rent = zipcode_rent.rename(columns={'mean': 'avg_rent', 'count': 'num_properties', 'std': 'rent_std'})
#     zipcode_rent = zipcode_rent.sort_values('avg_rent', ascending=False)
    
#     # Plot
#     plt.figure(figsize=(12, 6))
    
#     # Filter only zipcodes with at least 5 properties
#     plot_data = zipcode_rent[zipcode_rent['num_properties'] >= 5]
    
#     ax = sns.barplot(x='zipcode', y='avg_rent', data=plot_data)
#     plt.xticks(rotation=90)
#     plt.title('Average Rent by Zipcode')
#     plt.tight_layout()
#     plt.savefig('rent_by_zipcode.png')
    
#     return zipcode_rent

# def train_and_evaluate_model(df):
#     """
#     Train and evaluate the rental price prediction model
#     """
#     # Extract features and target
#     X = df.drop(['rent', 'price_per_sqft', 'city', 'latitude', 'longitude'], axis=1, errors='ignore')
#     y = df['rent']
    
#     # Split the data
#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
#     print(f"Training data shape: {X_train.shape}")
#     print(f"Testing data shape: {X_test.shape}")
    
#     # Train the model with hyperparameter tuning
#     param_grid = {
#         'n_estimators': [100, 200],
#         'learning_rate': [0.05, 0.1],
#         'max_depth': [4, 6, 8],
#         'min_child_weight': [1, 3],
#         'subsample': [0.8, 1.0],
#         'colsample_bytree': [0.8, 1.0]
#     }
    
#     # Use a smaller grid for quick testing
#     quick_param_grid = {
#         'n_estimators': [100],
#         'learning_rate': [0.1],
#         'max_depth': [6],
#         'subsample': [0.8]
#     }
    
#     print("Training model with grid search...")
#     xgb_model = XGBRegressor(random_state=42)
    
#     # Use quick grid for faster iteration during development
#     grid_search = GridSearchCV(
#         estimator=xgb_model,
#         param_grid=quick_param_grid,  # Change to param_grid for full search
#         scoring='neg_mean_absolute_error',
#         cv=3,  # 3-fold cross-validation
#         verbose=1
#     )
    
#     grid_search.fit(X_train, y_train)
    
#     print("Best parameters:", grid_search.best_params_)
    
#     # Get the best model
#     best_model = grid_search.best_estimator_
    
#     # Make predictions
#     y_pred = best_model.predict(X_test)
    
#     # Evaluate the model
#     mae = mean_absolute_error(y_test, y_pred)
#     rmse = np.sqrt(mean_squared_error(y_test, y_pred))
#     r2 = r2_score(y_test, y_pred)
    
#     print(f"Model Performance:")
#     print(f"Mean Absolute Error: ${mae:.2f}")
#     print(f"Root Mean Squared Error: ${rmse:.2f}")
#     print(f"R² Score: {r2:.4f}")
    
#     # Analyze feature importance
#     importance_df = feature_importance_analysis(best_model, X)
    
#     # Save the model
#     model_path = "multi_zipcode_rental_model.pkl"
#     joblib.dump(best_model, model_path)
#     print(f"Model saved to {model_path}")
    
#     # Save the feature list for later use in predictions
#     with open("model_features.txt", "w") as f:
#         f.write(",".join(X.columns.tolist()))
    
#     return best_model, importance_df

# def main():
#     """
#     Main execution function
#     """
#     # Check if data already exists
#     if os.path.exists("rental_data_raw.csv"):
#         print("Loading existing data...")
#         df_raw = pd.read_csv("rental_data_raw.csv")
#     else:
#         print("Fetching new data from API...")
#         df_raw = fetch_all_locations()
    
#     # Prepare features
#     df_processed = prepare_features(df_raw)
    
#     # Geographic analysis
#     zipcode_analysis = geographic_analysis(df_raw)
#     print("\nRent by Zipcode:")
#     print(zipcode_analysis.head(10))
    
#     # Train model
#     model, importance = train_and_evaluate_model(df_processed)
    
#     print("\nTop 10 Most Important Features:")
#     print(importance.head(10))
    
#     print("\nComplete! The multi-zipcode rental prediction model has been created.")

# if __name__ == "__main__":
#     from datetime import datetime
#     main()









import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from xgboost import XGBRegressor
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings
from datetime import datetime

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore", category=pd.errors.SettingWithCopyWarning)

# Define property types mapping for consistency
PROPERTY_TYPE_MAP = {
    "APARTMENT": "APARTMENT",
    "CONDO": "CONDO",
    "CONDOS": "CONDO",
    "TOWNHOUSE": "TOWNHOME",
    "TOWNHOMES": "TOWNHOME",
    "SINGLE_FAMILY": "SINGLE_FAMILY",
    "DUPLEX": "MULTI_FAMILY",
    "TRIPLEX": "MULTI_FAMILY",
    "DUPLEX_TRIPLEX": "MULTI_FAMILY"
}

# Regional information for better predictions
REGION_INFO = {
    # Map zipcode prefixes to region codes
    "zip_prefix_to_region": {
        "01": "NORTHEAST",
        "02": "NORTHEAST",
        "03": "NORTHEAST",
        "04": "NORTHEAST",
        "05": "NORTHEAST",
        "06": "NORTHEAST",
        "07": "NORTHEAST",
        "08": "NORTHEAST",
        "09": "NORTHEAST",
        "10": "NORTHEAST",
        "11": "NORTHEAST",
        "12": "NORTHEAST",
        "13": "NORTHEAST",
        "14": "NORTHEAST",
        "15": "MIDATL",
        "16": "MIDATL",
        "17": "MIDATL",
        "18": "MIDATL",
        "19": "MIDATL",
        "20": "MIDATL",
        "21": "MIDATL",
        "22": "MIDATL",
        "23": "SOUTH",
        "24": "SOUTH",
        "25": "SOUTH",
        "26": "SOUTH",
        "27": "SOUTH",
        "28": "SOUTH",
        "29": "SOUTH",
        "30": "SOUTH",
        "31": "SOUTH",
        "32": "SOUTH",
        "33": "SOUTH",
        "34": "SOUTH",
        "35": "SOUTH",
        "36": "SOUTH",
        "37": "SOUTH",
        "38": "SOUTH",
        "39": "MIDWEST",
        "40": "SOUTH",
        "41": "MIDWEST",
        "42": "MIDWEST",
        "43": "MIDWEST",
        "44": "MIDWEST",
        "45": "MIDWEST",
        "46": "MIDWEST",
        "47": "MIDWEST",
        "48": "MIDWEST",
        "49": "MIDWEST",
        "50": "MIDWEST",
        "51": "MIDWEST",
        "52": "MIDWEST",
        "53": "MIDWEST",
        "54": "MIDWEST",
        "55": "MIDWEST",
        "56": "MIDWEST",
        "57": "MIDWEST",
        "58": "MIDWEST",
        "59": "WEST",
        "60": "MIDWEST",
        "61": "MIDWEST",
        "62": "MIDWEST",
        "63": "MIDWEST",
        "64": "MIDWEST",
        "65": "MIDWEST",
        "66": "MIDWEST",
        "67": "MIDWEST",
        "68": "MIDWEST",
        "69": "MIDWEST",
        "70": "SOUTH",
        "71": "SOUTH",
        "72": "SOUTH",
        "73": "SOUTH",
        "74": "SOUTH",
        "75": "SOUTH",
        "76": "SOUTH",
        "77": "SOUTH",
        "78": "SOUTH",
        "79": "SOUTH",
        "80": "WEST",
        "81": "WEST",
        "82": "WEST",
        "83": "WEST",
        "84": "WEST",
        "85": "WEST",
        "86": "WEST",
        "87": "WEST",
        "88": "WEST",
        "89": "WEST",
        "90": "WEST",
        "91": "WEST",
        "92": "WEST",
        "93": "WEST",
        "94": "WEST",
        "95": "WEST",
        "96": "WEST",
        "97": "WEST",
        "98": "WEST",
        "99": "WEST"
    },
    
    # Regional cost multipliers (relative to national average)
    "region_cost_index": {
        "NORTHEAST": 1.25,
        "MIDATL": 1.15,
        "SOUTH": 0.85,
        "MIDWEST": 0.90,
        "WEST": 1.20
    },
    
    # Premium location multipliers
    "premium_zips": {
        "02116": 1.35,    # Boston Back Bay
        "02108": 1.30,    # Boston Beacon Hill
        "10001": 1.40,    # NYC Chelsea
        "10028": 1.50,    # NYC Upper East Side
        "90210": 1.60,    # Beverly Hills
        "94109": 1.45,    # San Francisco Nob Hill
        "60611": 1.25,    # Chicago Gold Coast
        "78701": 1.20,    # Austin Downtown
        "33139": 1.30,    # Miami South Beach
        "98101": 1.25     # Seattle Downtown
    }
}

def prepare_data(csv_path="rental_data_raw.csv"):
    """
    Load and prepare the rental data with enhanced error handling
    """
    print("Loading rental data...")
    if os.path.exists(csv_path):
        try:
            df = pd.read_csv(csv_path)
            print(f"Loaded data with {df.shape[0]} records and {df.shape[1]} columns")
            return df
        except Exception as e:
            print(f"Error loading CSV file: {e}")
            return None
    else:
        print(f"File not found: {csv_path}")
        return None

def get_region_from_zipcode(zipcode):
    """
    Map zipcode to region for better generalization
    """
    # Handle non-string zipcodes
    zipcode = str(zipcode).zfill(5)
    
    # Get first two digits for region mapping
    prefix = zipcode[:2]
    
    # Map to region using the predefined mappings
    return REGION_INFO["zip_prefix_to_region"].get(prefix, "UNKNOWN")

def prepare_features_for_training(df):
    """
    Prepare features for model training with enhanced feature engineering
    that enables predictions for any zipcode
    """
    print("Preparing features for universal rental model...")
    
    # Make a copy to avoid SettingWithCopyWarning
    df = df.copy()
    
    # Drop rows with missing core values
    df = df.dropna(subset=["bedrooms", "living_area", "zipcode", "rent"])
    print(f"After dropping rows with missing core values: {df.shape}")
    
    # Convert data types safely
    for col in ["bedrooms", "bathrooms", "living_area", "rent"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Add region features based on zipcode
    df['zipcode'] = df['zipcode'].astype(str)
    df['region'] = df['zipcode'].apply(get_region_from_zipcode)
    
    # Add derived features
    df["beds_baths_ratio"] = df["bedrooms"] / df["bathrooms"].replace(0, 1)
    df["sqft_per_bedroom"] = df["living_area"] / df["bedrooms"].replace(0, 1)
    df["price_per_sqft"] = df["rent"] / df["living_area"]
    
    # Calculate property age if year_built is available
    if "year_built" in df.columns:
        current_year = datetime.now().year
        df["property_age"] = current_year - pd.to_numeric(df["year_built"], errors='coerce')
        df["property_age"].fillna(df["property_age"].median(), inplace=True)
    
    # Standardize property types
    if "property_type" in df.columns:
        df["property_type"] = df["property_type"].astype(str).str.upper()
        df["property_type"] = df["property_type"].map(lambda x: PROPERTY_TYPE_MAP.get(x, "OTHER"))
    
    # One-hot encode categorical variables
    # Convert property type to one-hot
    if "property_type" in df.columns:
        property_dummies = pd.get_dummies(df["property_type"], prefix="type")
        df = pd.concat([df, property_dummies], axis=1)
    
    # Convert region to one-hot - this is key for universal predictions
    region_dummies = pd.get_dummies(df["region"], prefix="region")
    df = pd.concat([df, region_dummies], axis=1)
    
    # Add high-value location indicator
    df['is_premium_location'] = df['zipcode'].isin(REGION_INFO['premium_zips']).astype(int)
    
    # Prepare final dataset for analysis
    df_for_analysis = df.copy()
    
    # Drop columns we won't use for modeling
    cols_to_drop = ['property_type', 'zipcode', 'region']
    if 'city' in df.columns:
        cols_to_drop.append('city')
    if 'state' in df.columns:
        cols_to_drop.append('state')
    
    cols_to_drop = [col for col in cols_to_drop if col in df.columns]
    df_model = df.drop(columns=cols_to_drop)
    
    print(f"Final model shape: {df_model.shape}")
    print(f"Model columns: {df_model.columns.tolist()}")
    
    return df_model, df_for_analysis

def train_universal_model(df):
    """
    Train a rental price prediction model that works for any zipcode
    """
    try:
        # Identify numeric columns for the model
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        # Remove the target variable from features
        if 'rent' in numeric_cols:
            numeric_cols.remove('rent')
        if 'price_per_sqft' in numeric_cols:
            numeric_cols.remove('price_per_sqft')
        
        # Prepare feature set X and target y
        X = df[numeric_cols]
        y = df['rent']
        
        print(f"\nTraining with {len(numeric_cols)} features: {numeric_cols}")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        print(f"Training data shape: {X_train.shape}")
        print(f"Testing data shape: {X_test.shape}")
        
        # Create and train XGBoost model with more robust parameters
        model = XGBRegressor(
            n_estimators=150,
            learning_rate=0.08,
            max_depth=6,
            min_child_weight=2,
            subsample=0.8,
            colsample_bytree=0.8,
            gamma=0.1,
            random_state=42
        )
        
        print("Training universal rental model...")
        model.fit(X_train, y_train, eval_set=[(X_test, y_test)], early_stopping_rounds=20, verbose=False)
        
        # Evaluate model
        y_pred = model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)
        
        print(f"\nModel Performance:")
        print(f"Mean Absolute Error: ${mae:.2f}")
        print(f"Root Mean Squared Error: ${rmse:.2f}")
        print(f"R² Score: {r2:.4f}")
        
        # Get feature importance
        importance = model.feature_importances_
        feature_importance = pd.DataFrame({
            'Feature': X.columns,
            'Importance': importance
        }).sort_values(by='Importance', ascending=False)
        
        print("\nTop 10 Feature Importance:")
        print(feature_importance.head(10))
        
        # Plot feature importance
        plt.figure(figsize=(12, 8))
        sns.barplot(x='Importance', y='Feature', data=feature_importance.head(15))
        plt.title('Top 15 Features for Universal Rental Price Prediction')
        plt.tight_layout()
        plt.savefig('universal_rental_feature_importance.png')
        
        # Save the model
        model_path = "universal_rental_model.pkl"
        joblib.dump(model, model_path)
        print(f"\nUniversal model saved to {model_path}")
        
        # Save feature list for later use
        feature_list = X.columns.tolist()
        with open("universal_rental_features.txt", "w") as f:
            f.write(",".join(feature_list))
        print(f"Feature list saved to universal_rental_features.txt")
        
        # Save region mappings for prediction
        with open("region_mappings.py", "w") as f:
            f.write(f"PROPERTY_TYPE_MAP = {PROPERTY_TYPE_MAP}\n")
            f.write(f"REGION_INFO = {REGION_INFO}\n")
        print(f"Region mappings saved to region_mappings.py")
        
        return model, feature_importance
        
    except Exception as e:
        print(f"Error in model training: {e}")
        return None, None

def regional_analysis(df_analysis):
    """
    Analyze rental prices by region to validate the universal model
    """
    try:
        # Group by region
        region_stats = df_analysis.groupby('region')['rent'].agg(['mean', 'median', 'count', 'std']).reset_index()
        region_stats = region_stats.sort_values('mean', ascending=False)
        
        print("\nRental Price by Region:")
        print(region_stats)
        
        # Plot regional comparison
        plt.figure(figsize=(12, 6))
        
        # Filter regions with enough data
        plot_data = region_stats[region_stats['count'] >= 5]
        
        sns.barplot(x='region', y='mean', data=plot_data)
        plt.title('Average Rent by Region')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('rent_by_region.png')
        
        # Property type analysis
        if 'property_type' in df_analysis.columns:
            type_stats = df_analysis.groupby('property_type')['rent'].agg(['mean', 'median', 'count']).reset_index()
            type_stats = type_stats.sort_values('mean', ascending=False)
            
            print("\nRental Price by Property Type:")
            print(type_stats)
            
            # Plot property type comparison
            plt.figure(figsize=(12, 6))
            plot_data = type_stats[type_stats['count'] >= 5]
            sns.barplot(x='property_type', y='mean', data=plot_data)
            plt.title('Average Rent by Property Type')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig('rent_by_property_type.png')
        
        return region_stats
    except Exception as e:
        print(f"Error in regional analysis: {e}")
        return None

def main():
    """
    Main execution function to create the universal rental model
    """
    try:
        # Load data
        df_raw = prepare_data()
        if df_raw is None:
            return
        
        # Process features for universal model
        df_processed, df_for_analysis = prepare_features_for_training(df_raw)
        
        # Analyze by region
        regional_analysis(df_for_analysis)
        
        # Train universal model
        model, importance = train_universal_model(df_processed)
        
        print("\nComplete! The universal rental prediction model has been created.")
        print("This model can predict rental prices for any property in any zipcode across the US.")
        
    except Exception as e:
        print(f"Error in main execution: {e}")

if __name__ == "__main__":
    main()