import win32api
import win32gui
import win32con
import os
import tkinter as tk
from tkinter import messagebox, filedialog
import shutil
from PIL import ImageTk, Image
import win10toast
import threading
import _tkinter


defaultPath = os.getcwd() + '\\Wallpapers\\'
ImagesPath = {}
FavoritesPath = []


# init - load the favorites wallpapers
FavoritesWallFile = open("Favorites_Images.txt", "r")
for line in FavoritesWallFile:
    FavoritesPath.append(line.strip("\n"))


# classes

class ChangeWallpaper:
    def __init__(self, path):
        self.path = path
        key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
        win32api.RegSetValueEx(key, "WallpaperStyle", 0, win32con.REG_SZ, "0")
        win32api.RegSetValueEx(key, "TileWallpaper", 0, win32con.REG_SZ, "0")
        win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, self.path, 3)


class UploadImage:
    def __init__(self, path):
        try:
            self.path = path
            shutil.copy(self.path, "Wallpapers")
            HomeFrame.destroy()
            Home()
        except FileNotFoundError:
            pass


class AddToFavorites:
    def __init__(self, path):
        self.path = path
        if self.path not in FavoritesPath:
            FavoritesPath.append(self.path)
            with open("Favorites_Images.txt", "a") as f:
                f.write(self.path + "\n")
            f.close()
            print(FavoritesPath)


class RemoveFromFavorites:
    def __init__(self, path):
        self.path = path
        if self.path in FavoritesPath:
            FavoritesPath.remove(self.path)
            with open("Favorites_Images.txt", "r+") as f:
                d = f.readlines()
                f.seek(0)
                for i in d:
                    if i.strip("\n") != self.path:
                        f.write(i)
                f.truncate()


# Fonts To Use: Gabriola, Impact, Courier New, Corbel Light, Consolas, Comic Sans MS, Candara Light, Arial Black


App = tk.Tk()
App.title("Wallpaper App")
App.geometry("1200x700")
App.resizable(width=False, height=False)
App.iconbitmap("Wallpaper App Icon.ico")

sidebar = tk.Frame(App, width=200, bg="#ccc")
sidebar.pack(side="left", fill="y")


ActiveScreen = "Home"


def Home():
    global ActiveScreen, HomeFrame
    ActiveScreen = "Home"
    HomeFrame = tk.Frame(App)
    HomeFrame.pack(side="right", expand=True, fill="both")

    HomeLabel = tk.Label(HomeFrame, text="Home", font=("Comic Sans MS", 16))
    HomeLabel.pack()

    def ChooseWallpaperUpload():
        FileName = filedialog.askopenfilename(initialdir=os.getcwd(), title="Wallpaper to upload", filetypes=(("PNG Format", "*.png"), ("JPG Format", "*.jpg")))
        UploadImage(FileName)


    UploadWallpaperBtn = tk.Button(HomeFrame, text="Upload Wallpaper", bd=0, font=("Consolas", 11), command=ChooseWallpaperUpload)
    UploadWallpaperBtn.pack(side="right", anchor="nw")

    WallpapersFiles = os.listdir("Wallpapers")

    WallpaperFrame = tk.Frame(HomeFrame)
    wallCanvas = tk.Canvas(WallpaperFrame, height=650, width=900)
    scroll_bar = tk.Scrollbar(WallpaperFrame, command=wallCanvas.yview)

    scroll_bar.config(command=wallCanvas.yview)
    scroll_bar.pack(side="right", fill="y")
    scrollable_frame = tk.Frame(wallCanvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: wallCanvas.configure(
            scrollregion=wallCanvas.bbox("all")
        )
    )

    def on_mousewheel(event):
        shift = (event.state & 0x1) != 0
        scroll = -1 if event.delta > 0 else 1
        if shift:
            wallCanvas.xview_scroll(scroll, "units")
        else:
            wallCanvas.yview_scroll(scroll, "units")

    App.bind("<MouseWheel>", on_mousewheel)

    wallCanvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    wallCanvas.configure(yscrollcommand=scroll_bar.set)

    WallpaperFrame.pack(expand=True, fill="both")
    wallCanvas.pack()
    scroll_bar.pack()


    def LoadImages():
        try:
            columnIndex = 0
            rowIndex = 0
            numImage = 0

            for wallpaperFile in WallpapersFiles:
                path = "Wallpapers/" + wallpaperFile

                openWallpaperFile = Image.open(path)
                NewReduceImage = openWallpaperFile.resize((283, 160))
                image = ImageTk.PhotoImage(NewReduceImage)

                ChangeWallpaperBtn = tk.Button(scrollable_frame, image=image, bd=0,  command=lambda wallpaperFile=wallpaperFile: ChangeWallpaper(defaultPath + wallpaperFile))
                ChangeWallpaperBtn.image = image
                ChangeWallpaperBtn.grid(row=rowIndex, column=columnIndex)

                ChangeWallpaperBtn.bind("<Button-3>", lambda event=None, wallpaperFile=wallpaperFile: AddToFavorites(defaultPath + wallpaperFile))

                numImage += 1
                columnIndex += 1
                if columnIndex == 3:
                    rowIndex += 1
                    columnIndex = 0

        except _tkinter.TclError:
            pass

    Load = threading.Thread(target=LoadImages)
    Load.start()


