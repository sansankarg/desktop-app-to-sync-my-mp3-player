import os
import io
import tkinter as tk
from tkinter import filedialog, messagebox, Listbox, Scrollbar, simpledialog
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload
from googleapiclient.http import MediaIoBaseDownload

SCOPES = ['https://www.googleapis.com/auth/drive']

def authenticate_drive():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
    return build('drive', 'v3', credentials=creds)

service = authenticate_drive()

MUSIC_FOLDER_ID = '1oHgr3X3Gh9Y7W3_MvhWNalEo9KpLJWxp'

class FileManagerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Soul Sync")
        self.current_folder_id = MUSIC_FOLDER_ID
        self.folder_history = []
        self.folder_names = ["Music"]
        self.local_music_folder_path = None
        self.file_name_to_id_map = {}

        self.bg_color = "#f0f8ff"
        self.button_color = "#008cba"
        self.label_color = "#005f73"

        self.master.configure(bg=self.bg_color)

        self.path_frame = tk.Frame(master, bg=self.bg_color)
        self.path_frame.pack(fill=tk.X, padx=10, pady=5)

        self.current_path_label = tk.Label(
            self.path_frame,
            text="Current Path: Music",
            anchor='w',
            font=("Arial", 12, "bold"),
            bg=self.bg_color,
            fg=self.label_color
        )
        self.current_path_label.pack(fill=tk.X)

        self.button_frame = tk.Frame(master, bg=self.bg_color)
        self.button_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=5)

        self.back_button = tk.Button(self.path_frame, text="Back", command=self.go_back, bg=self.button_color, fg="#ffffff")
        self.back_button.pack(side=tk.RIGHT, padx=5)

        self.upload_button = tk.Button(self.button_frame, text="Upload File", command=self.upload_file, bg=self.button_color, fg="#ffffff")
        self.upload_button.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        self.delete_button = tk.Button(self.button_frame, text="Delete File", command=self.delete_file, bg=self.button_color, fg="#ffffff")
        self.delete_button.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        self.create_folder_button = tk.Button(self.button_frame, text="Create Subfolder", command=self.create_subfolder, bg=self.button_color, fg="#ffffff")
        self.create_folder_button.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        self.sync_button = tk.Button(self.button_frame, text="Sync", command=self.sync_files, bg=self.button_color, fg="#ffffff")
        self.sync_button.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        self.set_folder_button = tk.Button(self.button_frame, text="Set Local Music Folder", command=self.set_local_music_folder, bg=self.button_color, fg="#ffffff")
        self.set_folder_button.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        self.developer_label = tk.Label(self.button_frame, text="Developed by sansankarg", bg=self.bg_color,
                                        fg=self.label_color)
        self.developer_label.pack(side=tk.BOTTOM, padx=5, pady=5)

        self.file_frame = tk.Frame(master, bg=self.bg_color)
        self.file_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=5)

        self.file_list = Listbox(self.file_frame, width=50, height=15, font=("Arial", 10), bg="#ffffff", fg="#000000")
        self.file_list.pack(side=tk.LEFT, fill=tk.BOTH)

        scrollbar = Scrollbar(self.file_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.file_list.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.file_list.yview)

        self.file_list.bind('<Double-1>', self.open_subfolder)

        self.load_files()

    def set_local_music_folder(self):
        folder_path = filedialog.askdirectory(title="Select Local Music Folder")
        if folder_path:
            self.local_music_folder_path = folder_path
            messagebox.showinfo("Folder Set", f"Local Music Folder set to: {self.local_music_folder_path}")

    def load_files(self):
        self.file_list.delete(0, tk.END)
        files = list_files_in_folder(self.current_folder_id)
        print(files)
        for file in files:
            self.file_list.insert(tk.END, f"{file['name']}")
            self.file_name_to_id_map[file['name']] = file['id']
        self.update_current_path_label()

    def upload_file(self):

        file_path = filedialog.askopenfilename()
        if file_path:
            try:
                upload_file_to_folder(file_path, self.current_folder_id)
                messagebox.showinfo("Success", "File uploaded successfully!")
                self.load_files()
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")


    def delete_file(self):
        selected_file = self.file_list.curselection()
        if selected_file:
            file_info = self.file_list.get(selected_file[0])
            file_id = self.file_name_to_id_map.get(file_info)
            delete_file(file_id)
            self.load_files()
        else:
            messagebox.showwarning("Warning", "Please select a file to delete.")

    def create_subfolder(self):
        subfolder_name = simpledialog.askstring("Subfolder Name", "Enter subfolder name:")
        if subfolder_name:
            create_subfolder_in_folder(subfolder_name, self.current_folder_id)
            self.load_files()

    def open_subfolder(self, event):
        selected_file = self.file_list.curselection()
        if selected_file:
            file_info = self.file_list.get(selected_file[0])
            print(file_info)
            file_id = self.file_name_to_id_map.get(file_info)
            self.folder_history.append(self.current_folder_id)
            self.folder_names.append(file_info)
            self.current_folder_id = file_id
            self.load_files()

    def go_back(self):
        if self.folder_history:
            self.current_folder_id = self.folder_history.pop()
            self.folder_names.pop()
            self.update_current_path_label()
            self.load_files()

    def sync_files(self):
        if not self.local_music_folder_path:
            messagebox.showwarning("Warning", "Please set the local Music folder path first.")
            return

        drive_file = build_file_structure(self.current_folder_id)
        local_file = build_local_file_structure(self.local_music_folder_path)

        print(f"Total structure of drive : {drive_file}")
        print(f"Total structure of local : {local_file}")

        missing_files = find_missing_files(drive_file, local_file)

        print(f"Missing files : {missing_files}")
        if missing_files:
            create_missing_folders(missing_files, self.local_music_folder_path)
            sync_missing_files(drive_file, self.local_music_folder_path, missing_files)
            messagebox.showinfo("Sync Info", f"Synced successfully")
        else:
            messagebox.showinfo("Sync Info", "No changes to sync")

    def update_current_path_label(self):
        full_path = " > ".join(self.folder_names)
        self.current_path_label.config(text=f"Current Path: {full_path}")

