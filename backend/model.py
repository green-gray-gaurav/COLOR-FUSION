import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from matplotlib.image import imread
import cv2
import copy

# base image


def fusion_kMeans(image, image_2, ext=".jpg",  clusters=10, alpha=0.01, beta=0.01, mf=5):

    mean_value = np.mean(image)
    variance_value = np.var(image)

    gaussian = np.random.normal(
        mean_value * alpha, variance_value * beta, image_2.shape)
    image_2 = image_2 + gaussian

    list_image = image.reshape(-1, 3)

    cv2.imwrite("backend/assets/fused_image"+ext, image_2)
    image_2 = cv2.medianBlur(cv2.imread("backend/assets/fused_image"+ext), mf)
    list_image_2 = (image_2).reshape(-1, 3)
    print("fusion ongoing")
    kmeans_model = KMeans(n_clusters=clusters, ).fit(list_image)
    print("fusion_complete")

    # creating a image blended image
    labels = kmeans_model.predict(list_image_2)
    list_image_2 = kmeans_model.cluster_centers_[labels]
    image_2 = list_image_2.reshape(image_2.shape)
    image_2 = image_2.astype(dtype=int)
    cv2.imwrite("backend/assets/fused_image"+ext, image_2[:, :, ::-1])

    return image_2[:, :, ::-1]


def fusion_kMeans_V2(image, image_2, ext=".jpg",  clusters=10, enchant=0.8, mf=5):

    list_image = image.reshape(-1, 3)
    list_image_2 = copy.deepcopy(image_2.reshape(-1, 3))

    print("fusion ongoing")
    kmeans_model = KMeans(n_clusters=clusters, ).fit(list_image)
    print("fusion_complete")
    # creating a image blended image
    labels = kmeans_model.predict(list_image_2)
    list_image_2 = kmeans_model.cluster_centers_[labels]

    image_2 = enchant * list_image_2.reshape(image_2.shape) + (
        1 - enchant) * image_2
    image_2 = image_2.astype(dtype=int)

    cv2.imwrite("backend/assets/fused_image"+ext, image_2[:, :, ::-1])
    image_2 = cv2.medianBlur(cv2.imread("backend/assets/fused_image"+ext), mf)
    cv2.imwrite("backend/assets/fused_image"+ext, image_2)
    return image_2


def fusion_kMeans_V3(image, image_2, ext=".jpg",  clusters=10, image_shift=0.3,  enchant=0.8, mf=5):

    list_image = image.reshape(-1, 3)

    list_image_2 = copy.deepcopy(image_2.reshape(-1, 3))
    list_image_2 = list_image_2 + image_shift * list_image_2

    mean_value_r = np.mean(image[:, :, 0])
    

    mean_value_g = np.mean(image[:, :, 1])
   

    mean_value_b = np.mean(image[:, :, 2])
  

    print("fusion ongoing")
    kmeans_model = KMeans(n_clusters=clusters, ).fit(list_image)
    print("fusion_complete")

    # creating a image blended image
    for pixel in range(256):
        f = max([image_shift, 1 - pixel/255])
        value = [f * mean_value_r,
                 f * mean_value_g,
                 f * mean_value_b]
        list_image_2[(list_image_2 == [pixel, pixel, pixel]
                      ).any(axis=1)] = value

    labels = kmeans_model.predict(list_image_2)

    non_black_centers = kmeans_model.cluster_centers_[
        (kmeans_model.cluster_centers_ != [0, 0, 0]).any(axis=1)]

  
    list_image_2 = non_black_centers[labels]
 

    image_2_fused = list_image_2.reshape(image_2.shape)

    image_2 = image_2_fused - image_shift * image_2_fused  # this is negative shift

    # image_2 = enchant * image_2_fused + (1 - enchant) * image_2

    image_2 = image_2.astype(dtype=int)

    cv2.imwrite("backend/assets/fused_image"+ext, image_2[:, :, ::-1])
    image_2 = cv2.medianBlur(cv2.imread("backend/assets/fused_image"+ext), mf)
    cv2.imwrite("backend/assets/fused_image"+ext, image_2)
    return image_2