def CheckHome():
    global ActiveScreen
    if ActiveScreen == "Home":
        pass
    else:
        FavoritesFrame.destroy()
        Home()


def Favorites():
    global ActiveScreen, FavoritesFrame
    ActiveScreen = "Favorites"

    FavoritesFrame = tk.Frame(App)
    FavoritesFrame.pack(side="right", expand=True, fill="both")

    FavoritesLabel = tk.Label(FavoritesFrame, text="Favorites", font=("Comic Sans MS", 16))
    FavoritesLabel.pack()

    WallpapersFrame = tk.Frame(FavoritesFrame)
    wallCanvas = tk.Canvas(WallpapersFrame, height=650, width=900)
    scroll_bar = tk.Scrollbar(WallpapersFrame, command=wallCanvas.yview)

    scroll_bar.config(command=wallCanvas.yview)
    scroll_bar.pack(side="right", fill="y")
    scrollable_frame = tk.Frame(wallCanvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: wallCanvas.configure(
            scrollregion=wallCanvas.bbox("all")
        )
    )

    def on_mousewheel(event):
        shift = (event.state & 0x1) != 0
        scroll = -1 if event.delta > 0 else 1
        if shift:
            wallCanvas.xview_scroll(scroll, "units")
        else:
            wallCanvas.yview_scroll(scroll, "units")

    App.bind("<MouseWheel>", on_mousewheel)

    wallCanvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    wallCanvas.configure(yscrollcommand=scroll_bar.set)

    WallpapersFrame.pack(expand=True, fill="both")
    wallCanvas.pack(expand=True, fill="both")
    scroll_bar.pack()


    def LoadImages():
        columnIndex = 0
        rowIndex = 0
        numImage = 0

        try:
            for imagePath in FavoritesPath:
                wallPath = Image.open(imagePath)
                ReduceImage = wallPath.resize((243, 140))
                image = ImageTk.PhotoImage(ReduceImage)

                FavoriteWallpaperBtn = tk.Button(scrollable_frame, image=image, bd=0, command=lambda imagePath=imagePath: ChangeWallpaper(imagePath))
                FavoriteWallpaperBtn.image = image
                FavoriteWallpaperBtn.grid(row=rowIndex, column=columnIndex)

                FavoriteWallpaperBtn.bind("<Button-3>", lambda event=None, imagePath=imagePath: RemoveFromFavorites(imagePath))

                numImage += 1
                columnIndex += 1
                if columnIndex == 4:
                    rowIndex += 1
                    columnIndex = 0

        except RuntimeError:
            pass

        except AttributeError:
            pass

    Load = threading.Thread(target=LoadImages)
    Load.start()


def CheckFavorites():
    if ActiveScreen == "Favorites":
        pass
    else:
        HomeFrame.destroy()
        Favorites()

HomeBtn = tk.Button(sidebar, text="Home", bd=0, width=20, bg="#e6e6e6", height=2, font=('Corbel Light', 14), command=CheckHome)
HomeBtn.pack(side="top", anchor="nw")

FavoritesBtn = tk.Button(sidebar, text="Favorites", bd=0, width=20, bg="#e6e6e6", height=2, font=('Corbel Light', 14), command=CheckFavorites)
FavoritesBtn.pack(side="top", anchor="nw")

HomeBtn.bind("<Enter>", lambda event=None: HomeBtn.config(bg="#bfbfbf"))
HomeBtn.bind("<Leave>", lambda event=None: HomeBtn.config(bg="#e6e6e6"))

FavoritesBtn.bind("<Enter>", lambda event=None: FavoritesBtn.config(bg="#bfbfbf"))
FavoritesBtn.bind("<Leave>", lambda event=None: FavoritesBtn.config(bg="#e6e6e6"))

Home()
App.mainloop()


# finish 280 lines of code