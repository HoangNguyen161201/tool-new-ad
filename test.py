from gtts import gTTS
import os
import tempfile
import shutil
import subprocess

def speak_with_bgm(
    text: str,
    bgm_path: str = None,
    output_path: str = "final_mix.aac",
    speed: float = 1.0,
    lang: str = "en",
    volume_voice: float = 2.0,
    volume_bgm: float = 0.3
):
    """
    Tạo giọng đọc từ văn bản, tăng âm lượng, điều chỉnh tốc độ và (tuỳ chọn) ghép nhạc nền.

    :param text: Nội dung cần đọc.
    :param bgm_path: Đường dẫn file nhạc nền (nếu có).
    :param output_path: File đầu ra (mặc định: final_mix.aac).
    :param speed: Tốc độ đọc (0.5 → 2.0).
    :param lang: Mã ngôn ngữ ('vi', 'en', ...).
    :param volume_voice: Hệ số tăng âm lượng giọng (1.0 = bình thường, 2.0 = to gấp đôi).
    :param volume_bgm: Âm lượng nhạc nền (0.0 → 1.0).
    :return: Đường dẫn file âm thanh hoàn chỉnh.
    """

    if shutil.which("ffmpeg") is None:
        raise EnvironmentError("❌ ffmpeg chưa được cài đặt hoặc không có trong PATH.")

    tmp_mp3 = os.path.join(tempfile.gettempdir(), "tts_temp.mp3")
    tmp_voice = os.path.join(tempfile.gettempdir(), "tts_voice.aac")

    print("🔊 Đang tạo giọng đọc bằng gTTS...")

    # --- Bước 1: tạo file giọng đọc bằng gTTS
    tts = gTTS(text=text, lang=lang, slow=False)
    tts.save(tmp_mp3)

    # --- Bước 2: chỉnh tốc độ và tăng âm lượng giọng
    ff_speed = min(max(speed, 0.5), 2.0)
    cmd_voice = [
        "ffmpeg", "-y", "-i", tmp_mp3,
        "-filter:a", f"atempo={ff_speed},volume={volume_voice}",
        "-c:a", "aac", "-b:a", "128k",
        tmp_voice
    ]
    subprocess.run(cmd_voice, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # --- Bước 3: nếu không có nhạc nền → chỉ xuất giọng đọc
    if not bgm_path:
        shutil.move(tmp_voice, output_path)
        print(f"✅ Đã tạo file giọng đọc: {output_path}")
        return output_path

    # --- Bước 4: lấy độ dài giọng đọc để canh nhạc nền
    cmd_duration = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", tmp_voice
    ]
    duration = float(subprocess.check_output(cmd_duration).decode().strip())

    tmp_bgm = os.path.join(tempfile.gettempdir(), "bgm_temp.aac")

    # --- Bước 5: loop hoặc cắt nhạc nền cho vừa thời lượng
    cmd_loop = [
        "ffmpeg", "-y", "-stream_loop", "-1", "-i", bgm_path,
        "-t", str(duration), "-c:a", "aac", "-b:a", "128k", tmp_bgm
    ]
    subprocess.run(cmd_loop, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # --- Bước 6: trộn nhạc nền và giọng đọc, giữ nguyên âm lượng voice
    cmd_mix = [
        "ffmpeg", "-y",
        "-i", tmp_voice,
        "-i", tmp_bgm,
        "-filter_complex",
        f"[1:a]volume={volume_bgm}[bgm];[0:a][bgm]amix=inputs=2:duration=first:weights=1 {volume_bgm}:dropout_transition=3[a]",
        "-map", "[a]",
        "-c:a", "aac",
        "-b:a", "192k",
        output_path
    ]
    subprocess.run(cmd_mix, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # --- Bước 7: dọn file tạm
    for f in [tmp_mp3, tmp_voice, tmp_bgm]:
        if os.path.exists(f):
            os.remove(f)

    if os.path.exists(output_path):
        print(f"✅ Đã tạo file hoàn chỉnh: {output_path}")
        return output_path
    else:
        print("❌ Lỗi: Không tạo được file.")
        return None
    
speak_with_bgm(
    text="""
    On the evening of October 16 in Hanoi, Jack performed a new, unreleased song. 
    Social media quickly filled with discussions and debates about his performance.
    """,
    bgm_path="./public/more/bg.mp3",
    output_path="./final.aac",
    speed=1.2,
    
    volume_voice=3.0,   # voice 3x louder
    volume_bgm=0.2    # background music volume 35%
)