# LLM-Software-Testing-Tool
This utility is a fully functional test generation application designed to automate the creation of quality assurance assets. By utilizing Large Language Models (LLMs) and a recursive project parser, the tool analyzes source code and generates comprehensive Whitebox and Blackbox test suites tailored to specific project requirements

Recursive Code Analysis: automatically explores the "Artifact Under Study" to map each function and class.

Automated Whitebox Testing: Creates test cases for statement and condition coverage (optional Block and Path coverage). Includes Block and path coverage for bonus credit

Automated blackbox testing generates boundary value analysis (BVA) and equivalence class partitioning (ECP) situations.

CI/CD Ready: generates automation files (GitHub Actions YAML or Dockerfile) for integrating tests into any workflow.

# Prerequisites:

- **Python 3.x**

- **An API key for your chosen LLM (OpenAI/Anthropic)**

The project source code you wish to test (the "Artifact Under Study")

# Installation:

1.Clone this repository to your local machine.
2.Install dependencies: pip install -r requirements.txt
3.Set your API Key: export LLM_API_KEY='your_key_here'

# Usage
Place your detailed specifications in a Context.json file in the root directory.

Run the utility: python main.py --path /path/to/your/project

Find your generated test cases in the newly created /Test_Folder

# Deliverables
- Upon execution, the tool provides:
- Test Suite: A folder containing all generated test scripts.
- Automation File: A package.json or workflow.yaml to run the tests automatically.
- Documentation: A data model overview and usage guide for the generated tests.
