from pytube import YouTube
import PySimpleGUI as sg
from threading import Thread
import os
import pyperclip
import time
from win10toast import ToastNotifier
import ctypes
import glob

myappid = 'Bean.YTDownloader.Downloader.1'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

tn = ToastNotifier()
bmc_logo = os.path.realpath(__file__).replace("ytdownloader.py","bmc-button.png")
coffee_icon = os.path.realpath(__file__).replace("ytdownloader.py","cicon.ico")

sg.theme("LightBrown4")


layout = [
    [sg.Text("Bean YTDownloader")],
    [sg.InputText("", key="output"), sg.FolderBrowse("Select Download Folder", target=(1,0))],
    [sg.InputText("Type or Paste Youtube Link Here", key="ytlink"), sg.Button("Paste Link", key="paste")],
    [sg.Radio("Video", group_id="dopts", key="video"), sg.Radio("Simply Audio", group_id="dopts")],
    [sg.Button("Click to Download", key="download")],
    [sg.ProgressBar(100, orientation="h", size=(50,10), key="progress")],
    [sg.Button("Close", key="quit"), sg.Button("Help!", key="help")]
]

fsize = 0
window = sg.Window(title="Bean YTDownloader", layout=layout, element_justification="c", icon=coffee_icon)

progress = window["progress"]

sg.popup("Welcome to Bean YTDownloader!\nPlease note this is an open source project that is currently in development.\n\nNOTE: You should only use this tool to download videos you have created or own the copyright for.\nDownloading videos you don't own the rights to is considered a copyright violation.", title="Welcome!", icon=coffee_icon)

def output_loc():
    dirloc = str(values["output"])
    return dirloc

def progress_func(stream=None, data=None, fleft=None):
    percent = (100*(fsize-fleft))/fsize
    progress.update(percent)
    print(percent)

def yt_download(window):
    global fsize
    dirloc = str(values["output"])
    ytlink = values["ytlink"]
    yt = YouTube(ytlink, on_progress_callback=progress_func)

    info = yt.vid_info
    title = yt.title
    if values["video"] == True:
        print(dirloc)
        videofile = yt.streams.filter(res="1080p", progressive=True).first()
        if videofile == None:
            try:
                videofile = yt.streams.filter(progressive=True).get_highest_resolution()
            except:
                sg.popup("Video could not be downloaded at the moment!", title="Sorry!")
        print(videofile)
        fsize = int(videofile.filesize)
        videofile.download(output_path = dirloc)
    if values["video"] == False:
        #str_title = str(title).replace("&", "").replace(":","").replace("?","").replace("*","").replace("|","")
        audiofile = yt.streams.filter(only_audio=True).first()
        fsize = int(audiofile.filesize)
        file = audiofile.download(output_path = dirloc+"/")
        download_dir = glob.glob(dirloc+"/*.mp4")
        old_file = max(download_dir, key=os.path.getctime)
        print(old_file)
        new_file = old_file.replace(".mp4",".mp3")
        print(new_file)
        os.rename(old_file, new_file)
    
    tn.show_toast(title="Download Complete!", msg="Your Youtube download is ready! Enjoy!", icon_path=coffee_icon)

def yt_thread():
    threading = Thread(target=yt_download, args=(window, ), daemon=True).start()

def help_window():
    help_layout = [
        [sg.Text("How to Use Bean YTDownloader", font=("bold, 15"))],
        [sg.Text("Bean YTDownloader is a simple and lightweight program that allows you to\ndownload Youtube video and audio quickly and safely.\n1. Select download location.\n2. Paste Youtube Link\n3. Wait for the download notifaction.\n4. Enjoy your tunes or video!\n5. Buy me a coffee! (Optional)\n\nThis program uses the Pytube and PySimpleGUI Python Packages.")],
        [sg.Text("Version 1.00")],
        [sg.Image(filename=bmc_logo, enable_events=True, key="bmc")],
        [sg.Button("Close", key="close")]
    ]

    window = sg.Window(title="Help Me!", layout=help_layout, element_justification="c", icon=coffee_icon)

    while True:
        event, values = window.Read(timeout=300)
        if event == "close" or event == sg.WIN_CLOSED:
            window.close()
            break
        if event == "bmc":
            os.system("start https://www.buymeacoffee.com/zgoreczny")

while True:
    event, values = window.Read()
    if event == "quit" or event == sg.WIN_CLOSED:
        break
    if event == "download":
        if values["ytlink"].__contains__("youtube") and values["output"] != "":
            yt_thread()
            output_loc()
        else:
            sg.popup("Please insert a valid Youtube link and select a download folder!", title="Whoops!", icon=coffee_icon)
    if event == "help":
        help_window()
    if event == "paste":
        paste = pyperclip.paste()
        window["ytlink"].update(paste)

