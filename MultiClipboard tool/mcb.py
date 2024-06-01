
#please use mcb2 instead, paths brokn in here

import shelve
import pyperclip
import pyinputplus
import os
from pathlib import Path

def checkcreateMCB(cpath, existing_shelves):
  while True:
    title = pyinputplus.inputStr('(create) enter MCB title: ')
    if not (cpath / f"{title}.dat").exists():
      result = createMCB(cpath, title)
      if result == 'user done': 
        break
    else:
      if pyinputplus.inputYesNo(f'A MCB with the title {title} already exists!\nView it?') != 'yes': 
        continue      
      viewMCB(cpath, title, existing_shelves)
      continue
#farhad

def createMCB(cpath, title):       #is run only if in checkcreateMCB() the MCB entered doesn't exist
  x = 0
  with shelve.open(cpath / title) as mcb_shelf:
    while x < 11:
      current_clipboard = pyperclip.paste()
      if pyinputplus.inputYesNo(f"add \"{current_clipboard}\" to MCB {title}?") == 'yes':
        x += 1
        mcb_shelf[str(x)] = current_clipboard
      else:
        if pyinputplus.inputYesNo('continue?') == 'no': 
          return 'user done'

def viewMCB(cpath, title, existing_shelves):       #is run if user tries to create an existing MCB and chooses to view || user simply chooses to view/edit
  if title == '':
    if len(existing_shelves) == 1:       #handle scenario where there are no existing MCBs
      title = existing_shelves[0]
    elif len(existing_shelves) ==0:
      print('No existing MCBs to view!')
      return None
    else:
      title = pyinputplus.inputChoice(existing_shelves, caseSensitive=False)
  with shelve.open(cpath/title) as view:
    for key in view:
      print(f"{key}. {view[key]}")
    if pyinputplus.inputYesNo('Edit the MCB?') == 'yes': 
      editMCB(view)

def editMCB(view):        #is only run via viewMCB wherein the shelve to view is already opened
  while True:
    all_current_MCB_keys = list(view.keys())
    if pyinputplus.inputChoice(['add','edit']) == 'add':
      user_add_MCB = pyinputplus.inputStr('paste or enter value to add: ')
      view[str(len(all_current_MCB_keys)+1)] = user_add_MCB
      continue
    if len(all_current_MCB_keys)==1:
      print('Only one item present')
      choice = all_current_MCB_keys[0]
    else: 
      choice = pyinputplus.inputChoice(list(view.keys()))
    view[choice] = input(f"replace {view[choice]} with: ")
    for i in list(view.keys()):
      print(i, view[i])
    if pyinputplus.inputYesNo('continue? ') == 'no':
      break

def selectMCB(cpath, existing_shelves):
  if len(existing_shelves) == 1:       #handle scenario where there are no existing MCBs
    choice = existing_shelves[0]
  elif len(existing_shelves) ==0:
    print('No existing MCBs to view!')
    return None
  else:
    choice = pyinputplus.inputChoice(existing_shelves)
  with shelve.open(cpath/choice) as use_MCB:
    for i in list(use_MCB.keys()):
      print(f"{i}. {use_MCB[i]}")
    if len(list(use_MCB.keys())) == 1:
      copy_choice = list(use_MCB.keys())[0]
      print(f'Only one item present.. {use_MCB[copy_choice]} copied')
    else:
      copy_choice = pyinputplus.inputChoice(list(use_MCB.keys()))
    pyperclip.copy(use_MCB[copy_choice])
    print('done!')
  return pyinputplus.inputYesNo('copy another?')

def main():
  cpath = Path.cwd() / 'multiclipboard'
  existing_shelves = [str(dat_file.stem) for dat_file in list(cpath.glob("*.dat"))]      #checks for and holds .dat files in current directory

  print("'c' - Create a MCB\n'v' - View and edit all MCB\n's' - Select & use a MCB")
  start_choice = pyinputplus.inputChoice(['c','v','s'])
  os.system('clear')
  if start_choice == 'c':
    checkcreateMCB(cpath, existing_shelves)
  elif start_choice == 'v':
    viewMCB(cpath, '', existing_shelves)
  elif start_choice == 's':
    while True:
      repeat_choice = selectMCB(cpath, existing_shelves)
      if repeat_choice == 'no': 
        break

if __name__ == '__main__':
  main()
