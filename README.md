
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
Use unique credentials — each user operates in an isolated sandbox.
Tabs are not allowed in YAML; use spaces only.
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


Jenkins Setup using Docker
docker run -d --name jenkins \
  -p 8080:8080 -p 50000:50000 \
  jenkins/jenkins:lts-jdk11


Retrieve admin password:

docker logs jenkins

Open Jenkins in browser:

http://localhost:8080

Install Required Plugins
Plugin,
Git,
Pipeline,
Credentials,
docker-pipeline.
 
 Pipeline Job Setup
 Create New Item → Pipeline,
 Set source code: GitHub Repo URL,
 Branch: main,
 Pipeline script from SCM → Jenkinsfile.

Jenkinsfile (Automation Pipeline)

Stages implemented:

Stage	Purpose
Checkout SCM	Pull code from GitHub
Setup Environment	Create venv + install requirements
Run Automation	Execute Python test workflow

Jenkins Pipeline success	
Console output (Run Automation)

Started by user K R Prudhvi Reddy

Obtained Jenkinsfile from git https://github.com/prudhvireddy20/Test_Automation_Framework.git
[Pipeline] Start of Pipeline
[Pipeline] node
Running on Jenkins
 in /var/jenkins_home/workspace/test-automation-pipeline
[Pipeline] {
[Pipeline] stage
[Pipeline] { (Declarative: Checkout SCM)
[Pipeline] checkout
The recommended git tool is: git
No credentials specified
 > git rev-parse --resolve-git-dir /var/jenkins_home/workspace/test-automation-pipeline/.git # timeout=10
Fetching changes from the remote Git repository
 > git config remote.origin.url https://github.com/prudhvireddy20/Test_Automation_Framework.git # timeout=10
Fetching upstream changes from https://github.com/prudhvireddy20/Test_Automation_Framework.git
 > git --version # timeout=10
 > git --version # 'git version 2.39.5'
 > git fetch --tags --force --progress -- https://github.com/prudhvireddy20/Test_Automation_Framework.git +refs/heads/*:refs/remotes/origin/* # timeout=10
 > git rev-parse refs/remotes/origin/main^{commit} # timeout=10
Checking out Revision bee7766adbd9c4f3b4e91fd48ac9cf7b7677ad2f (refs/remotes/origin/main)
 > git config core.sparsecheckout # timeout=10
 > git checkout -f bee7766adbd9c4f3b4e91fd48ac9cf7b7677ad2f # timeout=10
Commit message: "fix"
 > git rev-list --no-walk bee7766adbd9c4f3b4e91fd48ac9cf7b7677ad2f # timeout=10
[Pipeline] }
[Pipeline] // stage
[Pipeline] withEnv
[Pipeline] {
[Pipeline] stage
[Pipeline] { (Checkout)
[Pipeline] checkout
The recommended git tool is: git
No credentials specified
 > git rev-parse --resolve-git-dir /var/jenkins_home/workspace/test-automation-pipeline/.git # timeout=10
Fetching changes from the remote Git repository
 > git config remote.origin.url https://github.com/prudhvireddy20/Test_Automation_Framework.git # timeout=10
Fetching upstream changes from https://github.com/prudhvireddy20/Test_Automation_Framework.git
 > git --version # timeout=10
 > git --version # 'git version 2.39.5'
 > git fetch --tags --force --progress -- https://github.com/prudhvireddy20/Test_Automation_Framework.git +refs/heads/*:refs/remotes/origin/* # timeout=10
 > git rev-parse refs/remotes/origin/main^{commit} # timeout=10
Checking out Revision bee7766adbd9c4f3b4e91fd48ac9cf7b7677ad2f (refs/remotes/origin/main)
 > git config core.sparsecheckout # timeout=10
 > git checkout -f bee7766adbd9c4f3b4e91fd48ac9cf7b7677ad2f # timeout=10
Commit message: "fix"
[Pipeline] }
[Pipeline] // stage
[Pipeline] stage
[Pipeline] { (Setup Environment)
[Pipeline] sh
+ python3 -m venv .venv
+ . .venv/bin/activate
+ deactivate nondestructive
+ [ -n  ]
+ [ -n  ]
+ [ -n  -o -n  ]
+ [ -n  ]
+ unset VIRTUAL_ENV
+ unset VIRTUAL_ENV_PROMPT
+ [ ! nondestructive = nondestructive ]
+ VIRTUAL_ENV=/var/jenkins_home/workspace/test-automation-pipeline/.venv
+ export VIRTUAL_ENV
+ _OLD_VIRTUAL_PATH=/opt/java/openjdk/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
+ PATH=/var/jenkins_home/workspace/test-automation-pipeline/.venv/bin:/opt/java/openjdk/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
+ export PATH
+ [ -n  ]
+ [ -z  ]
+ _OLD_VIRTUAL_PS1=$ 
+ PS1=(.venv) $ 
+ export PS1
+ VIRTUAL_ENV_PROMPT=(.venv) 
+ export VIRTUAL_ENV_PROMPT
+ [ -n  -o -n  ]
+ pip install --upgrade pip
Requirement already satisfied: pip in ./.venv/lib/python3.11/site-packages (23.0.1)
Collecting pip
  Downloading pip-25.3-py3-none-any.whl (1.8 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.8/1.8 MB 823.0 kB/s eta 0:00:00
Installing collected packages: pip
  Attempting uninstall: pip
    Found existing installation: pip 23.0.1
    Uninstalling pip-23.0.1:
      Successfully uninstalled pip-23.0.1
Successfully installed pip-25.3
+ pip install -r requirements.txt
Collecting requests==2.31.0 (from -r requirements.txt (line 1))
  Downloading requests-2.31.0-py3-none-any.whl.metadata (4.6 kB)
Collecting PyYAML==6.0.2 (from -r requirements.txt (line 2))
  Downloading PyYAML-6.0.2-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (2.1 kB)
Collecting charset-normalizer<4,>=2 (from requests==2.31.0->-r requirements.txt (line 1))
  Downloading charset_normalizer-3.4.4-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (37 kB)
Collecting idna<4,>=2.5 (from requests==2.31.0->-r requirements.txt (line 1))
  Downloading idna-3.11-py3-none-any.whl.metadata (8.4 kB)
Collecting urllib3<3,>=1.21.1 (from requests==2.31.0->-r requirements.txt (line 1))
  Downloading urllib3-2.5.0-py3-none-any.whl.metadata (6.5 kB)
Collecting certifi>=2017.4.17 (from requests==2.31.0->-r requirements.txt (line 1))
  Downloading certifi-2025.10.5-py3-none-any.whl.metadata (2.5 kB)
Downloading requests-2.31.0-py3-none-any.whl (62 kB)
Downloading PyYAML-6.0.2-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (762 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 763.0/763.0 kB 337.9 kB/s  0:00:01
Downloading charset_normalizer-3.4.4-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (151 kB)
Downloading idna-3.11-py3-none-any.whl (71 kB)
Downloading urllib3-2.5.0-py3-none-any.whl (129 kB)
Downloading certifi-2025.10.5-py3-none-any.whl (163 kB)
Installing collected packages: urllib3, PyYAML, idna, charset-normalizer, certifi, requests

Successfully installed PyYAML-6.0.2 certifi-2025.10.5 charset-normalizer-3.4.4 idna-3.11 requests-2.31.0 urllib3-2.5.0
[Pipeline] }
[Pipeline] // stage
[Pipeline] stage
[Pipeline] { (Run Automation)
[Pipeline] sh
+ . .venv/bin/activate
+ deactivate nondestructive
+ [ -n  ]
+ [ -n  ]
+ [ -n  -o -n  ]
+ [ -n  ]
+ unset VIRTUAL_ENV
+ unset VIRTUAL_ENV_PROMPT
+ [ ! nondestructive = nondestructive ]
+ VIRTUAL_ENV=/var/jenkins_home/workspace/test-automation-pipeline/.venv
+ export VIRTUAL_ENV
+ _OLD_VIRTUAL_PATH=/opt/java/openjdk/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
+ PATH=/var/jenkins_home/workspace/test-automation-pipeline/.venv/bin:/opt/java/openjdk/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
+ export PATH
+ [ -n  ]
+ [ -z  ]
+ _OLD_VIRTUAL_PS1=$ 
+ PS1=(.venv) $ 
+ export PS1
+ VIRTUAL_ENV_PROMPT=(.venv) 
+ export VIRTUAL_ENV_PROMPT
+ [ -n  -o -n  ]
+ python3 main.py --config config.yml
2025-11-02 16:51:27,647 | INFO     | root | Logging initialized at INFO level
2025-11-02 16:51:29,321 | INFO     | root | Logged in as candidate_user
2025-11-02 16:51:29,321 | INFO     | root | Starting 3 worker(s)
2025-11-02 16:51:29,323 | INFO     | runner | Running test case 'disable-backend-vs-1' for VS 'backend-vs-t1r_1000-1'
2025-11-02 16:51:29,326 | INFO     | runner | Running test case 'sample-case-2' for VS 'some-other-vs'
2025-11-02 16:51:31,414 | ERROR    | runner | Virtual Service named some-other-vs not found
2025-11-02 16:51:31,415 | INFO     | root | Test 'sample-case-2' finished: False
2025-11-02 16:51:31,585 | INFO     | runner | Pre-Validation: VS backend-vs-t1r_1000-1 enabled=True
2025-11-02 16:51:31,585 | INFO     | runner | Triggering PUT to disable VS uuid=virtualservice-2ccaddb9-a3be-458e-9ad5-c0be41ce28e3
2025-11-02 16:51:31,695 | INFO     | runner | Post-validation GET for uuid=virtualservice-2ccaddb9-a3be-458e-9ad5-c0be41ce28e3
2025-11-02 16:51:31,796 | INFO     | runner | Post-Validation: enabled=False
2025-11-02 16:51:31,796 | INFO     | runner | Test PASS: VS backend-vs-t1r_1000-1 disabled
2025-11-02 16:51:31,796 | INFO     | root | Test 'disable-backend-vs-1' finished: True
Results: {'sample-case-2': False, 'disable-backend-vs-1': True}
[Pipeline] }
[Pipeline] // stage
[Pipeline] stage
[Pipeline] { (Declarative: Post Actions)
[Pipeline] echo
Automation completed successfully
[Pipeline] }
[Pipeline] // stage
[Pipeline] }
[Pipeline] // withEnv
[Pipeline] }
[Pipeline] // node
[Pipeline] End of Pipeline
Finished: SUCCESS



 Evaluation Mapping
Requirement	Status
YAML-driven framework	-- Yes
Parallel execution	-- Yes
Mock SSH/RDP components	-- Included
Jenkins automated pipeline	-- Working


Author
K R Prudhvi Reddy
Cybersecurity & Cloud Automation Enthusiast
GitHub: https://github.com/prudhvireddy20
