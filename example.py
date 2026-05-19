import gxipy as gx
import cv2
import time

device_manager = gx.DeviceManager()
dev_num, dev_info_list = device_manager.update_device_list()

if dev_num == 0:
  print("Nenhuma câmera encontrada")
  exit()

cam = device_manager.open_device_by_index(1)

# =========================
# CONFIG FPS
# =========================
TARGET_FPS = 60 

try:
  # habilita controle de FPS
  cam.AcquisitionFrameRateMode.set(gx.GxSwitchEntry.ON)
  cam.AcquisitionFrameRate.set(TARGET_FPS)

  actual_fps_config = cam.AcquisitionFrameRate.get()
  print(f"FPS configurado: {actual_fps_config:.2f}")

except Exception as e:
  print("Não foi possível configurar FPS:", e)

try:
  cam.stream_on()

  print("CTRL + C para sair")

  # controle FPS real
  frame_count = 0
  fps_start_time = time.time()

  # controle temperatura
  last_temp_time = 0

  while True:
    raw_image = cam.data_stream[0].get_image()

    if raw_image is None:
      continue

    status = raw_image.get_status()

    if status != 0:
      print(f"Frame inválido: {status}")
      continue

    rgb_image = raw_image.convert("RGB")

    if rgb_image is None:
      continue

    numpy_image = rgb_image.get_numpy_array()

    if numpy_image is None:
      continue

    # =========================
    # FPS REAL
    # =========================
    frame_count += 1

    elapsed = time.time() - fps_start_time

    if elapsed >= 1.0:
      real_fps = frame_count / elapsed

      print(f"FPS real: {real_fps:.2f}")

      frame_count = 0
      fps_start_time = time.time()

    # =========================
    # TEMPERATURA
    # =========================
    if time.time() - last_temp_time > 2:
      last_temp_time = time.time()

      try:
        temperature = cam.DeviceTemperature.get()
        print(f"Temperatura: {temperature:.2f} °C")
      except Exception as e:
        print("Temperatura não suportada:", e)

    # =========================
    # EXIBE IMAGEM
    # =========================
    cv2.imshow("MER2-302-37GC", numpy_image)

    # sair com Q
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break

except KeyboardInterrupt:
  print("\nEncerrando...")

finally:
  cam.stream_off()
  cam.close_device()
  cv2.destroyAllWindows()