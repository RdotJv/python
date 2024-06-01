from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by  import By
from selenium.webdriver.support.ui  import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, re, pprint
import openpyxl as pxl

#scrapes only sponsored items from query specified in line 18 and writes to an xlsx document 


sponsored_items_data = {}

browser = webdriver.Chrome()
browser.get("https://www.amazon.com")
input() #wait for user to solve captcha
search_bar = browser.find_element(By.XPATH,'//*[@id="twotabsearchtextbox"]')
search_bar.send_keys('dog toy')
search_bar.send_keys(Keys.RETURN)
time.sleep(1)

num_of_sponsored_items = len(browser.find_elements(By.CLASS_NAME, 'sg-col-4-of-24.sg-col-4-of-12.s-result-item.s-asin.sg-col-4-of-16.AdHolder.sg-col.s-widget-spacing-small.sg-col-4-of-20'))
for i in range(num_of_sponsored_items):
  result = browser.find_elements(By.CLASS_NAME, 'sg-col-4-of-24.sg-col-4-of-12.s-result-item.s-asin.sg-col-4-of-16.AdHolder.sg-col.s-widget-spacing-small.sg-col-4-of-20')[i]
  item = result.find_element(By.CSS_SELECTOR, '.a-link-normal.s-no-outline')   #find and click-on an item 
  item_url = item.get_attribute('href')
  item.click()
  e_store_name = WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.XPATH, '//*[@id="bylineInfo"]')))
  store_name = e_store_name.text[10:]
  store_url = e_store_name.get_attribute('href').strip()
  item_name = browser.find_element(By.XPATH, '//*[@id="productTitle"]').text
                                                           
  html_item_price = browser.find_element(By.XPATH, '//*[@id="corePrice_feature_div"]/div/div/span[1]/span[2]').get_attribute('innerHTML')
  pattern = re.compile(r'>(.{0,}?)<')
  item_price = ''.join(pattern.findall(html_item_price))

  sponsored_items_data.setdefault(store_name, {})           #store_name : {}
  sponsored_items_data[store_name].setdefault('items', {})  #store_name : {'items': {}}
  sponsored_items_data[store_name]['store url'] = store_url #store_name : {store_url: '...',
                                                            #              'items': {}      }
  sponsored_items_data[store_name]['items']['name'] = item_name
  sponsored_items_data[store_name]['items']['price'] = item_price
  sponsored_items_data[store_name]['items']['url'] = item_url


  pprint.pprint(sponsored_items_data)
  browser.back()
  time.sleep(1)
wb = pxl.Workbook()
sheet = wb.active
sheet.title = 'page 1 sponsored items'
sheet['A1'] = 'Store Name'
sheet['B1'] = 'Store URL'
sheet['C1'] = 'Item'
sheet['D1'] = 'Price'
sheet['E1'] = 'Item URL'

for index, current_store in enumerate(list(sponsored_items_data.keys())):
  sheet[f'A{index+2}'] = current_store
  sheet[f'B{index+2}'] = sponsored_items_data[current_store]['store url']
  sheet[f'C{index+2}'] = sponsored_items_data[current_store]['items']['name']
  sheet[f'D{index+2}'] = sponsored_items_data[current_store]['items']['price']
  sheet[f'E{index+2}'] = sponsored_items_data[current_store]['items']['url']

sheet.freeze_panes = 'A2'
wb.save('amazon_spons_scrape.xlsx')
input()

# store : {'items': {'name': name,
#                    'price': 69,
#                    'url': www.eggs.com},
#          'store url: www.bacon.com}