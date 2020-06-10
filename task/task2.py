import sys
from PySide2 import QtCore, QtGui, QtWidgets
import xml.etree.ElementTree as ET
import os
from classes import worker,department




events = ("start", "end", "start-ns", "end-ns")
file=os.path.join(os.getcwd(),'test.xml')
departments={}

def parse(file,events,departments):

    for event, elem in ET.iterparse(file,events=events):
        if event == 'start':
            if elem.attrib:
                if departments.get(elem.attrib[elem.keys()[0]]) is None:
                    departments.update({elem.attrib[elem.keys()[0]]:
                                            department(elem.attrib[elem.keys()[0]])})
                else:
                    pass
            elif elem.tag=='employment':
                last_key=list(departments.keys())[-1]
                departments[last_key].push_worker(worker(0,0,0,0,0))

            elif elem.text.strip():

                last_key = list(departments.keys())[-1]
                worker_=departments[last_key].get_last_worker()
                setattr(worker_,elem.tag,elem.text) if elem.tag != "salary" else setattr(worker_,elem.tag,int(elem.text))

parse(file,events,departments)

class CommandEdit(QtWidgets.QUndoCommand):
    def __init__(self, itemWidget, item, index, textBeforeEdit,descr):
        super(CommandEdit, self).__init__(descr)
        self.itemWidget = itemWidget
        self.textBeforeEdit = textBeforeEdit
        self.textAfterEdit = item.text()
        self.index=index
        self.item=item


    def redo(self):
        self.itemWidget.blockSignals(True)
        self.itemWidget.itemFromIndex(self.index).setText(self.textAfterEdit)
        self.itemWidget.blockSignals(False)

    def undo(self):
        self.itemWidget.blockSignals(True)
        self.itemWidget.itemFromIndex(self.index).setText(self.textBeforeEdit)
        self.itemWidget.blockSignals(False)


class Window(QtWidgets.QWidget):
    def __init__(self, data):
        super(Window, self).__init__()

        self.undoStack = QtWidgets.QUndoStack(self)
        undo_label=QtWidgets.QLabel("История операций")
        v_layout=QtWidgets.QVBoxLayout()
        v_layout.addWidget(undo_label)

        undoView = QtWidgets.QUndoView(self.undoStack)

        v_layout.addWidget(undoView)

        h_lay=QtWidgets.QHBoxLayout(self)
        self.tree = QtWidgets.QTreeView(self)
        layout = QtWidgets.QVBoxLayout(self)
        h_lay.addLayout(layout,1)
        h_lay.addLayout(v_layout)


        layout.addWidget(self.tree)
        self.stack_of_obj=set()


        cancel_button=QtWidgets.QPushButton("Отмена")
        undo_cancel_button=QtWidgets.QPushButton("Отмена изменений")
        save_button=QtWidgets.QPushButton("Cохранить изменения")
        layout_buttons=QtWidgets.QHBoxLayout(self)
        layout_buttons.addStretch(1)
        layout_buttons.addWidget(cancel_button,)
        layout_buttons.addWidget(undo_cancel_button,)
        layout_buttons.addWidget(save_button)
        layout_buttons.addSpacing(40)
        layout_buttons.insertSpacing(2,20)
        layout.addLayout(layout_buttons)
        cancel_button.clicked.connect(self.undoStack.undo)
        undo_cancel_button.clicked.connect(self.undoStack.redo)
        save_button.clicked.connect(self.save_changes)
        self.model = QtGui.QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Название', 'Средняя зарплата\nсотрудников'
                                                 ,'Количество сотрудников','Должность','Зарплата'])
        self.tree.header().setDefaultSectionSize(400)
        self.tree.setModel(self.model)
        self.tree.clicked[QtCore.QModelIndex].connect(self.clicked)
        self.model.itemChanged.connect(self.changed)
        self.model.setRowCount(0)
        self.pos ={}
        self.bulid_tree(data)
        self.textBeforeEdit = ""
        self.index=None
        self.tree.expandAll()


    def bulid_tree(self,data):
        self.model.setRowCount(0)
        root = self.model.invisibleRootItem()
        item = QtGui.QStandardItem("Отделы")
        root.appendRow(item)
        root=item
        for obj in data:
            item=QtGui.QStandardItem(obj)
            self.pos.update({str(item).split()[3]:data[obj]})
            root.appendRow([item,QtGui.QStandardItem(str(data[obj].get_avg_salary())),
                            QtGui.QStandardItem(str(data[obj].get_quantity_of_workers()))])

            dep=data[obj]
            root=item
            for employ in dep.get_workers():
                full_name=QtGui.QStandardItem(employ.get_full_name())
                function_=QtGui.QStandardItem(employ.get_function())
                salary=QtGui.QStandardItem(str(employ.get_salary()))

                self.pos.update({str(full_name).split()[3]:["full_name", employ],
                                 str(function_).split()[3]:["function",employ],
                                 str(salary).split()[3]:['salary',employ]})
                root.appendRow([full_name,
                            QtGui.QStandardItem(),
                            QtGui.QStandardItem(),function_,salary
                            ])


            root=self.model.item(self.model.rowCount()-1)

    def clicked(self, index):
        item = self.model.itemFromIndex(index)
        self.textBeforeEdit=item.text()
        self.index=index



    def changed(self,item):

        command = CommandEdit(self.model, item, self.index,
                              self.textBeforeEdit,
                              f"Изменен объект {self.textBeforeEdit} на {item.text()}")
        self.undoStack.push(command)
        self.stack_of_obj.add(self.index)


    def save_changes(self):
        for item in self.stack_of_obj:
            self.change_into_class(self.model.itemFromIndex(item))


    def change_into_class(self,item):
        key = str(item).split()[3]
        try:
            if self.pos[key].__class__.__name__ == 'department':
                self.pos[key].name = item.text()
                print(self.pos[key], self.pos[key].name)
            elif self.pos[key][1].__class__.__name__ == 'worker':
                worker_ = self.pos[key][1]
                print(worker_)
                if self.pos[key][0] == 'full_name':
                    try:
                        worker_.surname, worker_.name, worker_.middleName = item.text().split()
                    except ValueError:
                        task = [worker_.surname, worker_.name, worker_.middleName]
                        for attr in enumerate(item.text().split()):
                            task[attr[0]] = attr[1]
                else:
                    setattr(worker_, self.pos[key][0], int(item.text())) if \
                        self.pos[key][0] == 'salary' else setattr(worker_, self.pos[key][0], item.text())
        except KeyError:
            pass





if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    window = Window(departments)
    window.setGeometry(500, 50, 1400, 500)
    window.show()
    sys.exit(app.exec_())