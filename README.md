# PayPal Autonomous Procurement Agent

An enterprise-grade, CLI-driven Agentic Commerce engine that autonomously evaluates, audits, and executes secure procurement transactions using the PayPal Developer Platform and Google Gemini AI.

License: MIT
Python: 3.10+
Environment: PayPal Sandbox

---

## Overview

PayPal Autonomous Procurement Agent bridges the gap between natural language intent and secure financial execution. Designed for modern infrastructure provisioning and automated corporate purchasing, the agent analyzes procurement requests, applies strict local compliance guardrails, evaluates financial risk via LLMs, and executes direct server-to-server payments through the PayPal REST API v2.

---

## Key Architecture & Features

- Autonomous Agentic Commerce: Executes end-to-end order creation and automated capture in PayPal Sandbox without requiring manual browser interactions.
- AI-Powered Compliance & Risk Analysis: Utilizes Google Gemini to extract items, calculate costs, assess risk levels (LOW, MEDIUM, HIGH), and enforce hard spending limits.
- Resilient Fallback Engine: Features an intelligent heuristic fallback mechanism ensuring continuous operational reliability even during upstream LLM service spikes.
- Professional Terminal UI: Built with rich to provide real-time structured tables, visual feedback, and secure transaction receipts.
- Enterprise Security: Implements idempotency keys and strict environment variable isolation.

---

## Prerequisites & Installation

Ensure you have Python 3.10+ installed inside your development environment.

1. Clone the repository:
   git clone https://github.com/MigMarGil/paypal-procurement-agent.git
   cd paypal-procurement-agent

2. Set up a virtual environment:
   python3 -m venv venv
   source venv/bin/activate

3. Install dependencies:
   pip install --upgrade pip
   pip install -r requirements.txt

4. Configure environment variables:
   Create a `.env` file in the root directory:
   PAYPAL_CLIENT_ID=your_sandbox_client_id_here
   PAYPAL_CLIENT_SECRET=your_sandbox_client_secret_here
   PAYPAL_MODE=sandbox
   GEMINI_API_KEY=your_gemini_api_key_here

---

## Usage & Execution

The agent provides two primary operational modes via its CLI interface:

### 1. Compliance Audit Mode (No Live Orders)
Evaluates a procurement prompt against corporate risk policies and displays the structured decision table without executing financial calls:
python3 src/cli.py audit --prompt "High-performance GPU Cluster Rental for 150 USD"

### 2. Autonomous Purchase & Settlement Mode
Evaluates the intent, requests user confirmation, connects to PayPal Sandbox, and executes the complete payment lifecycle:
python3 src/cli.py buy --prompt "Cloud Server Infrastructure Setup for 200 USD"

---

## Testing

To verify core components and execution logic:
python3 -m unittest discover tests

---

## License

Distributed under the MIT License. See LICENSE for more information.
