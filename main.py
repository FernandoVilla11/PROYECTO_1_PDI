#Archivo principal

from procesamiento import procesar_video

if __name__ == "__main__":
    VIDEO_PATH = "./data/PV_4.mp4"
    
    df = procesar_video(VIDEO_PATH)