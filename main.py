#Archivo principal

import pandas as pd
from procesamiento import procesar_video

if __name__ == "__main__":
    VIDEO_PATH = "./data/PV_3.mp4"
    
    df = procesar_video(VIDEO_PATH)