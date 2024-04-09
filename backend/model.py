import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from matplotlib.image import imread
import cv2
import copy


# base image
kmeans_model = None


def fusion_kMeans(image, image_2, ext=".jpg",  clusters=10, alpha=0.01, beta=0.01, mf=5, compute=True):
    global kmeans_model
    mean_value = np.mean(image)
    variance_value = np.var(image)

    gaussian = np.random.normal(
        mean_value * alpha, variance_value * beta, image_2.shape)
    image_2 = image_2 + gaussian

    list_image = image.reshape(-1, 3)

    cv2.imwrite("backend/assets/fused_image"+ext, image_2)
    image_2 = cv2.medianBlur(cv2.imread("backend/assets/fused_image"+ext), mf)
    list_image_2 = (image_2).reshape(-1, 3)
    if (kmeans_model == None or compute):
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


def fusion_kMeans_V2(image, image_2, ext=".jpg",  clusters=10, enchant=0.8, mf=5, compute=True):
    global kmeans_model
    list_image = image.reshape(-1, 3)
    list_image_2 = copy.deepcopy(image_2.reshape(-1, 3))

    if (kmeans_model == None or compute):
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


# async def black_ecnhant(model, start=0, end=255, image, image_shift, mr, mg, mb):
#     for pixel in range(start, end + 1):
#         print("pixel", pixel)
#         f = max([image_shift, 1 - pixel/255])
#         value = [f * mr,
#                  f * mg,
#                  f * mb]
#         image[(image == [pixel, pixel, pixel]
#                ).any(axis=1)] = model.predict([value])
#     pass


# def fusion_kMeans_V3(image, image_2, ext=".jpg",  clusters=10, image_shift=0.3,  enchant=0.8, mf=5):

#     list_image = image.reshape(-1, 3)

#     list_image_2 = copy.deepcopy(image_2.reshape(-1, 3))
#     list_image_2 = list_image_2 + image_shift * list_image_2

#     mean_value_r = np.mean(image[:, :, 0])
#     mean_value_g = np.mean(image[:, :, 1])
#     mean_value_b = np.mean(image[:, :, 2])

#     print("fusion ongoing")
#     kmeans_model = KMeans(n_clusters=clusters, ).fit(list_image)
#     print("fusion_complete")

#     labels = kmeans_model.predict(list_image_2)

#     non_black_centers = kmeans_model.cluster_centers_[
#         (kmeans_model.cluster_centers_ != [0, 0, 0]).any(axis=1)]

#     list_image_2 = non_black_centers[labels]

#     for pixel in range(256):
#         print("pixel", pixel)
#         f = max([image_shift, 1 - pixel/255])
#         value = [f * mean_value_r,
#                  f * mean_value_g,
#                  f * mean_value_b]
#         list_image_2[(list_image_2 == [pixel, pixel, pixel]
#                       ).any(axis=1)] = kmeans_model.predict([value])

#     image_2_fused = list_image_2.reshape(image_2.shape)

#     # image_2 = image_2_fused - image_shift * image_2_fused  # this is negative shift

#     image_2 = enchant * image_2_fused + (1 - enchant) * image_2

#     image_2 = image_2.astype(dtype=int)

#     cv2.imwrite("backend/assets/fused_image"+ext, image_2[:, :, ::-1])
#     image_2 = cv2.medianBlur(cv2.imread("backend/assets/fused_image"+ext), mf)
#     cv2.imwrite("backend/assets/fused_image"+ext, image_2)
#     return image_2

def fusion_kMeans_V3(image, image_2, ext=".jpg",  clusters=10, image_shift=0.3,  enchant=0.8, mf=5, compute=True):
    global kmeans_model
    list_image = image.reshape(-1, 3)
    list_image_2 = copy.deepcopy(image_2.reshape(-1, 3))
    # list_image_2 = list_image_2 + image_shift * list_image_2
    mean_value_r = np.mean(image[:, :, 0])
    mean_value_g = np.mean(image[:, :, 1])
    mean_value_b = np.mean(image[:, :, 2])

    mean_value_r_2 = np.mean(image_2[:, :, 0])
    mean_value_g_2 = np.mean(image_2[:, :, 1])
    mean_value_b_2 = np.mean(image_2[:, :, 2])

    # here we are changing the image
    list_image[(list_image == [0, 0, 0]).any(axis=1)] = [
        image_shift * mean_value_r,  image_shift * mean_value_g, image_shift * mean_value_b]

    if (kmeans_model == None or compute):
        print("fusion ongoing")
        kmeans_model = KMeans(n_clusters=clusters, ).fit(list_image)
        print("fusion_complete")
    else:
        print("using")

    labels = kmeans_model.predict(list_image_2)
    list_image_2 = kmeans_model.cluster_centers_[labels]

    list_image_2 = list_image_2[labels]
    list_image_2[(list_image_2 == [0, 0, 0]).any(axis=1)] = kmeans_model.predict([[
        mean_value_r_2, mean_value_g_2, mean_value_b_2]])

    image_2_fused = list_image_2.reshape(image_2.shape)

    image_2 = enchant * image_2_fused + (1 - enchant) * image_2

    image_2 = image_2.astype(dtype=int)

    cv2.imwrite("backend/assets/fused_image"+ext, image_2[:, :, ::-1])
    image_2 = cv2.medianBlur(cv2.imread("backend/assets/fused_image"+ext), mf)
    cv2.imwrite("backend/assets/fused_image"+ext, image_2)
    return image_2
