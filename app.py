
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import os
# import joblib
# import numpy as np
# import pandas as pd
# from datetime import datetime
# import json
# import requests
# from werkzeug.middleware.proxy_fix import ProxyFix
# import random
# import logging
# import xgboost as xgb

# # Set up logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# app = Flask(__name__)
# CORS(app)  # Enable CORS for all routes
# app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)

# # Realtor API Config
# REALTOR_API_KEY = "6b504def46msha6bf4ff53605f98p1c0c1djsn3fcd43362b33"
# REALTOR_HOST = "realty-in-us.p.rapidapi.com"
# HEADERS = {
#     "X-RapidAPI-Key": REALTOR_API_KEY,
#     "X-RapidAPI-Host": REALTOR_HOST,
#     "Content-Type": "application/json"
# }

# # Load both models
# def load_models():
#     """Load both models"""
#     models = {}
    
#     # Load sale price model
#     sale_model_path = 'ml_models/price-prediction-model/xgboost/xgboost_final_model.pkl'
#     alternative_path = 'ml_models/price-prediction-model/xgboost_final_model.json'
    
#     try:
#         # Try to load as pickle first
#         models['sale'] = joblib.load(sale_model_path)
#         print(f"Sale price model loaded successfully from {sale_model_path}")
#         print(f"Model type: {type(models['sale'])}")
#     except Exception as e:
#         print(f"Error loading sale price model: {e}")
#         try:
#             # Try to load as JSON if pickle fails
#             sale_model = xgb.Booster()
#             sale_model.load_model(alternative_path)
#             models['sale'] = sale_model
#             print(f"Sale price model loaded successfully from {alternative_path}")
#             print(f"Model type: {type(sale_model)}")
#         except Exception as e2:
#             print(f"Error loading alternative sale price model: {e2}")
#             models['sale'] = None
    
#     # Load rental model
#     rental_model_path = 'ml_models/rental_model.pkl'
#     alternative_rental_path = 'universal_rental_model.pkl'
    
#     try:
#         models['rental'] = joblib.load(rental_model_path)
#         print(f"Rental model loaded successfully from {rental_model_path}")
#         print(f"Model type: {type(models['rental'])}")
#     except Exception as e:
#         print(f"Error loading rental model: {e}")
#         try:
#             # Try alternative path
#             models['rental'] = joblib.load(alternative_rental_path)
#             print(f"Rental model loaded successfully from {alternative_rental_path}")
#             print(f"Model type: {type(models['rental'])}")
#         except Exception as e2:
#             print(f"Error loading alternative rental model: {e2}")
#             models['rental'] = None
    
#     return models

# MODELS = load_models()

# def fetch_properties_from_api(location):
#     """Fetch properties from Realtor API"""
#     url = "https://realty-in-us.p.rapidapi.com/properties/v3/list"
#     payload = {
#         "limit": 15,
#         "offset": 0,
#         "status": ["for_sale"],
#         "sort": {"direction": "desc", "field": "list_date"},
#         "search_location": location
#     }

#     print(f"Making API request to {url} with location: {location}")

#     if location.isdigit() and len(location) == 5:
#         payload["postal_code"] = location
#     else:
#         payload["city"] = location

#     try:
#         print("Sending request to Realtor API...")
#         response = requests.post(url, headers=HEADERS, json=payload, timeout=10)
        
#         print(f"Response status code: {response.status_code}")
#         if response.status_code == 200:
#             data = response.json()
#             results = data.get("data", {}).get("home_search", {}).get("results", [])
#             print(f"API returned {len(results)} properties")
#             return results
#         else:
#             print(f"API Error Response: {response.text[:500]}")  # Print first 500 chars of error
#             logger.error(f"API Error: {response.status_code} - {response.text}")
#             return []
#     except Exception as e:
#         print(f"Exception during API request: {str(e)}")
#         logger.error(f"Request Exception: {e}")
#         return []

# @app.route('/')
# def home():
#     """Simple endpoint to verify server is running"""
#     return jsonify({
#         'status': 'success',
#         'message': 'Server is running',
#         'models_loaded': {
#             'sale': MODELS['sale'] is not None,
#             'rental': MODELS['rental'] is not None
#         }
#     })

# @app.route('/api/search', methods=['POST'])
# def search_properties():
#     """Search for properties in a location"""
#     try:
#         data = request.get_json()
#         location = data.get("location", "").strip()
        
#         print(f"Search request received for location: {location}")
        
#         if not location:
#             print("Error: Empty location provided")
#             return jsonify({"status": "error", "message": "Location is required."}), 400
            
#         properties = fetch_properties_from_api(location)
#         if not properties:
#             print("No properties found in API response")
#             return jsonify({"status": "error", "message": "No properties found."}), 404
            
#         print(f"Processing {len(properties)} properties from API response")
        
