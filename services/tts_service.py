import os
import asyncio
import logging
from typing import List, Tuple
import edge_tts
from pydub import AudioSegment
from api.models import TTSRequest
from core.audio_processing import remove_silence, format_time
from core.text_processing import tokenize_text
from repositories.file_repository import FileRepository
from config.settings import Settings

logger = logging.getLogger(__name__)

class TTSService:
    def __init__(self):
        self.settings = Settings()
        self.file_repository = FileRepository(self.settings.AUDIO_OUTPUT_DIR)

    VOICE_MAP = {
        "pt-BR": {
            "Male": "pt-BR-AntonioNeural",
            "Female": "pt-BR-FranciscaNeural"
        }
    }

    async def generate_audio_for_sentence(self, text: str, voice: str, rate: str, volume: str, output_prefix: str) -> Tuple[str, int]:
        communicate = edge_tts.Communicate(text, voice, rate=rate, volume=volume)
        audio_file = f"{output_prefix}.mp3"

        try:
            await self.file_repository.save_audio_stream(audio_file, communicate.stream())

            if not os.path.exists(audio_file) or os.path.getsize(audio_file) == 0:
                raise Exception(f"Falha ao gerar arquivo de áudio: {audio_file}")

            audio = AudioSegment.from_mp3(audio_file)
            audio_without_silence = remove_silence(audio)
            duration = len(audio_without_silence)

            self.file_repository.save_audio(audio_file, audio_without_silence)

            return audio_file, duration
        except Exception as e:
            logger.error(f"Erro ao gerar áudio para a sentença: {e}")
            if os.path.exists(audio_file):
                os.remove(audio_file)
            return None, 0

    async def process_text(self, text: str, voice: str, rate: str, volume: str, task_uuid: str, is_title: bool = False) -> List[Tuple[str, str, int]]:
        sentences = tokenize_text(text)
        audio_files = []

        async def process_sentence(sentence: str, index: int):
            output_prefix = os.path.join(self.settings.AUDIO_OUTPUT_DIR, f"{task_uuid}_{'title' if is_title else 'body'}_{index}")
            audio_file, duration = await self.generate_audio_for_sentence(sentence, voice, rate, volume, output_prefix)
            if audio_file:
                return sentence, audio_file, duration
            return None

        tasks = [process_sentence(sentence, i) for i, sentence in enumerate(sentences)]
        results = await asyncio.gather(*tasks)

        return [result for result in results if result]

    async def process_request(self, request: TTSRequest):
        try:
            voice = self.VOICE_MAP.get(request.language, {}).get(request.gender)
            if not voice:
                raise ValueError(f"Idioma ou gênero inválido: {request.language}-{request.gender}")

            title_results = await self.process_text(request.title, voice, request.rate, request.volume, str(request.task_uuid), True)
            body_results = await self.process_text(request.body, voice, request.rate, request.volume, str(request.task_uuid))

            all_results = title_results + body_results

            combined_audio = AudioSegment.empty()
            current_time = 0
            srt_content = []

            for index, (sentence, audio_file, duration) in enumerate(all_results, start=1):
                audio = AudioSegment.from_mp3(audio_file)
                combined_audio += audio

                end_time = current_time + duration
                srt_content.append(f"{index}\n{format_time(current_time)} --> {format_time(end_time)}\n{sentence}\n")

                current_time = end_time

            if title_results and body_results:
                pause_duration = 300
                pause = AudioSegment.silent(duration=pause_duration)
                title_end = sum(duration for _, _, duration in title_results)
                combined_audio = combined_audio[:title_end] + pause + combined_audio[title_end:]

            final_audio_file = os.path.join(self.settings.AUDIO_OUTPUT_DIR, f"{request.task_uuid}.mp3")
            final_subtitle_file = os.path.join(self.settings.AUDIO_OUTPUT_DIR, f"{request.task_uuid}.srt")

            self.file_repository.save_audio(final_audio_file, combined_audio)
            self.file_repository.save_text(final_subtitle_file, "\n".join(srt_content))

            for _, audio_file, _ in all_results:
                self.file_repository.delete_file(audio_file)

            return {
                "message": "Arquivos de áudio e SRT gerados com sucesso",
                "audio_file": final_audio_file,
                "srt_file": final_subtitle_file
            }
        except Exception as e:
            logger.error(f"Erro em process_request: {e}")
            raise