import librosa
import numpy as np
import matplotlib.pyplot as plt
import json
import os

def analyze_and_compare(bibiri_path, seijyo_path, logic_path):
    # ロジックの読み込み
    if not os.path.exists(logic_path):
        print(f"Error: {logic_path} not found.")
        return

    with open(logic_path, 'r', encoding='utf-8') as f:
        logic = json.load(f)
    
    threshold_hz = logic['chatter_detection']['frequency_threshold_hz']
    
    print("FUSION Lathe-Master: Analysis Started...")
    
    plt.figure(figsize=(12, 6))
    
    files = [seijyo_path, bibiri_path]
    labels = ['Normal (Seijyo)', 'Chatter (Bibiri)']
    colors = ['blue', 'red']
    
    for path, label, color in zip(files, labels, colors):
        if not os.path.exists(path):
            print(f"Warning: {path} not found. Skipping.")
            continue
            
        # 音声読み込み
        y, sr = librosa.load(path)
        
        # 周波数解析 (FFT)
        D = np.abs(librosa.stft(y))
        db = librosa.amplitude_to_db(D, ref=np.max)
        mean_db = np.mean(db, axis=1)
        freqs = librosa.fft_frequencies(sr=sr)
        
        # グラフ描画
        plt.plot(freqs, mean_db, label=label, color=color, alpha=0.7)
        
        # 高周波（ビビリ領域）の平均パワーを計算
        mask = freqs > threshold_hz
        avg_power = np.mean(mean_db[mask])
        print(f"{label:15} - Avg Power above {threshold_hz}Hz: {avg_power:.2f} dB")

    # 判定ラインの描画
    plt.axvline(x=threshold_hz, color='green', linestyle='--', label='Detection Threshold')
    plt.title('Lathe Sound Analysis: Normal vs Chatter (Sakai-Tech Sample)')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude (dB)')
    plt.xlim(0, 8000)
    plt.legend()
    
    # フォルダがなければ作成
    if not os.path.exists('docs'):
        os.makedirs('docs')
        
    output_img = "docs/analysis_result.png"
    plt.savefig(output_img)
    print(f"\n--- Analysis Complete ---")
    print(f"Result graph saved to: {output_img}")
    print(f"Advice: {logic['chatter_detection']['advice']}")

if __name__ == "__main__":
    analyze_and_compare(
        "videos/bibiri.wav", 
        "videos/seijyo.wav", 
        "data/master_logic.json"
    )