#         # Process and return properties with predictions
#         results = []
#         for i, prop in enumerate(properties):
#             try:
#                 # Get property details
#                 location_data = prop.get("location", {}).get("address", {})
#                 desc = prop.get("description", {})
                
#                 property_data = {
#                     "address": location_data.get("line", "N/A"),
#                     "city": location_data.get("city", "N/A"),
#                     "state": location_data.get("state_code", "N/A"),
#                     "zipcode": location_data.get("postal_code", ""),
#                     "beds": desc.get("beds", "N/A"),
#                     "baths": desc.get("baths", "N/A"),
#                     "livingArea": desc.get("sqft", 1500),  # Renamed to match prediction input
#                     "yearBuilt": desc.get("year_built", 2005),
#                     "propertyType": desc.get("type", "SINGLE_FAMILY"),  # Renamed to match prediction input
#                     "list_price": prop.get("list_price", 0),
#                     "image_url": prop.get("photos", [{}])[0].get("href", "https://via.placeholder.com/400x300?text=No+Image"),
#                     "latitude": prop.get("location", {}).get("coordinate", {}).get("lat"),
#                     "longitude": prop.get("location", {}).get("coordinate", {}).get("lon"),
#                     # Default values for required fields in prediction
#                     "lotArea": 0.25,
#                     "daysOnMarket": 0,
#                     "hasGarage": 1 if any("garage" in tag.lower() for tag in prop.get("tags", [])) else 0,
#                     "hasPool": 1 if any("pool" in tag.lower() for tag in prop.get("tags", [])) else 0,
#                     "hasFireplace": 1 if any("fireplace" in tag.lower() for tag in prop.get("tags", [])) else 0,
#                     "hasBasement": 1 if any("basement" in tag.lower() for tag in prop.get("tags", [])) else 0,
#                     "hasCentralAir": 1 if any("central air" in tag.lower() for tag in prop.get("tags", [])) else 0,
#                     "hasSecuritySystem": 0,
#                     "hasSprinklerSystem": 0,
#                     "hasSolarPanels": 0
#                 }
                
#                 print(f"Processing property {i+1}: {property_data['address']}, {property_data['city']}")
                
#                 # Get predictions
#                 try:
#                     predictions = get_predictions(property_data)
#                     property_data.update(predictions)
#                 except Exception as pred_e:
#                     print(f"Error getting predictions for property {i+1}: {pred_e}")
#                     property_data['predictedSalePrice'] = fallback_sale_prediction(property_data)
#                     property_data['predictedRent'] = fallback_rental_prediction(property_data)
                
#                 results.append(property_data)
#             except Exception as e:
#                 print(f"Error processing property {i+1}: {e}")
#                 logger.error(f"Error processing property: {e}")
#                 continue
                
#         print(f"Returning {len(results)} processed properties")
#         return jsonify({"status": "success", "results": results})
        
#     except Exception as e:
#         print(f"Global error in search endpoint: {e}")
#         logger.error(f"Error in search: {e}")
#         return jsonify({"status": "error", "message": str(e)}), 500

# @app.route('/api/predict', methods=['POST'])
# def predict():
#     """API endpoint for making predictions"""
#     try:
#         # Get data from request
#         data = request.get_json()
#         print("Received prediction request:", data)
        
#         # Required fields
#         required_fields = ['zipcode', 'bedrooms', 'propertyType']
        
#         # Check if all required fields are present
#         missing_fields = [field for field in required_fields if field not in data]
#         if missing_fields:
#             return jsonify({
#                 'status': 'error', 
#                 'message': f'Missing required fields: {", ".join(missing_fields)}'
#             }), 400
        
#         # Prepare input data with defaults for missing fields
#         input_data = {
#             'zipcode': data['zipcode'],
#             'bedrooms': int(data['bedrooms']),
#             'bathrooms': float(data.get('bathrooms', 1)),
#             'propertyType': data['propertyType'],
#             'livingArea': int(data.get('livingArea', 1000)),
#             'lotArea': float(data.get('lotArea', 0.25)),
#             'daysOnMarket': int(data.get('daysOnMarket', 0)),
#             'yearBuilt': int(data.get('yearBuilt', 1980)),
#             'hasGarage': int(data.get('hasGarage', 1)),
#             'hasPool': int(data.get('hasPool', 0)),
#             'hasFireplace': int(data.get('hasFireplace', 0)),
#             'hasBasement': int(data.get('hasBasement', 1)),
#             'hasCentralAir': int(data.get('hasCentralAir', 1)),
#             'hasSecuritySystem': int(data.get('hasSecuritySystem', 0)),
#             'hasSprinklerSystem': int(data.get('hasSprinklerSystem', 0)),
#             'hasSolarPanels': int(data.get('hasSolarPanels', 0))
#         }
        
#         print("Input data for prediction:", input_data)
        
#         # Initialize result dictionary
#         result = {
#             'status': 'success',
#             'timestamp': datetime.now().isoformat(),
#             'input': data
#         }
        
