import re
from sentence_transformers import SentenceTransformer, util

# Load the SBERT model
model = SentenceTransformer('all-MiniLM-L6-v2')

def extract_model_number(text):
    """Extract potential model numbers from the given text."""
    pattern = r'[A-Za-z0-9]+(?:[-_/\.][A-Za-z0-9]+)*'
    return re.findall(pattern, text)

def match_sbert(models, alerts):
    """Match model numbers to alerts with improved precision."""
    results = []
    for alert in alerts:
        # extract model numbers from the affected_products
        extracted_numbers = extract_model_number(alert)
        for extracted in extracted_numbers:
            for model_number in models:
                # check similarity between model numbers and affected products
                similarity = util.cos_sim(
                    model.encode(model_number), model.encode(extracted)
                ).item()
                similarity_percentage = similarity * 100
                if (similarity_percentage > 75):
                    results.append({
                        'model_number': model_number,
                        'alert': alert,
                        'extracted_number': extracted,
                        'similarity': similarity_percentage
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

# Run Matching
matches = match_sbert(model_numbers, affected_products)

# Print Results
for match in matches:
    print(f"Model: {match['model_number']}\n Extracted: {match['extracted_number']}\n Similarity: {match['similarity']:.2f}%\n Alert: {match['alert']}\n\n")
