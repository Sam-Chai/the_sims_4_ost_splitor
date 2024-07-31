import os
import hashlib
from pydub import AudioSegment

# 计算音频的RMS能量
def calculate_rms(file_path):
    audio = AudioSegment.from_wav(file_path)
    return audio.rms

# 获取文件大小
def get_file_size(file_path):
    try:
        with open(file_path, 'rb') as f:
            f.seek(0, 2)  # 移动到文件末尾
            return f.tell()
    except Exception as e:
        print(f"获取文件大小时出错: {e}")
        return None

# 计算文件的MD5哈希值
def calculate_md5(file_path, chunk_size=8192):
    md5 = hashlib.md5()
    try:
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(chunk_size), b''):
                md5.update(chunk)
        return md5.hexdigest()
    except Exception as e:
        print(f"计算MD5时出错: {e}")
        return None

# 判断两个文件是否完全一致
def are_files_identical(file1, file2):
    size1 = get_file_size(file1)
    size2 = get_file_size(file2)
    
    if size1 is None or size2 is None:
        print("无法获取文件大小")
        return False
    
    if size1 != size2:
        print("文件大小不一致")
        return False

    md51 = calculate_md5(file1)
    md52 = calculate_md5(file2)

    if md51 is None or md52 is None:
        print("无法计算文件的MD5")
        return False

    return md51 == md52

# 删除重复文件
def remove_duplicate_files(folder, new_file):
    files_to_delete = []
    for existing_file in os.listdir(folder):
        existing_file_path = os.path.join(folder, existing_file)
        if existing_file_path != new_file and are_files_identical(existing_file_path, new_file):
            print(f"删除重复文件: {existing_file_path}")
            files_to_delete.append(existing_file_path)
    for file_path in files_to_delete:
        os.remove(file_path)

# 分离音轨并保存
def split_audio_file(file_path, ep_name, index):
    audio = AudioSegment.from_wav(file_path)
    
    if audio.channels != 16:
        raise ValueError("音频文件需要包含16个单声道音轨")

    channels = audio.split_to_mono()

    output_folder = os.path.splitext(file_path)[0]
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for i in range(0, 16, 2):
        left = channels[i].pan(-1)
        right = channels[i + 1].pan(1)
        stereo_track = left.overlay(right)
        output_file = os.path.join(output_folder, f"{ep_name} {index} track_{i//2 + 1}.wav")
        stereo_track.export(output_file, format="wav")
        print(f"导出文件: {output_file}")

# 重命名文件根据RMS值
def rename_files_based_on_rms(output_folder, ep_name, index):
    dynamics = ["ppp", "pp", "p", "mp", "mf", "f", "ff", "fff"]
    rms_values = []

    # 查找子目录中的所有 WAV 文件
    audio_files = [f for f in os.listdir(output_folder) if f.endswith(".wav")]
    
    if not audio_files:
        print(f"文件夹 {output_folder} 中没有需要处理的文件")
        return

    # 计算所有音频文件的 RMS 能量
    for audio_file in audio_files:
        file_path = os.path.join(output_folder, audio_file)
        rms = calculate_rms(file_path)
        rms_values.append((file_path, rms))

    # 根据 RMS 值对音频文件进行排序
    rms_values.sort(key=lambda x: x[1])

    # 重新命名文件
    for i, (file_path, rms) in enumerate(rms_values):
        base_name = os.path.basename(file_path)
        new_name = f"{ep_name} {index} {dynamics[i]}.wav"
        new_path = os.path.join(output_folder, new_name)
        if os.path.exists(file_path):
            os.rename(file_path, new_path)
            print(f"重命名文件: {new_name}")
            remove_duplicate_files(output_folder, new_path)

# 重命名并分离音轨
def rename_and_split_audio_files(base_dir, ep_mapping):
    ignored_dirs = ["GP09"]  # 要忽略的文件夹

    for ep_dir in os.listdir(base_dir):
        if ep_dir in ignored_dirs:
            print(f"忽略文件夹: {ep_dir}")
            continue
        
        if ep_dir in ep_mapping:
            ep_name = ep_mapping[ep_dir]
            audio_files = [f for f in os.listdir(os.path.join(base_dir, ep_dir)) if f.startswith("S4") and f.endswith(".wav")]
            
            for index, audio_file in enumerate(audio_files):
                new_name = f"{ep_name} {index + 1}.wav"
                old_path = os.path.join(base_dir, ep_dir, audio_file)
                new_path = os.path.join(base_dir, ep_dir, new_name)
                os.rename(old_path, new_path)
                split_audio_file(new_path, ep_name, index + 1)
                output_folder = os.path.splitext(new_path)[0]
                rename_files_based_on_rms(output_folder, ep_name, index + 1)

