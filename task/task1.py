import time
import win32file,win32con
import multiprocessing
import os


class MyProcess(multiprocessing.Process):
    def __init__(self,type_of_worker,locker):

        multiprocessing.Process.__init__(self)
        self.type_of_worker=type_of_worker
        self.locker=locker


        pname=self.name

        if self.type_of_worker == 'писатель':

            self.locker.acquire()
            work(self.type_of_worker, pname)
            self.locker.release()

        else:

            work(self.type_of_worker, pname)




def work(name,number):


    print(f'Начало работы для потока:{name} c номером:{number} и PID {os.getpid()}')

    handle = win32file.CreateFile(os.path.join(os.getcwd(), 'task.txt'),
                                  win32file.FILE_GENERIC_WRITE | win32file.FILE_GENERIC_READ,
                                  win32file.FILE_SHARE_READ | win32file.FILE_SHARE_WRITE,
                                  None,
                                  win32con.OPEN_EXISTING,
                                  win32con.FILE_ATTRIBUTE_NORMAL,
                                  None)

    rc, buffer = win32file.ReadFile(handle, 1024)
    if name=="писатель":

        to_write=(f"писатель {number} сделал запись {time.asctime()}\n").encode('utf')

        win32file.WriteFile(handle,to_write)

        handle.Close()

    else:

        handle.Close()
        print(f'читатель с номером:{number} прочитал запись:\n{buffer.decode()}')


    time.sleep(5)




if __name__ == '__main__':
    hfile = win32file.CreateFile(os.path.join(os.getcwd(), 'task.txt'),
                                 win32file.GENERIC_WRITE | win32file.GENERIC_READ,
                                 win32file.FILE_SHARE_READ | win32file.FILE_SHARE_WRITE
                                 ,
                                 None,
                                 win32con.CREATE_ALWAYS,
                                 win32con.FILE_ATTRIBUTE_NORMAL,
                                 None
                                 )
    hfile.Close()


    workers=('писатель','читатель')
    lock=multiprocessing.Lock()
    cpu_counts=multiprocessing.cpu_count()

    processes=[MyProcess(type_of_worker=worker, locker=lock) for _ in range(int(cpu_counts / 2)) for worker in workers]
    for process in processes:
        print(process.name,' ',process.type_of_worker)

    for process in processes:
        process.start()

    for process in processes:
        process.join()







