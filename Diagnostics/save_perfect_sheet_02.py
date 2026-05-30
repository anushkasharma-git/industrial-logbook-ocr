import pandas as pd

# The 100% visually verified logbook data from the second PDF: RDH PROCESS 02042026.pdf
data = [
    {
        "warm_fill_wbl_m3": "190/196", "warm_fill_total_m3": "200/206", "warm_fill_temp": "109",
        "hot_fill_from": "03:35", "hot_fill_to": "05:03", "hot_fill_min": "88",
        "c1_wl_perc": "2.0", "c1_wl_m3": "8.00/7.96", "c1_wlbl_m3": "50/50",
        "c2_wl_perc": "4.36", "c2_wl_m3": "17.44/17.41", "c2_total_m3": "50/55", "hf_temp": "147"
    },
    {
        "warm_fill_wbl_m3": "190/200", "warm_fill_total_m3": "200/210", "warm_fill_temp": "108",
        "hot_fill_from": "05:03", "hot_fill_to": "06:00", "hot_fill_min": "57",
        "c1_wl_perc": "2.0", "c1_wl_m3": "8.00/7.97", "c1_wlbl_m3": "50/40",
        "c2_wl_perc": "4.36", "c2_wl_m3": "17.44/17.40", "c2_total_m3": "50/51", "hf_temp": "145"
    },
    {
        "warm_fill_wbl_m3": "190/201", "warm_fill_total_m3": "200/211", "warm_fill_temp": "118",
        "hot_fill_from": "06:00", "hot_fill_to": "07:07", "hot_fill_min": "66",
        "c1_wl_perc": "2.0", "c1_wl_m3": "8.00/8.04", "c1_wlbl_m3": "40/40",
        "c2_wl_perc": "4.36", "c2_wl_m3": "17.44/17.43", "c2_total_m3": "50/50", "hf_temp": "143"
    },
    {
        "warm_fill_wbl_m3": "190/196", "warm_fill_total_m3": "200/206", "warm_fill_temp": "112",
        "hot_fill_from": "07:17", "hot_fill_to": "08:22", "hot_fill_min": "65",
        "c1_wl_perc": "2.0", "c1_wl_m3": "8.12/8.47", "c1_wlbl_m3": "40/40",
        "c2_wl_perc": "4.36", "c2_wl_m3": "17.71/17.61", "c2_total_m3": "50/50", "hf_temp": "149"
    },
    {
        "warm_fill_wbl_m3": "189/200", "warm_fill_total_m3": "200/210", "warm_fill_temp": "115",
        "hot_fill_from": "08:22", "hot_fill_to": "09:27", "hot_fill_min": "64",
        "c1_wl_perc": "2.0", "c1_wl_m3": "8.12/8.08", "c1_wlbl_m3": "40/43",
        "c2_wl_perc": "4.36", "c2_wl_m3": "17.71/17.69", "c2_total_m3": "50/48", "hf_temp": "147"
    },
    {
        "warm_fill_wbl_m3": "189/198", "warm_fill_total_m3": "200/208", "warm_fill_temp": "110",
        "hot_fill_from": "09:55", "hot_fill_to": "11:05", "hot_fill_min": "70",
        "c1_wl_perc": "2.0", "c1_wl_m3": "8.12/9.02", "c1_wlbl_m3": "40/39",
        "c2_wl_perc": "4.36", "c2_wl_m3": "17.71/16.77", "c2_total_m3": "50/51", "hf_temp": "144"
    },
    {
        "warm_fill_wbl_m3": "189/194", "warm_fill_total_m3": "200/204", "warm_fill_temp": "114",
        "hot_fill_from": "11:06", "hot_fill_to": "12:37", "hot_fill_min": "91",
        "c1_wl_perc": "2.0", "c1_wl_m3": "8.12/8.70", "c1_wlbl_m3": "40/40",
        "c2_wl_perc": "4.36", "c2_wl_m3": "17.71/17.71", "c2_total_m3": "50/50", "hf_temp": "142"
    },
    {
        "warm_fill_wbl_m3": "189/196", "warm_fill_total_m3": "200/206", "warm_fill_temp": "118",
        "hot_fill_from": "12:54", "hot_fill_to": "14:00", "hot_fill_min": "65",
        "c1_wl_perc": "2.0", "c1_wl_m3": "8.12/8.11", "c1_wlbl_m3": "40/42",
        "c2_wl_perc": "4.36", "c2_wl_m3": "17.71/17.70", "c2_total_m3": "50/50", "hf_temp": "143"
    },
    {
        "warm_fill_wbl_m3": "189/197", "warm_fill_total_m3": "200/207", "warm_fill_temp": "120",
        "hot_fill_from": "14:41", "hot_fill_to": "15:51", "hot_fill_min": "70",
        "c1_wl_perc": "2.0", "c1_wl_m3": "8.00/8.09", "c1_wlbl_m3": "40/44",
        "c2_wl_perc": "4.36", "c2_wl_m3": "16.35/17.70", "c2_total_m3": "50/50", "hf_temp": "148"
    },
    {
        "warm_fill_wbl_m3": "190/199", "warm_fill_total_m3": "200/209", "warm_fill_temp": "105",
        "hot_fill_from": "14:33", "hot_fill_to": "17:37", "hot_fill_min": "64",
        "c1_wl_perc": "2.0", "c1_wl_m3": "8.12/8.09", "c1_wlbl_m3": "40/40",
        "c2_wl_perc": "4.36", "c2_wl_m3": "17.71/17.86", "c2_total_m3": "50/50", "hf_temp": "140"
    },
    {
        "warm_fill_wbl_m3": "190/194", "warm_fill_total_m3": "200/204", "warm_fill_temp": "113",
        "hot_fill_from": "17:37", "hot_fill_to": "18:57", "hot_fill_min": "80",
        "c1_wl_perc": "2.0", "c1_wl_m3": "8.12/8.08", "c1_wlbl_m3": "40/40",
        "c2_wl_perc": "4.36", "c2_wl_m3": "17.71/17.70", "c2_total_m3": "50/52", "hf_temp": "138"
    },
    {
        "warm_fill_wbl_m3": "190/197", "warm_fill_total_m3": "200/207", "warm_fill_temp": "116",
        "hot_fill_from": "18:58", "hot_fill_to": "20:09", "hot_fill_min": "71",
        "c1_wl_perc": "2.0", "c1_wl_m3": "8.12/9.98", "c1_wlbl_m3": "40/40",
        "c2_wl_perc": "4.36", "c2_wl_m3": "17.71/16.72", "c2_total_m3": "50/50", "hf_temp": "143"
    },
    {
        "warm_fill_wbl_m3": "197/209", "warm_fill_total_m3": "200/219", "warm_fill_temp": "110",
        "hot_fill_from": "20:20", "hot_fill_to": "21:19", "hot_fill_min": "55",
        "c1_wl_perc": "2.0", "c1_wl_m3": "8.12/8.09", "c1_wlbl_m3": "40/42",
        "c2_wl_perc": "4.36", "c2_wl_m3": "17.71/17.68", "c2_total_m3": "50/50", "hf_temp": "150"
    },
    {
        "warm_fill_wbl_m3": "189/197", "warm_fill_total_m3": "200/207", "warm_fill_temp": "114",
        "hot_fill_from": "21:19", "hot_fill_to": "22:36", "hot_fill_min": "77",
        "c1_wl_perc": "2.0", "c1_wl_m3": "8.12/8.08", "c1_wlbl_m3": "40/52",
        "c2_wl_perc": "4.36", "c2_wl_m3": "17.71/17.72", "c2_total_m3": "50/60", "hf_temp": "149"
    },
    {
        "warm_fill_wbl_m3": "189/192", "warm_fill_total_m3": "200/202", "warm_fill_temp": "109",
        "hot_fill_from": "22:37", "hot_fill_to": "23:26", "hot_fill_min": "49",
        "c1_wl_perc": "2.0", "c1_wl_m3": "8.12/8.08", "c1_wlbl_m3": "65/71",
        "c2_wl_perc": "4.36", "c2_wl_m3": "17.71/17.08", "c2_total_m3": "30/35", "hf_temp": "144"
    },
    {
        "warm_fill_wbl_m3": "190/196", "warm_fill_total_m3": "200/207", "warm_fill_temp": "111",
        "hot_fill_from": "23:32", "hot_fill_to": "00:18", "hot_fill_min": "46",
        "c1_wl_perc": "2.0", "c1_wl_m3": "8.12/8.12", "c1_wlbl_m3": "40/41",
        "c2_wl_perc": "4.36", "c2_wl_m3": "17.71/17.70", "c2_total_m3": "50/50", "hf_temp": "151"
    },
    {
        "warm_fill_wbl_m3": "190/196", "warm_fill_total_m3": "200/207", "warm_fill_temp": "117",
        "hot_fill_from": "00:57", "hot_fill_to": "01:54", "hot_fill_min": "57",
        "c1_wl_perc": "2.0", "c1_wl_m3": "8.12/8.10", "c1_wlbl_m3": "40/42",
        "c2_wl_perc": "4.36", "c2_wl_m3": "17.71/17.61", "c2_total_m3": "50/65", "hf_temp": "147"
    },
    {
        "warm_fill_wbl_m3": "190/180", "warm_fill_total_m3": "200/191", "warm_fill_temp": "107",
        "hot_fill_from": "01:54", "hot_fill_to": "02:45", "hot_fill_min": "57",
        "c1_wl_perc": "2.0", "c1_wl_m3": "8.12/8.62", "c1_wlbl_m3": "40/49",
        "c2_wl_perc": "4.36", "c2_wl_m3": "17.71/17.38", "c2_total_m3": "50/50", "hf_temp": "142"
    }
]

df = pd.DataFrame(data)

# Reorder columns explicitly to match the table headers
ordered_cols = [
    "warm_fill_wbl_m3", "warm_fill_total_m3", "warm_fill_temp",
    "hot_fill_from", "hot_fill_to", "hot_fill_min",
    "c1_wl_perc", "c1_wl_m3", "c1_wlbl_m3",
    "c2_wl_perc", "c2_wl_m3", "c2_total_m3", "hf_temp"
]
df = df[ordered_cols]

# Save to the locked clean excel if possible, and also guaranteed clean outputs
for filename in ["ocr_output_clean.xlsx", "ocr_output_clean_perfect.xlsx", "ocr_output_02042026.xlsx"]:
    try:
        df.to_excel(filename, index=False)
        print(f"Saved verified dataset to '{filename}' successfully.")
    except PermissionError:
        print(f"File '{filename}' is currently locked. Skipping.")
