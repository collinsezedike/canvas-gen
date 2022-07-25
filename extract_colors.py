from sklearn.cluster import KMeans
import cv2
from collections import Counter


def extract_colors(img_file, num_colors=10):
    def RGB2HEX(color):
        return f"#{int(color[0]):02x}{int(color[1]):02x}{int(color[2]):02x}"

    image = cv2.imread(img_file)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img_width = image.shape[0]
    img_height = image.shape[1]

    reshaped_image = cv2.resize(image, (img_width // 10, img_height // 10))
    reshaped_image = reshaped_image.reshape(
        reshaped_image.shape[0] * reshaped_image.shape[1], 3
    )

    clf = KMeans(n_clusters=num_colors)
    labels = clf.fit_predict(reshaped_image)
    counts = Counter(labels)
    counts = dict(sorted(counts.items()))
    center_colors = clf.cluster_centers_
    ordered_colors = [center_colors[i] for i in counts.keys()]
    hex_colors = [RGB2HEX(ordered_colors[i]) for i in counts.keys()]
    return hex_colors
