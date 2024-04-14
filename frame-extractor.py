import argparse
import cv2
import os
import random
import sys

from tqdm import tqdm


def extract_frames(video_path, output_dir, num_frames, min_time=None, max_time=None):
    # Open the video file
    video = cv2.VideoCapture(video_path)

    # Get the total number of frames in the video
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    frames_per_second = video.get(cv2.CAP_PROP_FPS)

    # Calculate the minimum and maximum frame indices based on time
    if min_time is not None:
        min_frame_index = int(min_time * frames_per_second)
    else:
        min_frame_index = 0

    if max_time is not None:
        max_frame_index = int(max_time * frames_per_second)
    else:
        max_frame_index = total_frames

    # Generate random frame indices within the specified range
    frame_indices = random.sample(range(min_frame_index, max_frame_index), num_frames)

    # Extract and save the random frames
    for index in tqdm(frame_indices):
        # Set the frame index
        video.set(cv2.CAP_PROP_POS_FRAMES, index)

        # Read the frame
        ret, frame = video.read()

        # Save the frame as an image
        frame_path = os.path.join(output_dir, f"frame_{index}.jpg")
        cv2.imwrite(frame_path, frame)

    # Release the video file
    video.release()


if __name__ == '__main__':
    # Create the parser
    parser = argparse.ArgumentParser(description="Extract frames from a video")

    # Add the arguments
    parser.add_argument("video_path", type=str, help="The path to the video file")
    parser.add_argument("output_dir", type=str, help="The directory to save the frames")
    parser.add_argument("num_frames", type=int, help="The number of frames to extract")
    parser.add_argument("--min_time", type=str, help="The minimum time in HH:mm:ss format")
    parser.add_argument("--max_time", type=str, help="The maximum time in HH:mm:ss format")

    # Parse the arguments
    args = parser.parse_args()

    # Convert min_time and max_time to seconds
    min_time = None
    max_time = None
    if args.min_time:
        min_time_parts = args.min_time.split(':')
        min_time = int(min_time_parts[0]) * 3600 + int(min_time_parts[1]) * 60 + int(min_time_parts[2])
    if args.max_time:
        max_time_parts = args.max_time.split(':')
        max_time = int(max_time_parts[0]) * 3600 + int(max_time_parts[1]) * 60 + int(max_time_parts[2])

    # Call the extract_frames function with the command line arguments
    extract_frames(args.video_path, args.output_dir, args.num_frames, min_time, max_time)