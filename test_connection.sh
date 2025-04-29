#!/bin/bash

echo "Testing backend server..."
curl http://localhost:5001/test

echo -e "\nTesting POST endpoint..."
curl -X POST http://localhost:5001/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "bedrooms": 2,
    "bathrooms": 1,
    "sqft": 1000,
    "zipcode": "02108",
    "property_type": "SINGLE_FAMILY"
  }' 