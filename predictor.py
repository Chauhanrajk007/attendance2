"""
Attendance Predictor and Bunk Simulation Engine
Calculates safe bunks, recovery targets, On-Duty (OD/DL) credits, and schedule projections until last working day.
"""

from datetime import datetime, timedelta
import math

def calculate_course_metrics(course, target_pct=75.0, use_dl=True):
    """
    Computes attendance stats, safe bunks, recovery classes, and ODs needed for a course.
    """
    th = int(course.get('th', 0))
    ah = int(course.get('ah', 0))
    dl = int(course.get('dl', 0))
    effective_attended = (ah + dl) if use_dl else ah

    current_pct = round((effective_attended / th * 100) if th > 0 else 0.0, 2)

    # Safe bunks calculation:
    # (effective_attended) / (th + bunks) >= target / 100
    # bunks <= (100 * effective_attended - target * th) / target
    if th > 0 and current_pct >= target_pct:
        max_safe_bunks = int(math.floor((100.0 * effective_attended - target_pct * th) / target_pct))
        max_safe_bunks = max(0, max_safe_bunks)
    else:
        max_safe_bunks = 0

    # Recovery classes if attending regular upcoming classes:
    # (effective_attended + attend) / (th + attend) >= target / 100
    # attend >= (target * th - 100 * effective_attended) / (100 - target)
    if th > 0 and current_pct < target_pct and target_pct < 100.0:
        required_attend = int(math.ceil((target_pct * th - 100.0 * effective_attended) / (100.0 - target_pct)))
        required_attend = max(0, required_attend)
    else:
        required_attend = 0

    # ODs needed to hit target percentage (past missed class converted to Duty Leave):
    # (effective_attended + od) / th >= target / 100
    # od >= ceil((target * th) / 100) - effective_attended
    if th > 0 and current_pct < target_pct:
        ods_needed = int(math.ceil((target_pct * th) / 100.0) - effective_attended)
        ods_needed = max(0, ods_needed)
    else:
        ods_needed = 0

    status = 'safe' if current_pct >= target_pct else ('warning' if current_pct >= (target_pct - 10.0) else 'critical')

    return {
        'course_name': course.get('course_name', ''),
        'course_code': course.get('course_code', ''),
        'th': th,
        'ah': ah,
        'dl': dl,
        'effective_attended': effective_attended,
        'current_pct': current_pct,
        'status': status,
        'max_safe_bunks': max_safe_bunks,
        'required_attend': required_attend,
        'ods_needed': ods_needed,
        'target_pct': target_pct
    }


def simulate_bunk_impact(courses, overall, adjustments, target_pct=75.0, use_dl=True):
    """
    adjustments: dict of {course_code: {'bunk': int, 'attend': int, 'od': int, 'od_type': 'past'|'upcoming'}}
    Calculates projected percentage for each course and overall including expected OD credits.
    """
    projected_courses = []
    total_proj_th = 0
    total_proj_att = 0

    for c in courses:
        code = c.get('course_code', '')
        base_metrics = calculate_course_metrics(c, target_pct=target_pct, use_dl=use_dl)
        th = base_metrics['th']
        att = base_metrics['effective_attended']

        adj = adjustments.get(code, {})
        bunks = int(adj.get('bunk', 0))
        attended = int(adj.get('attend', 0))
        ods = int(adj.get('od', 0))
        od_type = adj.get('od_type', 'past')  # 'past' converts past absence to DL; 'upcoming' adds both TH and DL

        if od_type == 'upcoming':
            proj_th = th + bunks + attended + ods
            proj_att = att + attended + ods
        else:
            # Past recovery OD: boosts attended without increasing scheduled TH
            proj_th = th + bunks + attended
            proj_att = min(proj_th, att + attended + ods)

        proj_pct = round((proj_att / proj_th * 100) if proj_th > 0 else 0.0, 2)
        proj_status = 'safe' if proj_pct >= target_pct else ('warning' if proj_pct >= (target_pct - 10.0) else 'critical')

        diff = round(proj_pct - base_metrics['current_pct'], 2)

        course_result = dict(base_metrics)
        course_result.update({
            'simulated_bunks': bunks,
            'simulated_attended': attended,
            'simulated_ods': ods,
            'od_type': od_type,
            'projected_th': proj_th,
            'projected_att': proj_att,
            'projected_pct': proj_pct,
            'projected_status': proj_status,
            'pct_difference': diff
        })
        projected_courses.append(course_result)

        total_proj_th += proj_th
        total_proj_att += proj_att

    proj_overall_pct = round((total_proj_att / total_proj_th * 100) if total_proj_th > 0 else 0.0, 2)
    orig_overall_pct = overall.get('total_pct', 0.0) if overall else 0.0

    return {
        'courses': projected_courses,
        'overall': {
            'projected_th': total_proj_th,
            'projected_att': total_proj_att,
            'projected_pct': proj_overall_pct,
            'current_pct': orig_overall_pct,
            'difference': round(proj_overall_pct - orig_overall_pct, 2),
            'status': 'safe' if proj_overall_pct >= target_pct else ('warning' if proj_overall_pct >= (target_pct - 10.0) else 'critical')
        }
    }


