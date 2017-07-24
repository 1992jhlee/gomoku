# -*- coding: utf-8 -*-

import xml.etree.ElementTree as etree
import numpy as np
import pickle
import random


xmldoc = etree.parse("renju_dataset_only_games_full.txt") # contains 48688 games
root = xmldoc.getroot()

## 하나의 게임에서
## 문자열로 된 move sequence를 숫자로 변환 후 저장
coords_table = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7, 'i':8, 'j':9, 'k':10, 'l':11, 'm':12, 'n':13, 'o':14}

input_features = []
labels = []
data_num = 48688

try:
    print("raw data processing...")
    for k in range(data_num):
        move_seq_in_num = []
        move_seq_in_char = root[0][k][0].text.split(" ")
        # 참고사항 : 항상 시작은 1이 아닌 0으로 통일함
        for index, coords in enumerate(move_seq_in_char):
            coord_x = coords_table[coords[0]]

            if len(coords) == 2:
                coord_y = int(coords[1])-1
            elif len(coords) == 3:
                coord_y = int(coords[1:3])-1

            move_seq_in_num.append([coord_x, coord_y])

        ## 15*15*3 input feature를 얻기 위한 작업
        gameBoard_B = np.zeros([15, 15], dtype=np.float32)
        gameBoard_W = np.zeros([15, 15], dtype=np.float32)
        gameBoard_E = np.ones([15, 15], dtype=np.float32)
        input_tensor = np.zeros([3, 15, 15], dtype=np.float32)

        labels_indices = []
        for i, move in enumerate(move_seq_in_num):
            if i == len(move_seq_in_num)-1:
                break
            if i%2 == 0:
                gameBoard_B[move[1]][move[0]] = 1
                gameBoard_E[move[1]][move[0]] = 0
                input_tensor[0] = gameBoard_B.copy()
                input_tensor[1] = gameBoard_W.copy()
                input_tensor[2] = gameBoard_E.copy()
                input_tensor = np.transpose(input_tensor, (1,2,0))
                input_features.append(input_tensor.copy())
                input_tensor = np.transpose(input_tensor, (2,1,0))
            else:
                gameBoard_W[move[1]][move[0]] = 1
                gameBoard_E[move[1]][move[0]] = 0
                input_tensor[0] = gameBoard_B.copy()
                input_tensor[1] = gameBoard_W.copy()
                input_tensor[2] = gameBoard_E.copy()
                input_tensor = np.transpose(input_tensor, (1,2,0))
                input_features.append(input_tensor.copy())
                input_tensor = np.transpose(input_tensor, (2,1,0))

            labels_indices.append(move_seq_in_num[i+1][0] + 15*move_seq_in_num[i+1][1])

        # make labels
        for labels_index in labels_indices:
            idx = labels_index
            label = np.zeros([225])
            label[idx] = 1
            labels.append(label)

        #print(k)
        #print(len(input_features))
        #print(len(labels))
        #print("\n")
except:
    print(k)

print("raw data processing...fisined\n")
# 여기까지 최종적으로 k개의 게임데이터에서 뽑아낸 (s, a)가 만들어지는데
# s는 input_features, a는 labels에 저장된다.
# s는 (15, 15, 3), a는 (1, 225)


# Divide into 3 sets(training set, validation set, test set)
print("creating training set...")
sample_index = list(range(len(input_features)))
random.shuffle(sample_index)
input_features = [input_features[k] for k in sample_index]
labels = [labels[k] for k in sample_index]


# 80% of total data -> training set
training_inputs = input_features[:int(0.8*len(input_features))]
training_labels = labels[:int(0.8*len(labels))]
# 10% of total data -> validation set
validation_inputs = input_features[int(0.8*len(input_features))+1:int(0.9*len(input_features))]
validation_labels = labels[int(0.8*len(labels))+1:int(0.9*len(labels))]
# 10% of total data -> test set
test_inputs = input_features[int(0.9*len(input_features))+1:]
test_labels = labels[int(0.9*len(labels))+1:]
print("creating training set...finished\n")


# Save data files
print("saving data files...")
with open('training_inputs.txt', 'wb') as f:
    pickle.dump(training_inputs, f)
with open('training_labels.txt', 'wb') as f:
    pickle.dump(training_labels, f)
with open('validation_inputs.txt', 'wb') as f:
    pickle.dump(validation_inputs, f)
with open('validation_labels.txt', 'wb') as f:
    pickle.dump(validation_labels, f)
with open('test_inputs.txt', 'wb') as f:
    pickle.dump(test_inputs, f)
with open('test_labels.txt', 'wb') as f:
    pickle.dump(test_labels, f)
print("saving data files...finished\n")

print("process finished!")
