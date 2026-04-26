# LLM-Software-Testing-Tool

This utility is a fully functional test generation application designed to automate the creation of quality assurance assets. By utilizing a simulated Large Language Model (LLM) engine and a recursive project parser, the tool analyzes source code and generates comprehensive Whitebox and Blackbox test suites tailored to specific project requirements.

---

## Features

**Recursive Code Analysis:**  
Automatically explores the "Artifact Under Study" to map each function and class.

**Automated Whitebox Testing:**  
Creates test cases for statement and condition coverage. Includes optional Block and Path coverage for extended evaluation.

**Automated Blackbox Testing:**  
Generates Boundary Value Analysis (BVA) and Equivalence Class Partitioning (ECP) test cases.

**CI/CD Ready:**  
Generates automation files (GitHub Actions YAML) for integrating tests into development workflows.

---

## Prerequisites

- Python 3.x  
- The project source code you wish to test (the "Artifact Under Study")  

> Note: This version uses a simulated LLM engine and does NOT require an API key.

---

## Installation

1. Clone this repository to your local machine  
2. Install dependencies (if any):  
   ```bash
   pip install -r requirements.txt