# EP与对应名称的映射表
ep_mapping = {
    "EP01": "Get to Work",
    "EP02": "Get Together",
    "EP03": "City Living",
    "EP04": "Cats & Dogs",
    "EP05": "Seasons",
    "EP06": "Get Famous",
    "EP07": "Island Living",
    "EP08": "Discover University",
    "EP09": "Eco Lifestyle",
    "EP10": "Snowy Escape",
    "EP11": "Cottage Living",
    "EP12": "High School Years",
    "EP13": "Growing Together",
    "EP14": "Horse Ranch",
    "EP15": "For Rent",
    "FP01": "Holiday Celebration Pack",
    "GP01": "Outdoor Retreat",
    "GP02": "Spa Day",
    "GP03": "Dine Out",
    "GP04": "Vampires",
    "GP05": "Parenthood",
    "GP06": "Jungle Adventure",
    "GP07": "StrangerVille",
    "GP08": "Realm of Magic",
    "GP09": "Star Wars™: Journey to Batuu",  # 忽略这个文件夹，他妈的在Mac上编的没毛病，放Win上必炸
    "GP10": "Dream Home Decorator",
    "GP11": "My Wedding Stories",
    "GP12": "Werewolves",
    "SP01": "Luxury Party Stuff",
    "SP02": "Perfect Patio Stuff",
    "SP03": "Cool Kitchen Stuff",
    "SP04": "Spooky Stuff",
    "SP05": "Movie Hangout Stuff",
    "SP06": "Romantic Garden Stuff",
    "SP07": "Kids Room Stuff",
    "SP08": "Backyard Stuff",
    "SP09": "Vintage Glamour Stuff",
    "SP10": "Bowling Night Stuff",
    "SP11": "Fitness Stuff",
    "SP12": "Toddler Stuff",
    "SP13": "Laundry Day Stuff",
    "SP14": "My First Pet Stuff",
    "SP15": "Moschino Stuff",
    "SP16": "Tiny Living Stuff Pack",
    "SP17": "Nifty Knitting",
    "SP18": "Paranormal Stuff Pack",
    "SP20": "Throwback Fit Kit",
    "SP21": "Country Kitchen Kit",
    "SP22": "Bust the Dust Kit",
    "SP23": "Courtyard Oasis Kit",
    "SP24": "Fashion Street Kit",
    "SP25": "Industrial Loft Kit",
    "SP26": "Incheon Arrivals Kit",
    "SP28": "Modern Menswear Kit",
    "SP29": "Blooming Rooms Kit",
    "SP30": "Carnaval Streetwear Kit",
    "SP31": "Décor to the Max Kit",
    "SP32": "Moonlight Chic Kit",
    "SP33": "Little Campers Kit",
    "SP34": "First Fits Kit",
    "SP35": "Desert Luxe Kit",
    "SP36": "Pastel Pop Kit",
    "SP37": "Everyday Clutter Kit",
    "SP38": "Simtimates Collection Kit",
    "SP39": "Bathroom Clutter Kit",
    "SP40": "Greenhouse Haven Kit",
    "SP41": "Basement Treasures Kit",
    "SP42": "Grunge Revival Kit",
    "SP43": "Book Nook Kit",
    "SP44": "Poolside Splash Kit",
    "SP45": "Modern Luxe Kit",
    "SP46": "Home Chef Hustle Stuff Pack",
    "SP47": "Castle Estate Kit",
    "SP48": "Goth Galore Kit",
    "SP49": "Crystal Creations Stuff Pack",
    "SP50": "Urban Homage Kit",
    "SP51": "Party Essentials Kit",
    "SP52": "Riviera Retreat Kit",
    "SP53": "Cozy Bistro Kit",
}

# 运行脚本
base_dir = "The Sims 4 OST"
rename_and_split_audio_files(base_dir, ep_mapping)

print("处理完毕！")
