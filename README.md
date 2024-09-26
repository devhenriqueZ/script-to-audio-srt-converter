# Script-to-Audio-SRT Converter

This project provides a Python FastAPI application that converts text scripts into audio files and SRT subtitles using edge_tts. It's designed to streamline the video content creation workflow by automating the generation of audio narration and subtitles from a given script.

## Features

- Convert text scripts to MP3 audio files
- Generate SRT subtitle files synchronized with the audio
- Support for multiple languages and voices
- Adjustable speech rate and volume
- Docker support for easy deployment

## Prerequisites

- Docker
- Git

## Quick Start

1. Clone the repository:
   ```
   git clone https://github.com/devhenriqueZ/script-to-audio-srt-converter.git
   cd script-to-audio-srt-converter
   ```

2. Build and run the Docker container:
   ```
   docker compose up -d --build
   ```

3. The API will now be available at `http://localhost:8000`

## Usage

Send a POST request to `/generate-audio-and-srt` with the following JSON payload:

```json
{
  "task_uuid": "b56a45fd-e0c2-4fa7-b1ab-a8b64c660559",
  "title": "Your Video Title",
  "body": "Your video script content goes here...",
  "language": "pt-BR",
  "gender": "Male",
  "rate": "1.0",
  "volume": 100
}
```

## Output

The generated audio files (MP3) and subtitle files (SRT) will be saved in the `output` directory. You can easily import these files into video editing software like CapCut for further processing.

## API Endpoints

- `POST /generate-audio-and-srt`: Generate audio and SRT files from the provided script
- `GET /`: API health check

## Configuration

You can modify the following parameters in the API request:

- `language`: The language code (e.g., "pt-BR" for Brazilian Portuguese)
- `gender`: "Male" or "Female"
- `rate`: Speech rate (1.0 is normal speed, use higher values for faster speech)
- `volume`: Volume level (0-100)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.