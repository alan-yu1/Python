#定义学生类型 姓名、学号、科目
class Student:
    def __init__(self, id1,name,python_input,c_score_input,math_input, foreign_language_input):
        self.ID=id1
        self.name=name
        self.python =python_input
        self.math = math_input
        self.foreign_language = foreign_language_input
        self.C=c_score_input

    def __str__(self):
        return f"学号:{self.id}\n总分:{self.total()}\n"
    #计算它自己的总成绩
    def total(self):
        return self.python+ self.math + self.foreign_language+self.C




# 查询函数
def query():
    def menu():
        print("\t\t\t\t\t\t\t-------------------------------")
        print("\t\t\t\t\t\t\t      欢迎进入查询模块          ")
        print("\t\t\t\t\t\t\t------------------------------ ")
        print("\t\t\t\t\t\t\t     1.查询单个学生成绩         ")
        print("\t\t\t\t\t\t\t     2.查询所有学生成绩         ")
        print("\t\t\t\t\t\t\t     3.查询不及格名单           ")
        print("\t\t\t\t\t\t\t     4.查询班级平均成绩         ")
        print("\t\t\t\t\t\t\t     5.    退出模块            ")
        print("\t\t\t\t\t\t\t------------------------------")
    #功能1
    def single():
        global Data
        print("\t\t\t\t\t\t\t查看学员成绩：")
        print()
        # 列表生成式
        b = [i.ID for i in Data]
        # 判断该生是否存在
        while 1:
            id_input = input("\t\t\t\t\t\t\t请输入学号：")
            if id_input in b:
                break
            print('\t\t\t\t\t\t\t该生信息不存在，请重新输入！')
        # 过滤函数+匿名函数
        a = list(filter(lambda i: i.ID == id_input, Data))[0]#注意这个[0]
        print("\t\t\t\t\t\t\t学号：{:} 姓名:{:}".format(a.ID,a.name))
        print("\t\t\t\t\t\t\tpython成绩：{:} C语言：{:} 高等数学:{:} 外语:{}".format(a.python,a.C,a.math,a.foreign_language))
        print("\t\t\t\t\t\t\t",end="")
        if a.python<60:
            print("python成绩不及格",end=" ")
        if a.foreign_language<60:
            print("外语成绩不及格",end=" ")
        if a.math<60:
            print("数学成绩不及格",end=" ")
        if a.C<60:
            print("C语言成绩不及格",end=" ")
        print()

    #功能2
    def all():
        global Data
        for i in Data:
            print("\t\t\t\t\t\t\t学号：{:} 姓名:{:}".format(i.ID,i.name))
            print("\t\t\t\t\t\t\tpython成绩：{:} C语言：{:} 高等数学:{:} 外语:{}".format(i.python,i.C,i.math,i.foreign_language))
            print()


    # 查看不及格名单
    def failed():
        math_f = []
        python_f = []
        foreign_language_f= []
        c_f=[]
        global Data
        for i in Data:
            if i.math < 60:
                math_f.append([i.ID,i.name,i.math])
            if i.python < 60:
                python_f.append([i.ID,i.name,i.python])
            if i.foreign_language < 60:
                foreign_language_f.append([i.ID,i.name,i.foreign_language])
            if i.C < 60:
                c_f.append([i.ID,i.name,i.C])

        print("\t\t\t\t\t\t\t高等数学不及格名单：")
        list_name_math = []
        list_name_math.append('高等数学不及格人员')
        for i in math_f:
            print("\t\t\t\t\t\t\t学号:{} 姓名:{} 成绩:{}".format(i[0],i[1],i[2]))
            list_name_math.append(i[1])
        print()
        print("\t\t\t\t\t\t\tC语言不及格名单：")
        list_name_c = []
        list_name_c.append('C语言不合格人员')
        for i in c_f:
            print("\t\t\t\t\t\t\t学号:{} 姓名:{} 成绩:{}".format(i[0], i[1], i[2]))
            list_name_c.append(i[1])
        print()
        print("\t\t\t\t\t\t\tPython不及格名单：")
        list_name_python = []
        list_name_python.append('python不合格人员')
        for i in python_f:
            print("\t\t\t\t\t\t\t学号:{} 姓名:{} 成绩:{}".format(i[0],i[1],i[2]))
            list_name_python.append(i[1])
        print()
        print("\t\t\t\t\t\t\t外语不及格名单：")
        list_name_foreign_language = []
        list_name_foreign_language.append('外语不合格人员')
        for i in foreign_language_f:
            list_name_foreign_language.append(i[1])
            print("\t\t\t\t\t\t\t学号:{} 姓名:{} 成绩:{}".format(i[0],i[1],i[2]))
        list =[]
        list.append(list_name_math)
        list.append(list_name_c)
        list.append(list_name_python)
        list.append(list_name_foreign_language)
        return list

    #平均数查询
    def average():
        global Data
        c_score=[]
        python=[]
        math=[]
        foreign_language=[]
        num=len(Data)
        for i in Data:
            c_score.append(i.C)
            python.append(i.python)
            math.append(i.math)
            foreign_language.append(i.foreign_language)

        print("\t\t\t\t\t\t\t------------------------")
        print("\t\t\t\t\t\t\t     班级平均成绩        ")
        print("\t\t\t\t\t\t\t     高等数学：%.2f       "%(sum(math)/num))
        print("\t\t\t\t\t\t\t     C语言：%.2f          "%(sum(c_score)/num))
        print("\t\t\t\t\t\t\t     Python:%.2f          "%(sum(python)/num))
        print("\t\t\t\t\t\t\t     外语：%.2f           "%(sum(foreign_language)/num))
        print("\t\t\t\t\t\t\t-------------------------")



