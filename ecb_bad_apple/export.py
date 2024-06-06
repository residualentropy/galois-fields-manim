import numpy as np
from skvideo.io import vwrite, FFmpegWriter
from tqdm import trange

RES = (480, 360)
FPS = 30
N_FRAMES = 6571

frames_orig = None

def export(method: str, transform):
    if frames_orig is None:
        raise RuntimeError("cannot export: original frames have not been loaded")
    print("=== RUNNING EXPORT ({method}) ===")
    print(f"Encrypting and exporting with method {method} ({repr(transform)})...")
    output_params = {}
    w = FFmpegWriter(f'encrypted_{method}.mp4', outputdict= output_params)
    print(f"Created {RES} writer, outputting to 'encrypted_{method}.mp4'.")
    print(f"Output params are: {output_params}.")
    print("Encrypting...")
    encrypted = transform(frames_orig)
    print("[see progress] Writing frames...")
    for frame_no in trange(N_FRAMES):
        w.writeFrame(transform(encrypted[frame_no]))
    print("Write complete, closing writer.")
    w.close()
    print("=== EXPORT DONE ===")

if __name__ == '__main__':
    print("Loading compressed archive (bad_apple.compressed.npz)...")
    frames_orig_dict = np.load('bad_apple.compressed.npz')
    assert len(frames_orig_dict) == N_FRAMES
    print("[see progress] Loading frames into massive array...")
    frames_orig = np.empty([N_FRAMES, RES[1], RES[0], 3], dtype= np.uint8)
    for frame_no in trange(N_FRAMES):
        frames_orig[frame_no] = frames_orig_dict[f'arr_{frame_no}']
    print(f"Loaded {N_FRAMES} frames.")
    methods = [
        ('identity', lambda x: x),
    ]
    print(f"Running all exports ({[ name for name, _ in methods ]})...")
    for method, transform in methods:
        export(method, transform)
    print("All done.")
