# 针对 The Sims 4 中游戏本体与 DLC 的 CAS 音乐分轨提取

熟悉 The Sims 4 的朋友们都知道模拟人生中的 CAS 音乐会根据场景不同而播放不同的音轨。其中，我们将刨析 The Sims 4 本体与 DLC 的包装方式，并从中提取 CAS 音乐分轨。

准备工作：

- The Sims 4 游戏本体与 DLC（正版与学习版均可）
- EALayer 3
- Sims 4 Package Editor
- Cubase 或其他数字音频工作站（DAW）

## 关于 The Sims 4 的文件结构

我们找到游戏本体目录，会看到类似图中的文件目录结构：

![image-20240715184943589](https://s2.loli.net/2024/07/15/IbOwFTLoAqeHjmJ.png)

其中，游戏本体的数据在 `Data/Client` 中，而 DLC 则在图中 EPxx、FPxx、GPxx 中。目前，我还尚不知道这些文件夹对应哪些 DLC。

PS：文件夹对应的 DLC名字：

```
[EP01] Get to Work 
[EP02] Get Together 
[EP03] City Living 
[EP04] Cats & Dogs 
[EP05] Seasons 
[EP06] Get Famous 
[EP07] Island Living 
[EP08] Discover University 
[EP09] Eco Lifestyle 
[EP10] Snowy Escape 
[EP11] Cottage Living 
[EP12] High School Years 
[EP13] Growing Together 
[EP14] Horse Ranch 
[EP15] For Rent 
[FP01] Holiday Celebration Pack 
[GP01] Outdoor Retreat 
[GP02] Spa Day 
[GP03] Dine Out 
[GP04] Vampires 
[GP05] Parenthood 
[GP06] Jungle Adventure 
[GP07] StrangerVille 
[GP08] Realm of Magic 
[GP09] Star Wars™: Journey to Batuu 
[GP10] Dream Home Decorator 
[GP11] My Wedding Stories 
[GP12] Werewolves 
[SP01] Luxury Party Stuff 
[SP02] Perfect Patio Stuff 
[SP03] Cool Kitchen Stuff 
[SP04] Spooky Stuff 
[SP05] Movie Hangout Stuff 
[SP06] Romantic Garden Stuff 
[SP07] Kids Room Stuff 
[SP08] Backyard Stuff 
[SP09] Vintage Glamour Stuff 
[SP10] Bowling Night Stuff 
[SP11] Fitness Stuff 
[SP12] Toddler Stuff 
[SP13] Laundry Day Stuff 
[SP14] My First Pet Stuff 
[SP15] Moschino Stuff 
[SP16] Tiny Living Stuff Pack 
[SP17] Nifty Knitting 
[SP18] Paranormal Stuff Pack 
[SP20] Throwback Fit Kit 
[SP21] Country Kitchen Kit 
[SP22] Bust the Dust Kit 
[SP23] Courtyard Oasis Kit 
[SP24] Fashion Street Kit 
[SP25] Industrial Loft Kit 
[SP26] Incheon Arrivals Kit 
[SP28] Modern Menswear Kit 
[SP29] Blooming Rooms Kit 
[SP30] Carnaval Streetwear Kit 
[SP31] Décor to the Max Kit 
[SP32] Moonlight Chic Kit 
[SP33] Little Campers Kit 
[SP34] First Fits Kit 
[SP35] Desert Luxe Kit 
[SP36] Pastel Pop Kit 
[SP37] Everyday Clutter Kit 
[SP38] Simtimates Collection Kit 
[SP39] Bathroom Clutter Kit 
[SP40] Greenhouse Haven Kit 
[SP41] Basement Treasures Kit 
[SP42] Grunge Revival Kit 
[SP43] Book Nook Kit 
[SP44] Poolside Splash Kit 
[SP45] Modern Luxe Kit 
[SP46] Home Chef Hustle Stuff Pack 
[SP47] Castle Estate Kit 
[SP48] Goth Galore Kit 
[SP49] Crystal Creations Stuff Pack 
[SP50] Urban Homage Kit 
[SP51] Party Essentials Kit 
[SP52] Riviera Retreat Kit 
[SP53] Cozy Bistro Kit 
```



以游戏本体为例，会看到文件夹中有这些文件：

![image-20240715185141642](https://s2.loli.net/2024/07/15/ZIbyiYFpzDABjln.png)

这些后缀为 .package 的文件都是游戏必要的组成部分。其中，我们需要使用 Sims 4 Package Editor 来解压这些 .package 文件。

再让我们看看 DLC 的文件构成：

![image-20240715185239424](https://s2.loli.net/2024/07/15/58RwHBeQoDZ6maq.png)

可以看到与游戏本体的组成非常相似。

## Sims 4 Package Editor

这是一个由社区开发的针对修改模拟人生游戏内容的工具类软件，我们用它解密 .package 文件，并解压我们需要的内容。

![](https://s2.loli.net/2024/07/15/6BMCo2xdZIY3WFH.png)

打开软件后，点击 `File/Open...`，打开我们需要解压的 .package 文件。其中，包含音频的包有这些：

- ClientFullBuild1
- ClientFullBuild2
- ClientFullBuild3
- ClientFullBuild4
- ClientFullBuild5
- ClientDeltaBuild1
- ClientDeltaBuild2
- ClientDeltaBuild3
- ClientDeltaBuild4
- ClientDeltaBuild5

本体的音乐提取是比较麻烦和繁琐的，而 DLC 的都简单许多（通常只包含一个包）。

然后我们需要设置一下筛选，只保留音频文件。模拟人生中音频文件的 Tag 为 _AUD。

![image-20240715185830381](https://s2.loli.net/2024/07/15/eCJ6zvd7VY5RE4f.png)

点击 Set，就会出现只有 _AUD 这个 Tag 的文件。

但是，模拟人生中不仅包含 CAS 音乐，还包含广播、DJ、音效等等，这些都是 _AUD 格式的后缀。

我们需要根据文件大小和类型查看到底是 CAS 还是其他的音效。

![image-20240715190531610](https://s2.loli.net/2024/07/15/CP1zWhaBRA7Myod.png)

所有的广播和 CAS 音乐的 Type 都为 `0x01EEF63A`，我们只需要根据这个 Type 寻找即可。而 CAS 音乐通常更大（20-30MB），所以同时查看 Memsize，可以看到前三个都是 `0x01` 开头，而第四个则是 `0x004...`。所以我们可以判定前三个是 CAS 音乐，后面的则是广播音乐。

然后我们选中这三个看起来非常像 CAS 音乐的文件，点击右键，选择 `Export/To File...`。然后寻找一个合适的文件夹来存放。我这里建议与 EALayer 3 存放在一起，像这样：

![image-20240715190919301](https://s2.loli.net/2024/07/15/ZGgSWBrihzlPsub.png)

图中 GP01 之类的文件夹是 DLC，本体我放在了 Games 文件夹中。

解压出来的文件是 .sns 文件结尾的。
![image-20240715191017612](https://s2.loli.net/2024/07/15/VkCEqsyvezpduoP.png)

这个时候，需要我们利用 EALayer 3 来解码 .sns 文件。

### DLC 解包

DLC 解包与游戏本体类似，例如 EP01 的 DLC 文件夹：

![image-20240715190721326](https://s2.loli.net/2024/07/15/heXRwCzV95iB34M.png)

只需要打开 `ClientFullBuild0.package` 就可以。

## EALayer 3 解码

经过我的测试，新版本的 EALayer（0.7.0）貌似无法解码 Multi Channel 的 wav 文件，但是老版本的 0.5.0 是可以的。在这里我选择老版本的 EALayer 进行解码。

解码的命令如下：

`.\ealayer3.exe -mc "文件名.sns"`

你可以使用这个命令来对单个的 .sns 文件解码。或者使用下方的 .ps1 脚本来批处理执行，在这里它会自动搜索在同级文件夹下的所有 .sns 文件并自动解码。

```powershell
$programDir = "C:\Plugins\ts4packageeditor\Decoder\ealayer3-0.5.0-win32"

Get-ChildItem -Path $programDir -Recurse -Filter *.sns | ForEach-Object {
    $snsFilePath = $_.FullName
    $command = $programDir + "\ealayer3.exe -mc `"$snsFilePath`""
    Write-Host "Executing command: $command"
    try {
        Invoke-Expression $command
        Write-Host "Successfully decoded: $snsFilePath"
    } catch {
        Write-Host "Failed to decode" + $snsFilePath + ":" + $_
    }
}
```

其中，`$programDir` 改为你自己的 ealayer3 目录，确保这个目录下的文件夹像我一样包含 CAS 音乐的 .sns 文件。

解码完成后，会在 .sns 文件的旁边出现一个 .wav 的音频文件。

![](https://s2.loli.net/2024/07/15/Mz5ZbalsANQ13yY.png)

## 打开 CAS 音乐分轨

模拟人生的 CAS 音乐分割成了 16 个单声道（8个立体声轨道）来完成对特定场景下切换音乐强弱的变化。

如果用默认的音乐播放器（如 VLC），只会听到乐器最少的那一轨。这是因为很多默认音乐播放器只播放 1 和 2 轨道。而放在其余的轨道由于并不属于立体声输出，所以不会被播放（如果有多输出音频接口，可能在其他轨道会有相应的声音出现）

这个时候，我们需要通过 DAW，即数字音频工作站打开。下面以 Cubase 举例：

![image-20240715191902203](https://s2.loli.net/2024/07/15/izRUCKZaQ1I2L9J.png)

将 wav 文件拖入 Cubase，会打开 16 个单声道轨道。在混音器中将单声道轨道的声像掰成极左极右。

![image-20240715192005662](https://s2.loli.net/2024/07/15/LBgtiq2cTQyNzXJ.png)

这样，我们单独听前两个轨道，就是最弱的那一轨。依次听 3、4，5、6，可以发现音乐由弱逐渐变强。这就是模拟人生中 CAS 音乐会根据场景而切换强弱的原理。现在，可以将自己想听的轨道进行独奏，并导出成音频文件。