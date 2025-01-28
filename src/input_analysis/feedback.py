import openai
import os
import requests
import logging
import json
import re

# Set up OpenAI API key (replace with your actual API key)
openai.api_key = 'sk-svcacct-PGXs0i97Eb2T186xp5w8hbKQZ6w_vb48YagbTuCrYznNuH9wAk7TUC_Sk60qwT3BlbkFJbt5lbbbOBVEqAus-uNDQ6SIjCHmYJNizcTPzuhUvgPVvnAeQxjic8YYiDQvAA'

# Define the paths to the input files and output file
input_dir = "StreamlitTempApp/data/output_generated_file"
branding_file = os.path.join(input_dir, 'Product_branding.txt')
content_marketing_file = os.path.join(input_dir, 'Product_content_marketing.txt')
smm_file = os.path.join(input_dir, 'Product_smm.txt')

# Function to read file content
def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Read the content from the three files
branding_content = read_file(branding_file)
content_marketing_content = read_file(content_marketing_file)
smm_content = read_file(smm_file)

# LLM request function based on your provided syntax
def request_analysis(system_message, user_message, model="gpt-4o-mini", max_tokens=1500):
    headers = {
        'Authorization': f'Bearer {openai.api_key}',
        'Content-Type': 'application/json'
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ],
        "max_tokens": max_tokens
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    if response.status_code == 200:
        try:
            return response.json().get("choices", [{}])[0].get("message", {}).get("content", "Unexpected response format")
        except Exception as e:
            logging.error(f"Error parsing response: {e}")
            logging.debug(f"Raw Response: {response.text}")
            return "Error parsing the response."
    else:
        logging.error(f"Request failed with status code {response.status_code}")
        return f"Error: {response.status_code}"

# Function to extract "Don'ts" using regex
import re

# Function to extract "Don'ts" using regex
def extract_donts(text):
    # Updated pattern to account for "Don't" or alternative phrasing.
    pattern = re.findall(r"(?:-\s*Don't\s+|-\s*)([^\n]+)", text)
    return [f"Don't {dont.strip()}" for dont in pattern if not dont.startswith("Don't")]



# Function to get "Don'ts" from GPT
def get_donts_from_gpt(content, category):
    system_message = (
    "You are an expert in branding, content marketing, and social media marketing. "
    "Based on the provided content, generate a list of 3-6 word 'Don'ts' for the company. "
    "Ensure each point MUST start with 'Don't' and write them as concise, actionable bullet points."
    )

    user_message = f"Category: {category}\nContent:\n{content}\n\nPlease provide the 'Don'ts' in bullet points."

    response = request_analysis(system_message, user_message)
    if response != "Error parsing the response.":
        return extract_donts(response)
    return []

# Function to clean text by removing unwanted characters (quotes, commas, periods)
def clean_text(text):
    # Remove quotes, commas, periods, and extra whitespace
    cleaned_text = re.sub(r'[\"\'.,]+', '', text).strip()
    return cleaned_text

# Get the "Don'ts" lists from GPT and clean them
branding_donts = get_donts_from_gpt(branding_content, "Brand Marketing")
content_marketing_donts = get_donts_from_gpt(content_marketing_content, "Content Marketing")
smm_donts = get_donts_from_gpt(smm_content, "Social Media Marketing")

# Clean the lists
branding_donts_cleaned = [clean_text(dont) for dont in branding_donts]
content_marketing_donts_cleaned = [clean_text(dont) for dont in content_marketing_donts]
smm_donts_cleaned = [clean_text(dont) for dont in smm_donts]

# Store cleaned results in lists
donts_output = {
    "Brand Marketing": branding_donts_cleaned,
    "Content Marketing": content_marketing_donts_cleaned,
    "Social Media Marketing": smm_donts_cleaned
}

# Print cleaned results
print(json.dumps(donts_output, indent=4))

