import os
import wave
import pyaudio
import keyboard

def record_audio(file_path="saves/record.wav", sample_rate=1600, chunk_size=1024, channels=1):
    """
    마이크로부터 음성을 녹음합니다. 특정 키 입력으로 녹음을 종료합니다.
    :param file_path: 저장할 파일 경로
    :param sample_rate: 샘플링 레이트
    :param chunk_size: 버퍼 크기
    :param channels: 채널 수
    """
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    audio_format = pyaudio.paInt16
    audio = pyaudio.PyAudio()
    stream = audio.open(format=audio_format, 
                        channels=channels, 
                        rate=sample_rate, 
                        input=True, 
                        frames_per_buffer=chunk_size)
    
    print("녹음을 시작합니다... (종료하려면 'q' 키를 누르세요.)")
    frames = []
    try:
        while True:
            data = stream.read(chunk_size)
            frames.append(data)
            # 'q' 키를 누르면 녹음 종료
            if keyboard.is_pressed('q'):
                print("녹음을 종료합니다...")
                break
    except KeyboardInterrupt:
        print("녹음이 중단되었습니다.")
    
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # WAV 파일로 저장
    wf = wave.open(file_path, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(audio.get_sample_size(audio_format))
    wf.setframerate(sample_rate)
    wf.writeframes(b''.join(frames))
    wf.close()

    return file_path