#主区域:
    menu()
    times=0
    while 1:
        if times>=2:
            print("\t\t\t\t\t\t\t按8可以查看菜单")
            print()
            times=0
        print()
        choose=eval(input("\t\t\t\t\t\t\t选择:"))
        print()
        if choose == 1:
            single()
            times+=1
        elif choose == 2:
            all()
            times+=1
        elif choose==3:
            failed_name = failed()
            print(failed_name)
            ########输出不合格人员功能#######
            path = "D:\\Program Files\\办公文档\\外接\\不合格人员.txt"  # 新创建的txt文件的存放路径
            t = ''
            with open(path, 'w') as q:
                for i in failed_name:
                    for e in range(len(i)):
                        t = t + str(i[e]) + ' '
                    q.write(t.strip(' '))
                    q.write('\n')
                    t = ''

            times+=1
        elif choose==4:
            average()
            times+=1
        elif choose==8:
            menu()
            times+=1
        else:
            break






#菜单
def menu_select():
   print("""


                               ✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨    ヾ(≧▽≦*)o ~hello
                               ✨----欢迎使用成绩管理系统-----✨
                               ✨-+------------------------+-✨     (*^▽^*)按下对应的键位即可~
                               ✨    1.进入信息管理模块       ✨
                               ✨----------------------------✨     (￣▽￣)"信息管理就是存入或删除学生学号姓名之类的
                               ✨    2.进入信息排序模块       ✨
                               ✨----------------------------✨     （＾∀＾●）ﾉｼ按学号或科目排序啦
                               ✨    3.进入信息查询模块       ✨
                               ✨----------------------------✨      (/▽＼)查询平均成绩、不及格名单啦
                               ✨    4. 退  出  系  统        ✨
                               ✨-+------------------------+-✨       (～￣▽￣)～    按4可以退出系统啦~
                               ✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨
   """)


