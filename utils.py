import os
import ffmpeg

def load_audio_file(filepath):
    """Загружает аудиофайл и возвращает его путь."""
    supported_formats = get_supported_formats()
    file_extension = os.path.splitext(filepath)[1][1:].lower()

    if file_extension not in supported_formats:
        raise ValueError(f"Формат файла {file_extension} не поддерживается. Поддерживаемые форматы: {supported_formats}")

    return filepath

def convert_audio_format(input_filepath, output_filepath, target_format):
    """Преобразует аудиофайл в указанный формат."""
    try:
        ffmpeg.input(input_filepath).output(output_filepath, format=target_format).run()
        return output_filepath
    except ffmpeg.Error as e:
        print(f"Ошибка при преобразовании формата: {e.stderr.decode()}")
        return None

def get_supported_formats():
    """Возвращает список поддерживаемых форматов аудиофайлов."""
    return ['mp3', 'wav', 'ogg', 'flac']