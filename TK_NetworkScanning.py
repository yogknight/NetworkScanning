import re
import subprocess
import sys
import threading
import webbrowser
from tkinter import Menu, Tk, messagebox, ttk, StringVar, Listbox
from tkinter.filedialog import askopenfilename, asksaveasfilename

from PIL import Image, ImageTk

TITLE_FONT = ("Helvetica", 16, "bold")
FALSE = False
function = 'function'

# images
img_about = Image.open('about_img.png')
img_IPtest = Image.open('IPtest_img.png')
img_Github = Image.open('GitHub_img.png')
img_ALL_IPimg = Image.open('ALL_IP_img.png')
img_infile = Image.open('infile_img.png')
img_outFile = Image.open('outFile_img.png')
img_go = Image.open('go_img.png')
img_one_IPtes=Image.open('one_IPtest_img.png')

# 定义图片尺寸
about_image = img_about.resize((60, 60), Image.ANTIALIAS)
IPtest_image = img_IPtest.resize((60, 60), Image.ANTIALIAS)
Github_image = img_Github.resize((10, 10), Image.ANTIALIAS)
ALL_IPimg_image = img_ALL_IPimg.resize((60, 60), Image.ANTIALIAS)
one_IPtest_image = img_one_IPtes.resize((60, 60), Image.ANTIALIAS)

# 导入导出
infile_image = img_infile.resize((25, 25), Image.ANTIALIAS)
outFile_image = img_outFile.resize((25, 25), Image.ANTIALIAS)

go_image = img_go.resize((25, 25), Image.ANTIALIAS)


