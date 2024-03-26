import os
import textwrap
from tkinter import messagebox

from PIL import Image
import requests
import customtkinter as ctk
from pytube import YouTube

ctk.set_appearance_mode("light")

class CtkWinYT(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        height = 520
        width = 640
        center_x = (self.winfo_screenwidth() // 2) - (width // 2)
        center_y = (self.winfo_screenheight() // 2) - (height // 2)
        
        self.geometry("{}x{}+{}+{}".format(width, height, center_x, center_y))
        self.title("YT Downloader")
        self.wm_resizable(False, False)


        #frames
        self.title_link_frame = ctk.CTkFrame(self, fg_color="white")
        self.title_link_frame.pack(pady=10)


        self.video_info_frame = ctk.CTkFrame(self, fg_color="white")


        self.download_opt_frame = ctk.CTkFrame(self, fg_color="white")
        
        
        self.download_status_frame = ctk.CTkFrame(self, fg_color="white")
        

        #labels
        self.title_label = ctk.CTkLabel(self.title_link_frame, text="YouTube Downloader",
                                   text_color="red",font=("Helvetica",28,"bold","underline"))
        self.title_label.pack(pady=18)


        self.video_title_label = ctk.CTkLabel(self.video_info_frame, text="",
                                              font=("helvetica",16,"bold"))
        self.video_title_label.pack(pady=10,padx=10)


        self.thumbnail_label = ctk.CTkLabel(self.video_info_frame, text="")
        self.thumbnail_label.pack(pady=10,padx=10)


        self.duration_label = ctk.CTkLabel(self.video_info_frame, text="",
                                           font=("helvetica",16,"bold"))
        self.duration_label.pack(pady=10,padx=10)
        
        
        self.progress_label = ctk.CTkLabel(self.download_status_frame, font=("helvetica",16,"bold"))
        self.progress_label.grid(row=0, column=1, padx=5, pady=10)
        
        self.progress_bar = ctk.CTkProgressBar(self.download_status_frame, mode="determinate",
                                               border_width=2, border_color="black",
                                               fg_color="white", progress_color="red")
        self.progress_bar.set(0)
        self.progress_bar.grid(row=0, column=0, padx=5, pady=10)
        


        #entries
        self.link_entry = ctk.CTkEntry(self.title_link_frame, width=340, border_color="black",
                                       fg_color="white", text_color="black",
                                       placeholder_text="Link here")
        self.link_entry.pack(pady=10, padx=15)



        #buttons
        self.load_video_button = ctk.CTkButton(self.title_link_frame, text="Load video",
                                fg_color="red", text_color="white",
                                border_width=2, border_color="black",
                                hover_color="orange",
                                command=self.load_video)
        self.load_video_button.pack(pady=10)


        self.download_button = ctk.CTkButton(self.download_opt_frame, text="Download",
                                             fg_color="red", text_color="white",
                                             border_width=2, border_color="black",
                                             hover_color="orange", width=80, 
                                             command=self.download_video_by_resolution)
        self.download_button.grid(row=0, column=0, padx=10, pady=10)


        self.mp3_button = ctk.CTkButton(self.download_opt_frame, text="Only Mp3",
                                        fg_color="red", text_color="white", border_width=2,
                                        border_color="black", hover_color="orange", width=80,
                                        command=self.download_mp3_only)
        self.mp3_button.grid(row=0, column=1, padx=10, pady=10)


        self.cancel_button = ctk.CTkButton(self.download_opt_frame, text="Cancel",
                                           fg_color="red", text_color="white", border_width=2,
                                           border_color="black", hover_color="orange",
                                           width=80, command=self.cancel_video_selected)
        self.cancel_button.grid(row=0, column=3, padx=10, pady=10)


        #Combobox
        self.resolutions = ["720p","480p","360p","240p","144p"]
        self.resolution_opt = ctk.CTkComboBox(self.download_opt_frame, width=80,
                                              fg_color="red", text_color="white",
                                              border_width=2, border_color="black", 
                                              button_hover_color="orange",
                                              values=self.resolutions, button_color="black")
        self.resolution_opt.grid(row=0, column=2, padx=10, pady=10)
        
    def load_video(self):
        try:
            url = self.link_entry.get()
            self.youtube = YouTube(url, on_progress_callback=self.on_progress)
            
            self.archive_name = self.youtube.title
            for i in ["?","<",">",":","\"","\\","/","|",".","*"]:
                self.archive_name = self.archive_name.replace(i, "")

            self.update()
            self.get_thumbnail_n_duration()
            self.set_n_show_video_info()
            
            
        except Exception as e:
            messagebox.showerror(title="ERROR", message=f"An error has ocurred: {e}")
            
    def get_thumbnail_n_duration(self):
        thumbnail_url = self.youtube.thumbnail_url
        request = requests.get(thumbnail_url, stream=True)
        self.img = Image.open(request.raw)
        self.thumbnail_image = ctk.CTkImage(light_image=self.img, size=(200,110))
        
        duration_sec = self.youtube.length
        hours = duration_sec // 3600
        mins = (duration_sec % 3600) // 60
        secs = duration_sec % 60
        self.duration_format = f"{hours:02d}:{mins:02d}:{secs:02d}"
        
    def set_n_show_video_info(self):
        title = self.youtube.title
        title = textwrap.wrap(title, width=50)
        title = "\n".join(title)
                
        self.video_title_label.configure(text=f"- {title} -")
        self.thumbnail_label.configure(image=self.thumbnail_image)
        self.duration_label.configure(text=f"Duration: - {self.duration_format} -")
        
        self.video_info_frame.pack(pady=15, padx=20)
        self.download_opt_frame.pack(pady=15, padx=20)

    
    def download_video_by_resolution(self):
        try:
            res = self.resolution_opt.get()
            self.update()
            stream = self.youtube.streams.get_by_resolution(res)
            self.update()
            
            if stream:
                os.path.join("Downloaded videos")
                stream.download(filename=f"{self.archive_name}.mp4", output_path="Downloaded videos")
                
                self.download_status_frame.pack_forget()
                
                messagebox.askokcancel(title="Downloaded!", message="The download was succesful!")
                self.cancel_video_selected()
            else:
                messagebox.showerror(title="Stream error", message="There isn't a Stream for the video in the resolution selected, please select another one.")
        except Exception as e:
            messagebox.showerror(title="ERROR", message=f"An error has ocurred: {e}")
        
    def on_progress(self, stream, chunk, bytes_remaining):
        self.download_opt_frame.pack_forget()
        
        total = stream.filesize
        bytes_downloaded = total - bytes_remaining
        percentage_completed = bytes_downloaded / total * 100
        
        self.download_status_frame.pack(pady=15, padx=20)
        
        self.progress_label.configure(text=f"{int(percentage_completed)}%")
        self.progress_bar.set(float(percentage_completed / 100))
        self.progress_label.update()
        
    
    def download_mp3_only(self):
        try:
            video_mp3 = self.youtube.streams.get_audio_only()
            self.update()
            
            if video_mp3:
                os.path.join("Downloaded audios")
                video_mp3.download(filename=f"{self.archive_name}.mp3", output_path="Downloaded audios")
                
                self.download_status_frame.pack_forget()
                
                messagebox.askokcancel(title="Downloaded!", message="The download was succesful!")
                self.cancel_video_selected()
            else:
                messagebox.showerror(title="Stream error", message="There isn't a Stream for the video's audio, sorry :( ")
        except Exception as e:
            messagebox.showerror(title="ERROR", message=f"An error has ocurred: {e}")
    
    def cancel_video_selected(self):
        self.video_info_frame.after(10, self.video_info_frame.pack_forget)
        self.download_opt_frame.after(10, self.download_opt_frame.pack_forget)
        self.link_entry.delete(0, ctk.END)


if __name__ == "__main__":
    app = CtkWinYT()
    app.mainloop()
    