import os
from django.shortcuts import render, redirect
from .forms import PhotoForm
from .models import ImageModel
import cv2 as cv
import matplotlib.pyplot as plt

import base64
from io import BytesIO
from PIL import Image

import json
import numpy as np
from .paths import get_image_path
def get_sift_descriptors(image_path):
    print("Image Path:", image_path)
    image = cv.imread(image_path)
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    sift = cv.SIFT_create()
    keypoints, descriptors = sift.detectAndCompute(gray, None)
    return keypoints, descriptors

def get_all_image_descriptors(image_paths):
    image_descriptors = {}
    for img_path in image_paths:
        keypoints, descriptors = get_sift_descriptors(img_path)
        image_descriptors[img_path] = descriptors
    return image_descriptors

def calculate_similarity(descriptor1, descriptor2):
    # Calculate Euclidean distance between two descriptors
    return np.linalg.norm(descriptor1 - descriptor2)

def main(main_image_path, original_path=''):
    # Find the most similar image based on descriptors
    best_match = None
    best_distance = float('inf')
    
    image_paths = get_image_path(original_path)
    
    query_keypoints, query_descriptors = get_sift_descriptors(main_image_path)

    for img_path, descriptors in get_all_image_descriptors(image_paths).items():
        for descriptor in descriptors:
            distance = calculate_similarity(query_descriptors, descriptor)
            if distance < best_distance:
                best_distance = distance
                best_match = img_path

    return best_match, best_distance
        
def process_image(image_path):
    image = cv.imread(image_path)
    gray_scale = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    sift = cv.SIFT_create()
    
    keypoints, descriptors = sift.detectAndCompute(gray_scale, None)
    sift_image = cv.drawKeypoints(gray_scale, keypoints, None)
    keypoint_sizes = [kp.size for kp in keypoints]
    keypoint_angles = [kp.angle for kp in keypoints]
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.hist(keypoint_sizes, bins=20, color='blue', alpha=0.7)
    plt.title("Histogram of Keypoint Sizes")
    plt.xlabel("Size")
    plt.ylabel("Frequency")

    plt.subplot(1, 2, 2)
    plt.hist(keypoint_angles, bins=20, color='orange', alpha=0.7)
    plt.title("Histogram of Keypoint Angles")
    plt.xlabel("Angle (degrees)")
    plt.ylabel("Frequency")

    plot_file = os.path.join(os.path.dirname(image_path), 'histogram_plot.png')
    plt.savefig(plot_file)
    plt.close()
    
    return sift_image, plot_file, descriptors


def home_view(request):
    upload_success = False
    form = PhotoForm()
    return render(request, 'home.html', {'form': form, 'upload_success': upload_success})


def process_image_final(image_path, best_match):
    # Load images
    image1 = cv.imread(image_path)
    image2 = cv.imread(best_match)
    # Convert to grayscale image
    gray_scale1 = cv.cvtColor(image1, cv.COLOR_BGR2GRAY)
    gray_scale2 = cv.cvtColor(image2, cv.COLOR_BGR2GRAY)
    # Initialize SIFT object
    sift = cv.SIFT_create()
    keypoints1, des1 = sift.detectAndCompute(gray_scale1, None) 
    keypoints2, des2 = sift.detectAndCompute(gray_scale2, None)
    # Initialize Brute force matching
    bf = cv.BFMatcher(cv.NORM_L1, crossCheck=True)
    # Match the descriptors
    matches = bf.match(des1, des2)
    # Sort the matches
    matches = sorted(matches, key=lambda match: match.distance)
    # Draw all matches
    matched_image = cv.drawMatches(gray_scale1, keypoints1, gray_scale2, keypoints2, matches[:30], None)
    
    # Convert the image to base64
    _, buffer = cv.imencode('.png', matched_image)
    img_str = base64.b64encode(buffer).decode('utf-8')
    
    return img_str

def upload_image(request):
    upload_success = False
    form = PhotoForm(request.POST, request.FILES)
    url_path = 'http://127.0.0.1:8000/media/images/'
    if form.is_valid():
        photo = form.save()
        upload_success = True
        original_image_path = photo.image.path
        original_path = photo.image.path.rsplit('\\', 1)[0] + '\\'
        best_match_image_path, best_distance = main(original_image_path, original_path)
        processed_image = process_image_final(original_image_path, best_match_image_path)
        print("Best match:", best_match_image_path, "Distance:", best_distance)
        return render(request, 'upload_success.html', {
                        'upload_success': upload_success,
                        'best_distance': best_distance,
                        'original_image_path': url_path + original_image_path.rsplit('\\', 1)[-1],
                        'best_match_image_path': url_path + best_match_image_path.rsplit('\\', 1)[-1],
                        'processed_image': processed_image,
                        'best_image_id': best_match_image_path.rsplit('\\', 1)[-1].rsplit('.', 1)[0],
                       })
def upload_success(request):
    return render(request, 'upload_success.html')