class Network_Test(Tk):
    """
    MainApp
    """

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        mainframe = ttk.Frame(self, padding=(3, 3, 12, 12),
                              borderwidth=2, relief='sunken')
        self.resizable(width=False, height=False)#禁止拉升窗口
        self.iconbitmap(".\\app_ico.ico")
        mainframe.grid(column=0, row=0, sticky="nwes")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.hig = []
        for i in range(0, 18):
            hi = mainframe.rowconfigure(i, weight=1)
            self.hig.append(hi)
        self.big = []
        for j in range(0, 25):
            tc = mainframe.columnconfigure(j, weight=1)
            self.big.append(tc)
        # self.geometry("600x300")
        self.frames = {}
        for F in (StartPage, Network_scan, About_page, ALL_IPtest):
            page_name = F.__name__
            frame = F(parent=mainframe, mainframe=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(ttk.Frame):
    """
    初始界面
    """

    def __init__(self, parent, mainframe):
        ttk.Frame.__init__(self, parent)
        self.mainframe = mainframe
        self.mainframe.title("网络测试(NetworkTest)")

        # 菜单栏
        self.mainframe.option_add('*tearOff', FALSE)
        menubar = Menu(self.mainframe)
        self.mainframe['menu'] = menubar
        menu_tools = Menu(menubar)
        menu_help = Menu(menubar)
        menubar.add_cascade(menu=menu_tools, label='工具库(Tools)')
        menubar.add_cascade(menu=menu_help, label='帮助(H)')
        menu_tools.add_command(label='IP地址测试(IP Test)',
                               command=lambda: mainframe.show_frame("StartPage"))
        menu_help.add_command(
            label='关于(About)', command=lambda: mainframe.show_frame("About_page"))
        menu_tools.add_command(label='网段扫描(Network scanning)',
                               command=lambda: mainframe.show_frame("Network_scan"))
        menu_tools.add_command(label='自定义扫描(Auto Test)',
                               command=lambda: mainframe.show_frame("ALL_IPtest"))
        

        #单个地址测试
        self.one_IPtest_img = ImageTk.PhotoImage(one_IPtest_image)
        self.IPtest = ttk.Label(self, text='IP地址测试',
                                image=self.one_IPtest_img, compound='left', font=TITLE_FONT, foreground='#1296db')

        self.Ip_start = ttk.Label(self, text='输入地址：', compound='left')
        self.one_iptest = StringVar()
        self.one_Ip_Entry = ttk.Entry(self, textvariable=self.one_iptest)
        self.one_scanning = ttk.Button(
            self, text="测试",command=lambda: self.One_IPtest())

        self.clear_views = ttk.Button(
            self, text="清空",command=lambda: self.cleane_view())

        self.Stop_test = ttk.Button(
            self, text="停止",command=lambda: self.Stop_Popen())


        self.choie_N = ttk.Label(self, text="选择测试次数：", compound='left')
        self.view_title = ttk.Label(self, text="测试结果", compound='left')

        #stop_popen
        self.stop_IPtest = StringVar()
        self.stop_IPtest.set('1')

        # 选择ping次数
        self.count_IPtest = StringVar()
        self.country_one = ttk.Combobox(self, textvariable=self.count_IPtest)
        self.country_one.bind('<< ComboboxSelected >>', function)
        self.country_one['values'] = ('2', '3', '4', '5','∞')
        self.count_IPtest.set('4')


        # 结果显示
        VERTICAL = "vertical"
        self.Scanning_one = Listbox(self, height=20, width=100)
        self.ScanViews_one = ttk.Scrollbar(
            self, orient=VERTICAL, command=self.Scanning_one.yview)
        self.Scanning_one['yscrollcommand'] = self.ScanViews_one.set
        ttk.Sizegrip().grid(column=2, row=4, sticky="se")



        #布局
        self.IPtest.grid(column=0, row=0, sticky="nwes", padx=5, pady=5)
        self.Ip_start.grid(column=1, row=1, sticky="nwes", padx=5, pady=5)
        self.one_Ip_Entry.grid(column=2, row=1, sticky="nwes", padx=5, pady=5)
        self.choie_N.grid(column=3, row=1, sticky="nwes", padx=5, pady=5)
        self.country_one.grid(column=4, row=1, sticky="nwes", padx=5, pady=5)
        self.one_scanning.grid(column=5, row=1, sticky="nwes", padx=5, pady=5)
        self.view_title.grid(column=1, row=2, sticky="nwes",padx=5, pady=5)
        self.ScanViews_one.grid(column=21, row=3, sticky="ns")
        self.Scanning_one.grid(column=1, row=3, sticky="nwes",columnspan=10,padx=5, pady=5)
        self.Stop_test.grid(column=1, row=11, sticky="nwes",columnspan=1,rowspan=1,padx=5, pady=5)
        self.clear_views.grid(column=10, row=11, sticky="nwes",columnspan=1,rowspan=1,padx=5, pady=5)
    

    #开始ping测试
    def One_IPtest(self):
        """
        获取IP，开始Ping测试，结果实时输出到窗口
        """
        one_ip = self.one_iptest.get()#获取IP
        count_testnum=self.count_IPtest.get()#获取测试次数
        control=self.stop_IPtest.get()
        self.stop_IPtest.set('1')
        if count_testnum=='∞':
            add_num="ping -t "
        else:
            add_num="ping -n {0} ".format(count_testnum)
        cmd=add_num+"{0}".format(one_ip)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell =True)
        while p.poll() is None:
                line = p.stdout.readline().decode('gbk')
                line = line.strip()
                control=self.stop_IPtest.get()
                if line:
                    test_out='Subprogram output: [{}]'.format(line)
                    self.Scanning_one.insert('end',test_out)
                    self.Scanning_one.update()
                if control=='0':
                        p.terminate()
                
    
    def cleane_view(self):
        self.Scanning_one.delete('0','end')
    
    def Stop_Popen(self):
        self.stop_IPtest.set('0')
        


