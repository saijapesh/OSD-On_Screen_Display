import cv2
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import win32com.client
import pythoncom

class MyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("My Application")
        self.root.geometry("400x300")

        # Set transparent icon
        self.root.iconbitmap('path_to_transparent_icon.ico')

        # Your application widgets and logic here
        tk.Label(self.root, text="Hello, Tkinter!").pack(padx=20, pady=20)
class CameraUtils:
    def __init__(self, root):
        self.root = root

    def get_camera_sources(self):
        self.root.minsize(340, 280)  # Adjust these values as needed
        camera_sources = []
        camera_names = self._get_camera_names()

        for index in range(10):  # Check up to 10 camera indices (adjust if needed)
            cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
            if cap.isOpened():
                camera_name = camera_names.get(index, f"Camera {index}")
                camera_sources.append((index, camera_name))
                cap.release()

        return camera_sources

    def _get_camera_names(self):
        camera_names = {}
        try:
            # Initialize COM library
            pythoncom.CoInitialize()

            # Create the system device enumerator
            sys_dev_enum = win32com.client.Dispatch("SystemDeviceEnumerator")
            # Get the video input device category
            category = win32com.client.Dispatch("DsDeviceCategory.VideoInputDevice")

            # Enumerate the video input devices
            enum_moniker = sys_dev_enum.CreateClassEnumerator(category.CLSID, None, 1)

            if enum_moniker is not None:
                while True:
                    moniker = enum_moniker.Next(1)
                    if moniker is None:
                        break

                    prop_bag = moniker.BindToStorage(None, None, win32com.client.Dispatch("PropertyBag"))
                    camera_name = prop_bag.Read("FriendlyName")
                    camera_index = len(camera_names)
                    camera_names[camera_index] = camera_name
                    moniker = None

        except Exception as e:
            print(f"Failed to get camera names: {e}")

        finally:
            # Uninitialize COM library
            pythoncom.CoUninitialize()

        return camera_names


class CameraPreviewApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Camera Preview")
        self.camera_utils = CameraUtils(root)
        self.camera_sources = self.camera_utils.get_camera_sources()

        if not self.camera_sources:
            tk.Label(self.root, text="No cameras detected.").pack(pady=20)
        else:
            tk.Label(self.root, text="Choose a camera source:").pack(pady=10)

            self.combo = ttk.Combobox(self.root, values=[name for _, name in self.camera_sources], width=20)
            self.combo.pack(pady=5)

            self.start_preview_button = ttk.Button(self.root, text="Start Preview", command=self.start_preview)
            self.start_preview_button.pack(pady=10)

            self.select_button = ttk.Button(self.root, text="Select", command=self.select_camera)
            self.select_button.pack(pady=10)

            self.preview_label = tk.Label(self.root)
            self.preview_label.pack(pady=10)

            self.preview_active = False
            self.cap = None
            self.selected_camera = None

    def start_preview(self):
        selected_name = self.combo.get()
        selected_source = next((index for index, name in self.camera_sources if name == selected_name), None)

        if selected_source is not None:
            if self.preview_active:
                self.stop_preview()
                self.root.update()  # Force GUI update to release resources

            # Release the current camera capture
            if self.cap is not None:
                self.cap.release()
                self.cap = None

            # Start a new camera capture with the selected source
            self.cap = cv2.VideoCapture(selected_source, cv2.CAP_DSHOW)
            if not self.cap.isOpened():
                messagebox.showerror("Error", "Failed to open selected camera.")
                return

            self.preview_active = True
            self.show_preview()

    def show_preview(self):
        if self.preview_active and self.cap is not None:
            ret, frame = self.cap.read()
            if ret:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_resized = cv2.resize(frame_rgb, (640, 480))
                pil_img = Image.fromarray(frame_resized)
                img_tk = ImageTk.PhotoImage(image=pil_img)

                self.preview_label.configure(image=img_tk)
                self.preview_label.image = img_tk

                # Schedule the next preview update after 10 milliseconds
                self.root.after(10, self.show_preview)
            else:
                self.stop_preview()

    def stop_preview(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None
        self.preview_active = False
        self.preview_label.configure(image=None)

    def select_camera(self):
        if self.preview_active:
            self.stop_preview()  # Stop the preview before selecting the camera

        selected_name = self.combo.get()
        selected_source = next((index for index, name in self.camera_sources if name == selected_name), None)

        if selected_source is not None:
            self.selected_camera = selected_source
            messagebox.showinfo("Camera Selected", f"Camera {self.selected_camera} selected.")


def main():
    root = tk.Tk()
    app = CameraPreviewApp(root)
    root.mainloop()

    # After main loop exits (GUI window is closed), print the selected camera source
    if app.selected_camera is not None:
        print(f"Selected camera source: {app.selected_camera}")
    return app.selected_camera


if __name__ == "__main__":
    main()
