from time import sleep
from random import randint
from selenium import webdriver
from pyvirtualdisplay import Display

class LoadingScraper():
    def __init__(self):
        self.url_to_crawl = "https://loading.se"
        self.threads = []

    def start_driver(self):
        print("Starting driver...")
        self.display = Display(visible=0, size=(800,600))
        self.display.start()
        self.driver = webdriver.Chrome("/var/chromedriver/chromedriver")
        sleep(4)

    def close_driver(self):
        print("Closing driver...")
        self.display.stop()
        self.driver.quit()
        print("Closed!")

    def get_page(self, url):
        print("Getting page...")
        self.driver.get(url)
        sleep(randint(2,3))
    
    def get_threads(self):
        print("Getting threads...")
        
        for div in self.driver.find_elements_by_xpath('//div[@class="Row-links-container"]'):
            data = self.process_thread_info(div)
            self.threads.append(data)

    def process_thread_info(self, div):
        title = ''
        creator = ''
        number_of_replies = ''

        title = div.find_element_by_xpath('.//div[@class="Row-title"]').text
        creation = div.find_element_by_xpath('.//div[@class="Row-creation-text"]').text
        number_of_replies = div.find_element_by_xpath('.//div[@class="Row-number"]').text
                
        creation_split = creation.split('     ')
        creator = creation_split[0]

        datetime_split = creation_split[1].split(' ')

        creation_date = datetime_split[0]
        creation_time = datetime_split[1]
        
        timesplit = creation_time.split(':')
        creation_hour = timesplit[0]
        creation_minute = timesplit[1]


        thread_info = {
                'title': title,
                'creator': creator,
                'creation_date': creation_date,
                'creation_hour': creation_hour,
                'creation_minute': creation_minute,
                'number_of_replies': number_of_replies
        }

        return thread_info

    def crawl_games(self):
        print("Crawling game section...")

        for i in range(1,9):
            print("Crawling page {0}...".format(i))

            current_url = self.url_to_crawl + "/spel/{0}".format(i)
            self.get_page(current_url)
            self.get_threads()
    
    def crawl_other(self):
        print("Crawling other section...")

        for i in range(1,5):
            print("Crawling page {0}...".format(i))

            current_url = self.url_to_crawl + "/annat/{0}".format(i)
            self.get_page(current_url)
            self.get_threads()

    def parse(self):
        self.start_driver()
        self.crawl_games()
        self.crawl_other()
        self.close_driver()

        return self.threads

def main():
    scraper = LoadingScraper()
    threads =scraper.parse()
    csv_dump(threads)
    print("Finished!")

def csv_dump(threads):
    output = open('loadingstats.csv','w+',encoding="utf-8")
    output.write('Title;Creator;CreationDate;CreationHour;CreationMinute;NumberOfReplies\n')

    for t in threads:
        output.write('{0};{1};{2};{3};{4};{5}\n'.format(t['title'],t['creator'],t['creation_date'],t['creation_hour'],t['creation_minute'],t['number_of_replies']))

    output.close
if __name__ == "__main__":main()