def list_files_in_folder(folder_id):
    query = f"'{folder_id}' in parents"
    results = service.files().list(q=query, pageSize=100, fields="files(id, name, mimeType)").execute()
    return results.get('files', [])


def upload_file_to_folder(file_path, folder_id):
    file_name = os.path.basename(file_path)
    file_metadata = {
        'name': file_name,
        'parents': [folder_id]
    }

    media = MediaFileUpload(file_path, chunksize=1024 * 1024, resumable=True)

    request = service.files().create(body=file_metadata, media_body=media, fields='id')

    try:
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"Uploaded {int(status.progress() * 100)}%.")
    except Exception as e:
        messagebox.showerror("Upload Error", f"An error occurred: {str(e)}")
        return


def delete_file(file_id):
    service.files().delete(fileId=file_id).execute()

def create_subfolder_in_folder(name, folder_id):
    file_metadata = {
        'name': name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [folder_id]
    }
    service.files().create(body=file_metadata, fields='id').execute()

def download_file_from_drive(file_id, destination_path):
    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(destination_path, 'wb')
    downloader = MediaIoBaseDownload(fh, request)

    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(f"Download {int(status.progress() * 100)}%.")
    fh.close()
    print(f"Downloaded file to {destination_path}")

def build_file_structure(folder_id):
    drive_files = list_files_in_folder(folder_id)
    result = {}

    for file in drive_files:
        file_info = {
            "filename": file['name'],
            "id": file['id'],
            "type": "folder" if file['mimeType'] == 'application/vnd.google-apps.folder' else "file"
        }

        if file['mimeType'] == 'application/vnd.google-apps.folder':
            file_info['content'] = build_file_structure(file['id'])

        result[file['name']] = file_info

    return result
def build_local_file_structure(directory):
    result = {}

    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)

        if os.path.isdir(item_path):
            result[item] = {
                "filename": item,
                "type": "folder",
                "content": build_local_file_structure(item_path)
            }
        else:
            result[item] = {
                "filename": item,
                "type": "file"
            }

    return result


def find_missing_files(drive_structure, local_structure, parent_path=""):
    missing_files = []

    for name, drive_item in drive_structure.items():
        full_path = f"{parent_path}\\{name}" if parent_path else name

        if name not in local_structure:
            if drive_item['type'] == 'file':
                missing_files.append(full_path)
            elif drive_item['type'] == 'folder':
                missing_files.append(full_path)
                folder_missing = find_missing_files(drive_item['content'], {}, full_path)
                missing_files.extend(folder_missing)
        else:
            if drive_item['type'] == 'folder':
                folder_missing = find_missing_files(drive_item['content'], local_structure[name]['content'], full_path)
                missing_files.extend(folder_missing)

    return missing_files

def create_missing_folders(missing_files, local_base_path):
    for missing_file in missing_files:
        local_file_path = os.path.join(local_base_path, missing_file)

        if not os.path.splitext(local_file_path)[1]:
            if not os.path.exists(local_file_path):
                os.makedirs(local_file_path)
                print(f"Created missing folder: {local_file_path}")


def sync_missing_files(drive_structure, local_base_path, missing_files):
    for missing_file in missing_files:
        local_file_path = os.path.join(local_base_path, missing_file)

        print("------------------------------------------")
        print(f"Local file path : {local_file_path}")
        if not os.path.splitext(local_file_path)[1]:
            continue

        path_parts = missing_file.split("\\")
        current_drive_dict = drive_structure

        print(f"Path parts : {path_parts}")
        print(f"Cuurent drive dict : {current_drive_dict}")

        for part in path_parts:
            current_drive_dict = current_drive_dict[
                'content'] if 'content' in current_drive_dict else current_drive_dict
            current_drive_dict = current_drive_dict[part]

        file_id = current_drive_dict['id']
        download_file_from_drive(file_id, local_file_path)


if __name__ == "__main__":
    root = tk.Tk()
    app = FileManagerApp(root)
    root.mainloop()
