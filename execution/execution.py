from tkinter import *
import os
import threading

def thread_it(func, *args):
    '''将函数打包进线程'''
    # 创建
    t = threading.Thread(target=func, args=args)
    # 守护 !!!
    t.setDaemon(True)
    # 启动
    t.start()
    # 阻塞--卡死界面！
    # t.join()

def startServer():

    os.chdir('C:\\Users\\肖洪才\\PycharmProjects\\liveTemplateManage')
    os.system('python manage.py runserver')


def test():
    print('test')

window = Tk()
window.configure(background='white')

window.title("Run Server")

window.geometry('350x200')

lbl = Label(window, text="Start livetemplate Management Server",font=(None, 15),bg="white", height=5, width=50)

lbl.grid(column=0, row=0)


def clicked():
    thread_it(startServer)

    lbl.configure(text="Success!",fg='green',font=(None,15))
    btn.configure(state=DISABLED,text='Success!')
    # window.destroy()



btn = Button(window, text="Run",font=(None, 15), command=clicked,bg="white",height = 3, width = 20)
window.geometry("500x200+530+300")

btn.grid(column=0, row=1)

window.mainloop()




