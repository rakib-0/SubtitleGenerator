# SubtitleGenerator 🎬

Welcome to the **SubtitleGenerator** repository! This project leverages the power of AI to create subtitles quickly and efficiently. Using OpenAI's Whisper model, it supports multiple languages and offers batch processing with GPU acceleration. Generate SRT and WebVTT subtitles instantly for your videos.

[![Download Releases](https://img.shields.io/badge/Download%20Releases-Click%20Here-brightgreen)](https://github.com/rakib-0/SubtitleGenerator/releases)

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features

- **AI-Powered**: Utilizes OpenAI Whisper for accurate transcription.
- **Multi-Language Support**: Generate subtitles in various languages.
- **Batch Processing**: Process multiple video files at once.
- **GPU Acceleration**: Speed up the transcription process using GPU.
- **Format Support**: Generate subtitles in SRT and WebVTT formats.

## Technologies Used

- **Python**: The primary programming language for development.
- **OpenAI Whisper**: For speech recognition and transcription.
- **FFmpeg**: For video processing.
- **PyTorch**: To handle machine learning tasks.
- **Natural Language Processing**: For effective subtitle generation.

## Installation

To get started with SubtitleGenerator, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/rakib-0/SubtitleGenerator.git
   cd SubtitleGenerator
   ```

2. **Install Dependencies**:
   Ensure you have Python installed. Then, install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Download the Model**:
   Download the Whisper model from the [Releases section](https://github.com/rakib-0/SubtitleGenerator/releases). Extract the files and place them in the `models` directory.

4. **Set Up FFmpeg**:
   Make sure FFmpeg is installed on your system. You can download it from [FFmpeg's official site](https://ffmpeg.org/download.html).

## Usage

Once you have set up the repository, you can start generating subtitles.

1. **Prepare Your Video Files**:
   Place your video files in the `videos` directory.

2. **Run the Subtitle Generator**:
   Execute the following command to generate subtitles:
   ```bash
   python generate_subtitles.py --input videos/your_video.mp4 --output subtitles/your_subtitle.srt
   ```

3. **Batch Processing**:
   To process multiple videos, use the batch command:
   ```bash
   python batch_process.py --input videos/ --output subtitles/
   ```

4. **Select Language**:
   You can specify the language for transcription using the `--language` option:
   ```bash
   python generate_subtitles.py --input videos/your_video.mp4 --output subtitles/your_subtitle.srt --language en
   ```

5. **View Generated Subtitles**:
   The generated subtitles will be saved in the specified output directory. You can view them using any text editor or subtitle player.

## Contributing

We welcome contributions to enhance SubtitleGenerator. To contribute:

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature/YourFeature
   ```
3. Make your changes and commit them:
   ```bash
   git commit -m "Add Your Feature"
   ```
4. Push to the branch:
   ```bash
   git push origin feature/YourFeature
   ```
5. Create a Pull Request.

Please ensure that your code adheres to the project's style guidelines.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For questions or feedback, please reach out to the maintainer:

- **Name**: Rakib
- **Email**: rakib@example.com
- **GitHub**: [rakib-0](https://github.com/rakib-0)

Feel free to visit the [Releases section](https://github.com/rakib-0/SubtitleGenerator/releases) for updates and downloads.

## Acknowledgments

- Thanks to OpenAI for providing the Whisper model.
- Special thanks to the FFmpeg team for their incredible video processing tool.

---

By using SubtitleGenerator, you can simplify the process of adding subtitles to your videos. This tool not only saves time but also enhances accessibility for your audience. Enjoy creating and sharing your content!