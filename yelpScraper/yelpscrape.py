from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by  import By
from selenium.webdriver.support.ui  import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import openpyxl as opx
import time

def handle_search(driver, query, location):
  search_bar_query, search_bar_location = [driver.find_element(By.XPATH, '//*[@id="search_description"]'), driver.find_element(By.XPATH ,'//*[@id="search_location"]')]
  search_bar_query.send_keys(query)
  search_bar_location.click()
  search_bar_location.send_keys(location)
  time.sleep(1)
  search_bar_location.send_keys(Keys.ARROW_DOWN)
  search_bar_location.send_keys(Keys.ARROW_DOWN)
  search_bar_location.send_keys(Keys.RETURN)
  
def main():
  driver = webdriver.Chrome()
  driver.get("http://yelp.com")

  handle_search(driver, 'cafe', 'Liberty Village')
  n = 0               #used to set next page
  num_of_pages = 2    #toggle to read more pages
  results = {}        #stores data to write to excel doc in the end
  for i in range(num_of_pages):
    elements = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'container__09f24__FeTO6.hoverable__09f24___UXLO.y-css-way87j')))
    for i in range(len(elements)):
      if (i in [0,1,len(elements)-1]): #skip sponsored items
        continue
      element = elements[i].find_element(By.CLASS_NAME, "y-css-12ly5yx")
      element.click()
      WebDriverWait(driver, 5).until(EC.number_of_windows_to_be(2))
      driver.switch_to.window(driver.window_handles[1])
      
      result_name = driver.find_element(By.CSS_SELECTOR, "h1.y-css-olzveb").text
      review_score, review_count = [driver.find_element(By.CSS_SELECTOR,'span.y-css-kw85nd').text, driver.find_element(By.CSS_SELECTOR, "a.y-css-12ly5yx").text]
      
      results[result_name] = {'review score': review_score, 'review count' : review_count}
      driver.close()
      driver.switch_to.window(driver.window_handles[0])

    n+=10
    if '&start' in driver.current_url:
      new_url = ''.join(driver.current_url.split("&start=")[:-1]) + '&start=' +str(n)
    else:
      new_url = f"{driver.current_url}&start="+str(n)
    driver.get(new_url)

  wb = opx.Workbook()
  sheet = wb.active
  sheet['A1'] = 'Name'
  sheet['B1'] = "Review score"
  sheet['C1'] = "Review count"
  for index, result in enumerate(results.keys()):
    sheet[f'A{index+2}'] = result
    sheet[f'B{index+2}'] = results[result]['review score']
    sheet[f'C{index+2}'] = results[result]['review count']
  wb.save("./upwork/yelp/yelpScrapeResults.xlsx")



if __name__ == '__main__':
  main()