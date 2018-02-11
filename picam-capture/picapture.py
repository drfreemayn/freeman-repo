import os
import argparse as ap

from picamera import PiCamera
from subprocess import check_output
from time import sleep

def init_camera():
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 60
    camera.awb_mode = 'auto'
    camera.exposure_mode = 'auto'
    camera.image_effect = 'colorbalance'
    camera.vflip = True

    camera.annotate_text = "Fredrik"
    camera.annotate_text_size = 32

    return camera

def record_video(camera, name, length, img_size):
    video_name = name + '.h264'
    converted_name = name + '.mp4'

    camera.start_recording(video_name, resize=img_size)
    sleep(float(length))
    camera.stop_recording()

    if os.path.exists(converted_name):
        os.remove(converted_name)
    str_args = ['MP4Box', '-fps', str(camera.framerate), '-add', video_name, converted_name]
    output = check_output(str_args)
    os.remove(video_name)

def capture_image(camera, name, img_size):
    file_name = name + '.jpg'
    camera.capture(file_name, resize=img_size)

def capture_timelapse(camera, name, length, interval):
    if not os.path.exists(name):
        os.mkdir(name)
    file_paths = os.path.join(name, name + '-{timestamp:%Y-%m-%d-%H-%M-%S}' + '.jpg')
    time_elapsed = 0
    frame_interval = float(interval)
    for filename in camera.capture_continuous(file_paths):
        if not time_elapsed >= float(length):
            print('Captured %s' % filename)
            sleep(frame_interval)
            time_elapsed += frame_interval
        else:
            break

def parse_args():
    parser = ap.ArgumentParser(description='Raspberry Pi Camera capture script')
    parser.add_argument('--out_file', '-o', required=True, help='Output file name')
    parser.add_argument('--mode', '-m', required=True, choices=['rec', 'img', 'timelapse'],
                                          default='rec', help='Capture mode (rec/img)')
    parser.add_argument('--length', '-l', default=5, help='Time in seconds')
    parser.add_argument('--interval', '-i', default=5, help='Time in seconds')
    parser.add_argument('--no-preview', dest='preview', action='store_false')
    args = parser.parse_args()
    
    return args
    
if __name__ == "__main__":
    args = parse_args()

    img_size = (640, 480)

    camera = init_camera()
    if args.preview:
        camera.start_preview()
        # Wait for the automatic gain control to settle
        #sleep(2)
    if args.mode == 'rec':
        record_video(camera, args.out_file, args.length, img_size)
    elif args.mode == 'img':
        capture_image(camera, args.out_file, img_size)
    elif args.mode == 'timelapse':
        capture_timelapse(camera, args.out_file, args.length, args.interval)
    else:
        print 'Invalid capture mode!'
    if args.preview:
        camera.stop_preview()