#         # Sale Price Prediction
#         if MODELS['sale'] is not None:
#             try:
#                 # Prepare features for XGBoost
#                 print("Preparing sale features...")
#                 sale_features = prepare_sale_features(input_data)
#                 print("Features prepared:", sale_features)
                
#                 # Make prediction using XGBoost
#                 print("Making sale price prediction...")
#                 if isinstance(MODELS['sale'], xgb.Booster):
#                     # For Booster models
#                     dmatrix = xgb.DMatrix(sale_features)
#                     sale_prediction = MODELS['sale'].predict(dmatrix)
#                 else:
#                     # For sklearn wrapper models
#                     sale_prediction = MODELS['sale'].predict(sale_features)
                    
#                 result['predictedSalePrice'] = round(float(sale_prediction[0]), 2)
#                 result['sale_method'] = 'model'
#                 print(f"Sale price prediction: {result['predictedSalePrice']}")
#             except Exception as e:
#                 print(f"Detailed error in sale price prediction: {str(e)}")
#                 print("Using fallback prediction for sale price")
#                 result['predictedSalePrice'] = fallback_sale_prediction(input_data)
#                 result['sale_note'] = 'Using fallback prediction'
#                 result['sale_method'] = 'fallback'
#         else:
#             print("Sale model is not loaded, using fallback")
#             result['predictedSalePrice'] = fallback_sale_prediction(input_data)
#             result['sale_note'] = 'Using fallback prediction (model not loaded)'
#             result['sale_method'] = 'fallback'
            
#         # Rental Price Prediction
#         if MODELS['rental'] is not None:
#             try:
#                 print("Preparing rental features...")
#                 rental_features = prepare_rental_features(input_data)
#                 print("Features prepared for rental prediction")
                
#                 # Make prediction
#                 print("Making rental price prediction...")
#                 rental_prediction = MODELS['rental'].predict(rental_features)
#                 result['predictedRent'] = round(float(rental_prediction[0]), 2)
#                 result['rental_method'] = 'model'
#                 print(f"Rental price prediction: {result['predictedRent']}")
#             except Exception as e:
#                 print(f"Error in rental price prediction: {e}")
#                 result['predictedRent'] = fallback_rental_prediction(input_data)
#                 result['rental_note'] = 'Using fallback prediction'
#                 result['rental_method'] = 'fallback'
#         else:
#             print("Rental model is not loaded, using fallback")
#             result['predictedRent'] = fallback_rental_prediction(input_data)
#             result['rental_note'] = 'Using fallback prediction (model not loaded)'
#             result['rental_method'] = 'fallback'
        
#         # Calculate investment metrics
#         try:
#             sale_price = result['predictedSalePrice']
#             rent = result['predictedRent']
            
#             # Calculate monthly rental income
#             annual_rental_income = rent * 12
            
#             # Calculate cap rate (net annual income / property value)
#             expenses_percent = 40  # Typical expenses as percentage of rental income
#             net_rental_income = annual_rental_income * (1 - expenses_percent/100)
#             cap_rate = (net_rental_income / sale_price) * 100
            
#             result['annualizedReturn'] = round(cap_rate, 2)
#             result['monthlyRentalIncome'] = round(rent, 2)
#             result['annualRentalIncome'] = round(annual_rental_income, 2)
#             result['estimatedAnnualExpenses'] = round(annual_rental_income * expenses_percent/100, 2)
#             result['netAnnualIncome'] = round(net_rental_income, 2)
#         except Exception as e:
#             print(f"Error calculating investment metrics: {e}")
        
#         return jsonify(result)
        
#     except Exception as e:
#         print(f"Error in prediction endpoint: {e}")
#         logger.error(f"Error in prediction endpoint: {e}")
#         return jsonify({'status': 'error', 'message': str(e)}), 500

# def get_predictions(property_data):
#     """Function to get predictions for both sale and rental prices"""
#     result = {}
    
#     # Sale Price Prediction
#     if MODELS['sale'] is not None:
#         try:
#             sale_features = prepare_sale_features(property_data)
            
#             # Make prediction based on model type
#             if isinstance(MODELS['sale'], xgb.Booster):
#                 # For Booster models
#                 dmatrix = xgb.DMatrix(sale_features)
#                 sale_prediction = MODELS['sale'].predict(dmatrix)
#             else:
#                 # For sklearn wrapper models
#                 sale_prediction = MODELS['sale'].predict(sale_features)
                
#             result['predictedSalePrice'] = round(float(sale_prediction[0]), 2)
#             print(f"Sale price prediction: {result['predictedSalePrice']}")
#         except Exception as e:
#             print(f"Error in sale price prediction for property: {e}")
#             result['predictedSalePrice'] = fallback_sale_prediction(property_data)
#     else:
#         result['predictedSalePrice'] = fallback_sale_prediction(property_data)
    
