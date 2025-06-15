# Agentic Content Generation Workflow

<!-- [![Project Status: Active](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active) -->
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/Python-3.12%2B-blue.svg?style=flat-square&logo=python)](https://www.python.org/)
[![YouTube Demo](https://img.shields.io/badge/YouTube-Demo-blue?style=flat-square&logo=youtube)](https://youtu.be/Rt3C6aTqe2U)

A proof-of-concept system demonstrating an automated, multi-agent pipeline for content generation and versioning. This project showcases how AI agents, human-in-the-loop feedback, and a vector database can be combined to create a sophisticated content workflow.

<!-- ![Workflow Diagram](assets/workflow_diagram.png) -->

## Core Features

*   **Agentic AI Pipeline:** Utilizes distinct LLM-powered agents (Writer, Reviewer) that work sequentially to rewrite and critique content, with the ability to incorporate human feedback for iterative refinement.
*   **Human-in-the-Loop (HITL):** A robust interactive Command-Line Interface (CLI) allows a human to act as an editor and reviewer, providing feedback or final approval for drafts.
*   **Vector-Based Versioning:** Every version of the content—original, AI drafts, and approved—is saved and indexed in a **ChromaDB** vector database, creating a complete, searchable history of the content's evolution.
*   **Intelligent Retrieval:** The system can reliably retrieve the final "approved" version using metadata filters or perform a semantic search to find the most contextually relevant versions based on a query.
*   **Automated Data Ingestion:** Uses **Playwright** to reliably scrape source content, with a smart file-based cache to prevent redundant scraping on subsequent runs.

## Technical Highlights

*   **Modular Architecture:** The logic is cleanly separated into modules for scraping (`scraper.py`), AI agents (`agents.py`), database interactions (`database.py`), and configuration (`config.py`).
*   **Secure Configuration:** Secrets like API keys are managed via a `.env` file, which is kept out of version control for security. An `.env.example` file is provided as a template.
*   **Automated Setup:** A `setup.py` script ensures a reliable and user-friendly installation process for all dependencies, including Playwright's browser binaries.

## Local Setup & Installation

This project includes an automated setup script for a smooth installation.

**1. Clone the Repository**
```bash
git clone https://github.com/YOUR_USERNAME/AI-Content-Workflow-Engine.git
cd AI-Content-Workflow-Engine
```

**2. Configure Your Environment**
This project requires an API key from Google AI Studio.
*   Create a copy of the example environment file. On Mac/Linux: `cp .env.example .env`. On Windows, just copy and rename the file.
*   Open the new `.env` file and add your `GEMINI_API_KEY`.

**3. Run the Automated Setup**
This single command will install all Python libraries and the necessary Playwright browsers.
```bash
python setup.py
```

## How to Run the Workflow

Once the setup is complete, start the interactive command-line application:
```bash
python main.py
```
Follow the on-screen commands (`spin`, `search`, `inspect`, `exit`) to interact with the system.

---
* Project by **MySelfMankar** 