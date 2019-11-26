# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 11:01:49 2019

@author: andrebmo
"""

# =============================== DATA ===============================


# ---------------------------- Installations ----------------------------

#InstNames = ['TRO', 'TRB', 'TRC', 'CPR', 'SEN', 'SDO', 'SEQ', 'OSE', 'OSB', 'OSC', 'OSO', 'SSC', 'OSS', 'DSD', 'KVB', 'VMO', 'WEL', 'VFB', 'WEP', 'HUL', 'STA', 'STB', 'STC', 'GFA', 'GFB', 'GFC', 'SOD']

#         ____________________________________
#        | Installations settings:            |
#        |------------------------------------|
#        | 0 - Clustering of installations    |
#        | 1 - Evenly spread of installations |
#         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Insts = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]

#Insts_sequence_1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]
#Insts_sequence_2 = [0, 1, 24, 8, 18, 3, 21, 14, 27, 20, 4, 15, 2, 13, 25, 22, 10, 6, 23, 11, 5, 26, 7, 9, 12, 16, 17, 19]


Distance =  [[[0.00, 43.47, 47.25, 43.76, 44.47, 44.65, 43.21, 41.73, 71.65, 71.65, 70.54, 64.49, 64.49, 75.08, 89.05, 76.84, 81.18, 81.18, 64.88, 71.58, 71.58, 97.52, 97.69, 96.75, 87.12, 86.97, 85.01, 37.67], 
              [43.47, 0.00, 10.14, 14.85, 6.83, 19.08, 12.96, 15.09, 28.27, 28.27, 28.11, 23.53, 23.53, 31.64, 46.71, 44.07, 47.01, 47.01, 25.81, 33.86, 33.86, 65.74, 64.90, 65.90, 55.13, 55.70, 54.09, 15.85], 
              [47.25, 10.14, 0.00, 7.23, 3.70, 11.07, 5.96, 8.76, 26.56, 26.56, 23.78, 17.26, 17.26, 31.44, 48.84, 34.32, 37.58, 37.58, 17.91, 25.37, 25.37, 56.04, 55.36, 56.08, 45.38, 45.86, 44.19, 11.98], 
              [43.76, 14.85, 7.23, 0.00, 8.42, 4.25, 1.90, 2.13, 33.24, 33.24, 29.62, 22.43, 22.43, 38.37, 56.00, 34.04, 37.99, 37.99, 21.65, 27.85, 27.85, 55.52, 55.24, 55.20, 44.86, 45.04, 43.21, 6.26], 
              [44.47, 6.83, 3.70, 8.42, 0.00, 12.65, 6.62, 9.18, 28.05, 28.05, 26.12, 20.13, 20.13, 32.47, 49.18, 38.02, 41.27, 41.27, 21.27, 28.91, 28.91, 59.74, 59.06, 59.76, 49.07, 49.54, 47.86, 11.26], 
              [44.65, 19.08, 11.07, 4.25, 12.65, 0.00, 6.12, 4.46, 36.01, 36.01, 31.73, 24.25, 24.25, 41.40, 59.35, 32.27, 36.53, 36.53, 22.62, 27.84, 27.84, 53.38, 53.31, 52.86, 42.80, 42.83, 40.93, 7.36], 
              [43.21, 12.96, 5.96, 1.90, 6.62, 6.12, 0.00, 2.81, 32.39, 32.39, 29.15, 22.16, 22.16, 37.37, 54.78, 35.24, 39.06, 39.06, 21.80, 28.39, 28.39, 56.82, 56.46, 56.56, 46.14, 46.38, 44.57, 6.32], 
              [41.73, 15.09, 8.76, 2.13, 9.18, 4.46, 2.81, 0.00, 35.11, 35.11, 31.66, 24.52, 24.52, 40.15, 57.59, 35.78, 39.82, 39.82, 23.78, 29.93, 29.93, 57.16, 56.95, 56.76, 46.52, 46.65, 44.79, 4.14], 
              [71.65, 28.27, 26.56, 33.24, 28.05, 36.01, 32.39, 35.11, 0.00, 0.00, 7.36, 13.61, 13.61, 6.07, 24.69, 36.68, 36.48, 36.48, 18.15, 22.79, 22.79, 54.28, 52.24, 55.61, 45.50, 46.92, 46.17, 38.54], 
              [71.65, 28.27, 26.56, 33.24, 28.05, 36.01, 32.39, 35.11, 0.00, 0.00, 7.36, 13.61, 13.61, 6.07, 24.69, 36.68, 36.48, 36.48, 18.15, 22.79, 22.79, 54.28, 52.24, 55.61, 45.50, 46.92, 46.17, 38.54], 
              [70.54, 28.11, 23.78, 29.62, 26.12, 31.73, 29.15, 31.66, 7.36, 7.36, 0.00, 7.64, 7.64, 13.23, 31.52, 29.33, 29.29, 29.29, 11.38, 15.43, 15.43, 47.41, 45.51, 48.62, 38.35, 39.72, 38.90, 35.46], 
              [64.49, 23.53, 17.26, 22.43, 20.13, 24.25, 22.16, 24.52, 13.61, 13.61, 7.64, 0.00, 0.00, 19.67, 38.31, 25.54, 26.75, 26.75, 4.95, 12.20, 12.20, 45.65, 44.18, 46.45, 35.74, 36.83, 35.69, 28.46], 
              [64.49, 23.53, 17.26, 22.43, 20.13, 24.25, 22.16, 24.52, 13.61, 13.61, 7.64, 0.00, 0.00, 19.67, 38.31, 25.54, 26.75, 26.75, 4.95, 12.20, 12.20, 45.65, 44.18, 46.45, 35.74, 36.83, 35.69, 28.46], 
              [75.08, 31.64, 31.44, 38.37, 32.47, 41.40, 37.37, 40.15, 6.07, 6.07, 13.23, 19.67, 19.67, 0.00, 18.65, 42.33, 41.81, 41.81, 24.22, 28.54, 28.54, 59.09, 56.90, 60.58, 50.73, 52.22, 51.58, 43.35], 
              [89.05, 46.71, 48.84, 56.00, 49.18, 59.35, 54.78, 57.59, 24.69, 24.69, 31.52, 38.31, 38.31, 18.65, 0.00, 59.62, 58.32, 58.32, 42.77, 46.27, 46.27, 73.96, 71.41, 75.82, 66.83, 68.48, 68.13, 60.40], 
              [76.84, 44.07, 34.32, 34.04, 38.02, 32.27, 35.24, 35.78, 36.68, 36.68, 29.33, 25.54, 25.54, 42.33, 59.62, 0.00, 4.99, 4.99, 20.82, 13.93, 13.93, 21.73, 21.22, 21.84, 11.06, 11.69, 10.27, 39.52], 
              [81.18, 47.01, 37.58, 37.99, 41.27, 36.53, 39.06, 39.82, 36.48, 36.48, 29.29, 26.75, 26.75, 41.81, 58.32, 4.99, 0.00, 0.00, 22.41, 14.57, 14.57, 19.00, 17.89, 19.71, 9.09, 10.44, 9.83, 43.68], 
              [81.18, 47.01, 37.58, 37.99, 41.27, 36.53, 39.06, 39.82, 36.48, 36.48, 29.29, 26.75, 26.75, 41.81, 58.32, 4.99, 0.00, 0.00, 22.41, 14.57, 14.57, 19.00, 17.89, 19.71, 9.09, 10.44, 9.83, 43.68], 
              [64.88, 25.81, 17.91, 21.65, 21.27, 22.62, 21.80, 23.78, 18.15, 18.15, 11.38, 4.95, 4.95, 24.22, 42.77, 20.82, 22.41, 22.41, 0.00, 8.19, 8.19, 41.41, 40.12, 42.06, 31.27, 32.27, 31.04, 27.89], 
              [71.58, 33.86, 25.37, 27.85, 28.91, 27.84, 28.39, 29.93, 22.79, 22.79, 15.43, 12.20, 12.20, 28.54, 46.27, 13.93, 14.57, 14.57, 8.19, 0.00, 0.00, 33.45, 32.03, 34.27, 23.60, 24.78, 23.76, 34.06], 
              [71.58, 33.86, 25.37, 27.85, 28.91, 27.84, 28.39, 29.93, 22.79, 22.79, 15.43, 12.20, 12.20, 28.54, 46.27, 13.93, 14.57, 14.57, 8.19, 0.00, 0.00, 33.45, 32.03, 34.27, 23.60, 24.78, 23.76, 34.06], 
              [97.52, 65.74, 56.04, 55.52, 59.74, 53.38, 56.82, 57.16, 54.28, 54.28, 47.41, 45.65, 45.65, 59.09, 73.96, 21.73, 19.00, 19.00, 41.41, 33.45, 33.45, 0.00, 3.13, 2.80, 10.69, 10.56, 12.52, 60.72], 
              [97.69, 64.90, 55.36, 55.24, 59.06, 53.31, 56.46, 56.95, 52.24, 52.24, 45.51, 44.18, 44.18, 56.90, 71.41, 21.22, 17.89, 17.89, 40.12, 32.03, 32.03, 3.13, 0.00, 5.88, 10.58, 11.00, 13.03, 60.62], 
              [96.75, 65.90, 56.08, 55.20, 59.76, 52.86, 56.56, 56.76, 55.61, 55.61, 48.62, 46.45, 46.45, 60.58, 75.82, 21.84, 19.71, 19.71, 42.06, 34.27, 34.27, 2.80, 5.88, 0.00, 10.84, 10.22, 11.99, 60.22], 
              [87.12, 55.13, 45.38, 44.86, 49.07, 42.80, 46.14, 46.52, 45.50, 45.50, 38.35, 35.74, 35.74, 50.73, 66.83, 11.06, 9.09, 9.09, 31.27, 23.60, 23.60, 10.69, 10.58, 10.84, 0.00, 1.89, 3.17, 50.13], 
              [86.97, 55.70, 45.86, 45.04, 49.54, 42.83, 46.38, 46.65, 46.92, 46.92, 39.72, 36.83, 36.83, 52.22, 68.48, 11.69, 10.44, 10.44, 32.27, 24.78, 24.78, 10.56, 11.00, 10.22, 1.89, 0.00, 2.03, 50.18], 
              [85.01, 54.09, 44.19, 43.21, 47.86, 40.93, 44.57, 44.79, 46.17, 46.17, 38.90, 35.69, 35.69, 51.58, 68.13, 10.27, 9.83, 9.83, 31.04, 23.76, 23.76, 12.52, 13.03, 11.99, 3.17, 2.03, 0.00, 48.28], 
              [37.67, 15.85, 11.98, 6.26, 11.26, 7.36, 6.32, 4.14, 38.54, 38.54, 35.46, 28.46, 28.46, 43.35, 60.40, 39.52, 43.68, 43.68, 27.89, 34.06, 34.06, 60.72, 60.62, 60.22, 50.13, 50.18, 48.28, 0.00]], 

             [[0.00, 43.47, 87.12, 71.65, 64.88, 43.76, 97.52, 89.05, 37.67, 71.58, 44.47, 76.84, 47.25, 75.08, 86.97, 97.69, 70.54, 43.21, 96.75, 64.49, 44.65, 85.01, 41.73, 71.65, 64.49, 81.18, 81.18, 71.58], 
              [43.47, 0.00, 55.13, 28.27, 25.81, 14.85, 65.74, 46.71, 15.85, 33.86, 6.83, 44.07, 10.14, 31.64, 55.70, 64.90, 28.11, 12.96, 65.90, 23.53, 19.08, 54.09, 15.09, 28.27, 23.53, 47.01, 47.01, 33.86], 
              [87.12, 55.13, 0.00, 45.50, 31.27, 44.86, 10.69, 66.83, 50.13, 23.60, 49.07, 11.06, 45.38, 50.73, 1.89, 10.58, 38.35, 46.14, 10.84, 35.74, 42.80, 3.17, 46.52, 45.50, 35.74, 9.09, 9.09, 23.60], 
              [71.65, 28.27, 45.50, 0.00, 18.15, 33.24, 54.28, 24.69, 38.54, 22.79, 28.05, 36.68, 26.56, 6.07, 46.92, 52.24, 7.36, 32.39, 55.61, 13.61, 36.01, 46.17, 35.11, 0.00, 13.61, 36.48, 36.48, 22.79], 
              [64.88, 25.81, 31.27, 18.15, 0.00, 21.65, 41.41, 42.77, 27.89, 8.19, 21.27, 20.82, 17.91, 24.22, 32.27, 40.12, 11.38, 21.80, 42.06, 4.95, 22.62, 31.04, 23.78, 18.15, 4.95, 22.41, 22.41, 8.19], 
              [43.76, 14.85, 44.86, 33.24, 21.65, 0.00, 55.52, 56.00, 6.26, 27.85, 8.42, 34.04, 7.23, 38.37, 45.04, 55.24, 29.62, 1.90, 55.20, 22.43, 4.25, 43.21, 2.13, 33.24, 22.43, 37.99, 37.99, 27.85], 
              [97.52, 65.74, 10.69, 54.28, 41.41, 55.52, 0.00, 73.96, 60.72, 33.45, 59.74, 21.73, 56.04, 59.09, 10.56, 3.13, 47.41, 56.82, 2.80, 45.65, 53.38, 12.52, 57.16, 54.28, 45.65, 19.00, 19.00, 33.45], 
              [89.05, 46.71, 66.83, 24.69, 42.77, 56.00, 73.96, 0.00, 60.40, 46.27, 49.18, 59.62, 48.84, 18.65, 68.48, 71.41, 31.52, 54.78, 75.82, 38.31, 59.35, 68.13, 57.59, 24.69, 38.31, 58.32, 58.32, 46.27], 
              [37.67, 15.85, 50.13, 38.54, 27.89, 6.26, 60.72, 60.40, 0.00, 34.06, 11.26, 39.52, 11.98, 43.35, 50.18, 60.62, 35.46, 6.32, 60.22, 28.46, 7.36, 48.28, 4.14, 38.54, 28.46, 43.68, 43.68, 34.06], 
              [71.58, 33.86, 23.60, 22.79, 8.19, 27.85, 33.45, 46.27, 34.06, 0.00, 28.91, 13.93, 25.37, 28.54, 24.78, 32.03, 15.43, 28.39, 34.27, 12.20, 27.84, 23.76, 29.93, 22.79, 12.20, 14.57, 14.57, 0.00], 
              [44.47, 6.83, 49.07, 28.05, 21.27, 8.42, 59.74, 49.18, 11.26, 28.91, 0.00, 38.02, 3.70, 32.47, 49.54, 59.06, 26.12, 6.62, 59.76, 20.13, 12.65, 47.86, 9.18, 28.05, 20.13, 41.27, 41.27, 28.91], 
              [76.84, 44.07, 11.06, 36.68, 20.82, 34.04, 21.73, 59.62, 39.52, 13.93, 38.02, 0.00, 34.32, 42.33, 11.69, 21.22, 29.33, 35.24, 21.84, 25.54, 32.27, 10.27, 35.78, 36.68, 25.54, 4.99, 4.99, 13.93], 
              [47.25, 10.14, 45.38, 26.56, 17.91, 7.23, 56.04, 48.84, 11.98, 25.37, 3.70, 34.32, 0.00, 31.44, 45.86, 55.36, 23.78, 5.96, 56.08, 17.26, 11.07, 44.19, 8.76, 26.56, 17.26, 37.58, 37.58, 25.37], 
              [75.08, 31.64, 50.73, 6.07, 24.22, 38.37, 59.09, 18.65, 43.35, 28.54, 32.47, 42.33, 31.44, 0.00, 52.22, 56.90, 13.23, 37.37, 60.58, 19.67, 41.40, 51.58, 40.15, 6.07, 19.67, 41.81, 41.81, 28.54], 
              [86.97, 55.70, 1.89, 46.92, 32.27, 45.04, 10.56, 68.48, 50.18, 24.78, 49.54, 11.69, 45.86, 52.22, 0.00, 11.00, 39.72, 46.38, 10.22, 36.83, 42.83, 2.03, 46.65, 46.92, 36.83, 10.44, 10.44, 24.78], 
              [97.69, 64.90, 10.58, 52.24, 40.12, 55.24, 3.13, 71.41, 60.62, 32.03, 59.06, 21.22, 55.36, 56.90, 11.00, 0.00, 45.51, 56.46, 5.88, 44.18, 53.31, 13.03, 56.95, 52.24, 44.18, 17.89, 17.89, 32.03], 
              [70.54, 28.11, 38.35, 7.36, 11.38, 29.62, 47.41, 31.52, 35.46, 15.43, 26.12, 29.33, 23.78, 13.23, 39.72, 45.51, 0.00, 29.15, 48.62, 7.64, 31.73, 38.90, 31.66, 7.36, 7.64, 29.29, 29.29, 15.43], 
              [43.21, 12.96, 46.14, 32.39, 21.80, 1.90, 56.82, 54.78, 6.32, 28.39, 6.62, 35.24, 5.96, 37.37, 46.38, 56.46, 29.15, 0.00, 56.56, 22.16, 6.12, 44.57, 2.81, 32.39, 22.16, 39.06, 39.06, 28.39], 
              [96.75, 65.90, 10.84, 55.61, 42.06, 55.20, 2.80, 75.82, 60.22, 34.27, 59.76, 21.84, 56.08, 60.58, 10.22, 5.88, 48.62, 56.56, 0.00, 46.45, 52.86, 11.99, 56.76, 55.61, 46.45, 19.71, 19.71, 34.27], 
              [64.49, 23.53, 35.74, 13.61, 4.95, 22.43, 45.65, 38.31, 28.46, 12.20, 20.13, 25.54, 17.26, 19.67, 36.83, 44.18, 7.64, 22.16, 46.45, 0.00, 24.25, 35.69, 24.52, 13.61, 0.00, 26.75, 26.75, 12.20], 
              [44.65, 19.08, 42.80, 36.01, 22.62, 4.25, 53.38, 59.35, 7.36, 27.84, 12.65, 32.27, 11.07, 41.40, 42.83, 53.31, 31.73, 6.12, 52.86, 24.25, 0.00, 40.93, 4.46, 36.01, 24.25, 36.53, 36.53, 27.84], 
              [85.01, 54.09, 3.17, 46.17, 31.04, 43.21, 12.52, 68.13, 48.28, 23.76, 47.86, 10.27, 44.19, 51.58, 2.03, 13.03, 38.90, 44.57, 11.99, 35.69, 40.93, 0.00, 44.79, 46.17, 35.69, 9.83, 9.83, 23.76], 
              [41.73, 15.09, 46.52, 35.11, 23.78, 2.13, 57.16, 57.59, 4.14, 29.93, 9.18, 35.78, 8.76, 40.15, 46.65, 56.95, 31.66, 2.81, 56.76, 24.52, 4.46, 44.79, 0.00, 35.11, 24.52, 39.82, 39.82, 29.93], 
              [71.65, 28.27, 45.50, 0.00, 18.15, 33.24, 54.28, 24.69, 38.54, 22.79, 28.05, 36.68, 26.56, 6.07, 46.92, 52.24, 7.36, 32.39, 55.61, 13.61, 36.01, 46.17, 35.11, 0.00, 13.61, 36.48, 36.48, 22.79], 
              [64.49, 23.53, 35.74, 13.61, 4.95, 22.43, 45.65, 38.31, 28.46, 12.20, 20.13, 25.54, 17.26, 19.67, 36.83, 44.18, 7.64, 22.16, 46.45, 0.00, 24.25, 35.69, 24.52, 13.61, 0.00, 26.75, 26.75, 12.2, ], 
              [81.18, 47.01, 9.09, 36.48, 22.41, 37.99, 19.00, 58.32, 43.68, 14.57, 41.27, 4.99, 37.58, 41.81, 10.44, 17.89, 29.29, 39.06, 19.71, 26.75, 36.53, 9.83, 39.82, 36.48, 26.75, 0.00, 0.00, 14.57], 
              [81.18, 47.01, 9.09, 36.48, 22.41, 37.99, 19.00, 58.32, 43.68, 14.57, 41.27, 4.99, 37.58, 41.81, 10.44, 17.89, 29.29, 39.06, 19.71, 26.75, 36.53, 9.83, 39.82, 36.48, 26.75, 0.00, 0.00, 14.57], 
              [71.58, 33.86, 23.60, 22.79, 8.19, 27.85, 33.45, 46.27, 34.06, 0.00, 28.91, 13.93, 25.37, 28.54, 24.78, 32.03, 15.43, 28.39, 34.27, 12.20, 27.84, 23.76, 29.93, 22.79, 12.20, 14.57, 14.57, 0.00]]]


ClosingInsts =  [[0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0], 
                 [0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

DemandNum = [[0, 2, 1, 2, 4, 4, 4, 4, 3, 4, 3, 4, 4, 4, 3, 5, 1, 3, 1, 2, 1, 3, 3, 3, 3, 3, 3, 3], 
             [0, 2, 3, 3, 1, 2, 3, 3, 3, 1, 4, 5, 1, 4, 3, 3, 3, 4, 3, 4, 4, 3, 4, 4, 4, 1, 3, 2]]

LayTime = [[0, 3, 4, 3, 4, 4, 4, 4, 3, 3, 3, 3, 2, 3, 4, 2, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3], 
           [0, 3, 3, 3, 3, 3, 3, 4, 3, 2, 4, 2, 4, 3, 3, 3, 3, 4, 3, 3, 4, 3, 4, 3, 2, 3, 3, 3]]

Demand = [[0, 200, 100, 100, 200, 150, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100], 
          [0, 200, 100, 100, 200, 150, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100]]

# ---------------------------- Vessels ----------------------------

Vessels = [0, 1, 2, 3, 4, 5]

AvaliableTime = [0, 24, 48, 0, 24, 48]

VesselCap = [600, 600, 600, 600, 600, 600]

Voys = [0, 1, 2, 3]


#Times

Times = [0,  1,  2,  3,  4,  5,  6,  7,  8,  9,  10,  11,  12,  13,  14,  15,  16,  17,  18,  19,  20,  21,  22,  23,  24,  25,  26,  27,  28,  29,  30,  31,  32,  33,  34,  35,  36,  37,  38,  39,  40,  41,  42,  43,  44,  45,  46,  47,  48,  49,  50,  51,  52,  53,  54,  55,  56,  57,  58,  59,  60,  61,  62,  63,  64,  65,  66,  67,  68,  69,  70,  71,  72,  73,  74,  75,  76,  77,  78,  79,  80,  81,  82,  83,  84,  85,  86,  87,  88,  89,  90,  91,  92,  93,  94,  95,  96,  97,  98,  99,  100,  101,  102,  103,  104,  105,  106,  107,  108,  109,  110,  111,  112,  113,  114,  115,  116,  117,  118,  119,  120,  121,  122,  123,  124,  125,  126,  127,  128,  129,  130,  131,  132,  133,  134,  135,  136,  137,  138,  139,  140,  141,  142,  143,  144,  145,  146,  147,  148,  149,  150,  151,  152,  153,  154,  155,  156,  157,  158,  159,  160,  161,  162,  163,  164,  165,  166,  167,  168,  169,  170,  171,  172,  173,  174,  175,  176,  177,  178,  179,  180,  181,  182,  183,  184,  185,  186,  187,  188,  189,  190,  191,  192,  193,  194,  195,  196,  197,  198,  199,  200,  201,  202,  203,  204,  205,  206,  207,  208,  209,  210,  211,  212,  213,  214,  215,  216]

# ---------------------------- WeatherForecast ----------------------------

#        ___________________________________________________________________________________
#       | Weather settings:                                                                 |
#       |-----------------------------------------------------------------------------------|
#       | W[0] = Hot Summer Day! (great weather - no nonservicable installations )          |
#       | W[1] = Bad weather coming ( bad weather rolling in towards the end of the week )  |
#       | W[2] = Bad weather ( platforms barely servicable some days )                      |
#        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Weather = [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
           [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],
           [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]]


SpeedImpact = [0, 0, 2, 3]

ServiceImpact = [0,1,1,300]

# ---------------------------- SingleParameters ----------------------------

nInstallations = len(Insts)

nVessels = len(Vessels)

nTimes = len(Times)

fuelPrice = 0.400

maxSpeed = 16

minSpeed = 7

serviceTime = 2

sailingFuelConsume = 340

dpFuelConsume = 170

idleFuelConsume = 120

depConsumption = 45

spotHourRate = 5653