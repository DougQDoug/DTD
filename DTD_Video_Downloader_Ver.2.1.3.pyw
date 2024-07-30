# DTD_Video_Downloader_Ver.2.1.3.pyw
# pyinstaller --onefile --name "DTD_Video_Downloader_Ver.2.1.3" --icon="DTD_Downloader2.ico" --add-data "yt-dlp.exe;." --add-data "C:\Users\Doug\Downloads\Python-3\2023 Projects\QT - DVD_Video_Downloader\ffmpeg\bin\ffmpeg.exe;." --disable-windowed-traceback DTD_Video_Downloader_Ver.2.1.3.pyw --clean
                                        # make sure that the yt-dlp is one that is a FULL .EXE file downloaded, not a pip install version!  Dont use a renamed file unless spefied with here!
                                        # To upgrade yt-dlp type in 'yt-dlp -U'  * make sure it's in the proper dir and use a cmd prompt. 
                                        # cd C:\Users\Doug\Downloads\Python-3\2023 Projects\QT - DVD_Video_Downloader  for the upgrade of yt-dlp
                                        # for the ffmpeg, it can't simply be updated.  Needs to be complied or downloaded fresh for updates.  Normal path is ...C:\...\ffmpeg\bin
                                        # visit https://www.gyan.dev/ffmpeg/builds/ to get the latest builds for FFMPEG.  Copy the 3 folders and 2 files inside the main folder
                                        # into C:\FFmpeg.  Simply overwrite, or create a old backup folder for the old one and drop new into it.
                                        # Updated on 8/14/2023, 10/1/2023

from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QCheckBox, QTableWidgetItem, QMessageBox
import sys, time, pyperclip, os
import subprocess 
from subprocess import Popen
from DTD_Video_Downloader_Ver2 import *
import signal
print("NOTES : Add in 30 second clock-out, add dict to process_dict. Change name.  Resize program. FILE HAS ALREADY BEEN SELECTED WARNING.")

global dir_name, time_tot, file_format, process_dict
process_dict = {}
for i in [1,2,3] :
    process_dict[i] = {"clipboard":"","file_format":"", 'status':'', 'playlist':False, 'cmd':''}
try:                                                                             # this section is to remove the need to send data forth
    with open('dtdtube.dat', 'r') as f:                                          # opening the dat file containing the default save files
        dir_name = f.read()                                                      # loading the data
    f.close()                                                                    # closing the open file, not necessary, but kind
except:                                                                          # if file doesn't exist one is created here.  
    with open('dtdtube.dat', 'w') as f:                                          # creating the file with the 'w' command
        dir_name = os.getcwd()                                                   # choosing the default directory as where things are saved.
        f.write(dir_name)                                                        # since it's new, set the variable (object) to be a dictionary
    f.close()                                                                    # closing the open file, not necessary, but kind
# check to see the directory is valid.  If not set to current directory
if os.path.exists(dir_name) == False :
    with open('dtdtube.dat', 'w') as f:                                          # creating the file with the 'w' command
        dir_name = os.getcwd()                                                   # choosing the default directory as where things are saved.
        f.write(dir_name)                                                        # since it's new, set the variable (object) to be a dictionary
    f.close()                                                                    # closing the open file, not necessary, but kind

def file_location():                   # used to find the location of key file.  
    # Check if MEIPASS attribute is available in sys else return current file path
    bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    path_to_ydl = os.path.abspath(os.path.join(bundle_dir,'yt-dlp.exe')) ; print(f"So...I find the path to be :{path_to_ydl}")
    return path_to_ydl

def file_location2():                   # used to find the location of key file.  
    # Check if MEIPASS attribute is available in sys else return current file path
    bundle_dir2 = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    path_to_ffmpeg = os.path.abspath(os.path.join(bundle_dir2,'ffmpeg.exe')) ; print(f"So...I find the path to be :{path_to_ffmpeg}")
    return path_to_ffmpeg