class Network_scan(ttk.Frame):
    """
    网段扫描工具
    """

    def __init__(self, parent, mainframe):
        ttk.Frame.__init__(self, parent)
        self.mainframe = mainframe
        self.IPtest_img = ImageTk.PhotoImage(IPtest_image)
        self.IPtest = ttk.Label(self, text='地址段扫描',
                                image=self.IPtest_img, compound='left', font=TITLE_FONT, foreground='#1296db')

        self.Ip_start = ttk.Label(self, text='开始地址：', compound='left')
        self.Ip_end = ttk.Label(self, text='结束地址：', compound='left')
        self.var = StringVar()
        self.Ip_Entry_s = ttk.Entry(self)
        self.Ip_Entry_e = ttk.Entry(self, textvariable=self.var)

        self.get_end_IP = ttk.Button(
            self, text="自动", command=lambda: self.set_end_ip())
        self.Do_scanning = ttk.Button(
            self, text="开始扫描", command=lambda: self.start_ping())
        self.choie_num = ttk.Label(self, text="选择测试次数：", compound='left')

        # 选择ping次数
        self.countryvar = StringVar()
        self.country = ttk.Combobox(self, textvariable=self.countryvar)
        self.country.bind('<< ComboboxSelected >>', function)
        self.country['values'] = ('1', '2', '3', '4', '5')
        self.countryvar.set('3')
        # 网段地址图标
        self.list_index = 0
        self.label_list = []
        for i in range(1, 17):
            for j in range(9, 25):
                self.label = ttk.Label(
                    self, text=self.list_index, background="#CBCBCB")
                self.list_index += 1
                self.label.grid(column=j, row=i, sticky="nwes", padx=5, pady=5)
                self.label_list.append(self.label)

        # 界面布局
        self.IPtest.grid(column=0, row=0, sticky="nwes", padx=5, pady=5)
        self.Ip_Entry_s.grid(column=0, row=2, sticky="nwes", padx=5, pady=5)
        self.Ip_start.grid(column=0, row=1, sticky="nwes", padx=5, pady=5)
        self.Ip_end.grid(column=0, row=3, sticky="nwes", padx=5, pady=5)
        self.get_end_IP.grid(column=1, row=4, sticky="nwes", padx=5, pady=5)
        self.Ip_Entry_e.grid(column=0, row=4, sticky="nwes", padx=5, pady=5)
        self.choie_num.grid(column=0, row=5, sticky="nwes", padx=5, pady=5)
        self.country.grid(column=0, row=6, sticky="nwes", padx=5, pady=5)
        self.Do_scanning.grid(column=0, row=7, sticky="nwes", padx=5, pady=5)

    def set_end_ip(self):
        """
        填写起始地址后，默认填写结束地址为同网段最后一个地址
        """
        startip = self.Ip_Entry_s.get()
        pattern = r"((?:(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))$)"
        m = re.match(pattern, startip)      # 检查IP地址是否合法
        if m:
            startip = startip.split('.')
            startip[3] = '255'
            endip = '.'.join(startip)
            endip = self.var.set(endip)
        else:
            messagebox.showinfo(message='IP地址错误！\n地址只能为一个网段的IP，请检查你的输入！')

    def start_ping(self):
        """
        启动多线程
        """
        # 检测截至IP
        endip = self.var.get()
        pattern = r"((?:(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))$)"
        m = re.match(pattern, endip)      # 检查IP地址是否合法
        if m:
            end_ip_test = True
        else:
            end_ip_test = False
            messagebox.showinfo(message='IP地址错误！\n 详细信息：\n结束地址错误，请检查你的输入！')

        # 开始测试
        self.reset_ui()
        startip = self.Ip_Entry_s.get().split('.')
        endip = self.var.get().split('.')
        tmp_ip = startip
        if int(startip[3]) <= int(endip[3]) and end_ip_test:
            pthread_list = []
            for i in range(int(startip[3]), int(endip[3]) + 1):
                tmp_ip[3] = str(i)
                ip = '.'.join(tmp_ip)
                pthread_list.append(threading.Thread(
                    target=self.get_ping_result, args=(ip,)))
            for item in pthread_list:
                item.setDaemon(True)
                item.start()
        elif end_ip_test and int(startip[3]) > int(endip[3]):
            messagebox.showinfo(
                message='IP地址错误！\n详细信息：\n结束地址需要大于开始地址，请检查你的输入！')

    def get_ping_result(self, ip):
        """
        检查对应的IP是否被占用
        """
        num = self.countryvar.get()
        commands = "ping -n {0} -w 600".format(num)
        cmd_str = commands+" {0}".format(ip)
        DETACHED_PROCESS = 0x00000008   # 不创建cmd窗口
        try:
            subprocess.run(cmd_str, creationflags=DETACHED_PROCESS,
                           check=True)  # 仅用于windows系统
        except subprocess.CalledProcessError as err:
            self.set_ui(False, ip)
        else:
            self.set_ui(True, ip)

    def reset_ui(self):
        """
        初始化窗口IP窗格为灰色背景
        """
        for item in self.label_list:
            item['background'] = "#CBCBCB"

    def set_ui(self, result, ip):
        """
        设置窗口颜色
        result：线程ping的结果
        ip：为对于的IP地址
        """
        index = int(ip.split('.')[3])
        if result:
            self.label_list[index]['background'] = "#55AA7F"  # 设置背景为绿色
        else:
            self.label_list[index]['background'] = "#FF8E77"   # 设置背景为红色


