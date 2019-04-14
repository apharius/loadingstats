from time import sleep
from random import randint
from selenium import webdriver
from pyvirtualdisplay import Display
from datetime import datetime

class LoadingScraper():
    def __init__(self):
        self.url_to_crawl = "https://loading.se"
        self.threads = []
        self.threadurls = []
        self.posts = []
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
        sleep(1)
    
    def get_threads(self):
        print("Getting threads...")
        
        return self.driver.find_elements_by_xpath('//div[@class="Row-links-container"]')

    def process_thread_info(self, div):
        title = ''
        creator = ''
        number_of_replies = ''

        title = div.find_element_by_xpath('.//div[@class="Row-title"]').text
        creation = div.find_element_by_xpath('.//div[@class="Row-creation-text"]').text
        number_of_replies = div.find_element_by_xpath('.//div[@class="Row-number"]').text
        thread_url = div.find_element_by_xpath('./a[@class="Row-forum-container"]')
        print("Processing thread {0}".format(title))
        thread_url = thread_url.get_attribute("href")
        self.threadurls.append(thread_url)

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
        thread_data = ["tmp"]
        i = 1
        while len(thread_data) > 0:
            print("Crawling page {0}...".format(i))
            current_url = self.url_to_crawl + "/spel/{0}".format(i)
            self.get_page(current_url)
            thread_data = self.get_threads()
            for div in thread_data:
                data = self.process_thread_info(div)
                self.threads.append(data)
            i += 1
    def crawl_other(self):
        print("Crawling other section...")
        thread_data = ["tmp"]
        i = 1
        
        while len(thread_data) > 0:
            print("Crawling page {0}...".format(i))

            current_url = self.url_to_crawl + "/annat/{0}".format(i)
            self.get_page(current_url)
            thread_data = self.get_threads()
            for div in thread_data:
                data = self.process_thread_info(div)
                self.threads.append(data)
            i += 1
    def crawl_posts(self):
        for url in self.threadurls:
            self.get_page(url)
            thread_title = self.driver.find_element_by_xpath("//div[@class=\"Boop-container\"]").text
            try:
                pagenumber = self.driver.find_elements_by_xpath("//div[@class=\"PostList-pagination\"]/a[@class=\"PostList-boxlink\"]")[-1].text
            except:
                pagenumber = 1
            pagenumber = int(pagenumber)
            print("Crawling thread {0}...".format(thread_title))

            for i in range(1,pagenumber + 1):
                print("\tPage {0} of {1}".format(i,pagenumber))
                posts = self.driver.find_elements_by_xpath("//div[@class=\"PostItem-container\"]")
                for post in posts:
                    self.process_post_info(post)
                if pagenumber > 1 and i < pagenumber:
                    self.get_page(url + "/" + str(i+1))
    
    def process_post_info(self,post):
        username = post.find_element_by_xpath(".//div[@class=\"PostItem-username\"]").text
        datetime = post.find_element_by_xpath(".//div[@class=\"PostItem-date\"]").text

        datetime_split = datetime.split(' ')
        date = datetime_split[0]
        time = datetime_split[1]

        time_split = time.split(':')
        hour = time_split[0]
        minute = time_split[1]
        second = time_split[2]

        postinfo = {
                "poster":username,
                "post_date":date,
                "post_hour":hour,
                "post_minute":minute,
                "post_second":second
        }

        self.posts.append(postinfo)

    def parse(self):
        self.start_driver()
        self.crawl_games()
        self.crawl_other()
        self.crawl_posts()
        self.close_driver()
        
        return (self.threads,self.posts)

def main():
    scraper = LoadingScraper()
    starttime = datetime.now()
    print("Beginning crawl at {0}".format(starttime))
    scraperesults =scraper.parse()
    endtime = datetime.now()
    print("Crawl finished at {0}".format(endtime))
    print("Elapsed time: {0}".format(endtime - starttime))
    threads = scraperesults[0]
    posts = scraperesults[1]
    csv_thread_dump(threads)
    csv_post_dump(posts)
    print("Finished! {0} threads and {1} posts processed.".format(len(threads),len(posts)))

def csv_thread_dump(threads):
    output = open('threads.csv','w+',encoding="utf-8")
    output.write('Title;Creator;CreationDate;CreationHour;CreationMinute;NumberOfReplies\n')

    for t in threads:
        output.write('{0};{1};{2};{3};{4};{5}\n'.format(t['title'],t['creator'],t['creation_date'],t['creation_hour'],t['creation_minute'],t['number_of_replies']))

    output.close

def csv_post_dump(posts):
    output = open('posts.csv','w+',encoding="utf-8")
    output.write('Poster;PostDate;PostHour;PostMinute;PostSecond\n')

    for p in posts:
        output.write('{0};{1};{2};{3};{4}\n'.format(p['poster'],p['post_date'],p['post_hour'],p['post_minute'],p['post_second']))

    output.close
if __name__ == "__main__":main()