class MyForm(QDialog):                                   #  Add         Dialog.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, True)
    def __init__(self):                                  #              Dialog.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, True)
        super().__init__()                               # to the DTD_Video_Downloader_Ver2 file for the min and max buttons.
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, True)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, True)

        self.thread={}

        self.ui.dirButton.setStyleSheet("text-align:left;")
        self.ui.dirButton.setText(dir_name)
        self.ui.dirButton.clicked.connect(self.open_dir_dialog)

        self.ui.pasteURL1.clicked.connect(self.downloadOption1)
        self.ui.stopPauseButton1.clicked.connect(self.stop_worker_1)
        self.ui.playlistButton1.clicked.connect(self.playlist_1)
        self.ui.playlistButton1.setCheckable(True)
        self.ui.stopPauseButton1.setEnabled(False)
        self.ui.stopPauseButton1.hide()
        self.ui.statusBar1.hide()

        self.ui.pasteURL1_2.clicked.connect(self.downloadOption2)
        self.ui.stopPauseButton1_2.clicked.connect(self.stop_worker_2)
        self.ui.playlistButton1_2.clicked.connect(self.playlist_1)
        self.ui.playlistButton1_2.setCheckable(True)
        self.ui.stopPauseButton1_2.setEnabled(False)
        self.ui.stopPauseButton1_2.hide()
        self.ui.statusBar1_2.hide()

        self.ui.pasteURL1_3.clicked.connect(self.downloadOption3)
        self.ui.stopPauseButton1_3.clicked.connect(self.stop_worker_3)
        self.ui.playlistButton1_3.clicked.connect(self.playlist_1)
        self.ui.playlistButton1_3.setCheckable(True)
        self.ui.stopPauseButton1_3.setEnabled(False)
        self.ui.stopPauseButton1_3.hide()
        self.ui.statusBar1_3.hide()

        self.fileFormats = ["mp4","mp3","mkv","mpg","avi","webm","m4a","wav","mov"]
        self.addcontent()
        self.ui.quitExitButton.clicked.connect(self.terminate)
        self.ui.playlistList.hide()
        self.ui.playlistDownload.hide()
        self.ui.playlistDownloadStop.hide()
        self.ui.playlistDownloadStop.clicked.connect(self.playlistStop)
        self.ui.playlistDownload.clicked.connect(self.playlist_2)

        self.show()

    def addcontent(self) :
        for i in self.fileFormats :
            self.ui.fileFormatBox1.addItem(i)
            self.ui.fileFormatBox1_2.addItem(i)
            self.ui.fileFormatBox1_3.addItem(i)

    def downloadOption1(self):
        global file_format
        file_format = self.ui.fileFormatBox1.itemText(self.ui.fileFormatBox1.currentIndex())
        self.thread[1] = ThreadClass(parent=None,index=1)
        self.thread[1].start()
        self.thread[1].any_signal.connect(self.my_function)
        self.ui.pasteURL1.setEnabled(False)
        self.ui.stopPauseButton1.setEnabled(True)
        self.ui.stopPauseButton1.show()
        self.ui.statusBar1.show()
        self.ui.playlistButton1.hide()
        
    def downloadOption2(self):
        global file_format
        file_format = self.ui.fileFormatBox1_2.itemText(self.ui.fileFormatBox1_2.currentIndex())
        self.thread[2] = ThreadClass(parent=None,index=2)
        self.thread[2].start()
        self.thread[2].any_signal.connect(self.my_function)
        self.ui.pasteURL1_2.setEnabled(False)
        self.ui.stopPauseButton1_2.setEnabled(True)
        self.ui.stopPauseButton1_2.show()
        self.ui.statusBar1_2.show()
        self.ui.playlistButton1_2.hide()

    def downloadOption3(self):
        global file_format
        file_format = self.ui.fileFormatBox1_3.itemText(self.ui.fileFormatBox1_3.currentIndex())
        self.thread[3] = ThreadClass(parent=None,index=3)
        self.thread[3].start()
        self.thread[3].any_signal.connect(self.my_function)
        self.ui.pasteURL1_3.setEnabled(False)
        self.ui.stopPauseButton1_3.setEnabled(True)
        self.ui.stopPauseButton1_3.show()
        self.ui.statusBar1_3.show()
        self.ui.playlistButton1_3.hide()
        
    def stop_worker_1(self):
        self.thread[1].stop()
        self.ui.pasteURL1.setText("+ Paste URL")
        self.ui.pasteLabel1.setText("Paste Link Here:")
        self.ui.pasteURL1.setEnabled(True)
        self.ui.stopPauseButton1.hide()
        self.ui.statusBar1.hide()
        self.ui.playlistButton1.show()
        process_dict[1] = {"clipboard":"","file_format":"", 'status':'stop', 'playlist':False, 'cmd':''}
        MyForm.shoud_I_Exit(self)
    

    def stop_worker_2(self):
        self.thread[2].stop()
        self.ui.pasteURL1_2.setText("+ Paste URL")
        self.ui.pasteLabel1_2.setText("Paste Link Here:")
        self.ui.pasteURL1_2.setEnabled(True)
        self.ui.stopPauseButton1_2.hide()
        self.ui.statusBar1_2.hide()
        self.ui.playlistButton1_2.show()
        process_dict[2] = {"clipboard":"","file_format":"", 'status':'stop', 'playlist':False, 'cmd':''}
        MyForm.shoud_I_Exit(self)


    def stop_worker_3(self):
        self.thread[3].stop()
        self.ui.pasteURL1_3.setText("+ Paste URL")
        self.ui.pasteLabel1_3.setText("Paste Link Here:")
        self.ui.pasteURL1_3.setEnabled(True)
        self.ui.stopPauseButton1_3.hide()
        self.ui.statusBar1_3.hide()
        self.ui.playlistButton1_3.show()
        process_dict[3] = {"clipboard":"","file_format":"", 'status':'stop', 'playlist':False, 'cmd':''}
        MyForm.shoud_I_Exit(self)


    def playlist_1(self):
        global file_format, playlist, thread_choice
        clipboard = pyperclip.paste()
        # clipboard = 'https://www.youtube.com/watch?v=qeMFqkcPYcg&list=RDCLAK5uy_lf8okgl2ygD075nhnJVjlfhwp8NsUgEbs&start_radio=1&rv=aCcjfweuYtI'
        # pyperclip.copy(clipboard)
        self.ui.pasteLabel1.hide()
        self.ui.pasteLabel1_2.hide()
        self.ui.pasteLabel1_3.hide()
        self.ui.label.hide()
        self.ui.label_2.hide()
        self.ui.label_3.hide()
        self.ui.fileFormatBox1.hide()
        self.ui.fileFormatBox1_2.hide()
        self.ui.fileFormatBox1_3.hide()

        if self.ui.playlistButton1.isChecked() == True :
            self.ui.playlistButton1.setCheckable(False)
            self.ui.playlistButton1.setCheckable(True)
            self.ui.label.show()
            self.ui.fileFormatBox1.show()
            thread_choice = 1
        
        if self.ui.playlistButton1_2.isChecked() == True :
            self.ui.playlistButton1_2.setCheckable(False)
            self.ui.playlistButton1_2.setCheckable(True)
            self.ui.label_2.show()
            self.ui.fileFormatBox1_2.show()
            thread_choice = 2

        if self.ui.playlistButton1_3.isChecked() == True :
            self.ui.playlistButton1_3.setCheckable(False)
            self.ui.playlistButton1_3.setCheckable(True)
            self.ui.label_3.show()
            self.ui.fileFormatBox1_3.show()
            thread_choice = 3

        clipboard = MyForm.checkClipboard(self, clipboard)                     # check to see if already in clipboard present !
        if clipboard == "" : 
            self.ui.playlistDownloadStop.hide()
            self.ui.playlistDownload.hide()
            self.ui.playlistList.hide()
            self.ui.pasteLabel1.show()
            self.ui.pasteLabel1_2.show()
            self.ui.pasteLabel1_3.show()
            self.ui.label.show()
            self.ui.label_2.show()
            self.ui.label_3.show()
            self.ui.fileFormatBox1.show()
            self.ui.fileFormatBox1_2.show()
            self.ui.fileFormatBox1_3.show()
            return                                            # process_dict[int] = {"clipboard":"","file_format":"", 'status':'', 'playlist':False, 'cmd':''}

        process_dict[thread_choice]["clipboard"] = clipboard
        print(f"228.  for stopping :{process_dict[thread_choice]['playlist']}")
        process_dict[thread_choice]["playlist"] = True

        # print(str(process_dict).encode('ascii', 'ignore').decode('ascii'))   # test of the dictionary
        # return
        count = 0 ; playlist = {}
        tube_dl = file_location()                                                         # this is the program to call on for the download
        cmd = [
            tube_dl ,
            "-i",
            "--get-filename",
            "--flat-playlist",
            #"-f", 
            #"bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best", 
            "-o", 
            "%(title)s", 
            #"--merge-output-format", 
            #"mp4", 
            str(clipboard)
            ]                                                                           # [tube_dl, '--get-filename', '-o', '%(title)s', str(clipboard)]
        # print(" ".join(cmd));print()
        # playlist = {1: 'Eurythmics, Annie Lennox, Dave Stewart - Sweet Dreams (Are Made Of This) (Official Video)', 2: 'Kenny Loggins - Footloose (Official Video)', 3: 'The Outfield - Your Love (Official HD Video)', 4: 'a-ha - Take On Me (Official Video) [Remastered in 4K]', 5: "Bon Jovi - Livin' On A Prayer", 6: 'Whitney Houston - I Wanna Dance With Somebody (Official 4K Video)', 7: 'Cyndi Lauper - Girls Just Want To Have Fun (Official Video)', 8: 'Survivor - Eye Of The Tiger (Official HD Video)', 9: 'Toto - Africa (Official HD Video)', 10: "Guns N' Roses - Sweet Child O' Mine (Official Music Video)", 11: 'Madonna - Material Girl (Official Video) [HD]', 12: 'Michael Jackson - Billie Jean (Official Video)', 13: 'The Police - Every Breath You Take (Official Video)', 14: "Journey - Don't Stop Believin' (Official Audio)", 15: 'Culture Club - Karma Chameleon (Official Music Video)', 16: "Starship - Nothing's Gonna Stop Us Now (Official Music Video) [HD]", 17: 'Men At Work - Down Under (Official HD Video)', 18: 'Cutting Crew - (I Just) Died In Your Arms (Official Music Video)', 19: 'Michael Jackson - The Way You Make Me Feel (Official Video)', 20: "Twisted Sister - We're Not Gonna Take it (Extended Version) (Official Music Video)", 21: 'Roxette - It Must Have Been Love (Official Music Video)', 22: 'Ray Parker Jr. - Ghostbusters (Official Video)', 23: 'Bonnie Tyler - Total Eclipse of the Heart (Video)', 24: 'Laura Branigan - Gloria (Official Music Video)', 25: 'Tears For Fears - Everybody Wants To Rule The World (Official Music Video)', 26: 'Bon Jovi - You Give Love A Bad Name (Official Music Video)', 27: 'Bruce Springsteen - Dancing In the Dark (Official Video)', 28: 'Whitney Houston - Greatest Love Of All (Official 4K Video)', 29: "Simple Minds - Don't You (Forget About Me)", 30: 'Fleetwood Mac - Gypsy (Official Music Video)', 31: 'Madonna - Like A Prayer (Official Video)', 32: 'Daryl Hall & John Oates - Maneater (Official Video)', 33: 'Spandau Ballet - True (HD Remastered)', 34: 'Queen - Under Pressure (Official Video)', 35: 'Men At Work - Who Can It Be Now (Video Version)', 36: "Rockwell - Somebody's Watching Me (Official Music Video)", 37: 'UB40 - Red Red Wine (Official Video)', 38: 'Van Halen - Jump (Official Music Video)', 39: 'Lionel Richie - All Night Long (All Night)', 40: 'The Bangles - Walk Like an Egyptian (Official Video)', 41: "The Human League - Don't You Want Me (Official Music Video)", 42: "Billy Joel - We Didn't Start the Fire (Official Video)", 43: 'Starship - We Built This City (Official Music Video) [HD]', 44: 'Prince & The Revolution - Raspberry Beret (Official Music Video)', 45: 'Whitney Houston - How Will I Know (Official Video)', 46: 'Paul Simon - You Can Call Me Al (Official Video)', 47: 'Dexys Midnight Runners, Kevin Rowland - Come On Eileen (1982 Version)', 48: 'Madonna - Like A Virgin (Official Video)', 49: 'Kim Carnes - Bette Davis Eyes (Official Music Video)', 50: 'Robert Palmer - Addicted To Love (Official Music Video)', 51: 'Thompson Twins - Hold Me Now', 52: 'Irene Cara  - Flashdance What A Feeling (Official Music Video)', 53: 'Daryl Hall & John Oates - You Make My Dreams (Official HD Video)', 54: 'Prince - Little Red Corvette (Official Music Video)', 55: "[I've Had] The Time Of My Life (From Dirty Dancing Soundtrack)", 56: 'Katrina & The Waves - Walking On Sunshine (Official Music Video)', 57: "Rick Springfield - Jessie's Girl (Official Video)", 58: 'The Buggles - Video Killed The Radio Star (Official Music Video)', 59: "Deniece Williams - Let's Hear It for the Boy", 60: 'Mr. Mister - Kyrie', 61: 'INXS - Need You Tonight (Official Music Video)', 62: 'New Kids On The Block - You Got It (The Right Stuff)', 63: 'Huey Lewis & The News - The Power Of Love (Official Video)', 64: 'George Michael - Faith (Official Video)', 65: 'Daryl Hall & John Oates - Private Eyes (Official HD Video)', 66: 'Steve Perry - Oh Sherrie (Video)', 67: 'Phil Collins - Sussudio (Official Music Video)', 68: 'Poison - Talk Dirty To Me', 69: 'Eddie Money - Take Me Home TonightBe My Baby', 70: 'Kiss', 71: 'Corey Hart - Sunglasses At Night (Official Music Video)', 72: 'Belinda Carlisle - Heaven Is A Place On Earth (Official Music Video)', 73: "The Pointer Sisters - I'm So Excited", 74: 'Night Ranger - Sister Christian (Official Music Video)', 75: "The Go-Go's - Our Lips Are Sealed", 76: 'Madness - Our House (Official 4K Video)', 77: 'Tommy Tutone - 867-5309Jenny', 78: 'Matthew Wilder - Break My Stride (Lyric Video)', 79: 'Love Shack', 80: 'Mony Mony', 81: 'Wang Chung - Everybody Have Fun Tonight', 82: 'The Hooters - And We Danced', 83: "Joan Jett - I Love Rock 'N Roll (Official Video)", 84: 'Hungry Like the Wolf', 85: 'Manic Monday', 86: 'Loverboy - Working For The Weekend (with Intro)', 87: 'Duran Duran - The Reflex (Official Music Video)', 88: 'The Clash - Should I Stay or Should I Go (Official Video)', 89: 'Soft Cell - Tainted Love (Lyric Video)', 90: 'Donna Summer - She Works Hard For The Money (1987) � TopPop', 91: 'Take My Breath Away'}
        # playlist = {'Eurythmics, Annie Lennox, Dave Stewart - Sweet Dreams (Are Made Of This) (Official Video)': 1, 'Kenny Loggins - Footloose (Official Video)': 2, 'The Outfield - Your Love (Official HD Video)': 3, 'a-ha - Take On Me (Official Video) [Remastered in 4K]': 4, "Bon Jovi - Livin' On A Prayer": 5, 'Whitney Houston - I Wanna Dance With Somebody (Official 4K Video)': 6, 'Cyndi Lauper - Girls Just Want To Have Fun (Official Video)': 7, 'Survivor - Eye Of The Tiger (Official HD Video)': 8, 'Toto - Africa (Official HD Video)': 9, "Guns N' Roses - Sweet Child O' Mine (Official Music Video)": 10, 'Madonna - Material Girl (Official Video) [HD]': 11, 'Michael Jackson - Billie Jean (Official Video)': 12, 'The Police - Every Breath You Take (Official Video)': 13, "Journey - Don't Stop Believin' (Official Audio)": 14, 'Culture Club - Karma Chameleon (Official Music Video)': 15, "Starship - Nothing's Gonna Stop Us Now (Official Music Video) [HD]": 16, 'Men At Work - Down Under (Official HD Video)': 17, 'Cutting Crew - (I Just) Died In Your Arms (Official Music Video)': 18, 'Michael Jackson - The Way You Make Me Feel (Official Video)': 19, "Twisted Sister - We're Not Gonna Take it (Extended Version) (Official Music Video)": 20, 'Roxette - It Must Have Been Love (Official Music Video)': 21, 'Ray Parker Jr. - Ghostbusters (Official Video)': 22, 'Bonnie Tyler - Total Eclipse of the Heart (Video)': 23, 'Laura Branigan - Gloria (Official Music Video)': 24, 'Tears For Fears - Everybody Wants To Rule The World (Official Music Video)': 25, 'Bon Jovi - You Give Love A Bad Name (Official Music Video)': 26, 'Bruce Springsteen - Dancing In the Dark (Official Video)': 27, 'Whitney Houston - Greatest Love Of All (Official 4K Video)': 28, "Simple Minds - Don't You (Forget About Me)": 29, 'Fleetwood Mac - Gypsy (Official Music Video)': 30, 'Madonna - Like A Prayer (Official Video)': 31, 'Daryl Hall & John Oates - Maneater (Official Video)': 32, 'Spandau Ballet - True (HD Remastered)': 33, 'Queen - Under Pressure (Official Video)': 34, 'Men At Work - Who Can It Be Now (Video Version)': 35, "Rockwell - Somebody's Watching Me (Official Music Video)": 36, 'UB40 - Red Red Wine (Official Video)': 37, 'Van Halen - Jump (Official Music Video)': 38, 'Lionel Richie - All Night Long (All Night)': 39, 'The Bangles - Walk Like an Egyptian (Official Video)': 40, "The Human League - Don't You Want Me (Official Music Video)": 41, "Billy Joel - We Didn't Start the Fire (Official Video)": 42, 'Starship - We Built This City (Official Music Video) [HD]': 43, 'Prince & The Revolution - Raspberry Beret (Official Music Video)': 44, 'Whitney Houston - How Will I Know (Official Video)': 45, 'Paul Simon - You Can Call Me Al (Official Video)': 46, 'Dexys Midnight Runners, Kevin Rowland - Come On Eileen (1982 Version)': 47, 'Madonna - Like A Virgin (Official Video)': 48, 'Kim Carnes - Bette Davis Eyes (Official Music Video)': 49, 'Robert Palmer - Addicted To Love (Official Music Video)': 50, 'Thompson Twins - Hold Me Now': 51, 'Irene Cara  - Flashdance What A Feeling (Official Music Video)': 52, 'Daryl Hall & John Oates - You Make My Dreams (Official HD Video)': 53, 'Prince - Little Red Corvette (Official Music Video)': 54, "[I've Had] The Time Of My Life (From Dirty Dancing Soundtrack)": 55, 'Katrina & The Waves - Walking On Sunshine (Official Music Video)': 56, "Rick Springfield - Jessie's Girl (Official Video)": 57, 'The Buggles - Video Killed The Radio Star (Official Music Video)': 58, "Deniece Williams - Let's Hear It for the Boy": 59, 'Mr. Mister - Kyrie': 60, 'INXS - Need You Tonight (Official Music Video)': 61, 'New Kids On The Block - You Got It (The Right Stuff)': 62, 'Huey Lewis & The News - The Power Of Love (Official Video)': 63, 'George Michael - Faith (Official Video)': 64, 'Daryl Hall & John Oates - Private Eyes (Official HD Video)': 65, 'Steve Perry - Oh Sherrie (Video)': 66, 'Phil Collins - Sussudio (Official Music Video)': 67, 'Poison - Talk Dirty To Me': 68, 'Eddie Money - Take Me Home TonightBe My Baby': 69, 'Kiss': 70, 'Corey Hart - Sunglasses At Night (Official Music Video)': 71, 'Belinda Carlisle - Heaven Is A Place On Earth (Official Music Video)': 72, "The Pointer Sisters - I'm So Excited": 73, 'Night Ranger - Sister Christian (Official Music Video)': 74, "The Go-Go's - Our Lips Are Sealed": 75, 'Madness - Our House (Official 4K Video)': 76, 'Tommy Tutone - 867-5309Jenny': 77, 'Matthew Wilder - Break My Stride (Lyric Video)': 78, 'Love Shack': 79, 'Mony Mony': 80, 'Wang Chung - Everybody Have Fun Tonight': 81, 'The Hooters - And We Danced': 82, "Joan Jett - I Love Rock 'N Roll (Official Video)": 83, 'Hungry Like the Wolf': 84, 'Manic Monday': 85, 'Loverboy - Working For The Weekend (with Intro)': 86, 'Duran Duran - The Reflex (Official Music Video)': 87, 'The Clash - Should I Stay or Should I Go (Official Video)': 88, 'Soft Cell - Tainted Love (Lyric Video)': 89, 'Donna Summer - She Works Hard For The Money (1987) � TopPop': 90, 'Take My Breath Away': 91}
        
        startupinfo = subprocess.STARTUPINFO()                                                  # sometimes a console will popup despite noconsole in the pyinstaller.  Issue traced to the 
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW                                  # subprocess.  Thus use this flags.  Else change shell=True, but often doesn't catch all info.
        process = subprocess.Popen(cmd, startupinfo=startupinfo, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE, universal_newlines=True, shell=False)
        for line in process.stdout:
            #print(repr(line))
            line = line.replace("\n","")
            line = line.encode('ascii', 'ignore').decode('ascii')
            if "WARNING:" in line : continue
            if "ERROR:" in line : continue
            # print(line)
            count += 1
            playlist[line] = count


        if not playlist : 
            process_dict[thread_choice]['playlist'] = False
            MyForm.playlistStop(self)
            return
        for i in playlist :
            # print(str(i).encode('ascii', 'ignore').decode('ascii'),playlist[i])     # displays a list of the playlist
            self.ui.playlistList.addItem(i)

        self.ui.playlistDownload.show()                       # download button
        self.ui.playlistList.show()                           # QDiaglog i.e. playlist windown.
        self.ui.playlistDownloadStop.show()

    def playlist_2(self):
        global cmd
        clipboard = pyperclip.paste()
        tube_dl = file_location()                                                         # this is the program to call on for the download
        # print(f"Welcome to playlist2.  here is the process_dict:\n{process_dict}\n{type(process_dict)}")

        if thread_choice == 1 : 
            file_format = self.ui.fileFormatBox1.itemText(self.ui.fileFormatBox1.currentIndex())
            # process_dict[1]["file_format"] = file_format
        if thread_choice == 2 : 
            file_format = self.ui.fileFormatBox1_2.itemText(self.ui.fileFormatBox1.currentIndex())
            # process_dict[2]["file_format"] = file_format
        if thread_choice == 3 : 
            file_format = self.ui.fileFormatBox1_3.itemText(self.ui.fileFormatBox1.currentIndex())
            # process_dict[3]["file_format"] = file_format
        
        self.ui.playlistDownloadStop.hide()
        self.ui.playlistDownload.hide()
        self.ui.playlistList.hide()
        self.ui.pasteLabel1.show()
        self.ui.pasteLabel1_2.show()
        self.ui.pasteLabel1_3.show()
        self.ui.label.show()
        self.ui.label_2.show()
        self.ui.label_3.show()
        self.ui.fileFormatBox1.show()
        self.ui.fileFormatBox1_2.show()
        self.ui.fileFormatBox1_3.show()
        process_dict[thread_choice]["cmd"] = {}
        selectedLayers = self.ui.playlistList.selectedItems()
        for i in selectedLayers :
            video_name = i.text()
            video_position = playlist[video_name] ; print(f"Selected file :{video_position}.  {video_name.encode('ascii', 'ignore').decode('ascii')}")

            if 'youtube' in str(clipboard).lower() :
                if file_format == "mp3" or file_format == "m4a" or file_format == "wav" :
                    cmd = [tube_dl ,
                        "-i",
                        "--playlist-items",
                        str(video_position),
                        "-f",
                        "ba",
                        "-x",
                        "--audio-format",
                        file_format,
                        str(clipboard),
                        "-o",
                        dir_name + chr(92) + "%(title)s.%(ext)s",
                        ]
                else :
                    cmd = [
                            tube_dl ,                                                                   # engine used in the command line
                            "-i",                                                                       # gnore download and postprocessing errors. also use '--ignore-errors'
                            "--playlist-items",                                                         # Comma separated playlist_index of the videos to download.
                            #str(vid),                                                                  # E.g. "-I 1:3,7,-5::2"
                            str(video_position),                                                        # this will be a single file instead of a parsing list of some order.
                            "-f",                                                                       # filters the format for download
                            "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",                 # format to find the best quality of mp4 and best audio of a m4a nature.
                            "-P",                                                                       # Download pathway to use
                            dir_name,                                                                       # option is used to specify the path each type of file should be saved to.
                            "-o",                                                                       # option is used to indicate a template for the output file names
                            "%(title)s",                                                                # 
                            "--merge-output-format", 
                            file_format, 
                            str(clipboard)
                        ]                                                                           # [tube_dl, '--get-filename', '-o', '%(title)s', str(clipboard)] 
            else :
                if file_format == "mp3" or file_format == "m4a" or file_format == "wav" :
                    cmd = [tube_dl,
                        "-i",                                                                       # gnore download and postprocessing errors. also use '--ignore-errors'
                        "--playlist-items",                                                         # Comma separated playlist_index of the videos to download.
                        str(video_position),                                                        # this will be a single file instead of a parsing list of some order.
                        "-x",
                        "--audio-format",
                        file_format,
                        str(clipboard),
                        "-o",
                        dir_name + chr(92) + "%(title)s.%(ext)s"
                        ]
                else :
                    cmd = [tube_dl,
                        "-i",                                                                       # gnore download and postprocessing errors. also use '--ignore-errors'
                        "--playlist-items",                                                         # Comma separated playlist_index of the videos to download.
                        str(video_position),                                                        # this will be a single file instead of a parsing list of some order.
                        "-o",
                        dir_name + chr(92) + "%(title)s.%(ext)s",
                        str(clipboard)
                        ]

            # cmd = [
            #         tube_dl ,                                                                   # engine used in the command line
            #         "-i",                                                                       # gnore download and postprocessing errors. also use '--ignore-errors'
            #         "--playlist-items",                                                         # Comma separated playlist_index of the videos to download.
            #         #str(vid),                                                                  # E.g. "-I 1:3,7,-5::2"
            #         str(video_position),
            #         "-f",                                                                       # filters the format for download
            #         "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",                 # format to find the best quality of mp4 and best audio of a m4a nature.
            #         "-P",                                                                       # Download pathway to use
            #         dir_name,                                                                       # option is used to specify the path each type of file should be saved to.
            #         "-o",                                                                       # option is used to indicate a template for the output file names
            #         "%(title)s",                                                                # 
            #         "--merge-output-format", 
            #         "mp4", 
            #         str(clipboard)
            #     ]                                                                           # [tube_dl, '--get-filename', '-o', '%(title)s', str(clipboard)] 

            process_dict[thread_choice]["cmd"][video_name] = cmd
        self.ui.playlistList.clear()
        # print(f"process_dict[1]['cmd']:{process_dict[1]['cmd']}")   # test section !
        process_dict[thread_choice]["file_format"] = file_format
        if thread_choice == 1 : 
            self.ui.pasteURL1.setEnabled(False)
            self.ui.stopPauseButton1.setEnabled(True)
            self.ui.stopPauseButton1.show()
            self.ui.statusBar1.show()
            self.ui.playlistButton1.hide()
            self.thread[1] = ThreadClass(parent=None,index=1)
            self.thread[1].start()
            self.thread[1].any_signal.connect(self.my_function)

        if thread_choice == 2 : 
            self.ui.pasteURL1_2.setEnabled(False)
            self.ui.stopPauseButton1_2.setEnabled(True)
            self.ui.stopPauseButton1_2.show()
            self.ui.statusBar1_2.show()
            self.ui.playlistButton1_2.hide()
            self.thread[2] = ThreadClass(parent=None,index=2)
            self.thread[2].start()
            self.thread[2].any_signal.connect(self.my_function)

        if thread_choice == 3 : 
            self.ui.pasteURL1_3.setEnabled(False)
            self.ui.stopPauseButton1_3.setEnabled(True)
            self.ui.stopPauseButton1_3.show()
            self.ui.statusBar1_3.show()
            self.ui.playlistButton1_3.hide()
            self.thread[3] = ThreadClass(parent=None,index=3)
            self.thread[3].start()
            self.thread[3].any_signal.connect(self.my_function)


    def playlistStop(self):
        MyForm.showDialog(self)
        self.ui.playlistList.clear()
        self.ui.playlistDownload.hide()
        self.ui.playlistDownloadStop.hide()
        self.ui.playlistList.hide() ; print("Line 420. was a hide playlistList")
        self.ui.pasteLabel1.show()
        self.ui.pasteLabel1_2.show()
        self.ui.pasteLabel1_3.show()
        self.ui.label.show()
        self.ui.label_2.show()
        self.ui.label_3.show()
        self.ui.fileFormatBox1.show()
        self.ui.fileFormatBox1_2.show()
        self.ui.fileFormatBox1_3.show()
        # thread_choice = 1
        process_dict[thread_choice]["clipboard"] = ""
        print("great I have gotten to 432")
        if thread_choice == 1 : 
            self.ui.playlistButton1.show()
            self.ui.playlistButton1.setCheckable(True)
        if thread_choice == 2 : 
            self.ui.playlistButton1_2.show()
            self.ui.playlistButton1_2.setCheckable(True)
        if thread_choice == 3 : 
            self.ui.playlistButton1_3.show()
            self.ui.playlistButton1_3.setCheckable(True)
        print(f"and I knew that the thread was {thread_choice}")


    def checkClipboard(self, clipboard):
        # check to see if url is not currently being downloaded !
        clipboard = clipboard
        for i in process_dict :
            # print(f"Test to find the problem: {str(i).encode('ascii', 'ignore').decode('ascii')} is a {type(i)}\nand then the process_dict is :{str(process_dict[i]).encode('ascii', 'ignore').decode('ascii')}")
            if (process_dict[i]['clipboard'] == clipboard) :
                print("FILE HAS ALREADY BEEN SELECTED !")
                clipboard = ""
        return clipboard


    def my_function(self,dict):
        dict=dict                          # counter is the object emitted from the tread
        index = self.sender().index            # process_dict = {'clipboard': '', 'file_format': '', 'status': '', 'playlist': False, 'cmd': ''}
        percent = dict[index]['percent']       # dict = {"percent":0,"time_tot":"Finished","stage":"+ Paste URL","video_name":"Playlist Downloaded"}
        time_tot = dict[index]['time_tot']
        stage = dict[index]['stage']
        video_name = dict[index]['video_name']

        if index==1:
            self.ui.pasteLabel1.setText(time_tot)
            self.ui.statusBar1.setValue(percent)
            if self.ui.pasteURL1.text() != stage :
                self.ui.pasteURL1.setText(stage)
            if self.ui.titleLabel1.text() != video_name :
                self.ui.titleLabel1.setText(video_name)
            if time_tot == "Finished" :
                self.ui.stopPauseButton1.hide()
                self.ui.playlistButton1.show()
                self.ui.pasteURL1.setEnabled(True)
                self.ui.pasteLabel1.setText("Paste Link Here:")
                self.ui.statusBar1.hide()
                process_dict[1]['status'] = 'stop'
                MyForm.shoud_I_Exit(self)

        if index==2: 
            self.ui.pasteLabel1_2.setText(time_tot)
            self.ui.statusBar1_2.setValue(percent)
            if self.ui.pasteURL1_2.text() != stage :
                self.ui.pasteURL1_2.setText(stage)
            if self.ui.titleLabel1_2.text() != video_name :
                self.ui.titleLabel1_2.setText(video_name)
            if time_tot == "Finished" :
                self.ui.stopPauseButton1_2.hide()
                self.ui.playlistButton1_2.show()
                self.ui.pasteURL1_2.setEnabled(True)
                self.ui.pasteLabel1_2.setText("Paste Link Here:")
                self.ui.statusBar1_2.hide()
                process_dict[2]['status'] = 'stop'
                MyForm.shoud_I_Exit(self)

        if index==3:
            self.ui.pasteLabel1_3.setText(time_tot)
            self.ui.statusBar1_3.setValue(percent)
            if self.ui.pasteURL1_3.text() != stage :
                self.ui.pasteURL1_3.setText(stage)
            if self.ui.titleLabel1_3.text() != video_name :
                self.ui.titleLabel1_3.setText(video_name)
            if time_tot == "Finished" :
                self.ui.stopPauseButton1_3.hide()
                self.ui.playlistButton1_3.show()
                self.ui.pasteURL1_3.setEnabled(True)
                self.ui.pasteLabel1_3.setText("Paste Link Here:")
                self.ui.statusBar1_3.hide()
                process_dict[3]['status'] = 'stop'
                MyForm.shoud_I_Exit(self)

    def shoud_I_Exit (self):
        shouldIExit = False
        # if "Thread" in process_dict : return
        print("Asking if I should exit? LINE 510")
        for i in process_dict :
            print(f"CHECKING THE STATUS OF {i}. {process_dict[i]['status']}") 
            if process_dict[i]['status'] == 'start' : return            
            if process_dict[i]['status'] == 'stop' : shouldIExit = True                 # test showed if only check for one stop, then it would exit when the first download finished. not all 3.
        if shouldIExit == True :
            if self.ui.autoExit.isChecked() == True :
                if self.ui.autoExit_2.isChecked() == True :
                    os.startfile(dir_name)
                #  FUTURE PROJECT : GIVE A TIMEDOWN COUNTER TO EXIT.
                self.close()


    def open_dir_dialog(self):
        global dir_name
        dir_name = QFileDialog.getExistingDirectory(self, "Select a Directory", dir_name)
        print(dir_name)
        if dir_name:
            self.ui.dirButton.setText(str(dir_name))
            with open('dtdtube.dat', 'w') as f:                                     # opening the dat file containing the default save files
                f.write(dir_name)                                                   # since it's new, set the variable (object) to be a dictionary
            f.close()                                                               # closing the open file, not necessary, but kind


    def terminate(self) :
        exit_condition = True
        if self.ui.pasteURL1.text() == "Downloading" :
            print("Quiting exit 1")
            MyForm.stop_worker_1(self)
            # time.sleep(1)
            exit_condition = False
        if self.ui.pasteURL1_2.text() == "Downloading" :
            print("Quiting exit 2")
            MyForm.stop_worker_2(self)
            exit_condition = False
            # time.sleep(1)
        if self.ui.pasteURL1_3.text() == "Downloading" :
            print("Quiting exit 3")
            MyForm.stop_worker_3(self)
            # time.sleep(1)
            exit_condition = False
        if exit_condition == True :
            if self.ui.autoExit_2.isChecked() == True :
                os.startfile(dir_name)
            self.close()  

    def showDialog(self):
       self.ui.msg = QMessageBox()
       self.ui.msg.setIcon(QMessageBox.Information)

       self.ui.msg.setText("This is a message box")
       self.ui.msg.setInformativeText(f"This is additional information")
       self.ui.msg.setWindowTitle("Unable to proceed")
       self.ui.msg.setDetailedText("The details are as follows:")
       self.ui.msg.setStandardButtons(QMessageBox.Ok)
       # self.ui.msg.buttonClicked.connect(msgbtn)
        
       self.ui.retval = self.ui.msg.exec_()
       print ("value of pressed message box button:", self.ui.retval)

    def msgbtn (self,i):
        print(f"Button pressed is :{i.text()}")
    