class ALL_IPtest(ttk.Frame):
    """
    任意IP地址扫描
    扫描结显示到窗口
    也可以选择导出到文本文件
    """

    def __init__(self, parent, mainframe):
        ttk.Frame.__init__(self, parent)
        self.mainframe = mainframe
        # 获取图片
        self.ALLIP_img = ImageTk.PhotoImage(ALL_IPimg_image)
        self.infile_img = ImageTk.PhotoImage(infile_image)
        self.outFile_img = ImageTk.PhotoImage(outFile_image)
        self.go_img = ImageTk.PhotoImage(go_image)
        self.IPtest = ttk.Label(self, text='自定义扫描',
                                image=self.ALLIP_img, compound='left', font=TITLE_FONT, foreground='#1296db')
        self.Get_IPtxt = ttk.Button(
            self, text="导入IP文件", image=self.infile_img, compound='left',command=lambda: self.start_ping()())
        self.Go_Scanning = ttk.Button(
            self, text="开始扫描", image=self.go_img, compound='left')
        self.Out_ScanningTxt = ttk.Button(
            self, text="导出结果", image=self.outFile_img, compound='left',command=lambda: self.save_view())
        self.TestView = ttk.Label(
            self, text='扫描结果：', font=TITLE_FONT, foreground='#1296db')

        # 结果显示
        VERTICAL = "vertical"
        self.Scanning_L = Listbox(self, height=20, width=100)
        self.ScanViews = ttk.Scrollbar(
            self, orient=VERTICAL, command=self.Scanning_L.yview)
        self.Scanning_L['yscrollcommand'] = self.ScanViews.set
        ttk.Sizegrip().grid(column=2, row=4, sticky="se")
        self.Scanning_L.insert('end', 'IP地址               测试次数                通信状态')



        self.ScanViews.grid(column=21, row=3, sticky="ns")
        self.Scanning_L.grid(column=1, row=3, sticky="nwes",columnspan=20,padx=5, pady=5)
        self.IPtest.grid(column=0, row=0, sticky="nwes", padx=5, pady=5)
        self.Get_IPtxt.grid(column=1, row=1, sticky="nwes",columnspan=1,rowspan=1,padx=5, pady=5)
        self.Go_Scanning.grid(column=2, row=1, sticky="nwes",columnspan=1,rowspan=1, padx=5, pady=5)
        self.Out_ScanningTxt.grid(
            column=20, row=20, sticky="nwes",columnspan=1,rowspan=1,padx=5, pady=5)
        self.TestView.grid(column=1, row=2, sticky="nwes", padx=5, pady=5)

    # 获取IP
    def check_file(self):
        """
         askopenfilename获取IP地址文件
        """
        self.open_filename = askopenfilename(
            title='打开文件', filetypes=[('All Files', '*')])
        with open(self.open_filename, 'r') as f:
            self.startip = f.readlines()
        return(self.startip)
    # 处理IP
    def start_ping(self):
        """
        启动多线程
        检查IP地址合法性
        """
        get_ALLip=self.check_file()
        pthread_list = []
        for line in get_ALLip:
            if len(line.strip()):
                ip=line.strip('\n')
                pattern = r"((?:(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))$)"
                m = re.match(pattern, line)      # 检查IP地址是否合法
                if m:
                    ip_check = True
                else:
                    ip_check = False
                # 开始测试
                pthread_list.append(threading.Thread(target=self.get_ping_result, args=(ip,)))
        for item in pthread_list:
            item.setDaemon(True)
            item.start()
        with open('./IPtest.txt','w+') as f:
            f.write("+---------------+----------+----------+\n")
            f.write("|    IP地址     |  扫描次数 |  通信情况 |\n")
            f.write("+---------------+----------+----------+\n")
        f.close()

    def get_ping_result(self, ip):
        """
        检查对应的IP是否被占用
        """
        cmd_str = "ping {0} -n 4 -w 600".format(ip)
        DETACHED_PROCESS = 0x00000008   # 不创建cmd窗口
        try:
            subprocess.run(cmd_str, creationflags=DETACHED_PROCESS,
                           check=True)  # 仅用于windows系统
        except subprocess.CalledProcessError as err:
            self.write_file(False, ip)
        else:
            self.write_file(True, ip)

    def write_file(self, result, ip):
        """
        将结果写入文件
        result：线程ping的结果
        ip：为对于的IP地址
        """
        ip=ip.strip('\n')
        with open('./IPtest.txt','a+') as f:
            if result:
                self.Scanning_L.insert('end', '%s               4               通信正常' % ip)
                f.write("|  {0}  |   4    |   通信正常  |\n".format(ip))
                f.write("+---------------+----------+----------+\n")
                self.Scanning_L.update()
            else:
                self.Scanning_L.insert('end', '%s               4               通信失败' % ip)
                f.write("|  {0}  |   4    |   通信失败  |\n".format(ip))
                f.write("+---------------+----------+----------+\n")
                self.Scanning_L.update()
    def save_view(self):
        r =asksaveasfilename(title='保存文件', initialdir='./', initialfile='table.txt')
        with open('./IPtest.txt','r+') as f:
            lines=f.read()
        with open(r,'a+') as S:
            S.write(lines)
        

