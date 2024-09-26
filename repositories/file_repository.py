import os
import aiofiles
from pydub import AudioSegment

class FileRepository:
    def __init__(self, base_dir: str):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)

    async def save_audio_stream(self, file_path: str, stream):
        async with aiofiles.open(file_path, 'wb') as f:
            async for chunk in stream:
                if chunk["type"] == "audio":
                    await f.write(chunk["data"])

    def save_audio(self, file_path: str, audio: AudioSegment):
        audio.export(file_path, format="mp3")

    def save_text(self, file_path: str, content: str):
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

    def delete_file(self, file_path: str):
        try:
            os.remove(file_path)
        except Exception as e:
            print(f"Erro ao remover arquivo {file_path}: {e}")