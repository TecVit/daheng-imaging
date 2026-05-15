import gxipy as gx
import cv2

# Inicializa o gerenciador de dispositivos
device_manager = gx.DeviceManager()
dev_num, dev_info_list = device_manager.update_device_list()

# Abre a primeira câmera encontrada
cam = device_manager.open_device_by_index(1)

# Configura e inicia aquisição
cam.stream_on()

# Captura um frame
raw_image = cam.data_stream[0].get_image()
rgb_image = raw_image.convert("RGB")

# Converte para numpy (compatível com OpenCV)
numpy_image = rgb_image.get_numpy_array()
cv2.imshow("MER2-302-37GC", numpy_image)
cv2.waitKey(0)

# Finaliza
cam.stream_off()
cam.close_device()
