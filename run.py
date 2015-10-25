from multiprocessing import Process
import csv
import read_send


data1 = csv.DictReader(open('output1.csv', 'rU'))
data2 = csv.DictReader(open('output2.csv', 'rU'))
data3 = csv.DictReader(open('output3.csv', 'rU'))
data4 = csv.DictReader(open('output4.csv', 'rU'))

read_send.unpack(data2)
# read_send.unpack(client1, data1)

# def runInParallel(*args):
#     processes = []
#     for x in args:
#         thread = read_send.ReadSend(x)
#         process = Process(thread.begin())
#         process.start()
#         processes.append(process)
#     for p in processes:
#         p.join()

# runInParallel(data1, data2, data3, data4)