import os
import argparse as ap

from picamera import PiCamera
from subprocess import check_output
from time import sleep

def init_camera():
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 30
    camera.awb_mode = 'cloudy' # auto-white balance, default: auto
    camera.exposure_mode = 'auto'
    camera.image_effect = 'colorbalance'

    camera.annotate_text = "Fredrik"
    camera.annotate_text_size = 32
    
    return camera

def record_video(camera, name):
    time_length = 1
    video_name = name + '.h264'
    converted_name = name + '.mp4'

    camera.start_recording(video_name)
    sleep(time_length)
    camera.stop_recording()

    str_args = ['MP4Box', '-fps', str(camera.framerate), '-add', video_name, converted_name]
    output = check_output(str_args)
    os.remove(video_name)

def capture_image(camera, name):
    sleep(2)
    file_name = name + '.jpg'
    camera.capture(file_name)

def parse_args():
    parser = ap.ArgumentParser(description='Raspberry Pi Camera capture script')
    parser.add_argument('--out_file', '-o', required=True, help='Output file name')
    parser.add_argument('--mode', '-m', default='rec', help='Capture mode (rec/img)')
    args = parser.parse_args()
    
    return args
    
if __name__ == "__main__":

    args = parse_args()
    
    camera = init_camera()

    camera.start_preview()
    if args.mode == 'rec':
        record_video(camera, args.out_file)
    elif args.mode == 'img':
        capture_image(camera, args.out_file)
    else:
        print 'Invalid capture mode!'
    camera.stop_preview()

