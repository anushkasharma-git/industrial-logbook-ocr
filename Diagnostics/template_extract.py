# import cv2
# import numpy as np
# from pdf2image import convert_from_path
# import os

# # =====================================
# # SETTINGS
# # =====================================

# PDF_PATH = "RDH PROCESS 01042026.pdf"

# OUTPUT_DIR = "template_output"

# os.makedirs(OUTPUT_DIR, exist_ok=True)

# CELL_DIR = f"{OUTPUT_DIR}/cells"

# os.makedirs(CELL_DIR, exist_ok=True)

# # =====================================
# # LOAD PDF
# # =====================================

# pages = convert_from_path(
#     PDF_PATH,
#     dpi=300
# )

# page = pages[0]

# img = np.array(page)

# img = cv2.cvtColor(
#     img,
#     cv2.COLOR_RGB2BGR
# )

# debug = img.copy()

# # =====================================
# # MAIN TABLE REGION
# # manually calibrated
# # =====================================

# TABLE_X1 = 40
# TABLE_Y1 = 195

# TABLE_X2 = 880
# TABLE_Y2 = 1040

# table = img[
#     TABLE_Y1:TABLE_Y2,
#     TABLE_X1:TABLE_X2
# ]

# # =====================================
# # COLUMN DEFINITIONS
# # (name, start_x, end_x)
# # calibrated manually
# # =====================================

# columns = [

#     ("warm_fill_wbl m3",      0,   63),
#     ("warm_fill_total m3",    63,  128),
#     ("warm_fill_temp",     128, 194),

#     ("hot_fill_from",      194, 251),
#     ("hot_fill_to",        251, 309),
#     ("hot_fill_min",       309, 360),

#     ("c1_wl_perc",         360, 418),
#     ("c1_wl_m3",           418, 486),
#     ("c1_wlbl_m3",         486, 565),

#     ("c2_wl_perc",         565, 633),
#     ("c2_wl_m3",           633, 714),
#     ("c2_total_m3",        714, 796),

#     ("hf_temp",            796, 840),
# ]

# # =====================================
# # ROW SETTINGS
# # =====================================

# FIRST_ROW_Y = 0

# ROW_HEIGHT = 38

# NUM_ROWS = 20

# # =====================================
# # EXTRACT CELLS
# # =====================================

# for r in range(NUM_ROWS):

#     row_y1 = FIRST_ROW_Y + r * ROW_HEIGHT
#     row_y2 = row_y1 + ROW_HEIGHT

#     for c, (name, x1, x2) in enumerate(columns):

#         cell = table[
#             row_y1:row_y2,
#             x1:x2
#         ]

#         # =====================================
#         # EMPTY CHECK
#         # =====================================

#         gray = cv2.cvtColor(
#             cell,
#             cv2.COLOR_BGR2GRAY
#         )

#         ink = cv2.countNonZero(
#             255 - gray
#         )

#         # skip blank cells
#         if ink < 250:
#             continue

#         # =====================================
#         # SAVE CELL
#         # =====================================

#         filename = (
#             f"r{r:02d}_{name}.png"
#         )

#         cv2.imwrite(
#             os.path.join(CELL_DIR, filename),
#             cell
#         )

#         # =====================================
#         # DEBUG DRAW
#         # =====================================

#         abs_x1 = TABLE_X1 + x1
#         abs_x2 = TABLE_X1 + x2

#         abs_y1 = TABLE_Y1 + row_y1
#         abs_y2 = TABLE_Y1 + row_y2

#         cv2.rectangle(
#             debug,
#             (abs_x1, abs_y1),
#             (abs_x2, abs_y2),
#             (0,255,0),
#             2
#         )

#         cv2.putText(
#             debug,
#             f"{r}",
#             (abs_x1+2, abs_y1+15),
#             cv2.FONT_HERSHEY_SIMPLEX,
#             0.4,
#             (0,0,255),
#             1
#         )

# # =====================================
# # SAVE DEBUG
# # =====================================

# cv2.imwrite(
#     f"{OUTPUT_DIR}/debug_template.png",
#     debug
# )

# print("DONE")
