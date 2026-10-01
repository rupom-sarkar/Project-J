import os


class FileController:

    def open_folder(self, folder_name):

        folder_name = folder_name.lower().strip()

        if "download" in folder_name:
            os.startfile(os.path.expanduser("~/Downloads"))
            return "Opening Downloads, Sir."

        elif "document" in folder_name:
            os.startfile(os.path.expanduser("~/Documents"))
            return "Opening Documents, Sir."

        elif "desktop" in folder_name:
            os.startfile(os.path.expanduser("~/Desktop"))
            return "Opening Desktop, Sir."

        elif "project j" in folder_name:
            os.startfile(r"G:\Project-J")
            return "Opening Project-J, Sir."

        else:
            return f"I don't know that folder yet, Sir."