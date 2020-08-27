from urllib.parse import urlparse
from multiprocessing import Pool
from threading import Lock
import statistics,requests,sys

GREEN = '\033[1;32;48m'
RED = '\033[1;31;48m'
UNDERLINE = '\033[4;37;48m'
END = '\033[1;37;0m'

api_url = "https://data.similarweb.com/api/v1/data?domain="

lock = Lock()

def num_to_word(number):
    nstr = str(number)
    nlen = len(nstr)
    classes = ["K", "x10K", "x100K", "M", "x10M", "x100M"]
    index = nlen - 4
    try:
        return nstr[0] + classes[index]
    except:
        return nstr


def process_thread(domain):
    response = requests.get(api_url + domain).json()
    if response:
        EstimatedMonthlyVisitsDict = response["EstimatedMonthlyVisits"]
        avg_visitors = round(statistics.mean(
            EstimatedMonthlyVisitsDict.values()))
        lock.acquire()
        print(f"{GREEN}[+]{END} Found that domain: {domain} has: {UNDERLINE}{num_to_word(avg_visitors)}{END} ({avg_visitors:,}) avg. visitors".replace(
            ",", f"{GREEN},{END}"))
        lock.release()
    else:
        lock.acquire()
        print(f"{RED}[!]{END} No data found for domain: {domain}")
        lock.release()

if __name__ == "__main__":
    pool = Pool(20)
    for line in open(sys.argv[1], "r").readlines():
        pool.apply_async(process_thread, (line,))
    pool.close()
    pool.join()
