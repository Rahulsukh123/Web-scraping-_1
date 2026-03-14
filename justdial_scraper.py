"""
JustDial Nagpur Hospitals Scraper
Short and easy scraper for multispeciality hospitals in Nagpur
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import csv
import time

def scrape_hospitals():
    """Scrape hospital data from JustDial"""
    
    url = "https://www.justdial.com/Nagpur/Multispeciality-Hospitals/nct-10547585"
    
    # Chrome setup
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    driver = webdriver.Chrome(options=options)
    hospitals = []
    
    try:
        print("Loading JustDial...")
        driver.get(url)
        time.sleep(3)
        
        # Find all hospital listings
        containers = driver.find_elements(By.CLASS_NAME, "resultbox")
        print(f"Found {len(containers)} hospitals")
        
        for i, container in enumerate(containers):
            try:
                # Extract hospital name
                title_elem = container.find_element(By.CLASS_NAME, "resultbox_title_anchor")
                name = title_elem.text.strip()
                
                # Extract phone number
                phone_elem = container.find_element(By.CLASS_NAME, "callcontent")
                phone = phone_elem.text.strip()
                
                # Extract address
                address_elem = container.find_element(By.CLASS_NAME, "locatcity")
                address = address_elem.text.strip()
                
                # Extract rating
                rating_elem = container.find_element(By.CLASS_NAME, "resultbox_totalrate")
                rating = rating_elem.text.strip()
                
                # Extract link
                link_elem = container.find_element(By.CSS_SELECTOR, ".resultbox_title a")
                link = link_elem.get_attribute('href')
                
                hospitals.append([name, phone, address, rating, link])
                print(f"{i+1}. {name} - {address}")
                
            except Exception as e:
                print(f"Error processing hospital {i+1}: {e}")
                continue
        
        # Save to CSV
        with open('nagpur_hospitals.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Hospital Name', 'Phone', 'Address', 'Rating', 'Link'])
            writer.writerows(hospitals)
        
        print(f"Successfully saved {len(hospitals)} hospitals to nagpur_hospitals.csv")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_hospitals()
