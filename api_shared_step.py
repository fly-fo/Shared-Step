import requests
import os
# library for loading data from env
from dotenv import load_dotenv


# function to get bearer token for the required instance using admin token
def get_bearer_token(testops_api_url, testops_token):
    # URL to get the token
    url = f"{testops_api_url}uaa/oauth/token"

    # Request data (in x-www-form-urlencoded format)
    data = {
        "grant_type": "apitoken",
        "scope": "openid",
        "token": testops_token
    }

    # Headers
    headers = {
        "Accept": "application/json"
    }

    # Send POST request
    response = requests.post(url, data=data, headers=headers)

    # Check if request was successful
    if response.status_code == 200:
        try:
            token = response.json().get("access_token")
            if token:
                print("Bearer token received")
                return token
            else:
                print("Response doesn't contain access_token:", response.json())
        except requests.exceptions.JSONDecodeError:
            print("JSON parsing error:", response.text)
    else:
        print("Token retrieval error:", response.status_code, response.text)

# function gets test case name,
# returns text variable
def get_testcase_name(instance_name, testcase_id):
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}",
        "Content-Type": "application/json"  # For proper JSON handling
    }
    response = requests.get(f"https://{instance_name}/api/testcase/{testcase_id}", headers=headers)
    scenario_data = response.json()
    # Extract the name
    scenario_name = scenario_data["name"]
    print(f'Test case name: {scenario_name}')
    return scenario_name

# function gets test case scenario,
# returns list of steps
def get_testcase_scenario(instance_name, testcase_id):
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}",
        "Content-Type": "application/json"  # For proper JSON handling
    }
    response = requests.get(f"https://{instance_name}/api/testcase/{testcase_id}/step", headers=headers)
    scenario_data = response.json()
    # Extract steps
    children_ids = scenario_data["root"]["children"]
    steps = []

    for step_id in children_ids:
        step_data = scenario_data["scenarioSteps"].get(str(step_id))
        if step_data:
            steps.append(step_data["body"])

    # Print the list of steps
    print('Scenario steps:')
    for i, step in enumerate(steps, 1):
        print(f"Step {i}: {step}")

    return steps

# function creates new shared step,
# returns shared step ID
def post_create_sharedstep(instance_name, project_id, sharedstep_name):
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}",
        "Content-Type": "application/json"  # For proper JSON handling
    }
    # Form the request body
    payload = {
        "projectId": project_id,
        "name": sharedstep_name,
        "archived": False
    }
    response = requests.post(f"https://{instance_name}/api/sharedstep", headers=headers, json=payload)
    data = response.json()
    sharedstep_id = data["id"]
    print(f'Shared step created. ID = {sharedstep_id}')
    return sharedstep_id

# function adds scenario from step list to shared step,
# returns nothing
def post_create_scenario_for_sharedstep(instance_name, sharedstep_id, testcase_scenario):
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}",
        "Content-Type": "application/json"  # For proper JSON handling
    }
    print('Adding steps to shared step:')
    for step in testcase_scenario:
        # Form the request body
        payload = {
            "sharedStepId": sharedstep_id,
            "body": step
        }
        print(payload)
        response = requests.post(f"https://{instance_name}/api/sharedstep/step", headers=headers, json=payload)
        print(f'Response status: {response.status_code}')
        print(f'Added step: {step}')
    return

# REQUIRED Replace all placeholder values with your actual TestOps information
# Your Project ID containing manual tests
# Find in: Project Settings → General or URL when viewing project
PROJECT_ID = "REPLACE_WITH_YOUR_PROJECT_ID"
# Manual Test Case ID to convert to shared step
# Find in: Test Case URL when viewing the specific test
TESTCASE_ID = "REPLACE_WITH_YOUR_TESTCASE_ID"
INSTANCE_NAME = "your-instance-name.testops.cloud"

# Load .env file
load_dotenv()
# Get token from .env file
TESTOPS_TOKEN = os.getenv("TESTOPS_TOKEN")
BEARER_TOKEN = get_bearer_token(f"https://{INSTANCE_NAME}/api/", TESTOPS_TOKEN)

# get test case name
TESTCASE_NAME = get_testcase_name(INSTANCE_NAME, TESTCASE_ID)
# get test case scenario
TESTCASE_SCENARIO = get_testcase_scenario(INSTANCE_NAME, TESTCASE_ID)
# create shared step
SHAREDSTEP_ID = post_create_sharedstep(INSTANCE_NAME, PROJECT_ID, TESTCASE_NAME)
# add scenario from step list to shared step
post_create_scenario_for_sharedstep(INSTANCE_NAME, SHAREDSTEP_ID, TESTCASE_SCENARIO)
