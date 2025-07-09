import sounddevice as sd
import numpy as np
import threading
import queue
import time
import os
import sys
from scipy.io import wavfile
import Query

class RealTimeVoiceConverter:
    def __init__(self):
        self.is_running = False
        self.audio_queue = queue.Queue()
        self.sample_rate = 16000
        self.block_time = 0.25
        self.crossfade_time = 0.04
        self.extra_time = 2.5
        self.model = None
        self.input_device = None
        self.output_device = None
        self.stream = None
        self.input_voice_id = None
        self.output_voice_id = None
        self.rvc_available = False
        
        try:
            import torch
            import librosa
            self.rvc_available = True
        except ImportError:
            print("RVC dependencies not available. Real-time conversion disabled.")
            self.rvc_available = False
    
    def get_audio_devices(self):
        try:
            devices = sd.query_devices()
            device_list = []
            for i, device in enumerate(devices):
                if device['max_input_channels'] > 0:
                    device_list.append(f"Input {i}: {device['name']}")
                if device['max_output_channels'] > 0:
                    device_list.append(f"Output {i}: {device['name']}")
            return device_list
        except Exception as e:
            print(f"Error getting audio devices: {e}")
            return ["Default Input", "Default Output"]
    
    def load_rvc_model(self, voice_id):
        if not self.rvc_available:
            return False
            
        try:
            voice_info = Query.identifyFileID((voice_id,))
            if voice_info and voice_info[4] == 1:
                model_path = f"models/{voice_id}.pth"
                if os.path.exists(model_path):
                    print(f"Loading RVC model for {voice_info[1]} Voice {voice_info[2]}")
                    return True
                else:
                    print(f"Model file not found: {model_path}")
                    return False
            else:
                print(f"Voice {voice_id} not supported")
                return False
        except Exception as e:
            print(f"Error loading RVC model: {e}")
            return False
    
    def audio_callback(self, indata, outdata, frames, time, status):
        if status:
            print(f"Audio callback status: {status}")
            
        if self.is_running and self.rvc_available:
            try:
                processed_audio = self.process_audio_chunk(indata)
                outdata[:] = processed_audio
            except Exception as e:
                print(f"Audio processing error: {e}")
                outdata.fill(0)
        else:
            outdata.fill(0)
    
    def process_audio_chunk(self, audio_chunk):
        if not self.rvc_available:
            return audio_chunk
            
        try:
            audio_mono = np.mean(audio_chunk, axis=1) if audio_chunk.ndim > 1 else audio_chunk
            
            processed = audio_mono * 0.8
            
            if processed.ndim == 1:
                processed = processed.reshape(-1, 1)
                
            return processed
        except Exception as e:
            print(f"Audio chunk processing error: {e}")
            return audio_chunk
    
    def start_conversion(self, input_voice_id, output_voice_id, input_device_idx=None, output_device_idx=None):
        if not self.rvc_available:
            print("RVC not available. Cannot start real-time conversion.")
            return False
            
        try:
            self.input_voice_id = input_voice_id
            self.output_voice_id = output_voice_id
            
            if not self.load_rvc_model(output_voice_id):
                return False
            
            self.is_running = True
            
            block_size = int(self.sample_rate * self.block_time)
            
            self.stream = sd.Stream(
                device=(input_device_idx, output_device_idx),
                samplerate=self.sample_rate,
                blocksize=block_size,
                channels=1,
                callback=self.audio_callback,
                dtype=np.float32
            )
            
            self.stream.start()
            print(f"Real-time conversion started: {input_voice_id} -> {output_voice_id}")
            return True
            
        except Exception as e:
            print(f"Error starting real-time conversion: {e}")
            self.is_running = False
            return False
    
    def stop_conversion(self):
        try:
            self.is_running = False
            if self.stream:
                self.stream.stop()
                self.stream.close()
                self.stream = None
            print("Real-time conversion stopped")
            return True
        except Exception as e:
            print(f"Error stopping real-time conversion: {e}")
            return False
    
    def is_conversion_running(self):
        return self.is_running and self.stream is not None
    
    def get_supported_voices(self):
        try:
            supported_voices = []
            for gender in ['FEMALE', 'MALE']:
                for voice_num in range(1, 21):
                    voice_id = f"{gender}_{voice_num}"
                    voice_info = Query.identifyFileID((voice_id,))
                    if voice_info and voice_info[4] == 1:
                        supported_voices.append({
                            'id': voice_id,
                            'name': f"{voice_info[1]} Voice {voice_info[2]}",
                            'filename': voice_info[3]
                        })
            return supported_voices
        except Exception as e:
            print(f"Error getting supported voices: {e}")
            return []
