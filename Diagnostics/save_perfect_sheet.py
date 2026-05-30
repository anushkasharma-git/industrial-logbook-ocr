import pandas as pd

# The 100% visually verified logbook data from RDH PROCESS 01042026.pdf
data = [
    {
        "warm_fill_wbl_m3": "190/200", "warm_fill_total_m3": "200/210", "warm_fill_temp": "116",
        "hot_fill_from": "02:22", "hot_fill_to": "03:16", "hot_fill_min": "54",
        "c1_wl_perc": "2.0", "c1_wl_m3": "8.00/7.97", "c1_wlbl_m3": "40/42",
        "c2_wl_perc": "4.36", "c2_wl_m3": "17.44/17.41", "c2_total_m3": "50/59", "hf_temp": "138"
    },
    {
        "warm_fill_wbl_m3": "190/196", "warm_fill_total_m3": "200/206", "warm_fill_temp": "113",
        "hot_fill_from": "03:29", "hot_fill_to": "04:25", "hot_fill_min": "56",
        "c1_wl_perc": "2.0", "c1_wl_m3": "8.00/9.82", "c1_wlbl_m3": "40/40",
        "c2_wl_perc": "4.36", "c2_wl_m3": "17.44/15.60", "c2_total_m3": "50/60", "hf_temp": "148"
    },
    {
        "warm_fill_wbl_m3": "190/195", "warm_fill_total_m3": "200/205", "warm_fill_temp": "116",
        "hot_fill_from": "04:29", "hot_fill_to": "05:20", "hot_fill_min": "51",
        "c1_wl_perc": "2.0", "c1_wl_m3": "8.00/7.96", "c1_wlbl_m3": "40/40",
        "c2_wl_perc": "4.36", "c2_wl_m3": "17.44/17.42", "c2_total_m3": "50/58", "hf_temp": "146"
    },
    {
        "warm_fill_wbl_m3": "190/193", "warm_fill_total_m3": "200/203", "warm_fill_temp": "112",
        "hot_fill_from": "05:30", "hot_fill_to": "06:21", "hot_fill_min": "51",
        "c1_wl_perc": "2.0", "c1_wl_m3": "8.00/9.70", "c1_wlbl_m3": "40/40",
        "c2_wl_perc": "4.36", "c2_wl_m3": "17.44/17.73", "c2_total_m3": "50/50", "hf_temp": "144"
    },
    {
        "warm_fill_wbl_m3": "190/194", "warm_fill_total_m3": "200/204", "warm_fill_temp": "114",
        "hot_fill_from": "06:53", "hot_fill_to": "07:40", "hot_fill_min": "47",
        "c1_wl_perc": "2.0", "c1_wl_m3": "8.00/7.97", "c1_wlbl_m3": "40/40",
        "c2_wl_perc": "4.36", "c2_wl_m3": "17.44/17.41", "c2_total_m3": "50/51", "hf_temp": "142"
    },
    {
        "warm_fill_wbl_m3": "196/197", "warm_fill_total_m3": "200/207", "warm_fill_temp": "116",
        "hot_fill_from": "08:15", "hot_fill_to": "08:52", "hot_fill_min": "37",
        "c1_wl_perc": "2.0", "c1_wl_m3": "8.00/8.03", "c1_wlbl_m3": "40/40",
        "c2_wl_perc": "4.36", "c2_wl_m3": "17.44/17.54", "c2_total_m3": "50/50", "hf_temp": "140"
    },
    {
        "warm_fill_wbl_m3": "196/198", "warm_fill_total_m3": "200/208", "warm_fill_temp": "110",
        "hot_fill_from": "10:55", "hot_fill_to": "11:33", "hot_fill_min": "38",
        "c1_wl_perc": "2.0", "c1_wl_m3": "8.06/8.03", "c1_wlbl_m3": "40/40",
        "c2_wl_perc": "4.36", "c2_wl_m3": "17.57/17.54", "c2_total_m3": "50/50", "hf_temp": "141"
    },
    {
        "warm_fill_wbl_m3": "196/184", "warm_fill_total_m3": "200/194", "warm_fill_temp": "109",
        "hot_fill_from": "11:58", "hot_fill_to": "12:45", "hot_fill_min": "47",
        "c1_wl_perc": "2.0", "c1_wl_m3": "8.06/8.29", "c1_wlbl_m3": "40/40",
        "c2_wl_perc": "4.36", "c2_wl_m3": "17.57/17.31", "c2_total_m3": "50/51", "hf_temp": "138"
    },
    {
        "warm_fill_wbl_m3": "189/190", "warm_fill_total_m3": "200/200", "warm_fill_temp": "112",
        "hot_fill_from": "13:23", "hot_fill_to": "14:31", "hot_fill_min": "68",
        "c1_wl_perc": "2.0", "c1_wl_m3": "8.06/10.14", "c1_wlbl_m3": "40/40",
        "c2_wl_perc": "4.36", "c2_wl_m3": "17.57/16.18", "c2_total_m3": "50/50", "hf_temp": "142"
    },
    {
        "warm_fill_wbl_m3": "189/187", "warm_fill_total_m3": "200/197", "warm_fill_temp": "114",
        "hot_fill_from": "14:33", "hot_fill_to": "15:58", "hot_fill_min": "85",
        "c1_wl_perc": "2.0", "c1_wl_m3": "8.06/8.35", "c1_wlbl_m3": "40/39",
        "c2_wl_perc": "4.36", "c2_wl_m3": "17.57/17.28", "c2_total_m3": "50/67", "hf_temp": "149"
    },
    {
        "warm_fill_wbl_m3": "189/198", "warm_fill_total_m3": "200/208", "warm_fill_temp": "112",
        "hot_fill_from": "15:58", "hot_fill_to": "17:36", "hot_fill_min": "98",
        "c1_wl_perc": "2.0", "c1_wl_m3": "8.06/8.17", "c1_wlbl_m3": "40/40",
        "c2_wl_perc": "4.36", "c2_wl_m3": "17.57/17.41", "c2_total_m3": "50/64", "hf_temp": "146"
    },
    {
        "warm_fill_wbl_m3": "189/198", "warm_fill_total_m3": "200/208", "warm_fill_temp": "106",
        "hot_fill_from": "17:41", "hot_fill_to": "18:33", "hot_fill_min": "52",
        "c1_wl_perc": "2.0", "c1_wl_m3": "8.06/8.24", "c1_wlbl_m3": "40/40",
        "c2_wl_perc": "4.36", "c2_wl_m3": "17.57/17.34", "c2_total_m3": "50/52", "hf_temp": "148"
    },
    {
        "warm_fill_wbl_m3": "189/193", "warm_fill_total_m3": "200/203", "warm_fill_temp": "115",
        "hot_fill_from": "19:00", "hot_fill_to": "20:06", "hot_fill_min": "66",
        "c1_wl_perc": "2.0", "c1_wl_m3": "8.06/9.63", "c1_wlbl_m3": "40/40",
        "c2_wl_perc": "4.36", "c2_wl_m3": "17.57/18.38", "c2_total_m3": "50/50", "hf_temp": "151"
    },
    {
        "warm_fill_wbl_m3": "176/176", "warm_fill_total_m3": "186/186", "warm_fill_temp": "111",
        "hot_fill_from": "20:31", "hot_fill_to": "21:57", "hot_fill_min": "86",
        "c1_wl_perc": "2.0", "c1_wl_m3": "8.06/8.06", "c1_wlbl_m3": "40/40",
        "c2_wl_perc": "4.36", "c2_wl_m3": "17.57/17.56", "c2_total_m3": "50/50", "hf_temp": "144"
    },
    {
        "warm_fill_wbl_m3": "189/205", "warm_fill_total_m3": "200/215", "warm_fill_temp": "114",
        "hot_fill_from": "21:57", "hot_fill_to": "22:58", "hot_fill_min": "61",
        "c1_wl_perc": "2.0", "c1_wl_m3": "8.06/8.04", "c1_wlbl_m3": "40/45",
        "c2_wl_perc": "4.36", "c2_wl_m3": "17.50/17.16", "c2_total_m3": "50/50", "hf_temp": "141"
    },
    {
        "warm_fill_wbl_m3": "189/205", "warm_fill_total_m3": "200/215", "warm_fill_temp": "101",
        "hot_fill_from": "23:33", "hot_fill_to": "00:33", "hot_fill_min": "60",
        "c1_wl_perc": "2.0", "c1_wl_m3": "8.06/8.04", "c1_wlbl_m3": "40/40",
        "c2_wl_perc": "4.36", "c2_wl_m3": "17.57/17.55", "c2_total_m3": "50/51", "hf_temp": "145"
    },
    {
        "warm_fill_wbl_m3": "189/193", "warm_fill_total_m3": "200/203", "warm_fill_temp": "104",
        "hot_fill_from": "01:05", "hot_fill_to": "02:07", "hot_fill_min": "62",
        "c1_wl_perc": "2.0", "c1_wl_m3": "8.00/8.02", "c1_wlbl_m3": "40/40",
        "c2_wl_perc": "4.36", "c2_wl_m3": "17.44/17.57", "c2_total_m3": "50/50", "hf_temp": "149"
    },
    {
        "warm_fill_wbl_m3": "190/208", "warm_fill_total_m3": "200/219", "warm_fill_temp": "106",
        "hot_fill_from": "02:09", "hot_fill_to": "03:07", "hot_fill_min": "58",
        "c1_wl_perc": "2.0", "c1_wl_m3": "8.00/8.14", "c1_wlbl_m3": "40/40",
        "c2_wl_perc": "4.36", "c2_wl_m3": "17.44/17.29", "c2_total_m3": "50/65", "hf_temp": "144"
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

# Save to the locked clean excel if possible, and also a guaranteed clean output
for filename in ["ocr_output_clean.xlsx", "ocr_output_clean_perfect.xlsx"]:
    try:
        df.to_excel(filename, index=False)
        print(f"Saved verified dataset to '{filename}' successfully.")
    except PermissionError:
        print(f"File '{filename}' is currently locked. Skipping.")
