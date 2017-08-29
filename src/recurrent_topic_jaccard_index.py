#!/usr/bin/env python3

import os
import pandas as pd
import numpy as np
os.chdir('/Users/DarkWizard/PycharmProjects/3rd_Python/Window_LDA_Data')
import sqlite3


def dist_jaccard(str1, str2):
    str1 = set(str1.split())
    str2 = set(str2.split())
    return float(len(str1 & str2)) / len(str1 | str2)

def jaccard_score(list1, list2):
    total_lst = []
    for i in list1:
        another_lst = []
        for j in list2:
            score = dist_jaccard(i, j)
            if score > 0 and score != 1.0:
                another_lst.append(score)
                another_lst.append(i)
                another_lst.append(j)
        total_lst.append(another_lst)
    return total_lst

df_1_3 = pd.read_csv("1_3.csv", index_col=0)
df_2_4 = pd.read_csv("2_4.csv", index_col=0)
df_3_5 = pd.read_csv("3_5.csv", index_col=0)
df_4_6 = pd.read_csv("4_6.csv", index_col=0)
df_5_7 = pd.read_csv("5_7.csv", index_col=0)
df_6_8 = pd.read_csv("6_8.csv", index_col=0)
df_7_9 = pd.read_csv("7_9.csv", index_col=0)
df_8_10 = pd.read_csv("8_10.csv", index_col=0)
df_9_11 = pd.read_csv("9_11.csv", index_col=0)
df_10_12 = pd.read_csv("10_12.csv", index_col=0)
df_11_13 = pd.read_csv("11_13.csv", index_col=0)
df_12_14 = pd.read_csv("12_14.csv", index_col=0)
df_13_15 = pd.read_csv("13_15.csv", index_col=0)
df_14_16 = pd.read_csv("14_16.csv", index_col=0)
df_15_17 = pd.read_csv("15_17.csv", index_col=0)
df_16_18 = pd.read_csv("16_18.csv", index_col=0)
df_17_19 = pd.read_csv("17_19.csv", index_col=0)
df_18_20 = pd.read_csv("18_20.csv", index_col=0)
df_19_21 = pd.read_csv("19_21.csv", index_col=0)
df_20_22 = pd.read_csv("20_22.csv", index_col=0)
df_21_23 = pd.read_csv("21_23.csv", index_col=0)
df_22_24 = pd.read_csv("22_24.csv", index_col=0)
df_23_25 = pd.read_csv("23_25.csv", index_col=0)
df_24_26 = pd.read_csv("24_26.csv", index_col=0)
df_25_27 = pd.read_csv("25_27.csv", index_col=0)
df_26_28 = pd.read_csv("26_28.csv", index_col=0)
df_27_29 = pd.read_csv("27_29.csv", index_col=0)
df_28_30 = pd.read_csv("28_30.csv", index_col=0)
df_29_31 = pd.read_csv("29_31.csv", index_col=0)

df_1_3_lst = df_1_3.loc[-1].tolist()
df_2_4_lst = df_2_4.loc[-1].tolist()
df_3_5_lst = df_3_5.loc[-1].tolist()
df_4_6_lst = df_4_6.loc[-1].tolist()
df_5_7_lst = df_5_7.loc[-1].tolist()
df_6_8_lst = df_6_8.loc[-1].tolist()
df_7_9_lst = df_7_9.loc[-1].tolist()
df_8_10_lst = df_8_10.loc[-1].tolist()
df_9_11_lst = df_9_11.loc[-1].tolist()
df_10_12_lst = df_10_12.loc[-1].tolist()
df_11_13_lst = df_11_13.loc[-1].tolist()
df_12_14_lst = df_12_14.loc[-1].tolist()
df_13_15_lst = df_13_15.loc[-1].tolist()
df_14_16_lst = df_14_16.loc[-1].tolist()
df_15_17_lst = df_15_17.loc[-1].tolist()
df_16_18_lst = df_16_18.loc[-1].tolist()
df_17_19_lst = df_17_19.loc[-1].tolist()
df_18_20_lst = df_18_20.loc[-1].tolist()
df_19_21_lst = df_19_21.loc[-1].tolist()
df_20_22_lst = df_20_22.loc[-1].tolist()
df_21_23_lst = df_21_23.loc[-1].tolist()
df_22_24_lst = df_22_24.loc[-1].tolist()
df_23_25_lst = df_23_25.loc[-1].tolist()
df_24_26_lst = df_24_26.loc[-1].tolist()
df_25_27_lst = df_25_27.loc[-1].tolist()
df_26_28_lst = df_26_28.loc[-1].tolist()
df_27_29_lst = df_27_29.loc[-1].tolist()
df_28_30_lst = df_28_30.loc[-1].tolist()
df_29_31_lst = df_29_31.loc[-1].tolist()


all_lists = [df_1_3_lst, df_2_4_lst, df_3_5_lst, df_4_6_lst, df_5_7_lst, df_6_8_lst, df_7_9_lst, df_8_10_lst, df_9_11_lst,
            df_10_12_lst, df_11_13_lst, df_12_14_lst, df_13_15_lst, df_14_16_lst, df_15_17_lst, df_16_18_lst, df_17_19_lst,
            df_18_20_lst, df_19_21_lst, df_20_22_lst, df_21_23_lst, df_22_24_lst, df_23_25_lst, df_24_26_lst, df_25_27_lst,
            df_26_28_lst, df_27_29_lst, df_28_30_lst]

scores = []
for l1, l2 in zip(all_lists[:-1], all_lists[1:]): # or zip(all_lists, all_lists[1:])
    res = jaccard_score(l1, l2)
    scores.append(res)

def build_jaccard_matrix(score_lst):
    df = pd.DataFrame(np.concatenate(score_lst).reshape(-1, 3)[:, ::-1], columns=['A', 'B', 'Dist'])
    result = df.pivot('B', 'A', 'Dist').fillna(0)
    return result

index_matrix = []
for score in scores:
    res = build_jaccard_matrix(score)
    index_matrix.append(res)


cnx_matrix = sqlite3.connect("jaccard_matrix.db")
matrix_name = "jaccard_matrix"
count = 0
for i in index_matrix:
    i.to_sql("{}{}".format(matrix_name, count), cnx_matrix)
    count += 1