#信息管理
def student_manage():

        #增加信息
        def record():
            global Data
            #列表生成式
            b = [i.ID for i in Data]
            while 1:
                id_input = input("\t\t\t\t\t\t\t请输入学号：").strip()#移除输入数字之前的0比如001 移除之后就是1
                # 检测重复输入学号
                if id_input not in b:
                    break
                print('\t\t\t\t\t\t\t该生信息已存在，请重新输入！')
            name=input("\t\t\t\t\t\t\t姓名:")
            python = int(input("\t\t\t\t\t\t\tpython成绩:"))
            c_score=eval(input("\t\t\t\t\t\t\tC语言成绩："))
            math = int(input("\t\t\t\t\t\t\t高等数学成绩:"))
            foreign_language = int(input("\t\t\t\t\t\t\t外语成绩:"))
            Data.append(Student(id_input,name,python,c_score,math,foreign_language))
            print("\t\t\t\t\t\t\t添加成功！")


        #删除学生信息
        def delete():
            global Data
            b = [i.ID for i in Data]
            while 1:
                id_input = input("\t\t\t\t\t\t\t请输入学号：")
                if id_input in b:
                    break
                print('\t\t\t\t\t\t\t该生信息不存在，请重新输入！')
            #匿名函数+筛选元素构成新列表，用新列表替换旧列表
            a = list(filter(lambda i: i.ID != id_input, Data))
            #替换
            Data = a
            print("\t\t\t\t\t\t\t删除成功!")



        #子菜单
        def menu():
            print("\t\t\t\t\t\t\t-------------------------------")
            print("\t\t\t\t\t\t\t    欢迎进入学生信息管理模块     ")
            print("\t\t\t\t\t\t\t------------------------------ ")
            print("\t\t\t\t\t\t\t     1.  添加学生信息         ")
            print("\t\t\t\t\t\t\t     2.  删除学生信息         ")
            print("\t\t\t\t\t\t\t     3.    退出模块            ")
            print("\t\t\t\t\t\t\t------------------------------")


        menu()
        while 1:
            print()
            choose=eval(input("\t\t\t\t\t\t\t选择："))
            print()
            if choose==1:
                record()
            elif choose==2:
                delete()
            elif choose==8:
                menu()
            else:
                break




#单科成绩排序、学号排序
def sort_made():

    def menu():
        print("\t\t\t\t\t\t\t-------------------------------")
        print("\t\t\t\t\t\t\t      欢迎进入排列模块          ")
        print("\t\t\t\t\t\t\t------------------------------ ")
        print("\t\t\t\t\t\t\t     1.  按学号排列         ")
        print("\t\t\t\t\t\t\t     2. 按单科成绩排列         ")
        print("\t\t\t\t\t\t\t     3.   退出模块            ")
        print("\t\t\t\t\t\t\t------------------------------")


    menu()
    global Data
    times=0
    while 1:
        if times>=2:
            print("\t\t\t\t\t\t\t按8可以显示菜单")
            print()
            times=0
        print()
        choose=eval(input("\t\t\t\t\t\t\t请选择："))
        if choose==1:
            Data=sorted(Data,key=lambda x:eval(x.ID))
            times+=1
        elif choose==2:
            subject=input("\t\t\t\t\t\t\t请输入科目：")
            times+=1
            if subject=="高等数学"or subject=="数学":
                Data=sorted(Data,key=lambda x:x.math,reverse=True)
            if subject=="外语":
                Data = sorted(Data, key=lambda x: x.foreign_language,reverse=True)
            if subject=="Python":
                Data = sorted(Data, key=lambda x: x.python,reverse=True)
            if subject=="C语言":
                Data = sorted(Data, key=lambda x: x.C,reverse=True)
        elif choose==8:
            menu()
        else:
            break




#起始
from random import randint

#提前创建对象0=99号 作用调试程序
Data=[]
for i in range(0,11):
    Data.append(Student(f"{i}","student"+ str(i), randint(40, 100), randint(50, 100),randint(30,100),randint(50,100)))
    # print(Data[i].ID)
#截止




#主函数
def main():
    menu_select()
    times=0
    while 1:
        if times>=2:
            print("\t\t\t\t\t\t\t按8可显示主菜单")
            print()
            times=0
        print()
        choose=eval(input("\t\t\t\t\t\t\t请输入:"))
        print()
        if choose==1:
            student_manage()
            times+=1
        elif choose==2:
            sort_made()
            times+=1
        elif choose==3:
            query()
            times+=1
        elif choose==4:
            break
        elif choose==8:
            menu_select()






if __name__=="__main__":
    main()
