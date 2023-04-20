import os
import yt_dlp

# 定義一個下載進度條的類別
class DownloadProgressBar:
    def progress_hook(self, data):
        if data["status"] == "downloading":
            downloaded_bytes = data["downloaded_bytes"]
            total_bytes = data["total_bytes"]
            progress = (downloaded_bytes / total_bytes) * 100
            print("\r下載中: {:.2f}%".format(progress), end="")  # 顯示下載進度的訊息

# 定義一個下載影片的函式
def download_video(url):
    ydl_opts = {
        "format": "best",  # 選擇下載的格式為最佳畫質
        "outtmpl": os.path.join("downloaded_videos", "%(title)s.%(ext)s"),  # 設定下載的檔名及儲存路徑
        "progress_hooks": [DownloadProgressBar().progress_hook],  # 設定下載進度條的顯示方式
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])  # 開始下載影片

if __name__ == "__main__":
    video_url = "https://www.youtube.com/watch?v=Z-iqf3D4UkQ"
    download_video(video_url)  # 執行下載影片的函式
