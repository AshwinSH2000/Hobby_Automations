#python script to download pdf files from a given url
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def download_pdf(url, folder="downloads"):

    if not os.path.exists(folder):                  # creates a folder if downloads doesnt exist
        os.makedirs(folder)
    
    response = requests.get(url)                    # fetch the html content of the page
    if response.status_code != 200:                 # 200 is the success code
        print(f"Failed to retrieve the URL: {url}")
        return

    
    soup = BeautifulSoup(response.text, 'html.parser')      # parse the page with BeautifulSoup

    links = soup.find_all('a', href=True)           # find all links in the page

    # filter links that end with '.pdf' 
    # i wanted only pdfs hence i hardcoded it here. this can be edited as per the requirement
    pdf_links = [urljoin(url, link['href']) for link in links if link['href'].lower().endswith('.pdf')]

    if not pdf_links:                               # empty list
        print(f"No PDF files found on {url}")
        return

    for pdf_url in pdf_links:
        try:
            # get the filename from the url
            filename = os.path.join(folder, pdf_url.split('/')[-1])
            
            # send get request to download the PDF
            pdf_response = requests.get(pdf_url)
            if pdf_response.status_code == 200:
                with open(filename, 'wb') as pdf_file:
                    pdf_file.write(pdf_response.content)
                print(f"Downloaded: {filename}")
            else:
                print(f"Failed to download: {pdf_url}")
        except Exception as e:
            print(f"Error downloading {pdf_url}: {e}")



if __name__ == "__main__":
    url = input("Enter the url to search the files: ")
    download_pdf(url)
