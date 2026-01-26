import subprocess
from collections import defaultdict

class TTSAnnouncer:
    def __init__(self, stable_frames=5):
        self.stable_frames = stable_frames
        self.seen_counts = defaultdict(int)
        self.announced_ids = set()

    def update_and_announce(self, track_id, text):
        if track_id is None or track_id < 0:
            return

        if track_id in self.announced_ids:
            return

        self.seen_counts[track_id] += 1

        if self.seen_counts[track_id] >= self.stable_frames:
            self.announced_ids.add(track_id)

            subprocess.Popen([
                "powershell",
                "-Command",
                f"Add-Type -AssemblyName System.Speech;"
                f"(New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak('{text}')"
            ])
