class worker:
    def __init__(self,name,surname,middleName,function,salary):
        self.name=name
        self.surname=surname
        self.middleName=middleName
        self.function=function
        self.salary=int(salary)


    def get_full_name(self):
        return self.surname + " " + self.name + " " +self.middleName

    def get_function(self):
        return self.function

    def get_salary(self):
        return self.salary

    def set_salary(self,salary):
        self.salary=salary

    def set_position(self,function):
        self.function=function

class department:
    def __init__(self,name):
        self.name=name
        self.avg_salary=0
        self.quantity_of_workers=0
        self.workers=[]

    def get_name(self):
        return self.name

    def get_quantity_of_workers(self):
        return len(self.workers)

    def get_avg_salary(self):
        salary=0
        for worker in self.workers:
            salary+=worker.get_salary()
        return  round(salary/self.get_quantity_of_workers())

    def push_worker(self,worker):
        self.workers.append(worker)
        self.workers.sort(key=lambda x:x.salary,reverse=True)

    def pop_worker(self,surname,position):
        for idx,worker in enumerate(self.workers):
            if worker.surname ==surname and worker.position==position:
                self.workers.pop(idx)

    def get_last_worker(self):
        return self.workers[-1]

    def get_workers(self):
        return self.workers
