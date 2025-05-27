# 🎬 Interactive Video Subtitle Generator

> 🌟 Automatically generate and translate subtitles for your videos using AI!

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![OpenAI Whisper](https://img.shields.io/badge/OpenAI-Whisper-green.svg)](https://github.com/openai/whisper)

## ✨ Features

- 🎙️ **Advanced Speech Recognition**: Powered by OpenAI's Whisper model
- 🌍 **Multi-language Support**: Transcribe in 99+ languages
- 🔄 **Real-time Translation**: Translate to 100+ languages
- 📝 **Multiple Formats**: Export as SRT or WebVTT
- 📦 **Batch Processing**: Handle multiple videos at once
- 🖥️ **Interactive Console**: Beautiful progress tracking
- ⚡ **GPU Acceleration**: Optional CUDA support for faster processing
- 🎯 **High Accuracy**: State-of-the-art speech recognition

## 🚀 Quick Start

### Prerequisites

- 🐍 Python 3.9 or higher
- 🎵 FFmpeg
- 🎮 CUDA-compatible GPU (optional, for faster processing)

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/msadeqsirjani/SubtitleGenerator.git
cd SubtitleGenerator
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Install FFmpeg:**
- 🍎 **macOS**: 
  ```bash
  brew install ffmpeg
  ```
- 🐧 **Linux**: 
  ```bash
  sudo apt-get install ffmpeg
  ```
- 🪟 **Windows**: Download from [FFmpeg website](https://ffmpeg.org/download.html)

## 💡 Usage

### Single Video Processing

```bash
python main.py --input video.mp4 --output subtitles.srt --language en
```

### Batch Processing

```bash
python main.py --input_dir videos/ --output_dir subtitles/ --language en
```

### Command Line Options

| Option | Description | Example |
|--------|-------------|---------|
| `--input` | 📁 Input video file | `--input video.mp4` |
| `--input_dir` | 📂 Input directory | `--input_dir videos/` |
| `--output` | 📝 Output subtitle file | `--output subs.srt` |
| `--output_dir` | 📂 Output directory | `--output_dir subtitles/` |
| `--language` | 🌐 Target language code | `--language es` |
| `--model` | 🤖 Whisper model size | `--model base` |
| `--format` | 📄 Output format | `--format srt` |
| `--gpu` | ⚡ Use GPU acceleration | `--gpu` |

### Available Models

| Model | Size | Memory | Relative Speed |
|-------|------|--------|----------------|
| tiny | 39M | 1GB | 32x |
| base | 74M | 1GB | 16x |
| small | 244M | 2GB | 6x |
| medium | 769M | 5GB | 2x |
| large | 1550M | 10GB | 1x |

## 📁 Project Structure

```
SubtitleGenerator/
├── 📜 main.py              # Main entry point
├── 📂 src/
│   ├── 🎙️ transcriber.py   # Speech recognition
│   ├── 🌐 translator.py    # Translation service
│   ├── 📝 formatter.py     # Subtitle formatting
│   └── 🛠️ utils.py         # Utility functions
├── 📋 requirements.txt     # Dependencies
└── 📖 README.md           # Documentation
```

## 🎯 Examples

### Basic Usage
```bash
# Generate English subtitles
python main.py --input lecture.mp4 --output lecture.srt

# Generate Spanish subtitles with GPU acceleration
python main.py --input video.mp4 --output video_es.srt --language es --gpu

# Process all videos in a directory
python main.py --input_dir courses/ --output_dir subtitles/ --language fr
```

### Advanced Usage
```bash
# Use a larger model for better accuracy
python main.py --input interview.mp4 --output subs.srt --model large --gpu

# Generate WebVTT format
python main.py --input video.mp4 --output video.vtt --format vtt

# Process videos with specific model and language
python main.py --input_dir videos/ --output_dir subs/ --model medium --language ja --gpu
```

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. 🍴 Fork the repository
2. 🌿 Create your feature branch (`git checkout -b feature/amazing-feature`)
3. 💾 Commit your changes (`git commit -m 'Add amazing feature'`)
4. 📤 Push to the branch (`git push origin feature/amazing-feature`)
5. 🎁 Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- 🎯 [OpenAI Whisper](https://github.com/openai/whisper) for the amazing speech recognition model
- 🌐 [Google Translate](https://cloud.google.com/translate) for translation services
- 🎨 [Rich](https://github.com/Textualize/rich) for the beautiful console interface

## 📚 Documentation

For more detailed information, check out our [Wiki](../../wiki) or the following guides:
- [Installation Guide](../../wiki/Installation)
- [Usage Examples](../../wiki/Usage-Examples)
- [Troubleshooting](../../wiki/Troubleshooting)
- [Contributing Guidelines](../../wiki/Contributing)

## 🐛 Bug Reports

Found a bug? Please open an issue with:
1. 🔍 Description of the issue
2. 📋 Steps to reproduce
3. 🖥️ System information
4. 📎 Error logs (if any)

## 📫 Contact

Have questions? Feel free to:
- 📮 Open an issue
- 🌟 Star the repository
- 🔗 Connect with contributors

---

<p align="center">
  Made with ❤️ by the Open Source Community
</p> 