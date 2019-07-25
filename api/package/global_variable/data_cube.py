from package.import_data.transform_data import transform
from package.import_data.transfom_xyz import transform as to_xyz

face_0_ledstrip = transform("package/import_data/data/cheminee.csv", 24)
face_1_ledstrip = transform("package/import_data/data/case.csv", 24)
face_2_ledstrip = transform("package/import_data/data/toit.csv", 24)
face_3_ledstrip = transform("package/import_data/data/vitre.csv", 24)
face_4_ledstrip = transform("package/import_data/data/haut.csv", 12)
face_5_ledstrip = transform("package/import_data/data/bas.csv", 12)

address_ledstrip = [face_0_ledstrip, face_1_ledstrip, face_2_ledstrip, face_3_ledstrip, face_4_ledstrip,
                    face_5_ledstrip]
address_xyz = to_xyz("package/import_data/data/xyz.csv")