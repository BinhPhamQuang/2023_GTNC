
from queue import Queue
from tabulate import tabulate


shift1 = [1, 4, 6, 7, 8, 9, 12, 13, 14]  # Shifts do not off at weekend
shift2 = [2, 3, 5, 10, 11]  # Shifts off at weekend


CSRs = [i for i in range(1, 15)]

shifts = [['C1', 'C0', 'C4', 'C5', 'OFF', 'C4', 'C5'],
          ['C4', 'C5', 'C0', 'C5', 'C5', 'C1', 'OFF'],
          ['OFF', 'C4', 'C0', 'C1', 'C5', 'C5', 'OFF'],
          ['C5', 'C5', 'C1', 'C2', 'OFF', 'C3', 'C4'],
          ['C5', 'C1', 'C4', 'C5', 'C0', 'OFF', 'C2'],
          ['C2', 'C4', 'C5', 'OFF', 'C0', 'C1', 'C5'],
          ['C5', 'C1', 'C5', 'C0', 'OFF', 'C2', 'C4'],
          ['C4', 'C0', 'C5', 'C1', 'OFF', 'C5', 'C1'],
          ['C0', 'C5', 'OFF', 'C1', 'C4', 'C5', 'C2'],
          ['C1', 'C0', 'C4', 'C5', 'C5', 'C5', 'OFF'],
          ['C0', 'C4', 'C1', 'C5', 'C2', 'OFF', 'C5'],
          ['OFF', 'C1', 'C0', 'C4', 'C1', 'C5', 'C5'],
          ['C5', 'C5', 'OFF', 'C4', 'C0', 'C1', 'C5'],
          ['C0', 'OFF', 'C5', 'C4', 'C4', 'C5', 'C1']]

def get_shift(schedule,is_off_weekend, CSRs):
  c = 0
  for CSR in CSRs:
    schedule[CSR][0] = "NV" + str(CSR)
    if is_off_weekend:
      schedule[CSR][1:] = shifts[shift2[c]-1]
    else:
      schedule[CSR][1:] = shifts[shift1[c]-1]
    c+=1
  return schedule


def get_csrs_off_weekend(q: Queue, CSRs):
  csrs = []
  for _ in range(5):
    csr = q.get()
    csrs.append(csr)
    q.put(csr)
  return q, csrs, list(set(CSRs) - set(csrs))


q = Queue()

for CSR in CSRs:
  q.put(CSR)

schedule = [[None for _ in range(8)] for _ in range(15)]
schedule[0] = ['CSR', 'Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun']


week = 1
while week < 20:
  print(f"Week: {week}")
  q, csrs_off, csrs_not_off =  get_csrs_off_weekend(q, CSRs)
  schedule = get_shift(schedule,True,csrs_off)
  schedule = get_shift(schedule,False,csrs_not_off)
  # print(schedule)
  print(tabulate(schedule, headers='firstrow', tablefmt='fancy_grid'))
  week += 1
