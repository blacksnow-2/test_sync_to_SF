import os
from dotenv import load_dotenv
import requests
import json
import subprocess


commit_message = input("Enter commit message: ")
try:
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", commit_message], check=True)
    subprocess.run(["git", "push"], check=True)
    print("Git push successful.")
except subprocess.CalledProcessError as e:
    print(f"Error executing Git commands: {e}")
    exit(1)





# Load environment variables from .env file
load_dotenv()

# Get environment variables
SNOWFLAKE_ACCOUNT = os.getenv('SNOWFLAKE_ACCOUNT')
SNOWFLAKE_USER = os.getenv('SNOWFLAKE_USER')
SNOWFLAKE_PASSWORD = os.getenv('SNOWFLAKE_PASSWORD')
SNOWFLAKE_ROLE = os.getenv('SNOWFLAKE_ROLE')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

# Ensure the environment variables are set
if not all([SNOWFLAKE_ACCOUNT, SNOWFLAKE_USER, SNOWFLAKE_PASSWORD, SNOWFLAKE_ROLE, GITHUB_TOKEN]):
    print("Please set your credentials in the .env file.")
    exit(1)

# GitHub repository details
REPO_OWNER = "blacksnow-2"
REPO_NAME = "test_sync_to_SF"

# Trigger the GitHub Actions workflow dispatch event
url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/actions/workflows/deploy.yml/dispatches"
headers = {
    "Accept": "application/vnd.github.v3+json",
    "Authorization": f"token {GITHUB_TOKEN}"
}
data = {
    "ref": "main",
    "inputs": {
        "snowflake_account": SNOWFLAKE_ACCOUNT,
        "snowflake_user": SNOWFLAKE_USER,
        "snowflake_password": SNOWFLAKE_PASSWORD,
        "snowflake_role": SNOWFLAKE_ROLE
    }
}
response = requests.post(url, headers=headers, data=json.dumps(data))

if response.status_code == 204:
    print("Workflow triggered successfully.")
else:
    print(f"Failed to trigger workflow: {response.status_code}")
    print(response.text)
