import wmi
import time
import tkinter as tk
from main import FileManagerApp

def detect():
    c = wmi.WMI()
    connected_devices = set()

    root = tk.Tk()
    app = FileManagerApp(root)

    root.withdraw()

    def show_app_window(mp3_drive):
        app.local_music_folder_path = mp3_drive
        time.sleep(3)
        root.deiconify()
        app.sync_files()

    while True:
        current_devices = set()

        for disk in c.Win32_DiskDrive():
            if "USB" in disk.PNPDeviceID:
                current_devices.add(disk.DeviceID)

                if disk.DeviceID not in connected_devices:
                    print(f"USB Device Connected: {disk.Caption}")
                    print(f"Device ID: {disk.DeviceID}")
                    print(f"Media Type: {disk.MediaType}")

                    print(type(disk.DeviceID))
                    print(type("\\.\PHYSICALDRIVE1"))
                    print(f"{disk.DeviceID} == \\\\.\\PHYSICALDRIVE1") #replace your mp3 player id if you have one or else get one ASAP
                    if disk.DeviceID == "\\\\.\\PHYSICALDRIVE1":

                        for partition in disk.associators("Win32_DiskDriveToDiskPartition"):
                            for logical_disk in partition.associators("Win32_LogicalDiskToPartition"):
                                mp3_drive = logical_disk.DeviceID
                                print(f"MP3 player drive detected at: {mp3_drive}")

                                show_app_window(mp3_drive)

        for device in connected_devices - current_devices:
            print(f"USB Device Removed: {device}")

        connected_devices = current_devices
        root.update()
        time.sleep(2)

    root.mainloop()

detect()