#     # Rental Price Prediction
#     if MODELS['rental'] is not None:
#         try:
#             rental_features = prepare_rental_features(property_data)
#             rental_prediction = MODELS['rental'].predict(rental_features)
#             result['predictedRent'] = round(float(rental_prediction[0]), 2)
#             print(f"Rental price prediction: {result['predictedRent']}")
#         except Exception as e:
#             print(f"Error in rental price prediction for property: {e}")
#             result['predictedRent'] = fallback_rental_prediction(property_data)
#     else:
#         result['predictedRent'] = fallback_rental_prediction(property_data)
    
#     return result

# def prepare_sale_features(input_data):
#     """Prepare features for sale price prediction"""
#     try:
#         # Create feature array with values in proper order
#         features = [
#             input_data['zipcode'],
#             input_data['bedrooms'],
#             input_data['bathrooms'],
#             input_data['propertyType'],
#             input_data['livingArea'],
#             input_data['lotArea'],
#             input_data['daysOnMarket'],
#             input_data['yearBuilt'],
#             input_data['hasGarage'],
#             input_data['hasPool'],
#             input_data['hasFireplace'],
#             input_data['hasBasement'],
#             input_data['hasCentralAir'],
#             input_data['hasSecuritySystem'],
#             input_data['hasSprinklerSystem'],
#             input_data['hasSolarPanels']
#         ]
        
#         # Convert to numeric values where needed
#         for i, feature in enumerate(features):
#             if isinstance(feature, str) and feature.isdigit():
#                 features[i] = float(feature)
#             elif isinstance(feature, str) and i != 3:  # Skip propertyType
#                 features[i] = 0.0  # Default for non-numeric values
        
#         return np.array(features).reshape(1, -1)
#     except Exception as e:
#         print(f"Error preparing sale features: {e}")
#         raise

# def prepare_rental_features(input_data):
#     """Prepare features for rental price prediction"""
#     try:
#         # Create feature array with values in proper order
#         features = [
#             input_data['zipcode'],
#             input_data['bedrooms'],
#             input_data['bathrooms'],
#             input_data['propertyType'],
#             input_data['livingArea'],
#             input_data['lotArea'],
#             input_data['daysOnMarket'],
#             input_data['yearBuilt'],
#             input_data['hasGarage'],
#             input_data['hasPool'],
#             input_data['hasFireplace'],
#             input_data['hasBasement'],
#             input_data['hasCentralAir'],
#             input_data['hasSecuritySystem'],
#             input_data['hasSprinklerSystem'],
#             input_data['hasSolarPanels']
#         ]
        
#         # Convert to numeric values where needed
#         for i, feature in enumerate(features):
#             if isinstance(feature, str) and feature.isdigit():
#                 features[i] = float(feature)
#             elif isinstance(feature, str) and i != 3:  # Skip propertyType
#                 features[i] = 0.0  # Default for non-numeric values
        
#         return np.array(features).reshape(1, -1)
#     except Exception as e:
#         print(f"Error preparing rental features: {e}")
#         raise

# def fallback_sale_prediction(input_data):
#     """Fallback prediction for sale price if model fails"""
#     # Base price by region (derived from zipcode)
#     zipcode = str(input_data['zipcode'])
#     region_base = {
#         "0": 450000,  # Northeast
#         "1": 390000,  # Northeast
#         "2": 380000,  # Northeast/Mid-Atlantic
#         "3": 320000,  # Mid-Atlantic/South
#         "4": 280000,  # South
#         "5": 250000,  # South
#         "6": 280000,  # South
#         "7": 270000,  # South/Midwest
#         "8": 290000,  # Midwest
#         "9": 450000   # West
#     }
    
#     # Get region prefix (first digit of zipcode)
#     prefix = zipcode[0] if len(zipcode) > 0 else "0"
#     base_price = region_base.get(prefix, 350000)
    
#     # Adjust for property attributes
#     bedrooms = float(input_data['bedrooms'])
#     bathrooms = float(input_data['bathrooms'])
#     living_area = float(input_data['livingArea'])
    
#     # Size adjustment
#     size_factor = (living_area / 1500) ** 0.8  # Non-linear scaling
    
#     # Room adjustment
#     room_factor = 1.0 + 0.1 * (bedrooms - 3) + 0.15 * (bathrooms - 2)
    
#     # Property type adjustment
#     property_type = input_data['propertyType']
#     type_factors = {
#         "SINGLE_FAMILY": 1.0,
#         "TOWNHOUSE": 0.85,
#         "CONDO": 0.75,
#         "MULTI_FAMILY": 1.2,
#         "APARTMENT": 0.7
#     }
#     type_factor = type_factors.get(property_type, 1.0)
    
