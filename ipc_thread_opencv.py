import cv2  # 導入OpenCV函式庫
import threading  # 導入多線程模組
import time  # 導入時間模組
from threading import Lock  # 從多線程模組導入Lock
import os  # 導入操作系統模組
import fnmatch  # 導入檔案名匹配模組

class Camera:
    def __init__(self, lane, file_path):
        self.lane = lane  # 車道
        self.file_path = file_path  # 視頻檔案路徑

        self.flag = True  # 控制視頻讀取線程的標誌
        self.last_frame = None  # 最後一幀
        self.last_ready = None  # 最後一幀是否準備好
        self.lock = Lock()  # 鎖定物件，確保多線程安全

        capture = cv2.VideoCapture(self.file_path)  # 創建一個視頻捕捉物件
        self.fps = capture.get(cv2.CAP_PROP_FPS) % 100  # 獲取視頻的幀率
        thread = threading.Thread(target=self.rtsp_cam_buffer, args=(capture,), name="rtsp_read_thread")  # 創建一個讀取視頻的線程
        thread.daemon = True  # 設置為守護線程
        thread.start()  # 啟動線程

    def get_ready(self):
        return self.last_ready  # 返回最後一幀是否準備好

    def rtsp_cam_buffer(self, capture):
        while self.flag:  # 當線程運行時
            with self.lock:  # 使用鎖定物件
                self.last_ready, self.last_frame = capture.read()  # 讀取視頻的一幀

                if not self.last_ready:  # 如果最後一幀沒有準備好
                    self.flag = False  # 停止線程
                    print(f"{self.file_path} has a problem")  # 輸出錯誤信息

            time.sleep(1 / self.fps)  # 等待一個時間間隔

    def get_frame(self):
        if (self.last_ready is not None) and (self.last_frame is not None):  # 如果最後一幀已經準備好
            return self.last_frame.copy()  # 返回最後一幀的副本
        else:
            return None  # 否則返回None


def find_first_mp4_file(directory):
    for root, _, files in os.walk(directory):  # 遍歷指定目錄及其子目錄
        for file in fnmatch.filter(files, "*.mp4"):  # 篩選出所有以.mp4結尾的文件
            return os.path.join(root, file)  # 返回找到的第一個.mp4文件的完整路徑
    return None  # 如果沒有找到任何.mp4文件，則返回None

if __name__ == "__main__":
    lane = "lane1"  # 車道名稱
    directory = "downloaded_videos/"  # 視頻文件所在的目錄
    file_path = find_first_mp4_file(directory)  # 查找第一個.mp4文件

    if file_path is not None:  # 如果找到了.mp4文件
        cam = Camera(lane, file_path)  # 創建一個Camera實例

        while True:  # 無限循環
            frame = cam.get_frame()  # 獲取當前幀
            if frame is not None:  # 如果幀存在
                cv2.imshow("Camera", frame)  # 在視窗中顯示當前幀
                if cv2.waitKey(1) & 0xFF == ord('q'):  # 如果用戶按下q鍵
                    break  # 跳出無限循環

        cv2.destroyAllWindows()  # 關閉所有視窗
    else:
        print("No MP4 files found in the directory.")  # 如果沒有找到任何.mp4文件，則輸出提示信息