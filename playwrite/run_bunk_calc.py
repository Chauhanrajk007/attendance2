import math
import json

# Attendance data from official report
attendance_raw = [
  {"code": "APT4006", "name": "Logical and Critical Thinking", "TH": 20, "AH": 14, "DL": 2, "AH_DL": 16, "AH_pct": 70.00, "AHDL_pct": 80.00},
  {"code": "CBC2000", "name": "Foundations of Blockchain Technology", "TH": 34, "AH": 21, "DL": 3, "AH_DL": 24, "AH_pct": 61.76, "AHDL_pct": 70.59},
  {"code": "CIT2500", "name": "FoG Computing for IoT", "TH": 33, "AH": 22, "DL": 2, "AH_DL": 24, "AH_pct": 66.67, "AHDL_pct": 72.73},
  {"code": "CIT2501", "name": "Wireless Communication in IoT", "TH": 33, "AH": 23, "DL": 3, "AH_DL": 26, "AH_pct": 69.70, "AHDL_pct": 78.79},
  {"code": "CIT2502", "name": "Privacy and Security in IoT", "TH": 37, "AH": 27, "DL": 2, "AH_DL": 29, "AH_pct": 72.97, "AHDL_pct": 78.38},
  {"code": "CIT2503", "name": "Mobile Application for IoT", "TH": 38, "AH": 24, "DL": 3, "AH_DL": 27, "AH_pct": 63.16, "AHDL_pct": 71.05},
  {"code": "CIT3402", "name": "IoT Architecture and Protocols", "TH": 49, "AH": 40, "DL": 4, "AH_DL": 44, "AH_pct": 81.63, "AHDL_pct": 89.80},
  {"code": "CSS2264", "name": "Essentials of AI", "TH": 37, "AH": 29, "DL": 2, "AH_DL": 31, "AH_pct": 78.38, "AHDL_pct": 83.78},
  {"code": "CSS2265", "name": "Essentials of AI Lab", "TH": 26, "AH": 16, "DL": 2, "AH_DL": 18, "AH_pct": 61.54, "AHDL_pct": 69.23},
  {"code": "CSS2285", "name": "Cloud Computing", "TH": 25, "AH": 19, "DL": 2, "AH_DL": 21, "AH_pct": 76.00, "AHDL_pct": 84.00},
  {"code": "CSS2286", "name": "Cloud Computing Lab", "TH": 26, "AH": 22, "DL": 0, "AH_DL": 22, "AH_pct": 84.62, "AHDL_pct": 84.62}
]

remaining_classes = {
  "APT4006": 4,
  "CBC2000": 6,
  "CIT2500": 5,
  "CIT2501": 6,
  "CIT2502": 5,
  "CIT2503": 6,
  "CIT3402": 8,
  "CSS2264": 5,
  "CSS2265": 4,
  "CSS2285": 4,
  "CSS2286": 2
}

def analyze_bunks(use_dl=True, target_pct=75.0):
    print(f"\n=======================================================")
    print(f" ANALYSIS WITH {'AH + DL (Duty Leave Included)' if use_dl else 'AH (Only Attended Hours)'} | TARGET: {target_pct}%")
    print(f"=======================================================")
    
    results = []
    for item in attendance_raw:
        code = item["code"]
        name = item["name"]
        TH = item["TH"]
        A = item["AH_DL"] if use_dl else item["AH"]
        curr_pct = item["AHDL_pct"] if use_dl else item["AH_pct"]
        R = remaining_classes.get(code, 0)
        T_final = TH + R
        
        # Min attended needed by end of sem
        A_needed = math.ceil((target_pct / 100.0) * T_final)
        must_attend = max(0, A_needed - A)
        
        # Max bunks allowed
        if must_attend > R:
            # Deficit: cannot reach target even if attending 100% of remaining classes
            max_bunks = 0
            shortage = must_attend - R
            status = f"CRITICAL SHORTAGE (Short by {shortage} classes even if 100% attended!)"
        else:
            max_bunks = R - must_attend
            if max_bunks == 0:
                status = f"BORDERLINE: MUST ATTEND ALL {R} CLASSES (0 Bunks allowed)"
            else:
                status = f"SAFE: Can bunk up to {max_bunks} classes (Must attend {must_attend}/{R})"
                
        max_possible_pct = round(((A + R) / T_final) * 100, 2)
        min_possible_pct = round((A / T_final) * 100, 2)
        
        results.append({
            "code": code,
            "name": name,
            "curr_att": A,
            "curr_th": TH,
            "curr_pct": curr_pct,
            "rem_classes": R,
            "final_th": T_final,
            "a_needed": A_needed,
            "must_attend": must_attend,
            "max_bunks": max_bunks,
            "max_possible_pct": max_possible_pct,
            "min_possible_pct": min_possible_pct,
            "status": status
        })
        
        print(f"[{code}] {name}")
        print(f"  Current: {A}/{TH} ({curr_pct}%) | Left: {R} classes | Final Total: {T_final}")
        print(f"  Target {target_pct}% needs: {A_needed}/{T_final} classes attended")
        print(f"  Must Attend: {must_attend}/{R} | Max Bunks Allowed: {max_bunks}")
        print(f"  Max Possible %: {max_possible_pct}% | Min Possible %: {min_possible_pct}%")
        print(f"  Status: {status}\n")
    return results

print("=== CALCULATING PREDICTIONS ===")
analyze_bunks(use_dl=True, target_pct=75.0)
analyze_bunks(use_dl=True, target_pct=80.0)
