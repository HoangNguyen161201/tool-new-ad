from gtts import gTTS
import os
import platform
import tempfile
import shutil
import subprocess
import time
from tqdm import tqdm
import wave
import contextlib

def speak(text: str, speed: float = 1.0, lang: str = "en", filename: str = None):
    """
    Tạo file giọng nói từ văn bản (không phát) và lưu dưới dạng AAC.
    
    :param text: Nội dung cần đọc.
    :param speed: Tốc độ đọc (0.5 → 2.0).
    :param lang: Mã ngôn ngữ (vd: 'en' hoặc 'vi').
    :param filename: Tên file lưu (mặc định: tts_output.aac).
    :return: Đường dẫn file AAC đã tạo.
    """
    if shutil.which("ffmpeg") is None:
        raise EnvironmentError("❌ ffmpeg chưa được cài đặt hoặc không có trong PATH.")

    tmp_mp3 = os.path.join(tempfile.gettempdir(), "tts_temp.mp3")
    output_aac = filename or os.path.join(os.getcwd(), "tts_output.aac")

    print("🔊 Đang tạo file giọng nói...")

    # Tạo file giọng đọc bằng gTTS
    tts = gTTS(text=text, lang=lang, slow=False)
    tts.save(tmp_mp3)

    # Giới hạn tốc độ đọc
    ff_speed = min(max(speed, 0.5), 2.0)

    # Chuyển sang AAC và điều chỉnh tốc độ
    cmd = [
        "ffmpeg", "-y", "-i", tmp_mp3,
        "-filter:a", f"atempo={ff_speed}",
        "-c:a", "aac",               # dùng encoder aac
        "-b:a", "128k",              # bitrate mặc định
        output_aac
    ]

    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if os.path.exists(output_aac):
        print(f"✅ Đã tạo file: {output_aac}")
        return output_aac
    else:
        print("❌ Không tạo được file AAC.")
        return None
    
# Ví dụ sử dụng:
speak("""
Once upon a time, in a small and peaceful village at the foot of a great mountain, there lived a boy named An and his beloved grandmother. Their humble house was surrounded by rice fields, tall bamboo trees, and the sound of running streams. Every morning, An helped his grandmother feed the chickens, gather firewood, and fetch water from a spring that came from the mountain.
An loved the mountain more than anything. He often spent his afternoons climbing its slopes, feeling the wind on his face and listening to the sweet songs of the birds echoing through the forest. To him, the mountain was not just a place—it was a friend, silent but full of life.
Once upon a time, in a small and peaceful village at the foot of a great mountain, there lived a boy named An and his beloved grandmother. Their humble house was surrounded by rice fields, tall bamboo trees, and the sound of running streams. Every morning, An helped his grandmother feed the chickens, gather firewood, and fetch water from a spring that came from the mountain.
An loved the mountain more than anything. He often spent his afternoons climbing its slopes, feeling the wind on his face and listening to the sweet songs of the birds echoing through the forest. To him, the mountain was not just a place—it was a friend, silent but full of life.
Once upon a time, in a small and peaceful village at the foot of a great mountain, there lived a boy named An and his beloved grandmother. Their humble house was surrounded by rice fields, tall bamboo trees, and the sound of running streams. Every morning, An helped his grandmother feed the chickens, gather firewood, and fetch water from a spring that came from the mountain.
An loved the mountain more than anything. He often spent his afternoons climbing its slopes, feeling the wind on his face and listening to the sweet songs of the birds echoing through the forest. To him, the mountain was not just a place—it was a friend, silent but full of life.
Once upon a time, in a small and peaceful village at the foot of a great mountain, there lived a boy named An and his beloved grandmother. Their humble house was surrounded by rice fields, tall bamboo trees, and the sound of running streams. Every morning, An helped his grandmother feed the chickens, gather firewood, and fetch water from a spring that came from the mountain.
An loved the mountain more than anything. He often spent his afternoons climbing its slopes, feeling the wind on his face and listening to the sweet songs of the birds echoing through the forest. To him, the mountain was not just a place—it was a friend, silent but full of life.
""", speed=1.2, lang= 'en', filename= './tt.aac')
