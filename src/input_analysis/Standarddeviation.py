import pandas as pd
import numpy as np
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# File paths
PRODUCT_FILE = "Output File/excel/product_analysis.xlsx"
COMPETITOR_FILE = "Output File/excel/competitor_analysis.xlsx"
OUTPUT_FOLDER = "StreamlitTempApp/data/output_generated_file/Output File/excel"
OUTPUT_FILE = os.path.join(OUTPUT_FOLDER, "top_3_sd_results.xlsx")

# Check if files exist
if not os.path.exists(PRODUCT_FILE) or not os.path.exists(COMPETITOR_FILE):
    raise FileNotFoundError("One or more required files are missing.")

# Load data
product_data = pd.read_excel(PRODUCT_FILE)
competitor_data = pd.read_excel(COMPETITOR_FILE)

# Criteria
branding_criteria = ["Logo Placement", "Consistency", "Alignment", "Brand Colors", "Typography Consistency", "Brand Identity", "Template Consistency"]
content_marketing_criteria = ["Content Visibility", "Engagement Cues", "Storytelling", "Aesthetic Coherence", "Content Relevance"]
social_media_marketing_criteria = ["Font Size", "Visibility of Text", "Alignment", "Aesthetic Appeal", "Repetitiveness"]

# Filter criteria
def filter_existing_criteria(data, criteria):
    return [criterion for criterion in criteria if criterion in data.columns]

branding_criteria = filter_existing_criteria(product_data, branding_criteria)
content_marketing_criteria = filter_existing_criteria(product_data, content_marketing_criteria)
social_media_marketing_criteria = filter_existing_criteria(product_data, social_media_marketing_criteria)

# Mean cache for efficiency
def calculate_mean_criterion_value(product_data, competitor_data, criterion):
    combined_values = np.concatenate([
        product_data[criterion].dropna().values,
        competitor_data[criterion].dropna().values,
    ])
    return np.nanmean(combined_values)

# Main matrix calculation
def calculate_sd_comparison_matrix(product_data, competitor_data, category_criteria):
    sd_matrix = np.zeros((6, 6))
    mean_values = {criterion: calculate_mean_criterion_value(product_data, competitor_data, criterion) for criterion in category_criteria}
    for i in range(6):
        for j in range(6):
            product_scores = product_data.iloc[i][category_criteria].values
            competitor_scores = competitor_data.iloc[j][category_criteria].values
            score_diff = np.nan_to_num(product_scores - competitor_scores, nan=lambda idx: mean_values[category_criteria[idx]])
            sd_matrix[i, j] = np.std(score_diff)
    return pd.DataFrame(sd_matrix, index=[f"Product_{i+1}" for i in range(6)], columns=[f"Competitor_{j+1}" for j in range(6)])

# Top results
def find_top_non_repetitive_sd(sd_matrix, product_data, competitor_data, category, top_count=3):
    top_results, used_product_images, used_competitor_images = [], set(), set()
    for i in range(sd_matrix.shape[0]):
        for j in range(sd_matrix.shape[1]):
            if len(top_results) >= top_count:
                continue
            product_image, competitor_image = product_data.iloc[i]['Image'], competitor_data.iloc[j]['Image']
            if product_image not in used_product_images and competitor_image not in used_competitor_images:
                top_results.append((category, product_image, competitor_image, sd_matrix.iloc[i, j]))
                used_product_images.add(product_image)
                used_competitor_images.add(competitor_image)
    return top_results

# Calculate matrices and top results
branding_sd_matrix = calculate_sd_comparison_matrix(product_data, competitor_data, branding_criteria)
branding_top_3 = find_top_non_repetitive_sd(branding_sd_matrix, product_data, competitor_data, "Brand Marketing")

# Save to Excel
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
pd.DataFrame(branding_top_3, columns=['Category', 'Product_Image_Name', 'Competitor_Image_Name', 'SD_Value']).to_excel(OUTPUT_FILE, index=False)
logging.info(f"Results saved to {OUTPUT_FILE}")
