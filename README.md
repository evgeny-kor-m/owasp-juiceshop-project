Test Automation with Docker
This project is a template for test automation using Docker, pytest, and Allure. It allows you to run tests in an isolated container and generate detailed reports.

Project Structure
tree -L 3 test_automation_framework
.
├── Makefile                     # Script for automating commands
├── README.md                    # This file
├── allure-reports/              # Generated Allure HTML reports
├── allure-results/              # Raw Allure data
├── docker/                      # Docker configuration files
│   ├── Dockerfile               # Image with the test environment
│   ├── allure-compose.yml       # Services for Allure and Nginx
│   ├── docker-compose.yml       # Main service for running tests
│   ├── .env.example             # Example environment variables
│   └── nginx.conf               # Nginx configuration for reports
├── html-reports/                # Generated HTML report (report.html)
├── owasp-juiceshop/             # Configuration for OWASP JuiceShop
│   └── juice-shop-deployment.yaml
├── pytest.ini                   # Pytest configuration
├── requirements.txt             # Python dependencies
└── test_automation_framework/   # Source code of your project
    ├── api/
    ├── pages/
    └── tests/
        ├──api-tests
        └──ui-tests

Quick Start
1. Environment Setup
   First, create an .env file from the example to configure the environment variables for the project.

# Copy the example file
cp docker/.env.example docker/.env

# Configure the variables as needed
nano docker/.env

2. Running Tests
   Use the make test command to build the image and run tests in the container. After the tests are complete, Allure and HTML reports will be automatically generated.

# Run from the project root
make test

3. Viewing Reports
   After the tests are finished, start the Allure and Nginx servers to view the reports in your browser.

# Start the server
make allure-start

Reports will be available at the following addresses:

Allure Report: http://localhost:5050/allure/

HTML Report: http://localhost:5050/reports/

URL of juse shop site: http://juice-shop.local:8080/

Makefile Commands
Command             Description
make help           Shows a list of available commands.
make test           Runs tests in a Docker container.
make allure-start   Starts the Allure and Nginx servers for viewing reports.
make allure-stop    Stops the Allure and Nginx servers.
make clean          Removes generated reports and temporary files.
make clean-all      Performs a full cleanup, including Docker images.
make status         Shows the status of all Docker services.
make logs           Shows the logs of the test runner container.