
1. Overview

### Objective
Design and implement a Python-based test framework that:
- Uses YAML configuration** for endpoints, credentials, and test data.  
- Supports parallel test execution.  
- Follows four stages: **Pre-Fetcher → Pre-Validation → Task/Trigger → Post-Validation.  
- Interacts with a mock Avi Load Balancer API.  
- Includes mock SSH/RDP methods.


 2. Project Structure

automation-framework/
├── api_client.py # Handles API communication (register, login, GET/PUT)
├── runner.py # Implements test stages & validation logic
├── utils.py # Logging setup + mock SSH/RDP
├── main.py # Entry point & parallel execution controller
├── config.yml # YAML configuration file
├── requirements.txt # Dependencies
└── README.md # This file

---

3. Installation & Setup

### Prerequisites
- Python 3.9 or newer
- Internet connection (mock API is hosted online)
- `pip`

## Setup Steps
# Clone or copy the project
cd automation-framework

# Create & activate a virtual environment
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt
 4. Configuration
Edit config.yml to match your credentials and target Virtual Service.
base_url: "https://avi-mock-api-production.up.railway.app"
credentials:
  username: "candidate_user"
  password: "candidate_pass"
target_vs_name: "backend-vs-t1r_1000-1"
concurrency: 2
logging:
  level: INFO
test_cases:
  - name: disable-backend-vs-1
    target_vs_name: "backend-vs-t1r_1000-1"
  - name: sample-case-2
    target_vs_name: "some-other-vs"
🔸 Use unique credentials — each user operates in an isolated sandbox.
🔸 Tabs are not allowed in YAML; use spaces only.
5. Running the Framework
python main.py --config config.yml
Expected Flow
    1. Registers & logs in to the mock API.
    2. Fetches tenants, virtual services, and service engines.
    3. Locates the target VS (backend-vs-t1r_1000-1).
    4. Validates that it’s enabled.
    5. Sends a PUT request to disable it.
    6. Performs post-validation to confirm "enabled": false.
Example Console Output
2025-10-31 16:20:10 INFO api_client: Registered user successfully
2025-10-31 16:20:11 INFO api_client: Logged in, token received
2025-10-31 16:20:11 INFO runner: Tenants count: 1
2025-10-31 16:20:11 INFO runner: VirtualServices count: 5
2025-10-31 16:20:11 INFO runner: Pre-Validation: VS backend-vs-t1r_1000-1 enabled=True
2025-10-31 16:20:12 INFO runner: PUT response: {'enabled': false}
2025-10-31 16:20:12 INFO runner: Post-Validation: enabled=False
Results: {'disable-backend-vs-1': True}
If you see "Test PASS: VS ... disabled" in the logs — your framework works correctly 