class ThreadClass(QtCore.QThread):
    any_signal = QtCore.pyqtSignal(object)                        # changed from simple sending a int to str then decided on a dict, so it's now a object!

    def __init__(self, parent=None,index=0):
        super(ThreadClass, self).__init__(parent)
        self.index=index
        self.is_running = True

    def run(self):
        global video_name, cmd, dict
        # var_exists = 'process_dict' in locals() or 'process_dict' in globals()
        # if not var_exists : 
        #     print("GLOBAL process_dict DID NOT EXIST.  CREATED ONE IN THREADCLASS.RUN !")
        #     process_dict = {}
        tube_dl = file_location()                                                         # this is the program to call on for the download
        # start_time = int(time.time())
        # start_time = time.time()
        # currentStartTime = time.perf_counter()
        print('Starting thread...',self.index)
        dict_thread = self.index
        clipboard = pyperclip.paste()
        video_name = clipboard
        dict = {}
        # clipboard = 'https://www.youtube.com/watch?v=qeMFqkcPYcg&list=RDCLAK5uy_lf8okgl2ygD075nhnJVjlfhwp8NsUgEbs&start_radio=1&rv=aCcjfweuYtI'
        try : print(f"Check out what I know about {dict_thread} :\nclipboard :{process_dict[dict_thread]['clipboard']}\nfile_format:{process_dict[dict_thread]['file_format']}\nstatus:{process_dict[dict_thread]['status']}\nplaylist:{process_dict[dict_thread]['playlist']}")
        except : print(f"Check out what I know about {str(dict_thread)} :{str(process_dict[dict_thread]).encode('ascii', 'ignore').decode('ascii')}")

        # check to see if a playlist is being checked.
        if process_dict[dict_thread]['playlist'] == True :
            if process_dict[dict_thread]["status"] != 'start' :
                for i in process_dict[dict_thread]["cmd"] :
                    video_name = i
                    cmd = process_dict[dict_thread]["cmd"][i]
                    process_dict[dict_thread]["clipboard"] = clipboard
                    # process_dict[dict_thread]["file_format"] = file_format    # this seems reduntant.
                    process_dict[dict_thread]["status"] = 'start'
                    # print(f"{video_name}\n{cmd}\n\n")
                    ThreadClass.mainDownload(self, cmd)
                    # if process_dict[dict_thread]['playlist'] == True : dict[dict_thread]['stage'] = 'Downloading'
                    dict[dict_thread] = {"percent":0,"time_tot":"","stage":"Downloading","video_name":f"Downloaded :{video_name}"}
                    self.any_signal.emit(dict)    
                dict[dict_thread] = {"percent":0,"time_tot":"Finished","stage":"+ Paste URL","video_name":"Playlist Downloaded"}
                process_dict[dict_thread]['playlist'] = False
                self.any_signal.emit(dict)
            return
        
        # check to see if url is not currently being downloaded !
        for i in process_dict :
            print(f"Test to find the problem: {str(i).encode('ascii', 'ignore').decode('ascii')} is a {type(i)}\nand then the process_dict is :{str(process_dict[i]).encode('ascii', 'ignore').decode('ascii')}")
            if (process_dict[i]['clipboard'] == clipboard) :
                print("FILE HAS ALREADY BEEN SELECTED !")
                return

        process_dict[dict_thread] = {"clipboard":clipboard,"file_format":file_format, 'status':'start', 'playlist':False, 'cmd':''}
        # print(f"https://tubitv.com/movies/502446/war-between-the-planets?start=trueClipboard :{clipboard}\ntube_dl :{tube_dl}\ndir_name :{dir_name}\nfile_format :{file_format}\nprocess_dict :{process_dict},\nLINE249 GOOD.")

        if 'youtube' in str(clipboard).lower() :
            if file_format == "mp3" or file_format == "m4a" or file_format == "wav" :
                cmd = [tube_dl ,
                    "-f",
                    "ba",
                    "-x",
                    "--audio-format",
                    file_format,
                    str(clipboard),
                    "-o",
                    dir_name + chr(92) + "%(title)s.%(ext)s",
                    ]
            else :
                cmd = [tube_dl ,
                    # '--write-sub', '--write-auto-sub', '--sub-lang', "en.*", '--sub-format', 'srt', '--skip-download',        # added on 8/27/2023 to get subtitles.  youtube only.
                    # '--write-sub', '--write-auto-sub', '--sub-lang', "en.*", '--convert-subs=srt',                            # added on 8/27/2023 to get subtitles.  youtube only.
                    '--write-sub', '--write-auto-sub', '--sub-lang', "en.*", '--sub-format', 'srt',                            # Skipping for fun
                    "-f",
                    "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
                    "-o",
                    dir_name + chr(92) + "%(title)s.%(ext)s",
                    "--merge-output-format",
                    file_format,
                    str(clipboard)
                    ]
        else :
            if file_format == "mp3" or file_format == "m4a" or file_format == "wav" :
                cmd = [tube_dl,
                    "-x",
                    "--audio-format",
                    file_format,
                    str(clipboard),
                    "-o",
                    dir_name + chr(92) + "%(title)s.%(ext)s"
                    ]
            else : 
                cmd = [tube_dl,
                    "-o",
                    dir_name + chr(92) + "%(title)s.%(ext)s",
                    str(clipboard)
                    ]

                cmd = [tube_dl,                                                         # Added on 11/6/2023 to by DRM videos
                    # "--allow-u",
                    # '--cookies-from-browser',
                    # 'firefox',
                    "-o",
                    dir_name + chr(92) + "%(title)s.%(ext)s",
                    str(clipboard),
                    '-v'
                    ] 
        video_cmd = [tube_dl, '--get-filename', '-o', '%(title)s', str(clipboard)]
        print(f"Clipboard :{clipboard}\ntube_dl :{tube_dl}\ndir_name :{dir_name}\nfile_format :{file_format}\nvideo_cmd :{video_cmd}\ncmd:{cmd}LINE677 GOOD.")
        print(f"Command :\n{' '.join(video_cmd)}")

        startupinfo = subprocess.STARTUPINFO()                                                  # sometimes a console will popup despite noconsole in the pyinstaller.  Issue traced to the 
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW                                  # subprocess.  Thus use this flags.  Else change shell=True, but often doesn't catch all info.
        process = subprocess.Popen(video_cmd, startupinfo=startupinfo, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE, universal_newlines=True, shell=False)   # use shell = True, when the cmd is a string and shell = False when it is a list
        for line in process.stdout:
            video_name = line.replace("\n",'').strip()
            print(line.replace("\n",""))                                                       # test line

        if 'operable program or batch file' in video_name : video_name = "Video name not recognized."
        ThreadClass.mainDownload(self, cmd)
        # print(f"Clipboard :{clipboard}\ntube_dl :{tube_dl}\ndir_name :{dir_name}\nfile_format :{file_format}\nvideo_cmd :{video_cmd}\nvideo_name: {video_name}\nLINE296 GOOD.")
    
    def mainDownload(self, cmd):
        clipboard = pyperclip.paste()
        tube_dl = file_location()                                                         # this is the program to call on for the download
        start_time = int(time.time())
        start_time = time.time()
        currentStartTime = time.perf_counter()
        dict_thread = self.index
        videoNameDict = {clipboard:video_name}
        test_command = str(" ".join(cmd)).replace(tube_dl,f'"{tube_dl}"').replace(dir_name,f'"{dir_name}"')
        print(f"\nCommand :{' '.join(cmd)}\n")
        print(f'\nTest Command:\n{test_command}\n')
        print(f'\nTest Command:\n{str(" ".join(cmd)).replace(tube_dl,f"{chr(34)}{tube_dl}{chr(34)}").replace(dir_name,f"{chr(34)}{dir_name}{chr(34)}")}\n')

        # print(f"\nTest Command :(str(' '.join(cmd)\n).encode("ascii", "ignore")).decode("ascii").replace(inputDirectory,'').replace(outputDirectory,""))
        startupinfo = subprocess.STARTUPINFO()                                                  # sometimes a console will popup despite noconsole in the pyinstaller.  Issue traced to the 
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW                                  # subprocess.  Thus use this flags.  Else change shell=True, but often doesn't catch all info.
        process = subprocess.Popen(cmd, startupinfo=startupinfo, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE, universal_newlines=True, shell=False)          # use shell = True, when the cmd is a string and shell = False when it is a list

        for line in process.stdout:
            if video_name == "Video name not recognized." : print(line)
            if 'ETA' in line :
                stage = "Downloading"
                percent = int(float(line[11:16]))  # % of bytes downloaded
                if percent == 0 : percent = 1
                #  time_tot = line[line.find('ETA'):]
                # if "(frag" in time_tot : time_tot = time_tot[:time_tot.find("(frag")-1]       # this will give the ETA as it appears in the line out.
                guess = (time.perf_counter() - currentStartTime) * ((100-percent)/percent)      # using difference * ((100-percent)/percent) to find ETA from % downloaded.
                #guess = ((time.perf_counter() - currentStartTime) / percent) * (1-percent)     # use this formula if the percent is a fraction and not whole number.
                time_tot = f"ETA   {time.strftime('%H:%M:%S', time.gmtime(guess))} "    # timeRemaining = (currentTime - startTime) * ((100-percent)/percent
                dict[dict_thread] = {"percent":percent,"time_tot":time_tot,"stage":stage, "video_name":videoNameDict[clipboard],"clipboard":clipboard}
                self.any_signal.emit(dict)
                continue
            elif "is not a valid URL" in line :
                print(f"You DunderHead, that is not a good URL !.\n{line}")
            elif "[Merger]" in line :
                dict[dict_thread] = {"percent":0,"time_tot":"ETA ?","stage":"Merging", "video_name":videoNameDict[clipboard]}
                self.any_signal.emit(dict)
                continue
            elif "Fixing " in line :
                dict[dict_thread] = {"percent":0,"time_tot":"ETA ?","stage":"Merging", "video_name":videoNameDict[clipboard]}   
                self.any_signal.emit(dict)
                continue
            elif "[ExtractAudio]" in line :
                dict[dict_thread] = {"percent":0,"time_tot":"ETA ?","stage":"Extracting", "video_name":videoNameDict[clipboard]}
                self.any_signal.emit(dict)
                continue
            elif ("Unable to open file" in line) and ("Retrying (3/3)" in line) :
                dict[dict_thread] = {"percent":0,"time_tot":"Finished","stage":"+ Paste URL","video_name":f"Unable to open file.  Try another time."}  
                self.any_signal.emit(dict)
                return 
            elif "\n" == line : continue
            elif ": Downloading webpage" in line : continue
            elif "Downloading android player API JSON" in line : continue
            elif "Downloading 1 format(s)" in line : continue
            elif "Resuming download at byte" in line : continue
            elif "[download] 100% of" in line : continue
            elif "Deleting original file" in line : continue
            elif "[download] Destination" in line : continue
            elif "ERROR: Unable to rename file" in line :
                print(f"Found problem :{repr(line)}\n\tPossible solution is simple wait 30 seconds.")
                time.sleep(30)

            else : 
                pass
                print(f"line :{repr(line)}") 

        if "This video is DRM protected" in line :
            dict[dict_thread] = {"percent":0,"time_tot":"Finished","stage":"+ Paste URL","video_name":f"This video is DRM protected. Unable to download."}    
            self.any_signal.emit(dict)
            return
        if "ERROR:" in line :
            dict[dict_thread] = {"percent":0,"time_tot":"Finished","stage":"+ Paste URL","video_name":f"Unable to proceed with download. Try another time."}    
            self.any_signal.emit(dict)
            return
 
        if process_dict[dict_thread]['playlist'] == True : return
        # print(f"I am Finished with {self.index}")
        dict[dict_thread] = {"percent":0,"time_tot":"Finished","stage":"+ Paste URL","video_name":f"Downloaded :{videoNameDict[clipboard]}"}
        # if process_dict[dict_thread]['playlist'] == True : dict[dict_thread]['stage'] = 'Downloading'
        self.any_signal.emit(dict)                                                # clears the value to 0
 
    def stop(self):
        self.is_running = False
        print('Stopping thread...',self.index)
        self.terminate()

    # def playlist_thread(self):
    #     global video_name
    #     print(process_dict)
    #     for i in process_dict[process_dict["Thread"]]["cmd"] :
    #         video_name = i
    #         cmd = process_dict[process_dict["Thread"]]["cmd"][i]
    #         print(f"{video_name}\n{cmd}\n\n")
    #         ThreadClass.mainDownload(self, cmd)
    #         # process.wait()

    #     crash








        # global cmd, video_name
        # count = 0 ; playlist = {}
        # tube_dl = file_location()                                                         # this is the program to call on for the download
        # cmd = [
        #     tube_dl ,
        #     "-i",
        #     "--get-filename",
        #     "--flat-playlist",
        #     #"-f", 
        #     #"bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best", 
        #     "-o", 
        #     "%(title)s", 
        #     #"--merge-output-format", 
        #     #"mp4", 
        #     str(clipboard)
        #     ]                                                                           # [tube_dl, '--get-filename', '-o', '%(title)s', str(clipboard)]
        # print(" ".join(cmd));print()
        # process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE, universal_newlines=True, shell=False)
        # for line in process.stdout:
        #     #print(repr(line))
        #     line = line.replace("\n","")
        #     count += 1
        #     playlist[count] = line

        # # for i in playlist :
        # #     print(i,playlist[i])

        # choice = [1, 5, 9, 13]       # needs to be a string, not a int. or a list
        # # choosen = "4,15,18,79"
        # for choosen in choice :
        #     video_name = playlist[choosen] 
        #     choosen = str(choosen)

        #     cmd = [
        #             tube_dl ,                                                                   # engine used in the command line
        #             "-i",                                                                       # gnore download and postprocessing errors. also use '--ignore-errors'
        #             "--playlist-items",                                                         # Comma separated playlist_index of the videos to download.
        #             #str(vid),                                                                  # E.g. "-I 1:3,7,-5::2"
        #             choosen,
        #             "-f",                                                                       # filters the format for download
        #             "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",                 # format to find the best quality of mp4 and best audio of a m4a nature.
        #             "-P",                                                                       # Download pathway to use
        #             dir_name,                                                                       # option is used to specify the path each type of file should be saved to.
        #             "-o",                                                                       # option is used to indicate a template for the output file names
        #             "%(title)s",                                                                # 
        #             "--merge-output-format", 
        #             "mp4", 
        #             str(clipboard)
        #         ]                                                                           # [tube_dl, '--get-filename', '-o', '%(title)s', str(clipboard)] 
            
        #     print(" ".join(cmd));print()
        #         # use shell = True, when the cmd is a string and shell = False when it is a list
        #         # if cmd is enclosed in either a ' or " then must be a string
        #         # to use a ' or " in a cmd list, set shell=False
        #     # process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE, universal_newlines=True, shell=False)
        #     # for line in process.stdout:
        #     #     line = line.replace("\n","")
        #     #     print(line)
        #     #     if 'ETA' in line :
        #     #         print(f"\r{line}           ",end = '')
        #     ThreadClass.mainDownload(self, cmd)
        # print("-Finished")


if __name__=="__main__":
    app = QApplication(sys.argv)
    w = MyForm()
    w.show()
    sys.exit(app.exec_())
