import sys
import importlib.util
from pathlib import Path
import requests
from PIL import Image

def update_status(status):
    """Update the status file with the current status."""
    with open("src/Report/status.txt", "w") as f:
        f.write(status)

def run_python_module(module_path, company_name):
    """
    Run a Python module directly in the current environment.
    
    Args:
        module_path (str): Relative path to the Python script (e.g., 'src/input_analysis/product-analysis/product_analysis.py').
        company_name (str): The company name to pass to the script.
    
    Returns:
        tuple: ("success", "") if successful, ("error", error_message) if failed.
    """
    try:
        # Resolve absolute path to the script
        abs_path = str(Path(__file__).parent.parent / module_path)
        
        # Dynamically import the module
        spec = importlib.util.spec_from_file_location("dynamic_module", abs_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules["dynamic_module"] = module
        spec.loader.exec_module(module)
        
        # Pass company_name to the module (if needed)
        module.__dict__["company_name"] = company_name
        
        return "success", ""
    except Exception as e:
        return "error", str(e)

def main():
    print('Running analysis...')
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
        # Run each script
        for script in scripts:
            status, message = run_python_module(script, company_name)
            if status == "error":
                # Update status file with error and stop execution
                update_status(f"error: {message}")
                print(f"Error in {script}: {message}")
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