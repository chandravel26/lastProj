import time
import requests
 
def run_time_test_requests(url):
    print("\n🔍 Using requests (static)...")
 
    # One hit
    start = time.time()
    requests.get(url)
    end = time.time()
    print(f"1 Hit Time: {round(end - start, 2)} seconds")
 
    # 50 hits
    start1 = time.time()
    for x in range(1, 51):
        start = time.time()
        requests.get(url)
        end = time.time()
        print(f"{x} th time with seconds of {round(end - start, 2)}")
 
    end = time.time()
    print(f"50 Hits Total Time: {round(end - start1, 2)} seconds")
 
def main():
    url = input("🔗 Enter the website URL: ").strip()
    run_time_test_requests(url)
 
if __name__ == "__main__":
    main()