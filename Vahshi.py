import subprocess
import os

input_dir = "F:/A2_25"    # please change dir
output_dir = os.path.join(input_dir, "one")
os.makedirs(output_dir, exist_ok=True)

camera_files = [f for f in os.listdir(input_dir) if f.startswith("cameraVoip") and f.endswith(".flv")]
screenshare_files = [f for f in os.listdir(input_dir) if f.startswith("screenshare") and f.endswith(".flv")]

for i in range(len(camera_files)):
    camera_file = os.path.join(input_dir, camera_files[i])
    screenshare_file = os.path.join(input_dir, screenshare_files[i % len(screenshare_files)])  

    output_file = os.path.join(output_dir, f"final_video_{i:04d}.flv")
    command = f'D:/ffmpeg/bin/ffmpeg -i "{camera_file}" -i "{screenshare_file}" -c copy -map 0:a:0 -map 1:v:0 -shortest -y "{output_file}"'
    
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    if result.returncode != 0:
        print(f"Error combining video {i}: {result.stderr.decode()}")
    else:
        print(f"Combined video saved at: {output_file}")

video_list_file = os.path.join(output_dir, "video_list.txt")
with open(video_list_file, 'w') as f:
    for i in range(len(camera_files)):
        f.write(f"file '{os.path.join(output_dir, f'final_video_{i:04d}.flv')}'\n")

final_command = f'D:/ffmpeg/bin/ffmpeg -safe 0 -y -f concat -i "{video_list_file}" -c copy "{os.path.join(output_dir, "final_combined_video.flv")}"'
final_result = subprocess.run(final_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

if final_result.returncode == 0:
    print(f"Final combined video saved at: {os.path.join(output_dir, 'final_combined_video.flv')}")
else:
    print(f"Error during final combination: {final_result.stderr.decode()}")
