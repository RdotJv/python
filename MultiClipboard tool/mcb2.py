import pyperclip
import shelve
import pyinputplus as pyip
from pathlib import Path

def saveMCB(mcbShelve):
  while True:
    current_CB = pyperclip.paste()
    mcbKey = pyip.inputStr('Enter a key for this entry: ')

    if mcbKey in mcbShelve: 
      print(f'{mcbKey} already exists!')
      if pyip.inputChoice(['overwrite', 'back']) == 'back':
        continue
    save_data_choice = pyip.inputChoice(['enter', 'use'], prompt=f'use {current_CB} or enter data yourself? (use/enter) ')
    if save_data_choice == 'use':
      mcbVal = current_CB
    else:
      mcbVal = pyip.inputStr(f'Enter the value for {mcbKey}')
      mcbShelve[mcbKey]  = mcbVal
    if pyip.inputYesNo('Done. Add more?') == 'no': 
      break
  
def editMCB(mcbShelve):
  viewMCB(mcbShelve)
  key_choice = check_len(mcbShelve)
  if not key_choice: 
    return 69
  mcbShelve[key_choice] = pyip.inputStr(f'enter new val for {key_choice}')
  viewMCB(mcbShelve)

def viewMCB(mcbShelve):
  if not check_len(mcbShelve):
    return 69
  for i in list(mcbShelve.keys()):
    print(f"{i}: {mcbShelve[i]}")

def selectMCB(mcbShelve):
  viewMCB(mcbShelve)
  pyip.inputChoice(list(mcbShelve.keys()), prompt='which key to select?')

def check_len(mcbShelve):
  if len(list(mcbShelve.keys())) == 1:
    print('only one key in MCB!')
    return list(mcbShelve.keys())[0]
  elif len(list(mcbShelve.keys())) == 0: 
    print('no keys or values found in MCB!')
    return False
  else: 
    return pyip.inputChoice(list(mcbShelve.keys()))

def main():
  main_action_choice = pyip.inputChoice(['save','edit' ,'view', 'select'])
  shelve_destination = str(Path.cwd()/'MCB/data')
  with shelve.open(shelve_destination) as mcbShelve:
    if main_action_choice == 'save':
      saveMCB(mcbShelve)
    elif main_action_choice == 'edit':
      editMCB(mcbShelve)
    elif main_action_choice == 'view':
      viewMCB(mcbShelve)
    elif main_action_choice == 'select':
      selectMCB(mcbShelve)

if __name__ == '__main__':
  main()