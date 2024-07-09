import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_job_board(job_title, num_pages):
    base_url = 'https://www.indeed.com/jobs'
    job_list = []

    for page in range(num_pages):
        params = {
            'q': job_title,
            'start': page * 10  # Indeed paginates with start parameter
        }
        response = requests.get(base_url, params=params)
        
        if response.status_code != 200:
            print(f"Failed to retrieve content for page {page + 1}: {response.status_code}")
            continue
        
        soup = BeautifulSoup(response.content, 'html.parser')
        job_elements = soup.find_all('div', class_='jobsearch-SerpJobCard')
        
        for job in job_elements:
            title_element = job.find('h2', class_='title')
            title = title_element.text.strip() if title_element else 'N/A'
            
            company_element = job.find('span', class_='company')
            company = company_element.text.strip() if company_element else 'N/A'
            
            location_element = job.find('div', class_='recJobLoc')
            location = location_element['data-rc-loc'] if location_element else 'N/A'
            
            job_list.append({'Title': title, 'Company': company, 'Location': location})
        
        time.sleep(5)  # Be kind to the server
    
    df = pd.DataFrame(job_list)
    df.to_csv('job_listings.csv', index=False)

# Set the job title to search for and the number of pages to scrape
job_title = 'software engineer'
num_pages = 5

# Start scraping
scrape_job_board(job_title, num_pages)
