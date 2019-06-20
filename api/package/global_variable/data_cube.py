from package.import_data.transform_data import transform
from package.import_data.transfom_xyz import transform as to_xyz

face_0 = [(2, 0, 512), (4, 0, 512), (5, 0, 512), (6, 0, 512), (7, 0, 512), (16, 0, 512), (17, 0, 512),
          (18, 0, 486)]  # cheminee
face_1 = [8, 9, 10, 11, 12, 14, 15, 18, 19]  # case
face_2 = [24, 26, 32, 33, 34, 35]  # toit
face_3 = [28, 29, 30, 31, 36, 37, 38, 39]  # vitre

face = [face_0, face_1, face_2, face_3]
face_0_ledstrip = transform("package/import_data/data/cheminee.txt")
face_1_ledstrip = transform("package/import_data/data/case.txt")
face_2_ledstrip = transform("package/import_data/data/toit.txt")
face_3_ledstrip = transform("package/import_data/data/vitre.txt")
face_4_ledstrip = transform("package/import_data/data/haut.txt")
face_5_ledstrip = transform("package/import_data/data/bas.txt")

address_ledstrip = [face_0_ledstrip, face_1_ledstrip, face_2_ledstrip, face_3_ledstrip, face_4_ledstrip,
                    face_5_ledstrip]

address_xyz = to_xyz("package/import_data/data/xyz.csv")


