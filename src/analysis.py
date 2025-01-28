import subprocess
import sys
import importlib 
import requests
from PIL import Image
# In analysis.py
import sys
from pathlib import Path

def run_python_file(file_name, company_name):
    # Add the project root to PYTHONPATH
    project_root = str(Path(__file__).parent.parent)
    sys.path.append(project_root)

    # Dynamically import the target script
    try:
        spec = importlib.util.spec_from_file_location("module_name", file_name)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return "Success"  # Adjust based on your script's output
    except Exception as e:
        return f"Error: {str(e)}"

# Retrieve company_name from command-line argument passed from app.py
if len(sys.argv) > 1:
    company_name = sys.argv[1]  # The second argument passed will be the company_name
else:
    company_name = "Default_Company"  # Default value if no argument is passed

# Call the scripts and pass the company_name
product_result = run_python_file('src/input_analysis/product-analysis/product_analysis.py', company_name)    
competitor_result = run_python_file('src/input_analysis/competitor-analysis/competitor_analysis.py', company_name)
stddev_result = run_python_file('src/input_analysis/Standarddeviation.py', company_name)
renamebranding_result = run_python_file('src/input_analysis/renamebranding.py', company_name)
path_result = run_python_file('src/input_analysis/path.py', company_name)
feedback_result = run_python_file('src/input_analysis/feedback.py', company_name)

# Now call brand.py, content.py, and social.py with company_name
brand_result = run_python_file('src/templates/brand.py', company_name)
content_result = run_python_file('src/templates/content.py', company_name)
social_result = run_python_file('src/templates/social.py', company_name)
updated_result = run_python_file('src/Report/updated1.py', company_name)
report_result = run_python_file('src/Report/Report.py', company_name)


import subprocess
import sys
import os

def update_status(status):
    """Update the status file with the current status."""
    with open("src/Report/status.txt", "w") as f:
        f.write(status)

def run_python_file(file_name, company_name):
    """Run a Python file with subprocess and capture its output."""
    try:
        # Run the Python script with the company name passed as an argument
        result = subprocess.run(
            ['python', file_name, company_name],  # Pass company_name as argument
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            return "success", result.stdout  # Return success and the output of the script
        else:
            return "error", f"Error in {file_name}: {result.stderr}"
    except Exception as e:
        return "error", f"An error occurred while running {file_name}: {str(e)}"

def main():
    # Retrieve company_name from command-line argument passed from app.py
    if len(sys.argv) > 1:
        company_name = sys.argv[1]  # The second argument passed will be the company_name
    else:
        company_name = "Default_Company"  # Default value if no argument is passed

    # Initialize status to pending
    update_status("pending")

    # List of scripts to run
    scripts = [
        'src/input_analysis/product-analysis/product_analysis.py',
        'src/input_analysis/competitor-analysis/competitor_analysis.py',
        'src/input_analysis/Standarddeviation.py',
        'src/input_analysis/renamebranding.py',
        'src/input_analysis/path.py',
        'src/input_analysis/feedback.py',
        'src/templates/brand.py',
        'src/templates/content.py',
        'src/templates/social.py',
        'src/Report/updated1.py',
        'src/Report/Report.py'
    ]

    try:
        for script in scripts:
            status, message = run_python_file(script, company_name)
            if status == "error":
                # Update status file with error and stop execution
                update_status(f"error: {message}")
                print(message)
                return
            else:
                print(f"{script} executed successfully.")

        # If all scripts run successfully, update status to done
        update_status("done")
        print("All scripts executed successfully. Report generation complete.")

    except Exception as e:
        # Update status file with the error message
        update_status(f"error: {str(e)}")
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
