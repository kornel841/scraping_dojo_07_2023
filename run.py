import requests,  os, json, orjsonl
from bs4 import BeautifulSoup
from dotenv import load_dotenv, dotenv_values

load_dotenv()
proxy = os.getenv('PROXY')
url = os.getenv('INPUT_URL')
filename = os.getenv('OUTPUT_FILE')


class Scrapper():
    def __init__(self,url, filename,proxy, verbose=False):
        self.url = url
        self.filename = filename
        self.proxy = proxy
        self.page = 1
        self.next_page = ''
        self.base_path = url
        self.verbose = verbose

    def get_json_data(self):
        response = requests.get(self.url)
        #response = requests.get(self.url, proxies=self.proxy)
        soup = BeautifulSoup(response.text, "html.parser")
        
        while True:
          
            scripts = soup.find_all('script')
           
            if len(scripts) == 0:
                if self.verbose:
                    print(f'On page {self.page} there are no quotes. Finishing scrapping.')
                break

            script = scripts[1].text.strip()[78:].strip()[:-491].strip()
            #Get data and write it to jsonl file
            self.data =  json.loads(script)
            self.write_into_file()
        
            if not(self.check_if_there_is_next_page(soup)):
                break
            
            self.url = self.next_page
            response = requests.get(self.url)
            soup = BeautifulSoup(response.text, "html.parser")
            self.page +=1

    def write_into_file(self):
        for row in self.data:
            row = self.convert_data(row)
            previous = orjsonl.load(self.filename)
            previous.append(row)
            orjsonl.save(self.filename, previous)

    def perform_scrapping(self):
        #creating new, empty file
        orjsonl.save(self.filename, [])
        self.get_json_data()

    def check_if_there_is_next_page(self, soup):
        nav_tag = soup.find('nav')
        a_tag = nav_tag.find_all('a')
        for hrefs in a_tag:
            if int(hrefs['href'][:-1][17:]) == (self.page + 1):
                self.next_page = self.base_path + hrefs['href'][-7:]
                if self.verbose:
                    print(f'Going into next page: {self.page + 1}')
                return True
        if self.verbose:
            print(f'There is no next page. Last page found: {self.page}')
        return False 
       
    #formatting data into right formating
    def convert_data(self, data):
        new_data = {"text": data['text'],
                    "by": data['author']['name'],
                    "tags": data['tags']}
        return new_data


simple_scrapper = Scrapper(url,filename,proxy, verbose=False)
simple_scrapper.perform_scrapping()
