# Attention!
This program is a prototype and is provided as an example. It is not part of the Allure TestOps product. Implementation, use, and maintenance are entirely the responsibility of the user.

# Functionality
The program retrieves a test case from Allure TestOps by its ID and converts all its steps into a shared step in Allure TestOps with the same name.

# How It Works
Using the API, the program reads the name and steps of the test case from Allure TestOps by ID. Then, using the API, it creates a new shared step with the same name and fills it with the steps from the test case.

# Limitations
1. All steps of the test case are retrieved.
2. Attachments are not retrieved.

# Usage Steps:
1. In the file api_shared_step.py, specify your instance in INSTANCE_NAME.
2. In the file api_shared_step.py, specify your project ID in PROJECT_ID.
3. In the file api_shared_step.py, specify the ID of the test case whose steps you want to convert into a shared step in TESTCASE_ID.
4. Obtain a user token in the TestOps interface.
5. Create a .env file in the root folder of the program and enter your token in the format: TESTOPS_TOKEN = "*******-****-****-****-************".
6. Run the file api_shared_step.py.
7. Done! A new shared step has been created from the test case steps.


