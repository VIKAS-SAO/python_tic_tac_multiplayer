import time 
import threading
import pickle
from decoder import decoder ,encoder

# def sleeper(name):
#     print(name ,' is going to sleep')
#     time.sleep(3)

#     print(name, ' has woken up!')

# thread_list=[]

# start_time = time.time()
# for i in range(5):
#     t  = threading.Thread(target=sleeper , name = 'sleeeper' ,args=['vikas'])
#     thread_list.append(t)
#     t.start()
# for i in range(5):
#     thread_list[i].join()

# end_time = time.time()
# print('time taken = ',end_time-start_time)






## nromal without the threads
# start_time = time.time()
# for i in range(5):
#     sleeper('vikas')

# end_time = time.time()
# print('time taken = ',end_time-start_time)
 







 