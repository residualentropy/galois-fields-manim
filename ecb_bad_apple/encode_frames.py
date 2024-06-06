import cv2
import numpy as np

# modified from: https://github.com/CalvinLoke/bad-apple
# (applies to this file)

video_path = "BadApple.mp4"
cap = cv2.VideoCapture(video_path)
current_frame = 1
total_frames = 200 # int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
arrays = []
while current_frame <= total_frames:
    ret, frame = cap.read()
    #frame = frame[:,:,0]
    arrays.append(frame)
    print(f"Loaded frame #{current_frame}.")
    current_frame += 1
cap.release()

print(f"Example frame (#{len(arrays) // 2}):")
print(arrays[len(arrays) // 2])

print("Saving compressed archive...")
out_path = "bad_apple.compressed.npz"
np.savez_compressed(out_path, *arrays)
print(f"Saved {len(arrays)} frames to {out_path}.")
