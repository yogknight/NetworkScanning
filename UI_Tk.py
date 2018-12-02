from tkinter import Tk, ttk, Menu
from PIL import ImageTk, Image
from tkinter import messagebox
import webbrowser

TITLE_FONT = ("Helvetica", 18, "bold")
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
        self.hig=[]
        for i in range(0,18):
                hi=mainframe.rowconfigure(i, weight=1)
                self.hig.append(hi)
        self.big=[]
        for j in range(0,25):
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
        IPtest = ttk.Label(self, text='局域网地址段扫描',
                           image=self.IPtest_img, compound='left')
        
        Ip_start = ttk.Label(self, text='开始地址：',compound='left')
        Ip_end = ttk.Label(self, text='结束地址：',compound='left')
        Ip_Entry_s = ttk.Entry(self)
        Ip_Entry_e = ttk.Entry(self)


        Do_scanning=ttk.Button(self, text="开始扫描")
        # 网段地址图标
        self.list_index = 0
        self.label_list = []
        for i in range(2, 18):
            for j in range(9, 25):
                self.label = ttk.Label(
                    self, text=self.list_index, background="#CBCBCB")
                self.list_index += 1
                self.label.grid(column=j, row=i, sticky="nwes",padx=5, pady=5)
                self.label_list.append(self.label)

        # 界面布局
        IPtest.grid(column=0, row=0, sticky="nwes",padx=5, pady=5)
        Ip_Entry_s.grid(column=0, row=3, sticky="nwes",padx=5, pady=5)
        Ip_start.grid(column=0, row=2, sticky="nwes",padx=5, pady=5)
        Ip_end.grid(column=0, row=4, sticky="nwes",padx=5, pady=5)
        Ip_Entry_e.grid(column=0, row=5, sticky="nwes",padx=5, pady=5)
        Do_scanning.grid(column=0, row=6, sticky="nwes",padx=5, pady=5)

        
class About_page(ttk.Frame):

    def __init__(self, parent, mainframe):
        ttk.Frame.__init__(self, parent)
        self.mainframe = mainframe
        self.about_img = ImageTk.PhotoImage(about_image)
        self.Github_img = ImageTk.PhotoImage(Github_image)
        About = ttk.Label(self, text='关于', image=self.about_img, compound='left')
        About_info1=ttk.Label(self, text='版本：0.1')
        About_info2=ttk.Label(self, text='提交：')
        About_info3=ttk.Label(self, text='日期：')
        About_info4=ttk.Label(self, text='源码：源码发布于GiHub')
        
        About_source=ttk.Button(self,image=self.Github_img,command=lambda: self.web_view())
        
        About.grid(column=0, row=0, sticky="nwes",padx=5, pady=5)
        About_info1.grid(column=1, row=1, sticky="nwes",padx=5, pady=5)
        About_info2.grid(column=1, row=2, sticky="nwes",padx=5, pady=5)
        About_info3.grid(column=1, row=3, sticky="nwes",padx=5, pady=5)
        About_info4.grid(column=1, row=4, sticky="nwes",padx=5, pady=5)
        About_source.grid(column=2, row=4, sticky="nwes",padx=5, pady=5)
    def web_view(self):
        webbrowser.open("http://www.baidu.com")

    

if __name__ == "__main__":
    app = Network_Test()
    app.mainloop()