# Save cleaned output to a file
output_file = os.path.join(input_dir, 'Product_donts_output_cleaned.txt')
with open(output_file, 'w') as file:
    for category, dont_list in donts_output.items():
        file.write(f"{category}:\n")
        for dont in dont_list:
            file.write(f"- {dont}\n")
        file.write("\n")

print(f"Cleaned output saved to {output_file}")



openai_api_key = 'sk-svcacct-PGXs0i97Eb2T186xp5w8hbKQZ6w_vb48YagbTuCrYznNuH9wAk7TUC_Sk60qwT3BlbkFJbt5lbbbOBVEqAus-uNDQ6SIjCHmYJNizcTPzuhUvgPVvnAeQxjic8YYiDQvAA'


# Function to strip unwanted characters (quotes, commas, periods, etc.)
def clean_text(text):
    # Remove quotes, commas, periods, and extra whitespace
    cleaned_text = re.sub(r'[\"\'.,]+', '', text).strip()
    return cleaned_text

# Function to strip inverted commas from list items
def strip_inverted_commas(items):
    return [item.replace('"', '').replace("'", "").strip() for item in items]

# Function to send requests to OpenAI API
def request_analysis(system_message, user_message, model="gpt-4", max_tokens=1500):
    headers = {
        'Authorization': f'Bearer {openai_api_key}',
        'Content-Type': 'application/json'
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ],
        "max_tokens": max_tokens
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    if response.status_code == 200:
        try:
            return response.json().get("choices", [{}])[0].get("message", {}).get("content", "Unexpected response format")
        except Exception as e:
            logging.error(f"Error parsing response: {e}")
            return "Error parsing the response."
    else:
        logging.error(f"Request failed with status code {response.status_code}")
        return f"Error: {response.status_code}"

# Function to generate suggestions from GPT
def get_suggestions_from_gpt(product_donts, category):
    system_message = """
    You are an expert marketing consultant. Based on the company's weaknesses, generate a list of suggestions for each category.
    The number of suggestions should match the number of "Don'ts" provided.
    Each suggestion should be 3-6 words, practical, and tailored to address the specific weakness.
    Provide output as a clean list without numbers, brackets, or extra formatting.
    """
    user_message = f"""
    Category: {category}
    Product Company's Weaknesses (Don'ts): {product_donts}
    Provide only the suggestions list as output, separated by new lines.
    """
    response = request_analysis(system_message, user_message)
    if response != "Error parsing the response.":
        # Clean up the response by removing unwanted symbols
        suggestions = [clean_text(line.strip().replace("-", "").strip()) for line in response.strip().split("\n") if line.strip()]
        return suggestions
    return []

# Generate lists of suggestions for each category
branding_suggestions = get_suggestions_from_gpt(branding_donts, "Brand Marketing")
content_marketing_suggestions = get_suggestions_from_gpt(content_marketing_donts, "Content Marketing")
smm_suggestions = get_suggestions_from_gpt(smm_donts, "Social Media Marketing")

# Prepare output dictionary
output = {
    "Brand Marketing": branding_suggestions,
    "Content Marketing": content_marketing_suggestions,
    "Social Media Marketing": smm_suggestions
}

# Print the output for verification
for category, items in output.items():
    print(f"{category}:")
    for item in items:
        print(f'- {item}')
    print()

# Save output to a file
output_file = os.path.join("StreamlitTempApp/data/output_generated_file", "Product_suggestions_output_cleaned.txt")


print("This branding don't ")
print(branding_donts_cleaned)

# Save cleaned output to a file
output_file = os.path.join(input_dir, 'Product_output_cleaned.txt')

with open(output_file, 'w') as file:
    for category in donts_output.keys():
        # Write the category
        file.write(f"{category}:\n")
        file.write("Don'ts:\n")
        # Write the "Don'ts"
        for dont in donts_output[category]:
            file.write(f"- {dont}\n")
        file.write("\nSuggestions:\n")
        # Write the corresponding suggestions
        suggestions = output[category]
        for suggestion in suggestions:
            file.write(f"- {suggestion}\n")
        file.write("\n" + "="*50 + "\n\n")

print(f"All outputs saved to {output_file}")