#     # Feature adjustments
#     feature_factor = 1.0
#     if input_data.get('hasGarage', 0) == 1:
#         feature_factor += 0.05
#     if input_data.get('hasPool', 0) == 1:
#         feature_factor += 0.08
#     if input_data.get('hasFireplace', 0) == 1:
#         feature_factor += 0.03
    
#     # Calculate final price
#     final_price = base_price * size_factor * room_factor * type_factor * feature_factor
    
#     # Add some randomness to prevent all similar properties having identical prices
#     variation = 0.95 + (0.1 * np.random.random())
    
#     return round(final_price * variation, 2)

# def fallback_rental_prediction(input_data):
#     """Fallback prediction for rental price if model fails"""
#     # Base rent by region (derived from zipcode)
#     zipcode = str(input_data['zipcode'])
#     region_base = {
#         "0": 2200,  # Northeast
#         "1": 2000,  # Northeast
#         "2": 1900,  # Northeast/Mid-Atlantic
#         "3": 1700,  # Mid-Atlantic/South
#         "4": 1500,  # South
#         "5": 1400,  # South
#         "6": 1500,  # South
#         "7": 1400,  # South/Midwest
#         "8": 1500,  # Midwest
#         "9": 2300   # West
#     }
    
#     # Get region prefix (first digit of zipcode)
#     prefix = zipcode[0] if len(zipcode) > 0 else "0"
#     base_rent = region_base.get(prefix, 1800)
    
#     # Adjust for property attributes
#     bedrooms = float(input_data['bedrooms'])
#     bathrooms = float(input_data['bathrooms'])
#     living_area = float(input_data['livingArea'])
    
#     # Size adjustment - smaller impact than on sale price
#     size_factor = (living_area / 1500) ** 0.6  # Non-linear scaling
    
#     # Room adjustment
#     room_factor = 1.0 + 0.15 * (bedrooms - 3) + 0.1 * (bathrooms - 2)
    
#     # Property type adjustment
#     property_type = input_data['propertyType']
#     type_factors = {
#         "SINGLE_FAMILY": 1.0,
#         "TOWNHOUSE": 0.9,
#         "CONDO": 0.85,
#         "MULTI_FAMILY": 0.8,
#         "APARTMENT": 0.75
#     }
#     type_factor = type_factors.get(property_type, 1.0)
    
#     # Feature adjustments
#     feature_factor = 1.0
#     if input_data.get('hasGarage', 0) == 1:
#         feature_factor += 0.03
#     if input_data.get('hasPool', 0) == 1:
#         feature_factor += 0.05
#     if input_data.get('hasFireplace', 0) == 1:
#         feature_factor += 0.02
    
#     # Calculate final rent
#     final_rent = base_rent * size_factor * room_factor * type_factor * feature_factor
    
#     # Add some randomness to prevent all similar properties having identical rents
#     variation = 0.95 + (0.1 * np.random.random())
    
#     return round(final_rent * variation, 2)

# # Add health check endpoint
# @app.route('/health', methods=['GET'])
# def health_check():
#     """Health check endpoint for monitoring"""
#     return jsonify({
#         'status': 'healthy',
#         'timestamp': datetime.now().isoformat(),
#         'models': {
#             'sale': MODELS['sale'] is not None,
#             'rental': MODELS['rental'] is not None
#         }
#     })

# if __name__ == '__main__':
#     # Try to detect the port from environment variables (for container deployments)
#     port = int(os.environ.get('PORT', 5000))
#     app.run(debug=True, host='0.0.0.0', port=port)






from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import joblib
import numpy as np
import pandas as pd
from datetime import datetime
import json
import requests
from werkzeug.middleware.proxy_fix import ProxyFix
import logging
import xgboost as xgb

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)

# Realtor API Config
REALTOR_API_KEY = "6b504def46msha6bf4ff53605f98p1c0c1djsn3fcd43362b33"
REALTOR_HOST = "realty-in-us.p.rapidapi.com"
HEADERS = {
    "X-RapidAPI-Key": REALTOR_API_KEY,
    "X-RapidAPI-Host": REALTOR_HOST,
    "Content-Type": "application/json"
}

