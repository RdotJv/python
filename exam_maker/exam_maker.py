import random
from pathlib import Path
capitals = {'Alabama': 'Montgomery', 'Alaska': 'Juneau', 'Arizona': 'Phoenix',
   'Arkansas': 'Little Rock', 'California': 'Sacramento', 'Colorado': 'Denver',
   'Connecticut': 'Hartford', 'Delaware': 'Dover', 'Florida': 'Tallahassee',
   'Georgia': 'Atlanta', 'Hawaii': 'Honolulu', 'Idaho': 'Boise', 'Illinois':
   'Springfield', 'Indiana': 'Indianapolis', 'Iowa': 'Des Moines', 'Kansas':
   'Topeka', 'Kentucky': 'Frankfort', 'Louisiana': 'Baton Rouge', 'Maine':
   'Augusta', 'Maryland': 'Annapolis', 'Massachusetts': 'Boston', 'Michigan':
   'Lansing', 'Minnesota': 'Saint Paul', 'Mississippi': 'Jackson', 'Missouri':
   'Jefferson City', 'Montana': 'Helena', 'Nebraska': 'Lincoln', 'Nevada':
   'Carson City', 'New Hampshire': 'Concord', 'New Jersey': 'Trenton', 'New Mexico': 'Santa Fe', 
   'New York': 'Albany', 'North Carolina': 'Raleigh', 'North Dakota': 'Bismarck', 
   'Ohio': 'Columbus', 'Oklahoma': 'Oklahoma City', 'Oregon': 'Salem', 'Pennsylvania': 'Harrisburg',
   'Rhode Island': 'Providence', 'South Carolina': 'Columbia', 'South Dakota': 'Pierre', 
   'Tennessee': 'Nashville', 'Texas': 'Austin', 'Utah': 'Salt Lake City', 
   'Vermont': 'Montpelier', 'Virginia': 'Richmond', 'Washington': 'Olympia', 
   'West Virginia': 'Charleston', 'Wisconsin': 'Madison', 'Wyoming': 'Cheyenne'}

states = list(capitals.keys())

def assembleQuestion(question_num, shuffled_states, mcq_options):
  return '''\nQuestion %d. What is the capital of %s?
  a. %s
  b. %s
  c. %s
  d. %s\n''' % (question_num+1, shuffled_states[question_num], mcq_options[0], mcq_options[1], mcq_options[2], mcq_options[3])

def create_mcq(question_num, shuffled_states):
  correct_answer = capitals[states[question_num]]
  wrong_answers = list(capitals.values())
  wrong_answers.remove(correct_answer)
  mcq_options = [correct_answer]
  mcq_options.extend(random.sample(wrong_answers, 3))
  random.shuffle(mcq_options)

  return assembleQuestion(question_num, shuffled_states, mcq_options), f'{question_num+1} {correct_answer}\n'
  
def main():
  for quiz_num in range(10):
    with open(Path.cwd() /'exam_maker/exam_questions'/f'Qstudent_{quiz_num+1}.txt', 'w') as quizQ, open(f'exam_maker/exam_questions/answers/Astudent_{quiz_num+1}.txt', 'w') as quizA:
      heading = 'Name: \nDate:\nClass:\n\n'+ ' '*20 + f'State Capital quiz form {quiz_num+1}\n'
      quizQ.write(heading)
      quizA.write(heading)
      random.shuffle(states)
      for question_num in range(20):
        mcq, correct_answer = create_mcq(question_num, states)
        quizQ.write(mcq)
        quizA.write(correct_answer)


if __name__ == '__main__':
  main()