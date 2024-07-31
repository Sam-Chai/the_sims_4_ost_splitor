import os
from pydub import AudioSegment

# 计算音频的RMS能量
def calculate_rms(file_path):
    audio = AudioSegment.from_wav(file_path)
    return audio.rms

# 根据RMS能量对音频文件进行重新命名
def rename_audio_files_based_on_rms(base_dir):
    dynamics = ["ppp", "pp", "p", "mp", "mf", "f", "ff", "fff"]

    for ep_dir in os.listdir(base_dir):
        ep_path = os.path.join(base_dir, ep_dir)
        if os.path.isdir(ep_path):
            for subdir in os.listdir(ep_path):
                subdir_path = os.path.join(ep_path, subdir)
                if os.path.isdir(subdir_path):
                    audio_files = [f for f in os.listdir(subdir_path) if f.endswith(".wav")]
                    
                    # 计算所有音频文件的RMS能量
                    rms_values = []
                    for audio_file in audio_files:
                        file_path = os.path.join(subdir_path, audio_file)
                        rms = calculate_rms(file_path)
                        rms_values.append((file_path, rms))

                    # 根据RMS值对音频文件进行排序
                    rms_values.sort(key=lambda x: x[1])

                    # 重新命名文件
                    for i, (file_path, rms) in enumerate(rms_values):
                        base_name = os.path.basename(file_path)
                        name_parts = base_name.split()
                        if len(name_parts) >= 2:
                            new_name = f"{name_parts[0]} {name_parts[1]} {dynamics[i]}.wav"
                            new_path = os.path.join(subdir_path, new_name)
                            os.rename(file_path, new_path)
                            print(f"重命名文件: {new_name}")

# 运行脚本
base_dir = "The Sims 4 OST"
rename_audio_files_based_on_rms(base_dir)
