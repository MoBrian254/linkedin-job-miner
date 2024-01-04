import requests
from bs4 import BeautifulSoup
import json

def scrape_linkedin_jobs(query):
    base_url = f'https://www.linkedin.com/jobs/search/?keywords={query}&location='
    headers = {
      'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0.2; SM-T535) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.74 Safari/537.36'
    }
    response = requests.get(base_url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        job_listings = soup.find_all('li', class_='job-result-card')

        results = []

        for job in job_listings:
            job_details = {
                'title': job.find('span', class_='screen-reader-text').text.strip(),
                'company': job.find('a', class_='job-result-card__subtitle-link').text.strip(),
                'location': job.find('span', class_='job-result-card__location').text.strip(),
                'link': job.find('a', class_='job-result-card__full-card-link')['href']
            }
            results.append(job_details)
            print(response.status_code) 

        return results
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        return None

query = 'data analyst'  # You can change the query as needed
jobs_data = scrape_linkedin_jobs(query)

if jobs_data:
    with open('linkedin_jobs.json', 'w') as json_file:
        json.dump(jobs_data, json_file, indent=2)
        print('Data scraped and saved to linkedin_jobs.json')