class About_page(ttk.Frame):
    """
    关于APP的详细信息
    """

    def __init__(self, parent, mainframe):
        ttk.Frame.__init__(self, parent)
        self.mainframe = mainframe
        self.about_img = ImageTk.PhotoImage(about_image)
        self.Github_img = ImageTk.PhotoImage(Github_image)
        self.About = ttk.Label(
            self, text='关于', image=self.about_img, compound='left', font=TITLE_FONT, foreground='#1296db')
        self.About_info1 = ttk.Label(self, text='版本：0.1(Toykang)')
        self.About_info2 = ttk.Label(self, text='提交：1')
        self.About_info3 = ttk.Label(
            self, text='日期：2018, 12, 3, 14, 27, 9, 402166 ')
        self.About_info4 = ttk.Label(self, text='源码：源码发布于GiHub，更多详细信息请点击')

        self.About_source = ttk.Button(
            self, image=self.Github_img, command=lambda: self.web_view())

        self.About.grid(column=0, row=0, sticky="nwes", padx=5, pady=5)
        self.About_info1.grid(column=1, row=1, sticky="nwes", padx=5, pady=5)
        self.About_info2.grid(column=1, row=2, sticky="nwes", padx=5, pady=5)
        self.About_info3.grid(column=1, row=3, sticky="nwes", padx=5, pady=5)
        self.About_info4.grid(column=1, row=4, sticky="nwes", padx=5, pady=5)
        self.About_source.grid(column=2, row=4, sticky="nwes", padx=5, pady=5)

    def web_view(self):
        webbrowser.open("https://github.com/Toykang/NetworkScanning")


if __name__ == "__main__":
    app = Network_Test()
    app.mainloop()
