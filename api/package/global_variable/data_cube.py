from package.import_data.transform_data import transform

face_0 = [(2, 0, 512), (4, 0, 512), (5, 0, 512), (6, 0, 512), (7, 0, 512), (16, 0, 512), (17, 0, 512),
          (18, 0, 486)]  # cheminee
face_1 = [8, 9, 10, 11, 12, 14, 15, 18, 19]  # case
face_2 = [24, 26, 32, 33, 34, 35]  # toit
face_3 = [28, 29, 30, 31, 36, 37, 38, 39]  # vitre

face = [face_0, face_1, face_2, face_3]
face_0_ledstrip = transform("package/import_data/data/cheminee.txt")

address_ledstrip = [face_0_ledstrip]


