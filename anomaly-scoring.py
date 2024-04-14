from collections import defaultdict
from dataclasses import dataclass
import os
import re
from typing import List
from PIL import Image
import argparse
import yaml

def count_white_pixels(image_path):
    image = Image.open(image_path)
    pixels = image.load()
    width, height = image.size
    count = 0

    for x in range(width):
        for y in range(height):
            if pixels[x, y] == 255:
                count += 1

    return count


@dataclass
class FindQuery:
    filename: str
    find_least_whitest: bool


@dataclass
class FindQueryCounter:
    paths: List[str]
    counts: List[int]


@dataclass
class Config:
    queries: List[FindQuery]


def find_whitest_images(directory: str, queries: List[FindQuery]):
    queries_map = { query.filename: query for query in queries }
    queries_filenames = queries_map.keys()

    counters = { query.filename: FindQueryCounter(paths=list(), counts=list()) for query in queries }

    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename in queries_filenames:
                counter = counters[filename]
                whitest_image_paths = counter.paths
                whitest_image_counts = counter.counts
                image_path = os.path.join(root, filename)
                white_pixel_count = count_white_pixels(image_path)
                # if len(whitest_image_paths) < 10:
                whitest_image_paths.append(image_path)
                whitest_image_counts.append(white_pixel_count)
                #else:
                #    if queries_map[filename].find_least_whitest:
                #        max_count_index = whitest_image_counts.index(max(whitest_image_counts))
                #        if white_pixel_count < whitest_image_counts[max_count_index]:
                #            whitest_image_paths[max_count_index] = image_path
                #            whitest_image_counts[max_count_index] = white_pixel_count
                #            # whitest_image_paths.sort(key=lambda x: whitest_image_counts[whitest_image_paths.index(x)])
                #            # whitest_image_counts.sort()
                #    else:
                #        min_count_index = whitest_image_counts.index(min(whitest_image_counts))
                #        if white_pixel_count > whitest_image_counts[min_count_index]:
                #            whitest_image_paths[min_count_index] = image_path
                #            whitest_image_counts[min_count_index] = white_pixel_count
                #            # whitest_image_paths.sort(key=lambda x: whitest_image_counts[whitest_image_paths.index(x)], reverse=True)
                #            # whitest_image_counts.sort(reverse=True)
    return counters


def read_config(file_path):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    output = Config(queries=[FindQuery(query['filename'], query['find_least_whitest']) for query in config['queries']])
    return output


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", help="Path to the directory containing images")
    args = parser.parse_args()

    config = read_config('config.yaml')
    queries = config.queries

    directory = args.directory

    counters = find_whitest_images(directory, queries)
    leaderboard = defaultdict(lambda: [0, list()])
    for query in queries:
        counter = counters[query.filename]
        print(f"Query: {query.filename}")
        results = [(c, p) for p, c in zip(counter.paths, counter.counts)]
        results.sort(reverse=not query.find_least_whitest)
        for i, (count, path) in enumerate(results):
            print(f"Image {i + 1}: {path}, White Pixel Count: {count}")
            run_name = re.findall(r'output\d+/', path)[0]
            leaderboard[run_name][0] += 11 - i
            leaderboard[run_name][1].append(i)

    leaderboard_list = list(leaderboard.keys())
    leaderboard_list.sort(key=lambda x: leaderboard[x][0], reverse=True)
    print("Leaderboard")
    for run_name in leaderboard_list:
        print(run_name, leaderboard[run_name], sep='\t')
        if max(leaderboard[run_name][1]) <= 90:
            print("!!!")