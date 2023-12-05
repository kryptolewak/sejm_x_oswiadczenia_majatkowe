from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests

def download_pdf(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as file:
        file.write(response.content)

def scrape_page(driver, page_id):
    url = f"https://sejm.gov.pl/Sejm10.nsf/posel.xsp?id={page_id}&type=A"
    driver.get(url)

    # Wait for the AJAX-triggered element to be clickable and click it
    wait = WebDriverWait(driver, 10)
    ajax_element = wait.until(EC.element_to_be_clickable((By.ID, 'osw')))
    ajax_element.click()

    # Wait for the AJAX request to complete and the new element to appear
    pdf_link_element = wait.until(EC.presence_of_element_located((By.ID, 'view:_id1:_id2:facetMain:_id190:_id257:0:_id262')))
    pdf_link = pdf_link_element.get_attribute('href')

    # Download and save the PDF
    pdf_filename = f"OSW10P_{page_id}.pdf"
    download_pdf(pdf_link, pdf_filename)

def main():
    driver = webdriver.Chrome()

    for i in range(1, 461):
        page_id = str(i).zfill(3)
        print(f"Scraping page ID: {page_id}")
        try:
            scrape_page(driver, page_id)
        except Exception as e:
            print(f"Error scraping page {page_id}: {e}")

    driver.quit()

if __name__ == "__main__":
    main()
