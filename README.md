# RAG_Product_Research

Product's Market Analysis using RAG
This repository contains a streamlined architecture for conducting market analysis on various companies, utilizing a combination of web scraping, data processing, and language modeling techniques.

# Architecture
1. Dependencies Installation: Ensure all required dependencies are installed by referring to the "requirements.txt" file.
2. Configuration: Set up the system by providing the necessary API keys for the language model and Tavlily search.
3. Execution: Run the app.py script, and utilize Streamlit to input the desired company name.
4. Report Generation: The system processes the input, retrieves relevant data, and generates a comprehensive report about the company.

![image](https://github.com/ManojAthreya/RAG_Product_Research/assets/39020374/038346fc-3aea-4129-838f-3b42d4efcea3)

# Cost for a query using ChatGPT 3.5 Turbo Model

![image](https://github.com/ManojAthreya/RAG_Product_Research/assets/39020374/608bd55c-6601-4e55-a310-68ce4a4104c3)

# Output  (8 pages of PDF file)

![image](https://github.com/ManojAthreya/RAG_Product_Research/assets/39020374/c167ded1-b35a-4ef5-8443-cfdc112f388e)

# Technology
- **Python Libraries**: os, json, nest_asyncio
- **Framework**: Langchain
- **Search Engine**: Tavily AI API
- **Vector Database**: Chroma DB
- **Language Models**: Google Gemini Pro, GPT-3.5-Turbo, Ollama (Llama2:chat), Together AI models
- **PHP Library**: fPDF (for PDF generation)
- **Front End**: Streamlit
- **Tracing & Logging**: LangSmith

# Functionality
- **User Input**: Users provide a company name as input.
- **Search Query Generation**: The system generates multiple search queries based on the provided company name.
- **Web Links Scraping**: Relevant data is extracted from websites corresponding to the generated search queries. This is facilitated by Tavily API Search and Wikipedia scraping.
- **Data Storage**: Extracted data is efficiently stored in the Chroma DB Vector Database, optimizing retrieval and processing.
- **Language Model Analysis**: The project supports various language models such as ChatGPT, Ollama, Together AI, and Google Gemini Pro. These models analyze the collected data to generate comprehensive reports about the company.
- **Report Generation**: A detailed report summarizing the findings is created using tools like fPDF, a PHP library for PDF generation.
- **Log Traces**: LangSmith helped to log traces for testing, deploying and monitoring the outputs generated and their latency.

# Getting Started
To utilize this system for conducting market analysis, follow these steps:
1. Clone the repository to your local machine.
2. Install the required dependencies using pip install -r requirements.txt.
3. Configure the system by providing appropriate API keys for the language model and Tavlily search.
4. Run the app.py script using Python.
5. Access the Streamlit interface, input the company name, and generate the report.
