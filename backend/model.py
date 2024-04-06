import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from matplotlib.image import imread
import cv2

# base image


def fusion_kMeans(image, image_2, ext=".jpg",  clusters=10, alpha=0.01, beta=0.01, mf=5):

    mean_value = np.mean(image)
    variance_value = np.var(image)

    gaussian = np.random.normal(
        mean_value * alpha, variance_value * beta, image_2.shape)

    list_image = image.reshape(-1, 3)
    list_image_2 = (gaussian + image_2).reshape(-1, 3)

    print("fusion ongoing")
    kmeans_model = KMeans(n_clusters=clusters, ).fit(list_image)
    print("fusion_complete")

    # creating a image blended image
    labels = kmeans_model.predict(list_image_2)
    list_image_2 = kmeans_model.cluster_centers_[labels]
    image_2 = list_image_2.reshape(image_2.shape)
    image_2 = image_2.astype(dtype=int)

    cv2.imwrite("backend/assets/fused_image"+ext, image_2)
    image_2 = cv2.medianBlur(cv2.imread("backend/assets/fused_image"+ext), mf)
    cv2.imwrite("backend/assets/fused_image"+ext, image_2)
    return image_2