# Load both models
def load_models():
    """Load both models"""
    models = {}
    
    # Load sale price model
    sale_model_path = 'ml_models/price-prediction-model/xgboost/xgboost_final_model.pkl'
    alternative_path = 'ml_models/price-prediction-model/xgboost/xgboost_final_model.json'
    
    try:
        # Try to load as pickle first
        models['sale'] = joblib.load(sale_model_path)
        print(f"Sale price model loaded successfully from {sale_model_path}")
        print(f"Model type: {type(models['sale'])}")
    except Exception as e:
        print(f"Error loading sale price model: {e}")
        try:
            # Try to load as JSON if pickle fails
            sale_model = xgb.Booster()
            sale_model.load_model(alternative_path)
            models['sale'] = sale_model
            print(f"Sale price model loaded successfully from {alternative_path}")
            print(f"Model type: {type(sale_model)}")
        except Exception as e2:
            print(f"Error loading alternative sale price model: {e2}")
            models['sale'] = None
    
    # Load rental model
    rental_model_path = 'ml_models/rental_model.pkl'
    alternative_rental_path = 'universal_rental_model.pkl'
    
    try:
        models['rental'] = joblib.load(rental_model_path)
        print(f"Rental model loaded successfully from {rental_model_path}")
        print(f"Model type: {type(models['rental'])}")
    except Exception as e:
        print(f"Error loading rental model: {e}")
        try:
            # Try alternative path
            models['rental'] = joblib.load(alternative_rental_path)
            print(f"Rental model loaded successfully from {alternative_rental_path}")
            print(f"Model type: {type(models['rental'])}")
        except Exception as e2:
            print(f"Error loading alternative rental model: {e2}")
            models['rental'] = None
    
    return models

MODELS = load_models()

