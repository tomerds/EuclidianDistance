import csv
import numpy as np
from scipy import spatial

def open_file_into_matrix(filename):
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        images = list(csv_reader)

        # Remove the first line of feature labels  
        images.pop(0)
        # List of image labels
        labels = []

        for image in images:
            pop = image.pop(0)
            labels.append(pop)

        images_matrix = np.array(images, dtype=np.float)

        labelled_matrix = []
        i = 0
        for item in images_matrix:
            labelled_item = [labels[i], item]
            labelled_matrix.append(labelled_item)
            i += 1


        return labelled_matrix

def matrix_maker(batch_list):
    matrix_list = []
    # Opens the collection
    if len(batch_list) == 1:
        return open_file_into_matrix(batch_list[0])
    # Opens the list of batches
    else:
        for file_name in batch_list:
            matrix_list.append(open_file_into_matrix(file_name))
        return matrix_list

def sort_by_second_element(list_name):
   list_name.sort(key = lambda x: x[1]) 
   return list_name

def find_nearest_neighbours(batch_matrix_list, collection_matrix):
    results_list = []
    for batch in batch_matrix_list:
        list_holder = []
        for deformed_image in batch:
            ed_list = []
            for image in collection_matrix:
                euclidean_distance = spatial.distance.euclidean(deformed_image[1], image[1])
                ed_list.append([image[0], euclidean_distance])

            sorted_list = sort_by_second_element(ed_list)
            top_10_matches = sorted_list[:10]
            list_holder.append([deformed_image[0], top_10_matches])

        results_list.append(list_holder)
    
    return results_list

def precision_counter(results_list, precision):
    precision_count = 0

    for batch in results_list:
        for image in batch:
            image_name = image[0]
            image_list = image[1]
            
            for tup in image_list[:precision]:
                if image_name == tup[0]:
                    precision_count += 1
    
    return precision_count

                

def main():
    """ Main program """
    collection = '/Users/tomerdusautoy/Documents/ARTPI/verisartARTPI/collection.csv'
    src = '/Users/tomerdusautoy/Documents/ARTPI/verisartARTPI/'
    batch_1 = src + 'batch_1_greyscale_features.csv'
    batch_2 = src + 'batch_2_rotate_180_features.csv'
    batch_3 = src + 'batch_3_blur_features.csv'
    batch_4 = src + 'batch_4_cropped_features.csv'
    batch_5 = src + 'batch_5_pixelated_features.csv'
    
    batch_list = [batch_1, batch_2, batch_3, batch_4, batch_5]
    batch_matrix_list = matrix_maker(batch_list)

    collection_matrix = matrix_maker([collection])

    # print('Collection: \n', collection_matrix, '\n', 'Batches: \n', batch_matrix_list)

    # **************** Batch_matrix_list: ****************
    # [
    #   [
    # ['1171_0d5f3174_original.jpg', array([-1.51377730e+00,  1.29529667e+00, ...])],
    # ['1171_0d5f3175_original.jpg', array([-1.51377730e+00,  1.29529667e+00, ...])],
    # ['1171_0d5f3176_original.jpg', array([-1.51377730e+00,  1.29529667e+00, ...])], 
    #  ... ], 
    #   [
    # ['1171_0d5f3174_original.jpg', array([-1.51377730e+00,  1.29529667e+00, ...])],
    # ['1171_0d5f3175_original.jpg', array([-1.51377730e+00,  1.29529667e+00, ...])],
    # ['1171_0d5f3176_original.jpg', array([-1.51377730e+00,  1.29529667e+00, ...])], 
    # ... ], 
    # ... 
    # ]

    results_list = find_nearest_neighbours(batch_matrix_list, collection_matrix)

    # ****************** results_list: *******************
    # [
    #   [
    #       ['101_5099f488_original.jpg', 
    #           [['101_5099f488_original.jpg', 1.2232986988024588], ['23_a32caac1_original.jpg', 1.8789829367466802], ... ]
    #       ], 
    #       ['10_c09921e0_original.jpg', 
    #           [['625_aec615cf_original.jpg', 1.8934894116072365], ['10_c09921e0_original.jpg', 1.8961420090118877], ... ]
    #       ], 
    #       ... , 
    #       ... , 
    #       ...
    #   ],
    #   [... batch_2 ...],
    #   [... batch_3 ...],
    #   [... batch_4 ...],
    #   [... batch_5 ...]
    # ]

    precision_1_count = precision_counter(results_list, 1)
    precision_5_count = precision_counter(results_list, 5)
    precision_10_count = precision_counter(results_list, 10)

    print(precision_1_count, precision_5_count, precision_10_count)

    count = 0
    for batch in results_list:
        for image in batch:
            count += 1
    
    print(count)




if __name__ == "__main__":
    main()