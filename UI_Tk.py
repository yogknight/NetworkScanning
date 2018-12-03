import re
import subprocess
import sys
import threading
import webbrowser
from tkinter import *
from tkinter import Menu, Tk, messagebox, ttk

from PIL import Image, ImageTk

TITLE_FONT = ("Helvetica", 16, "bold")
FALSE = False

# images
img_about = Image.open('about_img.png')
img_IPtest = Image.open('IPtest_img.png')
img_Github = Image.open('GitHub_img.png')
about_image = img_about.resize((60, 60), Image.ANTIALIAS)
IPtest_image = img_IPtest.resize((60, 60), Image.ANTIALIAS)
Github_image = img_Github.resize((10, 10), Image.ANTIALIAS)


class Network_Test(Tk):
    """
    MainApp
    """

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        mainframe = ttk.Frame(self, padding=(3, 3, 12, 12),
                              borderwidth=2, relief='sunken')

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
        for F in (StartPage, Network_scan, About_page):
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
        menu_help.add_command(
            label='关于(About)', command=lambda: mainframe.show_frame("About_page"))
        menu_tools.add_command(label='网段扫描(Network scanning)',
                               command=lambda: mainframe.show_frame("Network_scan"))


class Network_scan(ttk.Frame):

    def __init__(self, parent, mainframe):
        ttk.Frame.__init__(self, parent)
        self.mainframe = mainframe
        self.IPtest_img = ImageTk.PhotoImage(IPtest_image)
        self.IPtest = ttk.Label(self, text='局域网地址段扫描',
                                image=self.IPtest_img, compound='left',font=TITLE_FONT,foreground='#1296db')

        self.Ip_start = ttk.Label(self, text='开始地址：', compound='left')
        self.Ip_end = ttk.Label(self, text='结束地址：', compound='left')
        self.var = StringVar()
        self.Ip_Entry_s = ttk.Entry(self)
        self.Ip_Entry_e = ttk.Entry(self, textvariable=self.var)

        self.get_end_IP = ttk.Button(
            self, text="自动", command=lambda: self.set_end_ip())
        self.Do_scanning = ttk.Button(
            self, text="开始扫描", command=lambda: self.start_ping())
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
        self.Do_scanning.grid(column=0, row=5, sticky="nwes", padx=5, pady=5)

    def set_end_ip(self):
        """
        填写起始地址后，默认填写结束地址为xxx.xxx.xxx.255
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
        '''
        启动多线程
        '''
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
        cmd_str = "ping {0} -n 3 -w 600".format(ip)
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


class About_page(ttk.Frame):

    def __init__(self, parent, mainframe):
        ttk.Frame.__init__(self, parent)
        self.mainframe = mainframe
        self.about_img = ImageTk.PhotoImage(about_image)
        self.Github_img = ImageTk.PhotoImage(Github_image)
        self.About = ttk.Label(
            self, text='关于', image=self.about_img, compound='left',font=TITLE_FONT,foreground='#1296db')
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