def fetch_properties_from_api(location):
    """Fetch properties from Realtor API"""
    url = "https://realty-in-us.p.rapidapi.com/properties/v3/list"
    payload = {
        "limit": 15,
        "offset": 0,
        "status": ["for_sale"],
        "sort": {"direction": "desc", "field": "list_date"},
        "search_location": location
    }

    print(f"Making API request to {url} with location: {location}")

    if location.isdigit() and len(location) == 5:
        payload["postal_code"] = location
    else:
        payload["city"] = location

    try:
        print("Sending request to Realtor API...")
        response = requests.post(url, headers=HEADERS, json=payload, timeout=10)
        
        print(f"Response status code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            results = data.get("data", {}).get("home_search", {}).get("results", [])
            print(f"API returned {len(results)} properties")
            return results
        else:
            print(f"API Error Response: {response.text[:500]}")  # Print first 500 chars of error
            logger.error(f"API Error: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        print(f"Exception during API request: {str(e)}")
        logger.error(f"Request Exception: {e}")
        return []

@app.route('/')
def home():
    """Simple endpoint to verify server is running"""
    return jsonify({
        'status': 'success',
        'message': 'Server is running',
        'models_loaded': {
            'sale': MODELS['sale'] is not None,
            'rental': MODELS['rental'] is not None
        }
    })

@app.route('/api/search', methods=['POST'])
def search_properties():
    """Search for properties in a location"""
    try:
        data = request.get_json()
        location = data.get("location", "").strip()
        
        print(f"Search request received for location: {location}")
        
        if not location:
            print("Error: Empty location provided")
            return jsonify({"status": "error", "message": "Location is required."}), 400
            
        properties = fetch_properties_from_api(location)
        if not properties:
            print("No properties found in API response")
            return jsonify({"status": "error", "message": "No properties found."}), 404
            
        print(f"Processing {len(properties)} properties from API response")
        
        # Process and return properties with predictions
        results = []
        for i, prop in enumerate(properties):
            try:
                # Get property details
                location_data = prop.get("location", {}).get("address", {})
                desc = prop.get("description", {})
                
                property_data = {
                    "address": location_data.get("line", "N/A"),
                    "city": location_data.get("city", "N/A"),
                    "state": location_data.get("state_code", "N/A"),
                    "zipcode": location_data.get("postal_code", ""),
                    "beds": desc.get("beds", "N/A"),
                    "baths": desc.get("baths", "N/A"),
                    "livingArea": desc.get("sqft", 1500),  # Renamed to match prediction input
                    "yearBuilt": desc.get("year_built", 2005),
                    "propertyType": desc.get("type", "SINGLE_FAMILY"),  # Renamed to match prediction input
                    "list_price": prop.get("list_price", 0),
                    "image_url": prop.get("photos", [{}])[0].get("href", "https://via.placeholder.com/400x300?text=No+Image"),
                    "latitude": prop.get("location", {}).get("coordinate", {}).get("lat"),
                    "longitude": prop.get("location", {}).get("coordinate", {}).get("lon"),
                    # Default values for required fields in prediction
                    "lotArea": 0.25,
                    "daysOnMarket": 0,
                    "hasGarage": 1 if any("garage" in tag.lower() for tag in prop.get("tags", [])) else 0,
                    "hasPool": 1 if any("pool" in tag.lower() for tag in prop.get("tags", [])) else 0,
                    "hasFireplace": 1 if any("fireplace" in tag.lower() for tag in prop.get("tags", [])) else 0,
                    "hasBasement": 1 if any("basement" in tag.lower() for tag in prop.get("tags", [])) else 0,
                    "hasCentralAir": 1 if any("central air" in tag.lower() for tag in prop.get("tags", [])) else 0,
                    "hasSecuritySystem": 0,
                    "hasSprinklerSystem": 0,
                    "hasSolarPanels": 0
                }
                
                print(f"Processing property {i+1}: {property_data['address']}, {property_data['city']}")
                
                # Get predictions
                try:
                    predictions = get_predictions(property_data)
                    property_data.update(predictions)
                except Exception as pred_e:
                    print(f"Error getting predictions for property {i+1}: {pred_e}")
                    # Instead of using fallback, we'll skip properties where prediction fails
                    logger.error(f"Skipping property due to prediction error: {pred_e}")
                    continue
                
                results.append(property_data)
            except Exception as e:
                print(f"Error processing property {i+1}: {e}")
                logger.error(f"Error processing property: {e}")
                continue
                
        print(f"Returning {len(results)} processed properties")
        return jsonify({"status": "success", "results": results})
        
    except Exception as e:
        print(f"Global error in search endpoint: {e}")
        logger.error(f"Error in search: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/predict', methods=['POST'])
def predict():
    """API endpoint for making predictions"""
    try:
        # Get data from request
        data = request.get_json()
        print("Received prediction request:", data)
        
        # Required fields
        required_fields = ['zipcode', 'bedrooms', 'propertyType']
        
        # Check if all required fields are present
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({
                'status': 'error', 
                'message': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400
        
        # Prepare input data with defaults for missing fields
        input_data = {
            'zipcode': data['zipcode'],
            'bedrooms': int(data['bedrooms']),
            'bathrooms': float(data.get('bathrooms', 1)),
            'propertyType': data['propertyType'],
            'livingArea': int(data.get('livingArea', 1000)),
            'lotArea': float(data.get('lotArea', 0.25)),
            'daysOnMarket': int(data.get('daysOnMarket', 0)),
            'yearBuilt': int(data.get('yearBuilt', 1980)),
            'hasGarage': int(data.get('hasGarage', 1)),
            'hasPool': int(data.get('hasPool', 0)),
            'hasFireplace': int(data.get('hasFireplace', 0)),
            'hasBasement': int(data.get('hasBasement', 1)),
            'hasCentralAir': int(data.get('hasCentralAir', 1)),
            'hasSecuritySystem': int(data.get('hasSecuritySystem', 0)),
            'hasSprinklerSystem': int(data.get('hasSprinklerSystem', 0)),
            'hasSolarPanels': int(data.get('hasSolarPanels', 0))
        }
        
        print("Input data for prediction:", input_data)
        
        # Initialize result dictionary
        result = {
            'status': 'success',
            'timestamp': datetime.now().isoformat(),
            'input': data
        }
        
        # Sale Price Prediction
        if MODELS['sale'] is not None:
            try:
                # Prepare features for XGBoost
                print("Preparing sale features...")
                sale_features = prepare_sale_features(input_data)
                print("Features prepared:", sale_features)
                
                # Make prediction using XGBoost
                print("Making sale price prediction...")
                if isinstance(MODELS['sale'], xgb.Booster):
                    # For Booster models
                    dmatrix = xgb.DMatrix(sale_features)
                    sale_prediction = MODELS['sale'].predict(dmatrix)
                else:
                    # For sklearn wrapper models
                    sale_prediction = MODELS['sale'].predict(sale_features)
                    
                result['predictedSalePrice'] = round(float(sale_prediction[0]), 2)
                result['sale_method'] = 'model'
                print(f"Sale price prediction: {result['predictedSalePrice']}")
            except Exception as e:
                print(f"Detailed error in sale price prediction: {str(e)}")
                # Return error instead of using fallback
                return jsonify({
                    'status': 'error',
                    'message': 'Sale price prediction failed. Please check model and input data.',
                    'error': str(e)
                }), 500
        else:
            print("Sale model is not loaded")
            return jsonify({
                'status': 'error',
                'message': 'Sale price model is not loaded.'
            }), 500
            
        # Rental Price Prediction
        if MODELS['rental'] is not None:
            try:
                print("Preparing rental features...")
                rental_features = prepare_rental_features(input_data)
                print("Features prepared for rental prediction")
                
                # Make prediction
                print("Making rental price prediction...")
                rental_prediction = MODELS['rental'].predict(rental_features)
                result['predictedRent'] = round(float(rental_prediction[0]), 2)
                result['rental_method'] = 'model'
                print(f"Rental price prediction: {result['predictedRent']}")
            except Exception as e:
                print(f"Error in rental price prediction: {e}")
                # Return error instead of using fallback
                return jsonify({
                    'status': 'error',
                    'message': 'Rental price prediction failed. Please check model and input data.',
                    'error': str(e)
                }), 500
        else:
            print("Rental model is not loaded")
            return jsonify({
                'status': 'error',
                'message': 'Rental price model is not loaded.'
            }), 500
        
        # Calculate investment metrics
        try:
            sale_price = result['predictedSalePrice']
            rent = result['predictedRent']
            
            # Calculate monthly rental income
            annual_rental_income = rent * 12
            
            # Calculate cap rate (net annual income / property value)
            expenses_percent = 40  # Typical expenses as percentage of rental income
            net_rental_income = annual_rental_income * (1 - expenses_percent/100)
            cap_rate = (net_rental_income / sale_price) * 100
            
            result['annualizedReturn'] = round(cap_rate, 2)
            result['monthlyRentalIncome'] = round(rent, 2)
            result['annualRentalIncome'] = round(annual_rental_income, 2)
            result['estimatedAnnualExpenses'] = round(annual_rental_income * expenses_percent/100, 2)
            result['netAnnualIncome'] = round(net_rental_income, 2)
        except Exception as e:
            print(f"Error calculating investment metrics: {e}")
            # Return error for investment metric calculation failures
            return jsonify({
                'status': 'error',
                'message': 'Error calculating investment metrics.',
                'error': str(e)
            }), 500
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Error in prediction endpoint: {e}")
        logger.error(f"Error in prediction endpoint: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

def get_predictions(property_data):
    """Function to get predictions for both sale and rental prices"""
    result = {}
    
    # Sale Price Prediction
    if MODELS['sale'] is not None:
        try:
            sale_features = prepare_sale_features(property_data)
            
            # Make prediction based on model type
            if isinstance(MODELS['sale'], xgb.Booster):
                # For Booster models
                dmatrix = xgb.DMatrix(sale_features)
                sale_prediction = MODELS['sale'].predict(dmatrix)
            else:
                # For sklearn wrapper models
                sale_prediction = MODELS['sale'].predict(sale_features)
                
            result['predictedSalePrice'] = round(float(sale_prediction[0]), 2)
            print(f"Sale price prediction: {result['predictedSalePrice']}")
        except Exception as e:
            print(f"Error in sale price prediction for property: {e}")
            # No fallback here - just raise the exception
            raise
    else:
        # Don't predict if model is not available
        raise Exception("Sale price model is not loaded")
    
    # Rental Price Prediction
    if MODELS['rental'] is not None:
        try:
            rental_features = prepare_rental_features(property_data)
            rental_prediction = MODELS['rental'].predict(rental_features)
            result['predictedRent'] = round(float(rental_prediction[0]), 2)
            print(f"Rental price prediction: {result['predictedRent']}")
        except Exception as e:
            print(f"Error in rental price prediction for property: {e}")
            # No fallback here - just raise the exception
            raise
    else:
        # Don't predict if model is not available
        raise Exception("Rental price model is not loaded")
    
    return result

def prepare_sale_features(input_data):
    """Prepare features for sale price prediction"""
    try:
        # Create feature array with values in proper order
        features = [
            input_data['zipcode'],
            input_data['bedrooms'],
            input_data['bathrooms'],
            input_data['propertyType'],
            input_data['livingArea'],
            input_data['lotArea'],
            input_data['daysOnMarket'],
            input_data['yearBuilt'],
            input_data['hasGarage'],
            input_data['hasPool'],
            input_data['hasFireplace'],
            input_data['hasBasement'],
            input_data['hasCentralAir'],
            input_data['hasSecuritySystem'],
            input_data['hasSprinklerSystem'],
            input_data['hasSolarPanels']
        ]
        
        # Convert to numeric values where needed
        for i, feature in enumerate(features):
            if isinstance(feature, str) and feature.isdigit():
                features[i] = float(feature)
            elif isinstance(feature, str) and i != 3:  # Skip propertyType
                features[i] = 0.0  # Default for non-numeric values
        
        return np.array(features).reshape(1, -1)
    except Exception as e:
        print(f"Error preparing sale features: {e}")
        raise

def prepare_rental_features(input_data):
    """Prepare features for rental price prediction"""
    try:
        # Create feature array with values in proper order
        features = [
            input_data['zipcode'],
            input_data['bedrooms'],
            input_data['bathrooms'],
            input_data['propertyType'],
            input_data['livingArea'],
            input_data['lotArea'],
            input_data['daysOnMarket'],
            input_data['yearBuilt'],
            input_data['hasGarage'],
            input_data['hasPool'],
            input_data['hasFireplace'],
            input_data['hasBasement'],
            input_data['hasCentralAir'],
            input_data['hasSecuritySystem'],
            input_data['hasSprinklerSystem'],
            input_data['hasSolarPanels']
        ]
        
        # Convert to numeric values where needed
        for i, feature in enumerate(features):
            if isinstance(feature, str) and feature.isdigit():
                features[i] = float(feature)
            elif isinstance(feature, str) and i != 3:  # Skip propertyType
                features[i] = 0.0  # Default for non-numeric values
        
        return np.array(features).reshape(1, -1)
    except Exception as e:
        print(f"Error preparing rental features: {e}")
        raise

# Add health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'models': {
            'sale': MODELS['sale'] is not None,
            'rental': MODELS['rental'] is not None
        }
    })

if __name__ == '__main__':
    # Try to detect the port from environment variables (for container deployments)
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)