def project_until_last_working_day(courses, timetable, start_date_str=None, last_working_day_str='2026-12-01', holidays=None, target_pct=75.0, use_dl=True):
    """
    Calculates exact remaining classes for each course between start_date and last_working_day
    using the weekly timetable.
    """
    if holidays is None:
        holidays = ['2026-11-28']

    try:
        if start_date_str:
            curr = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        else:
            curr = datetime.now().date()
        end_date = datetime.strptime(last_working_day_str, '%Y-%m-%d').date()
    except Exception:
        curr = datetime(2026, 11, 19).date()
        end_date = datetime(2026, 12, 1).date()

    if curr > end_date:
        curr = end_date - timedelta(days=12)

    day_counts = {'Monday': 0, 'Tuesday': 0, 'Wednesday': 0, 'Thursday': 0, 'Friday': 0, 'Saturday': 0, 'Sunday': 0}
    day_date_list = []

    iter_date = curr
    while iter_date <= end_date:
        d_str = iter_date.strftime('%Y-%m-%d')
        weekday_name = iter_date.strftime('%A')
        if d_str not in holidays and weekday_name != 'Sunday':
            day_counts[weekday_name] += 1
            day_date_list.append({
                'date': d_str,
                'day': weekday_name,
                'formatted': iter_date.strftime('%b %d, %Y (%a)')
            })
        iter_date += timedelta(days=1)

    classes_per_day = {d: {} for d in day_counts.keys()}
    for day, periods in timetable.items():
        clean_day = day.capitalize()
        if clean_day not in classes_per_day:
            continue
        for p in periods:
            code = p.get('course_code', '')
            if code and code != 'FREE' and not p.get('is_free'):
                classes_per_day[clean_day][code] = classes_per_day[clean_day].get(code, 0) + 1

    remaining_by_course = {}
    for c in courses:
        code = c.get('course_code', '')
        count = 0
        for day, occ in day_counts.items():
            periods_in_day = classes_per_day.get(day, {}).get(code, 0)
            count += occ * periods_in_day
        remaining_by_course[code] = count

    projections = []
    for c in courses:
        base = calculate_course_metrics(c, target_pct=target_pct, use_dl=use_dl)
        code = base['course_code']
        rem = remaining_by_course.get(code, 0)

        best_th = base['th'] + rem
        best_att = base['effective_attended'] + rem
        best_pct = round((best_att / best_th * 100) if best_th > 0 else base['current_pct'], 2)

        worst_th = base['th'] + rem
        worst_att = base['effective_attended']
        worst_pct = round((worst_att / worst_th * 100) if worst_th > 0 else base['current_pct'], 2)

        can_reach_target = best_pct >= target_pct

        if best_pct >= target_pct and best_th > 0:
            max_future_bunks = int(math.floor(best_att - (target_pct / 100.0) * best_th))
            max_future_bunks = min(rem, max(0, max_future_bunks))
        else:
            max_future_bunks = 0

        projections.append({
            'course_name': base['course_name'],
            'course_code': code,
            'current_th': base['th'],
            'current_att': base['effective_attended'],
            'current_pct': base['current_pct'],
            'status': base['status'],
            'remaining_classes': rem,
            'best_case_pct': best_pct,
            'worst_case_pct': worst_pct,
            'can_reach_target': can_reach_target,
            'max_future_bunks': max_future_bunks,
            'min_future_attend': max(0, rem - max_future_bunks),
            'ods_needed': base['ods_needed']
        })

    return {
        'start_date': curr.strftime('%Y-%m-%d'),
        'last_working_day': end_date.strftime('%Y-%m-%d'),
        'remaining_working_days': len(day_date_list),
        'days_breakdown': day_counts,
        'upcoming_dates': day_date_list,
        'course_projections': projections
    }
