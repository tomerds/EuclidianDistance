import csv
import numpy as np
from scipy import spatial

def open_file_into_matrix(filename):
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        images = list(csv_reader)
        images.pop(0)
        for image in images:
            image.pop(0)

        images_matrix = np.array(images[1:], dtype=np.float)
        return images_matrix

def matrix_maker(batch_list):
    matrix_list = []
    if len(batch_list) == 1:
        return open_file_into_matrix(batch_list[0])
    else:
        for file_name in batch_list:
            matrix_list.append(open_file_into_matrix(file_name))
        return matrix_list


def main():
    """ Main program """
    collection = '/Users/tomerdusautoy/Documents/ARTPI/verisartARTPI/collection.csv'
    src = '/Users/tomerdusautoy/Documents/ARTPI/verisartARTPI/'
    batch_1 = src + 'batch_1_greyscale_features.csv'
    batch_2 = src + 'batch_2_rotate_180_features.csv'
    batch_3 = src + 'batch_3_blur_features.csv'
    batch_4 = src + 'batch_4_cropped_features.csv'
    batch_5 = src + 'batch_5_pixelated_features.csv'
    # Code goes over here.
    
    batch_list = [batch_1, batch_2, batch_3, batch_4, batch_5]
    batch_matrix_list = matrix_maker(batch_list)

    collection_matrix = matrix_maker([collection])

    print('Collection: \n', collection_matrix, '\n', 'Batches: \n', batch_matrix_list)

    for batch in batch_matrix_list:
        for deformed_image in batch:
            for image in collection_matrix:
                euclidian_distance = spatial.distance.euclidian(deformed_image, image)
                


if __name__ == "__main__":
    main()