
# -*- coding: utf-8 -*-
import gxipy as gx
import numpy as np
import cv2

def show_daheng_realtime(camera_sn):
    # Cihaz yöneticisini oluştur
    device_manager = gx.DeviceManager()
    dev_num, dev_info_list = device_manager.update_device_list()

    if dev_num == 0:
        print("Hiçbir kamera bulunamadı.")
        return

    # Kamera bağlantısını kur
    cam = device_manager.open_device_by_sn(camera_sn)
    cam.stream_on()
    print(f"Kamera {camera_sn} ile bağlantı kuruldu. Görüntü başlatılıyor...")

    try:
        while True:
            raw_image = cam.data_stream[0].get_image()
            if raw_image is None:
                print("Görüntü alınamadı.")
                continue

            rgb_image = raw_image.convert("RGB")
            if rgb_image is None:
                print("RGB'ye dönüşüm başarısız.")
                continue

            frame = rgb_image.get_numpy_array()
            if frame is None:
                print("NumPy dizisine dönüşüm başarısız.")
                continue

            # # --- Çözünürlüğü yazdır ---
            # height, width = frame.shape[:2]
            # print(f" Canlı görüntü çözünürlüğü: {width} x {height} piksel")

            # OpenCV ile göster
            cv2.namedWindow("Daheng Realtime Görüntü", cv2.WINDOW_NORMAL)
            cv2.resizeWindow("Daheng Realtime Görüntü", 1000, 800)

            frame = cv2.rotate(frame,cv2.ROTATE_180)
            cv2.imshow("Daheng Realtime Görüntü", frame)

            # q ile çıkış
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cam.stream_off()
        cam.close_device()
        cv2.destroyAllWindows()
        print("Kamera kapatıldı ve pencere kapatıldı.")

if __name__ == "__main__":
    CAMERA_SN = "FDC24100405"
    show_daheng_realtime(CAMERA_SN)
