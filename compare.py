from fuzzywuzzy import fuzz

def match_model_numbers(model_numbers, affected_products, threshold=70):
    results = []
    
    for model in model_numbers:
        for description in affected_products:
            # Calculate similarity score
            match_percentage = fuzz.partial_ratio(model, description)
            
            # If match percentage exceeds threshold, store the result
            if match_percentage >= threshold:
                results.append({
                    'model_number': model,
                    'alert_description': description,
                    'accuracy': match_percentage
                })
    
    return results


# Input Data
model_numbers = ["Triconex", "Honeywell"]
affected_products = [
    "Schneider electric tricon has an alert on its product.", 
    "schneider electric technial alert",
    "Schneider electric Triconex product has a technical alert.",
    "Technical alert from triconex123 - Schneider",
    "no alerts in this statement"
]

# Match and print results
matches = match_model_numbers(model_numbers, affected_products, threshold=50)

for match in matches:
    print(f"Model: {match['model_number']}\n Description: {match['alert_description']}\n Accuracy: {match['accuracy']}%\n")
