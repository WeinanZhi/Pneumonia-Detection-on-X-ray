import numpy as np
import pandas as pd
import cv2
import os
import tensorflow as tf


'''
The created dataset combine the original train and test set. All the images are converted into gray scale images and resized into 400*400 resolution 
for consistency. list X preserves the np.array type images and list Y preserves the corresponding labels(Y is for validation purpose). 
'''


def creatDataSet(categories, img_s1, img_s2):
    a = 0
    X, Y = [], []
    dirpath = "./chest_xray/"
    types = ['train', 'test']
    for t in types:
        traindir = os.path.join(dirpath, t)
        for cat in categories:
            Path = os.path.join(traindir, cat)
            class_num = categories.index(cat)
            for img in os.listdir(Path):
                image = os.path.join(Path, img)
                image = cv2.imread(image, cv2.IMREAD_ANYCOLOR)
                image = cv2.resize(image, (img_s1, img_s2))
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
                
                X.append(image)
                #X.append(cv2.flip(image, -1)) # 180 rotation
                Y.append(class_num)
                #Y.append(class_num)
                a += 1
    return X, Y


def one_hottie(labels, C):
    One_hot_matrix = tf.one_hot(labels, C)
    return tf.keras.backend.eval(One_hot_matrix)


def mk_dir(path):
    try: 
        os.mkdir(path)
    except OSError:
        print("Creation of the directory %s failed" % path)
    else:
        print("Successfully created the directory %s " % path)

def write_image(X, dir_path):
    # the output images are named after their corresponding index, starting from 0.
    for i in range(X.shape[0]):
        cv2.imwrite(os.path.join(dir_path, "{index}.jpeg".format(index=str(i))), X[i]*255.)
    np.savetxt('./labels.txt', Y.astype(int))

def main():
    '''
    After One-hot encoding, in Y, 1 means 'Pheumonia', 0 means 'Normal'.
    '''
    categories = os.listdir("./chest_xray/train")
    img_s1, img_s2 = 400, 400
    path = "./output"
    X, Y = creatDataSet(categories, img_s1, img_s2)
    gray_X = np.array(X)/255.
    Y = np.array(Y)
    Y = one_hottie(Y, 1)
    mk_dir(path)
    write_image(gray_X, path)

if __name__ == "__main__":
    main()
