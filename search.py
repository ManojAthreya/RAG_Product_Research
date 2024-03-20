import json
import os
from langchain_community.tools.tavily_search import TavilySearchResults
import nest_asyncio
from dotenv import load_dotenv

load_dotenv()
nest_asyncio.apply()

TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")

def web_search(company_name):
    directory = "./"
    file_name = company_name+"_data.json"
    
    queries = [
                "Who are "
                + company_name
                + "'s customers and what is their customer retention strategy and customer support",
                "What are "
                + company_name
                + "'s strengths, weaknesses, opportunities, and threats",
                "Who are the key players in "
                + company_name
                + "'s industry and what including their market share, products or services offered",
                "Who are "
                + company_name
                + "'s main competitors and key players in its industry ",
                "What are the key trends in consumer behavior, technological advancements in  "
                + company_name
                + "'s industry?",
                "What is "
                + company_name
                + "'s recent revenue, profit margin, return on investment and market share growth rate?",
                "What is "
                + company_name
                + "'s recent target market,products or services features, benefits,",
                "What are "
                + company_name
                + "'s recent marketing,sales and pricing strategy with numbers",
                "give details about "
                + company_name
                + "'s recent partnerships, collaborations and it's innovation",
            ]
    
    
    if os.path.exists(os.path.join(directory, file_name)):
        with open(company_name+"_data.json", "r", encoding='utf-8') as json_file:
            data = json.load(json_file)
    else:
        results = {}
        tool = TavilySearchResults()
        for query in queries:
            result_list = tool.invoke({"query": query})
            links = [item["url"] for item in result_list]

            results[query] = links

            # Storing links in JSON file
        with open(company_name+"_data.json", "w", encoding='utf-8') as json_file:
            json.dump(results, json_file, indent=1)
                
        with open(company_name+"_data.json", "r", encoding='utf-8') as json_file:
            data = json.load(json_file)

    unique_urls = set()
    cleaned_data = {}
    for key, urls in data.items():
        for url in urls:
            if url not in unique_urls:
                unique_urls.add(url)
                if key in cleaned_data:
                    cleaned_data[key].append(url)
                else:
                    cleaned_data[key] = [url]
    return cleaned_data