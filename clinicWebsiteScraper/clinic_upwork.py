import requests
from bs4 import BeautifulSoup
import openpyxl as opx

def get_clinic_name(url, clinic_id):
    response = requests.get(url.format(clinic_id))
    try:
        response.raise_for_status()
    except Exception as e:
        return 'N/A'
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    clinic_name = soup.find_all('h1')[-1].text.strip()
    if clinic_name not in ["Payment Confirmation", ""]:        
      return clinic_name
    return 'N/A'
def main():
  url = 'https://{}.portal.athenahealth.com/'
  clinics_arr = []
  for clinic_id in range(12695, 12725):
    result = get_clinic_name(url, clinic_id)
    clinic_data = {'clinic_id': f'{clinic_id}', 'doctor name': f'{result}'}
    clinics_arr.append(clinic_data)
    print(f"{clinic_id}: {result}")
  print(clinics_arr)
  # opx.Workbook()

if __name__ == '__main__':
    main()