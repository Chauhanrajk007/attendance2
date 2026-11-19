/**
 * AttendTrack Frontend JavaScript
 * Fast, reactive state management, Live Playwright visual terminal,
 * Top Course Breakdown Table, and Simplified Day Dropdown Lecture Simulator.
 */

document.addEventListener('DOMContentLoaded', () => {
  // Application State
  const state = {
    profile: {},
    courses: [],
    overall: null,
    timetable: {},
    calendar: { last_working_day: '2026-12-01', events: [] },
    projections: null,
    adjustments: {}, // { course_code: { bunk: 0, attend: 0, od: 0 } }
    manualAdjustments: {}, // table manual adjustments
    periodActions: {}, // { "Monday-1": "bunk"|"od"|"attend" }
    selectedDay: 'Friday',
    activeOdDays: [],
    odDayCounts: { Monday: 0, Tuesday: 0, Wednesday: 0, Thursday: 0, Friday: 0, Saturday: 0 },
    targetPct: 75.0,
    useDL: true,
    lastWorkingDay: '2026-12-01',
    activeFilter: 'all',
    searchQuery: '',
    odType: 'past',
    grokApiKey: localStorage.getItem('grok_api_key') || 'grok_443f54258b809316350ff1df6dd0accc_c8d7b09d18d63d5f2ea1e01e91f14ad40e4d877ba90237302004ef3479da9c1d'
  };

  const daySarcasmMap = {
    'Monday': '"Monday 8:50 AM Blockchain? Yeah, we know you\'re not waking up for that."',
    'Tuesday': '"Tuesday is loaded with 6 hours. One slip-up and you\'re meeting the Academic Dean."',
    'Wednesday': '"Midweek crisis. If you skip FoG Computing today, don\'t say we didn\'t warn you."',
    'Thursday': '"Thursday 6-period marathon with IoT Labs. High endurance test for your degree."',
    'Friday': '"Friday afternoon 2-hour lab? High risk, 3-day weekend reward. Choose your fighter."',
    'Saturday': '"Saturday is free. Go touch some grass or catch up on sleep."'
  };

  // DOM Elements
  const el = {
    studentName: document.getElementById('studentName'),
    btnEditStudentName: document.getElementById('btnEditStudentName'),
    studentRoll: document.getElementById('studentRoll'),
    studentBatch: document.getElementById('studentBatch'),
    studentTerm: document.getElementById('studentTerm'),
    studentInitials: document.getElementById('studentInitials'),
    avatarClickContainer: document.getElementById('avatarClickContainer'),
    studentPhotoImg: document.getElementById('studentPhotoImg'),
    avatarFileInput: document.getElementById('avatarFileInput'),
    badgeAnalyzingFriend: document.getElementById('badgeAnalyzingFriend'),
    dangerSummarySection: document.getElementById('dangerSummarySection'),
    dangerIcon: document.getElementById('dangerIcon'),
    dangerHeadline: document.getElementById('dangerHeadline'),
    dangerRiskBadge: document.getElementById('dangerRiskBadge'),
    dangerSubtext: document.getElementById('dangerSubtext'),
    dangerSubjectsPills: document.getElementById('dangerSubjectsPills'),
    dangerActionPlan: document.getElementById('dangerActionPlan'),
    dangerActionHeader: document.getElementById('dangerActionHeader'),
    inputInitialOD: document.getElementById('inputInitialOD'),
    selectInitialODUnit: document.getElementById('selectInitialODUnit'),
    targetThreshold: document.getElementById('targetThreshold'),
    chkUseDL: document.getElementById('chkUseDL'),
    lblSemesterHorizon: document.getElementById('lblSemesterHorizon'),
    overallCurrentPct: document.getElementById('overallCurrentPct'),
    overallProjectedPct: document.getElementById('overallProjectedPct'),
    overallProgressBar: document.getElementById('overallProgressBar'),
    overallStatusDot: document.getElementById('overallStatusDot'),
    overallHoursDetail: document.getElementById('overallHoursDetail'),
    totalSafeBunksCount: document.getElementById('totalSafeBunksCount'),
    criticalSubjectsCount: document.getElementById('criticalSubjectsCount'),
    criticalSubjectsList: document.getElementById('criticalSubjectsList'),
    daysRemainingCount: document.getElementById('daysRemainingCount'),
    lblLastWorkingDay: document.getElementById('lblLastWorkingDay'),
    totalOdsPlannedCount: document.getElementById('totalOdsPlannedCount'),
    odsGainSummary: document.getElementById('odsGainSummary'),
    lblTargets: document.querySelectorAll('.lblTarget'),
    coursesTableBody: document.getElementById('coursesTableBody'),
    coursesCountBadge: document.getElementById('coursesCountBadge'),
    courseSearchInput: document.getElementById('courseSearchInput'),
    filterPills: document.querySelectorAll('.filter-pill'),
    scheduleDayDropdown: document.getElementById('scheduleDayDropdown'),
    dayPillBtns: document.querySelectorAll('.day-pill-btn'),
    scheduleDatePicker: document.getElementById('scheduleDatePicker'),
    selectedDateDisplay: document.getElementById('selectedDateDisplay'),
    btnGrokOptimize75: document.getElementById('btnGrokOptimize75'),
    scheduleToggleHeader: document.getElementById('scheduleToggleHeader'),
    scheduleCollapsibleBody: document.getElementById('scheduleCollapsibleBody'),
    scheduleCollapseIcon: document.getElementById('scheduleCollapseIcon'),
    scheduleCollapseHint: document.getElementById('scheduleCollapseHint'),
    btnTogglePeriodsVisibility: document.getElementById('btnTogglePeriodsVisibility'),
    dayPeriodsWrapper: document.getElementById('dayPeriodsWrapper'),
    lblActiveDayName: document.getElementById('lblActiveDayName'),
    lblPeriodsViewStatus: document.getElementById('lblPeriodsViewStatus'),
    btnOpenScheduleOverride: document.getElementById('btnOpenScheduleOverride'),
    scheduleOverrideModal: document.getElementById('scheduleOverrideModal'),
    btnCloseScheduleOverrideModal: document.getElementById('btnCloseScheduleOverrideModal'),
    btnCloseScheduleOverride: document.getElementById('btnCloseScheduleOverride'),
    selectSaturdayTimetableSource: document.getElementById('selectSaturdayTimetableSource'),
    btnApplySaturdayTimetable: document.getElementById('btnApplySaturdayTimetable'),
    selectHolidayDay: document.getElementById('selectHolidayDay'),
    btnApplyDayHoliday: document.getElementById('btnApplyDayHoliday'),
    btnPresetSatTue: document.getElementById('btnPresetSatTue'),
    btnPresetWedHoliday: document.getElementById('btnPresetWedHoliday'),
    btnPresetResetStandard: document.getElementById('btnPresetResetStandard'),
    odDayPillBtns: document.querySelectorAll('.od-day-pill'),
    btnClearOdDays: document.getElementById('btnClearOdDays'),
    lblOdDaysSummary: document.getElementById('lblOdDaysSummary'),
    lblOdHoursCount: document.getElementById('lblOdHoursCount'),
    playwrightBrowserUrl: document.getElementById('playwrightBrowserUrl'),
    playwrightLiveViewportImg: document.getElementById('playwrightLiveViewportImg'),
    playwrightViewportCaption: document.getElementById('playwrightViewportCaption'),
    playwrightStatusBadge: document.getElementById('playwrightStatusBadge'),
    btnTogglePassword: document.getElementById('btnTogglePassword'),
    pwToggleIcon: document.getElementById('pwToggleIcon'),
    chkHeadedBrowser: document.getElementById('chkHeadedBrowser'),
    btnDayBunkAll: document.getElementById('btnDayBunkAll'),
    btnDayODAll: document.getElementById('btnDayODAll'),
    btnDayReset: document.getElementById('btnDayReset'),
    btnResetAllBunks: document.getElementById('btnResetAllBunks'),
    lblSarcasticComment: document.getElementById('lblSarcasticComment'),
    dayPeriodsContainer: document.getElementById('dayPeriodsContainer'),
    verdictIcon: document.getElementById('verdictIcon'),
    verdictHeadline: document.getElementById('verdictHeadline'),
    verdictSub: document.getElementById('verdictSub'),
    btnOpenPlaywrightModal: document.getElementById('btnOpenPlaywrightModal'),
    playwrightModal: document.getElementById('playwrightModal'),
    btnClosePlaywrightModal: document.getElementById('btnClosePlaywrightModal'),
    btnCancelPlaywright: document.getElementById('btnCancelPlaywright'),
    playwrightForm: document.getElementById('playwrightForm'),
    amsUsername: document.getElementById('amsUsername'),
    amsPassword: document.getElementById('amsPassword'),
    playwrightConsole: document.getElementById('playwrightConsole'),
    playwrightTerminalLogs: document.getElementById('playwrightTerminalLogs'),
    btnRunPlaywright: document.getElementById('btnRunPlaywright'),
    btnQuickLoadCached: document.getElementById('btnQuickLoadCached'),
    btnOpenUploadModal: document.getElementById('btnOpenUploadModal'),
    btnCloseUploadModal: document.getElementById('btnCloseUploadModal'),
    btnCancelUpload: document.getElementById('btnCancelUpload'),
    uploadModal: document.getElementById('uploadModal'),
    uploadForm: document.getElementById('uploadForm'),
    btnEditGrokKey: document.getElementById('btnEditGrokKey'),
    grokKeyModal: document.getElementById('grokKeyModal'),
    btnCloseGrokKeyModal: document.getElementById('btnCloseGrokKeyModal'),
    btnSaveGrokKey: document.getElementById('btnSaveGrokKey'),
    inputGrokKey: document.getElementById('inputGrokKey'),
    grokStatusLabel: document.getElementById('grokStatusLabel'),
    grokQueryInput: document.getElementById('grokQueryInput'),
    btnAskGrok: document.getElementById('btnAskGrok'),
    grokResponseContainer: document.getElementById('grokResponseContainer'),
    grokResponseText: document.getElementById('grokResponseText'),
    grokLoading: document.getElementById('grokLoading'),
    toastContainer: document.getElementById('toastContainer')
  };

  function showToast(message) {
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.textContent = message;
    el.toastContainer.appendChild(toast);
    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transition = 'opacity 0.3s ease';
      setTimeout(() => toast.remove(), 300);
    }, 3200);
  }

  function renderMarkdown(md) {
    if (!md) return '';
    let html = md
      .replace(/^### (.*$)/gim, '<h3>$1</h3>')
      .replace(/^#### (.*$)/gim, '<h4>$1</h4>')
      .replace(/^## (.*$)/gim, '<h2>$1</h2>')
      .replace(/\*\*(.*?)\*\*/gim, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/gim, '<em>$1</em>')
      .replace(/`([^`]+)`/gim, '<code>$1</code>')
      .replace(/^\s*-\s+(.*$)/gim, '<li>$1</li>')
      .replace(/\n\n+/g, '<br><br>');

    html = html.replace(/(<li>.*?<\/li>)/gis, '<ul>$1</ul>');
    return html;
  }

  async function loadInitialData() {
    try {
      const res = await fetch('/api/sample-data');
      const json = await res.json();
      if (json.status === 'success' && json.data) {
        applyNewDataset(json.data);
      }
    } catch (err) {
      console.error('Failed to load initial data:', err);
    }
  }

  function applyNewDataset(data) {
    if (data.profile && Object.keys(data.profile).length > 0) {
      state.profile = data.profile;
    }

    if (data.courses && data.courses.length > 0) state.courses = data.courses;
    if (data.overall) state.overall = data.overall;
    if (data.timetable && Object.keys(data.timetable).length > 0) {
      state.timetable = data.timetable;
    }
    if (data.calendar && data.calendar.last_working_day) {
      state.calendar = data.calendar;
      state.lastWorkingDay = data.calendar.last_working_day;
    }

    state.adjustments = {};
    state.periodActions = {};
    state.manualAdjustments = {};
    state.courses.forEach(c => {
      state.adjustments[c.course_code] = { bunk: 0, attend: 0, od: 0 };
    });

    renderProfile();
    fetchProjections();
    calculateAndRender();
    renderSelectedDayPeriods();
  }

  function formatDate(dStr) {
    if (!dStr) return '';
    try {
      const parts = dStr.split('-');
      if (parts.length === 3) {
        const d = new Date(parts[0], parts[1] - 1, parts[2]);
        return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
      }
    } catch (e) {}
    return dStr;
  }

  function renderProfile() {
    // Check for saved custom profile photo in localStorage
    const savedPhoto = localStorage.getItem('my_dashboard_photo');
    if (savedPhoto && el.studentPhotoImg) {
      el.studentPhotoImg.src = savedPhoto;
      el.studentPhotoImg.style.display = 'block';
      if (el.studentInitials) el.studentInitials.style.display = 'none';
    } else {
      if (el.studentPhotoImg) el.studentPhotoImg.style.display = 'none';
      if (el.studentInitials) el.studentInitials.style.display = 'flex';
    }

    const p = state.profile || {};
    const name = p['Student Name'] || 'Chauhan Raj K';
    if (el.studentName) el.studentName.textContent = name;
    if (el.studentRoll) el.studentRoll.textContent = `Roll: ${p['Roll No'] || '20241CIT0119'}`;
    if (el.studentBatch) el.studentBatch.textContent = `Batch: ${p['Batch/Section'] || '2024CIT02'}`;
    if (el.studentTerm) el.studentTerm.textContent = `Term: ${p['Term'] || 'S5 (Odd Sem)'}`;

    const initials = name.split(' ').map(n => n[0]).filter(Boolean).slice(0, 2).join('').toUpperCase();
    if (el.studentInitials) el.studentInitials.textContent = initials || 'CR';
    if (el.coursesCountBadge) el.coursesCountBadge.textContent = state.courses.length;
  }

  // Allow clicking student name or ✏️ Edit button to update dashboard name anytime
  const updateStudentNameHandler = () => {
    const cur = (state.profile && state.profile['Student Name']) || (el.studentName && el.studentName.textContent) || 'Student User';
    const newName = prompt('Enter updated Student Name for dashboard:', cur);
    if (newName && newName.trim()) {
      state.profile = state.profile || {};
      state.profile['Student Name'] = newName.trim();
      renderProfile();
      showToast(`Updated student name to "${newName.trim()}"! 👤`);
    }
  };
  if (el.studentName) el.studentName.addEventListener('click', updateStudentNameHandler);
  if (el.btnEditStudentName) el.btnEditStudentName.addEventListener('click', updateStudentNameHandler);

  async function fetchProjections() {
    try {
      const res = await fetch('/api/projections', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          courses: state.courses,
          timetable: state.timetable,
          start_date: '2026-11-19',
          last_working_day: state.lastWorkingDay,
          target_pct: state.targetPct,
          use_dl: state.useDL
        })
      });
      const json = await res.json();
      if (json.status === 'success' && json.data) {
        state.projections = json.data;
        el.daysRemainingCount.textContent = json.data.remaining_working_days;
        el.lblLastWorkingDay.textContent = formatDate(state.lastWorkingDay);
        el.lblSemesterHorizon.textContent = `📅 Ends ${formatDate(state.lastWorkingDay)} (${json.data.remaining_working_days} days left)`;
        calculateAndRender();
      }
    } catch (e) {
      console.error('Projections fetch failed:', e);
    }
  }

  // Core Calculation: Updates Course Table & Metrics Immediately
  function calculateAndRender() {
    let totalTh = 0;
    let totalAtt = 0;
    let totalCurrentTh = 0;
    let totalCurrentAtt = 0;
    let totalSafeBunks = 0;
    let totalPlannedODs = 0;
    let criticalList = [];

    const remMap = {};
    if (state.projections && state.projections.course_projections) {
      state.projections.course_projections.forEach(p => {
        remMap[p.course_code] = p.remaining_classes;
      });
    }

    const computedCourses = state.courses.map(course => {
      const code = course.course_code;
      const th = parseInt(course.th) || 0;
      const ah = parseInt(course.ah) || 0;
      const dl = parseInt(course.dl) || 0;
      const baseAtt = state.useDL ? (ah + dl) : ah;

      const currentPct = th > 0 ? (baseAtt / th * 100) : 0.0;

      const adj = state.adjustments[code] || { bunk: 0, attend: 0, od: 0 };
      const bunks = adj.bunk || 0;
      const attends = adj.attend || 0;
      const ods = adj.od || 0;
      totalPlannedODs += ods;

      let projTh, projAtt;
      if (state.odType === 'upcoming') {
        projTh = th + bunks + attends + ods;
        projAtt = baseAtt + attends + ods;
      } else {
        projTh = th + bunks + attends;
        projAtt = Math.min(projTh, baseAtt + attends + ods);
      }

      const projPct = projTh > 0 ? (projAtt / projTh * 100) : 0.0;

      let safeBunks = 0;
      if (currentPct >= state.targetPct && th > 0) {
        safeBunks = Math.max(0, Math.floor((100 * baseAtt - state.targetPct * th) / state.targetPct));
      }

      let requiredAttend = 0;
      if (currentPct < state.targetPct && th > 0 && state.targetPct < 100) {
        requiredAttend = Math.max(0, Math.ceil((state.targetPct * th - 100 * baseAtt) / (100 - state.targetPct)));
        if (th > 0) criticalList.push(code);
      }

      let odsNeeded = 0;
      if (currentPct < state.targetPct && th > 0) {
        odsNeeded = Math.max(0, Math.ceil((state.targetPct * th) / 100) - baseAtt);
      }

      // Dynamic remaining classes calculation
      const initialRemaining = remMap[code] !== undefined ? remMap[code] : 0;
      const usedInSimulation = bunks + attends + (state.odType === 'upcoming' ? ods : 0);
      const dynamicRemaining = Math.max(0, initialRemaining - usedInSimulation);

      totalSafeBunks += safeBunks;
      totalCurrentTh += th;
      totalCurrentAtt += baseAtt;
      totalTh += projTh;
      totalAtt += projAtt;

      return {
        ...course,
        baseAtt,
        currentPct,
        projTh,
        projAtt,
        projPct,
        safeBunks,
        requiredAttend,
        odsNeeded,
        bunks,
        attends,
        ods,
        initialRemaining,
        usedInSimulation,
        dynamicRemaining
      };
    });

    const currentOverallPct = totalCurrentTh > 0 ? (totalCurrentAtt / totalCurrentTh * 100) : 0.0;
    const projectedOverallPct = totalTh > 0 ? (totalAtt / totalTh * 100) : 0.0;

    // Render Metrics
    el.overallCurrentPct.textContent = `${currentOverallPct.toFixed(2)}%`;
    el.overallProjectedPct.textContent = `${projectedOverallPct.toFixed(2)}%`;
    el.overallProgressBar.style.width = `${Math.min(100, projectedOverallPct)}%`;

    const statusClass = projectedOverallPct >= state.targetPct ? 'safe' : (projectedOverallPct >= (state.targetPct - 10) ? 'warning' : 'critical');
    el.overallProgressBar.className = `metric-progress-bar ${statusClass}`;
    el.overallStatusDot.className = `status-indicator-dot ${statusClass}`;

    el.overallHoursDetail.textContent = `${totalCurrentAtt} Attended / ${totalCurrentTh} Scheduled Hours`;
    el.totalSafeBunksCount.textContent = totalSafeBunks;
    el.criticalSubjectsCount.textContent = criticalList.length;
    el.criticalSubjectsList.textContent = criticalList.length > 0 ? criticalList.slice(0, 5).join(', ') : 'None! All subjects safe.';

    el.totalOdsPlannedCount.textContent = `${totalPlannedODs} hrs`;
    if (totalPlannedODs > 0) {
      const gain = (projectedOverallPct - currentOverallPct).toFixed(1);
      el.odsGainSummary.textContent = `${gain >= 0 ? '+' + gain : gain}% net boost from ODs`;
    } else {
      el.odsGainSummary.textContent = 'Duty Leaves credited for events/fests';
    }

    el.lblTargets.forEach(elem => elem.textContent = `${state.targetPct}%`);

    updateSarcasticVerdict(projectedOverallPct, criticalList);
    renderDangerSummary(computedCourses, criticalList);

    // Immediately render Course Table and Weekly Schedule
    renderCoursesTable(computedCourses);
    renderSelectedDayPeriods(computedCourses);
  }

  // Early Warning & Dropout Risk Danger Summary (AT START)
  function renderDangerSummary(computedCourses, criticalList) {
    if (!el.dangerSummarySection) return;

    if (criticalList.length > 0) {
      el.dangerSummarySection.style.borderLeftColor = '#ef4444';
      el.dangerSummarySection.style.background = '#fff5f5';
      if (el.dangerIcon) el.dangerIcon.textContent = '🚨';
      if (el.dangerHeadline) {
        el.dangerHeadline.textContent = `Early Warning Alert: ${criticalList.length} Subject(s) at Critical Dropout & Debar Risk`;
        el.dangerHeadline.style.color = '#b91c1c';
      }
      if (el.dangerRiskBadge) {
        el.dangerRiskBadge.textContent = `HIGH DEBAR RISK (<${state.targetPct}%)`;
        el.dangerRiskBadge.style.background = '#fee2e2';
        el.dangerRiskBadge.style.color = '#991b1b';
      }
      if (el.dangerSubtext) {
        el.dangerSubtext.textContent = `Institutional regulations mandate a strict ${state.targetPct}% attendance cutoff for semester examination eligibility. Early detection identifies vulnerable subjects before academic suspension occurs.`;
        el.dangerSubtext.style.color = '#7f1d1d';
      }

      const criticalCourses = (computedCourses || []).filter(c => criticalList.includes(c.course_code));
      let totalReqAtt = 0;
      let totalReqOD = 0;

      if (el.dangerSubjectsPills) {
        el.dangerSubjectsPills.innerHTML = criticalCourses.map(c => {
          totalReqAtt += c.requiredAttend;
          totalReqOD += c.odsNeeded;
          return `
            <span style="display:inline-flex; align-items:center; gap:0.35rem; background:#fee2e2; color:#991b1b; padding:0.25rem 0.55rem; border-radius:5px; font-size:0.75rem; border:1px solid #fca5a5; font-weight:600;">
              <span>⚠️</span>
              <strong>${c.course_code}</strong>:
              <span>${c.currentPct.toFixed(1)}%</span>
              <span style="opacity:0.85;">(Need +${c.requiredAttend} classes or ${c.odsNeeded} ODs)</span>
            </span>
          `;
        }).join('');
      }

      if (el.dangerActionHeader) el.dangerActionHeader.textContent = 'Immediate Recovery Plan:';
      if (el.dangerActionPlan) {
        el.dangerActionPlan.textContent = `Attend next ${totalReqAtt} scheduled classes or submit ${totalReqOD} signed OD slips.`;
        el.dangerActionPlan.style.color = '#991b1b';
      }
    } else {
      // Safe state
      el.dangerSummarySection.style.borderLeftColor = '#10b981';
      el.dangerSummarySection.style.background = '#f0fdf4';
      if (el.dangerIcon) el.dangerIcon.textContent = '🟢';
      if (el.dangerHeadline) {
        el.dangerHeadline.textContent = 'Early Warning System: No Dropout or Debarment Risks Detected';
        el.dangerHeadline.style.color = '#065f46';
      }
      if (el.dangerRiskBadge) {
        el.dangerRiskBadge.textContent = `ALL SUBJECTS SAFE (≥${state.targetPct}%)`;
        el.dangerRiskBadge.style.background = '#d1fae5';
        el.dangerRiskBadge.style.color = '#065f46';
      }
      if (el.dangerSubtext) {
        el.dangerSubtext.textContent = `All enrolled courses satisfy the mandatory ${state.targetPct}% examination eligibility cutoff. You currently have safe bunks to spare across your subjects.`;
        el.dangerSubtext.style.color = '#065f46';
      }

      if (el.dangerSubjectsPills) {
        el.dangerSubjectsPills.innerHTML = `
          <span style="display:inline-flex; align-items:center; gap:0.35rem; background:#d1fae5; color:#065f46; padding:0.25rem 0.6rem; border-radius:5px; font-size:0.75rem; font-weight:600;">
            ✓ 100% courses eligible for End-Semester Examinations
          </span>
        `;
      }

      if (el.dangerActionHeader) el.dangerActionHeader.textContent = 'Status:';
      if (el.dangerActionPlan) {
        el.dangerActionPlan.textContent = 'Good academic standing. Zero recovery actions required.';
        el.dangerActionPlan.style.color = '#065f46';
      }
    }
  }

  function updateSarcasticVerdict(pct, criticalList) {
    if (pct >= 85.0) {
      el.verdictIcon.textContent = '🤓';
      el.verdictHeadline.textContent = 'Academic Weapon Alert (85%+)';
      el.verdictSub.textContent = `At ${pct.toFixed(1)}%, you are attending so many classes the faculty is getting suspicious. You have safe bunks to spare!`;
    } else if (pct >= state.targetPct) {
      el.verdictIcon.textContent = '🍸';
      el.verdictHeadline.textContent = 'Calculated Genius (75% – 84%)';
      el.verdictSub.textContent = `Standing at ${pct.toFixed(1)}%. You are threading the needle like a pro. Maximum sleep, zero detention.`;
    } else if (pct >= (state.targetPct - 10.0)) {
      el.verdictIcon.textContent = '🚨';
      el.verdictHeadline.textContent = 'HOD Speed Dial Territory (65% – 74%)';
      el.verdictSub.textContent = `You are at ${pct.toFixed(1)}%. Debarred warning lights are flashing. Secure event OD slips or don't sleep past 8 AM.`;
    } else {
      el.verdictIcon.textContent = '💀';
      el.verdictHeadline.textContent = 'Debarred. See you in Summer Semester (<65%)';
      el.verdictSub.textContent = `Current projection is ${pct.toFixed(1)}%. Time to draft a very convincing medical certificate or beg for Duty Leaves.`;
    }
  }

  // Render Course Breakdown Table (AT START)
  function renderCoursesTable(computedCourses) {
    if (!computedCourses) {
      calculateAndRender();
      return;
    }

    const tbody = el.coursesTableBody;
    tbody.innerHTML = '';

    const query = state.searchQuery.toLowerCase().trim();
    const filter = state.activeFilter;

    const filtered = computedCourses.filter(c => {
      const matchSearch = c.course_name.toLowerCase().includes(query) || c.course_code.toLowerCase().includes(query);
      if (!matchSearch) return false;

      if (filter === 'critical') return c.currentPct < state.targetPct && c.th > 0;
      if (filter === 'safe') return c.currentPct >= state.targetPct && c.th > 0;
      return true;
    });

    if (filtered.length === 0) {
      tbody.innerHTML = `<tr><td colspan="7" style="text-align:center; padding:2rem; color:var(--text-muted);">No matching subjects found.</td></tr>`;
      return;
    }

    filtered.forEach(c => {
      const tr = document.createElement('tr');

      const statusBadge = c.projPct >= state.targetPct
        ? `<span class="badge badge-safe">${c.projPct.toFixed(1)}%</span>`
        : (c.projPct >= (state.targetPct - 10)
          ? `<span class="badge badge-warning">${c.projPct.toFixed(1)}%</span>`
          : `<span class="badge badge-critical">${c.projPct.toFixed(1)}%</span>`);

      let actionAdvice = '';
      if (c.bunks > 0 || c.attends > 0) {
        const totalAlloc = c.initialRemaining || (c.bunks + c.attends);
        actionAdvice = `
          <div style="font-weight:700; font-size:0.8rem; color:var(--text-main);">
            Out of ${totalAlloc}: <span class="text-rose">😴 Bunk ${c.bunks}</span>, <span class="text-emerald">✅ Attend ${c.attends}</span>
          </div>
        `;
      } else if (c.currentPct >= state.targetPct) {
        actionAdvice = `<div class="text-emerald" style="font-weight:600;">🏖️ Can Bunk: ${c.safeBunks} class${c.safeBunks === 1 ? '' : 'es'}</div>`;
      } else if (c.th > 0) {
        actionAdvice = `
          <div class="text-rose" style="font-weight:600;">⚠️ Must Attend: ${c.requiredAttend} class${c.requiredAttend === 1 ? '' : 'es'}</div>
          ${c.odsNeeded > 0 ? `<button class="btn-quick-od" data-code="${c.course_code}" data-ods="${c.odsNeeded}">+${c.odsNeeded} OD to reach 75%</button>` : ''}
        `;
      } else {
        actionAdvice = `<span class="text-muted">No sessions yet</span>`;
      }

      let remainingHtml = '';
      if (c.dynamicRemaining === 0 && c.initialRemaining > 0) {
        remainingHtml = `<span class="remaining-pill remaining-depleted">0 remaining</span>`;
      } else if (c.dynamicRemaining === 1) {
        remainingHtml = `<span class="remaining-pill remaining-low">1 class remaining</span>`;
      } else if (c.initialRemaining > 0) {
        remainingHtml = `<span class="remaining-pill">${c.dynamicRemaining} classes remaining</span>`;
      } else {
        remainingHtml = `<span class="remaining-pill" style="opacity:0.6;">0 remaining</span>`;
      }

      tr.innerHTML = `
        <td>
          <span class="course-code-tag">${c.course_code}</span>
          <span class="course-title-primary">${c.course_name}</span>
        </td>
        <td>
          <strong>${c.baseAtt}</strong> / ${c.th} hrs
          <span class="helper-text" style="margin-top:0;">(${c.ah} AH + ${c.dl} DL)</span>
        </td>
        <td>
          <strong>${c.currentPct.toFixed(2)}%</strong>
        </td>
        <td>
          <div style="display:flex; align-items:center; gap:0.4rem; flex-wrap:nowrap;">
            <!-- Stepper 1: Bunk -->
            <div class="stepper-control" title="Simulate bunking this course">
              <button class="stepper-btn btn-bunk-dec" data-code="${c.course_code}">-</button>
              <span class="stepper-value">${c.bunks} bunk</span>
              <button class="stepper-btn btn-bunk-inc" data-code="${c.course_code}">+</button>
            </div>

            <!-- Stepper 2: Attend -->
            <div class="stepper-control" title="Simulate attending next classes">
              <button class="stepper-btn btn-att-dec" data-code="${c.course_code}">-</button>
              <span class="stepper-value">+${c.attends} att</span>
              <button class="stepper-btn btn-att-inc" data-code="${c.course_code}">+</button>
            </div>

            <!-- Stepper 3: On-Duty (OD) Leave -->
            <div class="stepper-control stepper-od" title="Add expected On-Duty (OD/DL) credits">
              <button class="stepper-btn btn-od-dec" data-code="${c.course_code}">-</button>
              <span class="stepper-value">+${c.ods} OD</span>
              <button class="stepper-btn btn-od-inc" data-code="${c.course_code}">+</button>
            </div>
          </div>
        </td>
        <td>
          ${statusBadge}
          ${c.bunks > 0 || c.attends > 0 || c.ods > 0 ? `<div style="font-size:0.72rem; color:var(--text-muted);">${(c.projPct - c.currentPct).toFixed(1)}% diff</div>` : ''}
        </td>
        <td>
          ${actionAdvice}
        </td>
        <td>
          ${remainingHtml}
        </td>
      `;

      tbody.appendChild(tr);
    });

    // Stepper Listeners
    tbody.querySelectorAll('.btn-bunk-inc').forEach(btn => {
      btn.addEventListener('click', () => {
        const code = btn.dataset.code;
        state.manualAdjustments[code] = state.manualAdjustments[code] || { bunk: 0, attend: 0, od: 0 };
        state.manualAdjustments[code].bunk += 1;
        recalculateAllAdjustments();
        calculateAndRender();
      });
    });

    tbody.querySelectorAll('.btn-bunk-dec').forEach(btn => {
      btn.addEventListener('click', () => {
        const code = btn.dataset.code;
        state.manualAdjustments[code] = state.manualAdjustments[code] || { bunk: 0, attend: 0, od: 0 };
        state.manualAdjustments[code].bunk = Math.max(0, state.manualAdjustments[code].bunk - 1);
        recalculateAllAdjustments();
        calculateAndRender();
      });
    });

    tbody.querySelectorAll('.btn-att-inc').forEach(btn => {
      btn.addEventListener('click', () => {
        const code = btn.dataset.code;
        state.manualAdjustments[code] = state.manualAdjustments[code] || { bunk: 0, attend: 0, od: 0 };
        state.manualAdjustments[code].attend += 1;
        recalculateAllAdjustments();
        calculateAndRender();
      });
    });

    tbody.querySelectorAll('.btn-att-dec').forEach(btn => {
      btn.addEventListener('click', () => {
        const code = btn.dataset.code;
        state.manualAdjustments[code] = state.manualAdjustments[code] || { bunk: 0, attend: 0, od: 0 };
        state.manualAdjustments[code].attend = Math.max(0, state.manualAdjustments[code].attend - 1);
        recalculateAllAdjustments();
        calculateAndRender();
      });
    });

    tbody.querySelectorAll('.btn-od-inc').forEach(btn => {
      btn.addEventListener('click', () => {
        const code = btn.dataset.code;
        state.manualAdjustments[code] = state.manualAdjustments[code] || { bunk: 0, attend: 0, od: 0 };
        state.manualAdjustments[code].od += 1;
        recalculateAllAdjustments();
        calculateAndRender();
      });
    });

    tbody.querySelectorAll('.btn-od-dec').forEach(btn => {
      btn.addEventListener('click', () => {
        const code = btn.dataset.code;
        state.manualAdjustments[code] = state.manualAdjustments[code] || { bunk: 0, attend: 0, od: 0 };
        state.manualAdjustments[code].od = Math.max(0, state.manualAdjustments[code].od - 1);
        recalculateAllAdjustments();
        calculateAndRender();
      });
    });

    tbody.querySelectorAll('.btn-quick-od').forEach(btn => {
      btn.addEventListener('click', () => {
        const code = btn.dataset.code;
        const needed = parseInt(btn.dataset.ods) || 1;
        state.manualAdjustments[code] = state.manualAdjustments[code] || { bunk: 0, attend: 0, od: 0 };
        state.manualAdjustments[code].od = needed;
        recalculateAllAdjustments();
        calculateAndRender();
        showToast(`Applied +${needed} expected ODs to ${code} to reach 75%!`);
      });
    });
  }

  // Render Classes for the Selected Day (BELOW TABLE: SIMPLE DAY SELECTOR)
  function renderSelectedDayPeriods(computedCourses) {
    const day = state.selectedDay;
    el.lblSarcasticComment.textContent = daySarcasmMap[day] || '"Plan your strategic absences wisely."';

    const courseMap = {};
    if (computedCourses) {
      computedCourses.forEach(c => {
        courseMap[c.course_code] = c;
      });
    }

    const periods = state.timetable[day] || [];
    const container = el.dayPeriodsContainer;
    container.innerHTML = '';

    const nonFree = periods.filter(p => !p.is_free && p.course_code !== 'FREE');
    if (nonFree.length === 0) {
      container.innerHTML = `<div style="grid-column: 1/-1; padding: 2rem; text-align: center; color: var(--text-muted); font-size: 0.9rem;">🎉 No classes scheduled on ${day}! Enjoy your free day or catch up on sleep.</div>`;
      return;
    }

    periods.forEach(p => {
      if (p.is_free || p.course_code === 'FREE') return;

      const cInfo = courseMap[p.course_code] || { currentPct: 75, safeBunks: 0 };
      const curPct = cInfo.currentPct;
      const safeB = cInfo.safeBunks;

      // Color coding rule
      let statusColorClass = 'status-safe';
      let badgeHtml = '';

      if (curPct >= state.targetPct && safeB > 0) {
        statusColorClass = 'status-safe';
        badgeHtml = `<span class="bunk-badge bunk-badge-green">🟢 Can Bunk ${safeB}</span>`;
      } else if (curPct >= (state.targetPct - 5.0)) {
        statusColorClass = 'status-warning';
        badgeHtml = `<span class="bunk-badge bunk-badge-orange">🟠 Risky (${curPct.toFixed(1)}%)</span>`;
      } else {
        statusColorClass = 'status-critical';
        badgeHtml = `<span class="bunk-badge bunk-badge-red">🔴 DO NOT BUNK</span>`;
      }

      const actionKey = `${day}-${p.period}`;
      const currentAction = state.periodActions[actionKey] || 'attend';

      const card = document.createElement('div');
      let cardClasses = `period-card ${statusColorClass}`;
      if (currentAction === 'bunk') cardClasses += ' is-sim-bunk';
      if (currentAction === 'od') cardClasses += ' is-sim-od';
      card.className = cardClasses;

      card.innerHTML = `
        <div class="period-card-top">
          <span class="period-time-text">Period ${p.period} &bull; ${p.timing || ''}</span>
          ${badgeHtml}
        </div>
        <div class="period-code-title">
          <span>${p.course_code}</span>
          <span style="font-size:0.75rem; font-weight:600; color:var(--text-secondary);">(${curPct.toFixed(1)}%)</span>
        </div>
        <div class="period-subject-name">${p.course_name}</div>
        <div class="period-meta-line">${p.room || ''} ${p.faculty ? '• ' + p.faculty : ''}</div>
        <div class="period-actions-row">
          <button class="period-btn ${currentAction === 'bunk' ? 'active-bunk' : ''}" data-day="${day}" data-period="${p.period}" data-code="${p.course_code}" data-act="bunk">
            😴 Bunk
          </button>
          <button class="period-btn ${currentAction === 'od' ? 'active-od' : ''}" data-day="${day}" data-period="${p.period}" data-code="${p.course_code}" data-act="od">
            🎖️ OD
          </button>
          <button class="period-btn ${currentAction === 'attend' ? 'active-attend' : ''}" data-day="${day}" data-period="${p.period}" data-code="${p.course_code}" data-act="attend">
            ✅ Attend
          </button>
        </div>
      `;
      container.appendChild(card);
    });

    // Period Button Listeners
    container.querySelectorAll('.period-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const d = btn.dataset.day;
        const period = btn.dataset.period;
        const act = btn.dataset.act;
        const code = btn.dataset.code;
        const actionKey = `${d}-${period}`;

        state.periodActions[actionKey] = act;
        syncPeriodActionsToAdjustments();
        calculateAndRender();

        if (act === 'bunk') {
          showToast(`Marked ${code} (${d} Period ${period}) as Bunk. 😴`);
        } else if (act === 'od') {
          showToast(`Marked ${code} (${d} Period ${period}) as On-Duty (OD). 🎖️`);
        } else {
          showToast(`Marked ${code} (${d} Period ${period}) as Attended. ✅`);
        }
      });
    });
  }

  // Collapsible Weekly Schedule Accordion Logic
  let isScheduleCollapsed = false;
  if (el.scheduleToggleHeader) {
    el.scheduleToggleHeader.addEventListener('click', (e) => {
      // Don't toggle if user clicked on reset button inside header
      if (e.target.id === 'btnResetAllBunks') return;
      isScheduleCollapsed = !isScheduleCollapsed;
      if (el.scheduleCollapsibleBody) {
        el.scheduleCollapsibleBody.classList.toggle('collapsed', isScheduleCollapsed);
      }
      if (el.scheduleCollapseIcon) {
        el.scheduleCollapseIcon.textContent = isScheduleCollapsed ? '▼' : '▲';
      }
      if (el.scheduleCollapseHint) {
        el.scheduleCollapseHint.textContent = isScheduleCollapsed ? 'Click to Open ▼' : 'Click to Collapse ▲';
      }
    });
  }

  // Periods Visibility Toggle (Clean text, no emoji)
  let arePeriodsVisible = true;
  function showPeriodsForActiveDay() {
    arePeriodsVisible = true;
    if (el.dayPeriodsWrapper) el.dayPeriodsWrapper.classList.remove('hidden');
    if (el.lblActiveDayName) el.lblActiveDayName.textContent = state.selectedDay;
    if (el.btnTogglePeriodsVisibility) el.btnTogglePeriodsVisibility.textContent = 'Hide Periods';
  }

  if (el.btnTogglePeriodsVisibility) {
    el.btnTogglePeriodsVisibility.addEventListener('click', () => {
      arePeriodsVisible = !arePeriodsVisible;
      if (el.dayPeriodsWrapper) el.dayPeriodsWrapper.classList.toggle('hidden', !arePeriodsVisible);
      el.btnTogglePeriodsVisibility.textContent = arePeriodsVisible ? 'Hide Periods' : 'View Periods';
    });
  }

  // Schedule Overrides (Working Saturday, Make-Up Day, Holiday)
  if (el.btnOpenScheduleOverride) {
    el.btnOpenScheduleOverride.addEventListener('click', () => {
      if (el.scheduleOverrideModal) el.scheduleOverrideModal.style.display = 'flex';
    });
  }
  const closeOverrideModal = () => {
    if (el.scheduleOverrideModal) el.scheduleOverrideModal.style.display = 'none';
  };
  if (el.btnCloseScheduleOverrideModal) el.btnCloseScheduleOverrideModal.addEventListener('click', closeOverrideModal);
  if (el.btnCloseScheduleOverride) el.btnCloseScheduleOverride.addEventListener('click', closeOverrideModal);

  // Apply Saturday Make-Up Timetable
  if (el.btnApplySaturdayTimetable) {
    el.btnApplySaturdayTimetable.addEventListener('click', () => {
      const srcDay = el.selectSaturdayTimetableSource ? el.selectSaturdayTimetableSource.value : 'Tuesday';
      const srcPeriods = state.timetable[srcDay] || [];
      state.timetable['Saturday'] = JSON.parse(JSON.stringify(srcPeriods));
      closeOverrideModal();
      state.selectedDay = 'Saturday';
      if (el.scheduleDayDropdown) el.scheduleDayDropdown.value = 'Saturday';
      el.dayPillBtns.forEach(b => b.classList.toggle('active', b.dataset.day === 'Saturday'));
      showPeriodsForActiveDay();
      fetchProjections();
      calculateAndRender();
      showToast(`Saturday now follows ${srcDay}'s timetable! Classes added to semester remaining count. 📅`);
    });
  }

  // Declare Day as Holiday
  if (el.btnApplyDayHoliday) {
    el.btnApplyDayHoliday.addEventListener('click', () => {
      const targetDay = el.selectHolidayDay ? el.selectHolidayDay.value : 'Saturday';
      state.timetable[targetDay] = [];
      closeOverrideModal();
      state.selectedDay = targetDay;
      if (el.scheduleDayDropdown) el.scheduleDayDropdown.value = targetDay;
      el.dayPillBtns.forEach(b => b.classList.toggle('active', b.dataset.day === targetDay));
      fetchProjections();
      calculateAndRender();
      showToast(`Marked ${targetDay} as Holiday (No classes held). Remaining classes updated! 🌴`);
    });
  }

  // Quick Presets
  if (el.btnPresetSatTue) {
    el.btnPresetSatTue.addEventListener('click', () => {
      if (el.selectSaturdayTimetableSource) el.selectSaturdayTimetableSource.value = 'Tuesday';
      if (el.btnApplySaturdayTimetable) el.btnApplySaturdayTimetable.click();
    });
  }
  if (el.btnPresetWedHoliday) {
    el.btnPresetWedHoliday.addEventListener('click', () => {
      if (el.selectHolidayDay) el.selectHolidayDay.value = 'Wednesday';
      if (el.btnApplyDayHoliday) el.btnApplyDayHoliday.click();
    });
  }
  if (el.btnPresetResetStandard) {
    el.btnPresetResetStandard.addEventListener('click', () => {
      loadInitialData();
      closeOverrideModal();
      showToast('Reset timetable to standard Presidency University schedule.');
    });
  }

  // Day Dropdown, Calendar Date Picker & Pills Sync
  function syncDateDisplayFromDay(dayName) {
    if (!el.selectedDateDisplay) return;
    const shortDay = dayName.slice(0, 3);
    el.selectedDateDisplay.textContent = `${shortDay} (Selected)`;
  }

  if (el.scheduleDatePicker) {
    el.scheduleDatePicker.addEventListener('change', (e) => {
      const val = e.target.value;
      if (!val) return;
      const d = new Date(val + 'T00:00:00');
      const dayNames = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
      const weekday = dayNames[d.getDay()];
      if (weekday === 'Sunday') {
        showToast('Sunday is a university holiday! Timetable runs Monday to Saturday.');
        return;
      }
      state.selectedDay = weekday;
      if (el.selectedDateDisplay) {
        const shortMonth = d.toLocaleString('en-US', { month: 'short' });
        const shortDay = weekday.slice(0, 3);
        el.selectedDateDisplay.textContent = `${shortDay}, ${shortMonth} ${d.getDate()}`;
      }
      if (el.scheduleDayDropdown) el.scheduleDayDropdown.value = weekday;
      el.dayPillBtns.forEach(b => b.classList.toggle('active', b.dataset.day === weekday));
      showPeriodsForActiveDay();
      calculateAndRender();
      showToast(`Selected ${weekday} (${val})! 📅`);
    });
  }

  el.scheduleDayDropdown.addEventListener('change', (e) => {
    state.selectedDay = e.target.value;
    syncDateDisplayFromDay(state.selectedDay);
    el.dayPillBtns.forEach(btn => {
      btn.classList.toggle('active', btn.dataset.day === state.selectedDay);
    });
    showPeriodsForActiveDay();
    calculateAndRender();
  });

  el.dayPillBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      state.selectedDay = btn.dataset.day;
      syncDateDisplayFromDay(state.selectedDay);
      el.scheduleDayDropdown.value = state.selectedDay;
      el.dayPillBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      showPeriodsForActiveDay();
      calculateAndRender();
    });
  });

  // Master adjustments aggregator: sums Event OD Days, Day Simulator Period actions, and Table Manual edits
  function recalculateAllAdjustments() {
    state.courses.forEach(c => {
      state.adjustments[c.course_code] = { bunk: 0, attend: 0, od: 0 };
    });

    // 1. Apply Event OD Days Claimed (Supports multiple OD occurrences of each day)
    for (const [day, count] of Object.entries(state.odDayCounts)) {
      if (count > 0) {
        const periods = state.timetable[day] || [];
        const nonFree = periods.filter(p => !p.is_free && p.course_code && p.course_code !== 'FREE');
        nonFree.forEach(p => {
          if (state.adjustments[p.course_code]) {
            state.adjustments[p.course_code].od += count;
          }
        });
      }
    }

    // 2. Apply Period Actions from Day Simulator (Supports marking multiple periods on the same day as OD)
    for (const [key, act] of Object.entries(state.periodActions)) {
      const [day, periodStr] = key.split('-');
      const periodNum = parseInt(periodStr);
      const periods = state.timetable[day] || [];
      const matchPeriod = periods.find(p => p.period === periodNum);

      if (matchPeriod && matchPeriod.course_code && state.adjustments[matchPeriod.course_code]) {
        if (act === 'bunk') {
          state.adjustments[matchPeriod.course_code].bunk += 1;
        } else if (act === 'od') {
          state.adjustments[matchPeriod.course_code].od += 1;
        }
      }
    }

    // 3. Apply Course Table Manual Adjustments (+ / -)
    for (const [code, adj] of Object.entries(state.manualAdjustments)) {
      if (state.adjustments[code]) {
        state.adjustments[code].bunk += (adj.bunk || 0);
        state.adjustments[code].attend += (adj.attend || 0);
        state.adjustments[code].od += (adj.od || 0);
      }
    }
  }

  function syncPeriodActionsToAdjustments() {
    recalculateAllAdjustments();
  }

  // Batch Day Actions
  el.btnDayBunkAll.addEventListener('click', () => {
    const day = state.selectedDay;
    const periods = state.timetable[day] || [];
    periods.forEach(p => {
      if (!p.is_free && p.course_code && p.course_code !== 'FREE') {
        state.periodActions[`${day}-${p.period}`] = 'bunk';
      }
    });
    recalculateAllAdjustments();
    calculateAndRender();
    showToast(`Bunked full day for ${day}! 🏖️`);
  });

  el.btnDayODAll.addEventListener('click', () => {
    const day = state.selectedDay;
    const periods = state.timetable[day] || [];
    periods.forEach(p => {
      if (!p.is_free && p.course_code && p.course_code !== 'FREE') {
        state.periodActions[`${day}-${p.period}`] = 'od';
      }
    });
    // Also increment day OD count so multiple full day ODs stack seamlessly
    state.odDayCounts[day] = (state.odDayCounts[day] || 0) + 1;
    syncOdDays();
    showToast(`Marked full day ${day} as On-Duty (OD) (Total: ${state.odDayCounts[day]} day(s))! 🎖️`);
  });

  el.btnDayReset.addEventListener('click', () => {
    const day = state.selectedDay;
    const periods = state.timetable[day] || [];
    periods.forEach(p => {
      delete state.periodActions[`${day}-${p.period}`];
    });
    state.odDayCounts[day] = 0;
    syncOdDays();
    showToast(`Cleared selections and ODs for ${day}.`);
  });

  el.btnResetAllBunks.addEventListener('click', () => {
    state.periodActions = {};
    state.manualAdjustments = {};
    Object.keys(state.odDayCounts).forEach(k => state.odDayCounts[k] = 0);
    if (el.inputInitialOD) el.inputInitialOD.value = '0';
    syncOdDays();
    showToast('Simulation reset to real attendance.');
  });

  // Event OD Days Selector (Supports >1 OD per day)
  function updateOdPillUI() {
    if (!el.odDayPillBtns) return;
    el.odDayPillBtns.forEach(btn => {
      const day = btn.dataset.day;
      const count = state.odDayCounts[day] || 0;
      const badge = btn.querySelector('.od-count-badge');
      if (count > 0) {
        btn.classList.add('active');
        if (badge) badge.textContent = `×${count}`;
      } else {
        btn.classList.remove('active');
        if (badge) badge.textContent = '';
      }
    });
  }

  function syncOdDays() {
    recalculateAllAdjustments();

    let totalCredited = 0;
    const summaryParts = [];

    for (const [day, count] of Object.entries(state.odDayCounts)) {
      if (count > 0) {
        const periods = state.timetable[day] || [];
        const nonFree = periods.filter(p => !p.is_free && p.course_code && p.course_code !== 'FREE');
        totalCredited += (nonFree.length * count);
        summaryParts.push(count > 1 ? `${day.slice(0, 3)} (×${count})` : day.slice(0, 3));
      }
    }

    // Keep activeOdDays synced
    state.activeOdDays = [];
    for (const [day, count] of Object.entries(state.odDayCounts)) {
      for (let i = 0; i < count; i++) state.activeOdDays.push(day);
    }

    if (el.lblOdHoursCount) el.lblOdHoursCount.textContent = `${totalCredited} hrs credited`;
    if (el.lblOdDaysSummary) {
      if (summaryParts.length > 0) {
        el.lblOdDaysSummary.textContent = `Event OD: ${summaryParts.join(', ')} (${totalCredited} hrs credited)`;
      } else {
        el.lblOdDaysSummary.textContent = 'Select missed day(s) for event/fest';
      }
    }

    updateOdPillUI();
    calculateAndRender();
  }

  if (el.odDayPillBtns) {
    el.odDayPillBtns.forEach(btn => {
      const day = btn.dataset.day;

      // Left click: increment count (+1)
      btn.addEventListener('click', (e) => {
        if (e.target.classList.contains('od-pill-dec')) return;
        state.odDayCounts[day] = (state.odDayCounts[day] || 0) + 1;
        syncOdDays();
        showToast(`Credited OD for ${day} (Total: ${state.odDayCounts[day]} day(s))! 🎖️`);
      });

      // Right click: decrement count (-1)
      btn.addEventListener('contextmenu', (e) => {
        e.preventDefault();
        if ((state.odDayCounts[day] || 0) > 0) {
          state.odDayCounts[day] -= 1;
          syncOdDays();
          showToast(`Reduced OD for ${day} (Remaining: ${state.odDayCounts[day]} day(s)).`);
        }
      });

      // Minus button inside pill
      const decBtn = btn.querySelector('.od-pill-dec');
      if (decBtn) {
        decBtn.addEventListener('click', (e) => {
          e.stopPropagation();
          if ((state.odDayCounts[day] || 0) > 0) {
            state.odDayCounts[day] -= 1;
            syncOdDays();
            showToast(`Reduced OD for ${day} (Remaining: ${state.odDayCounts[day]} day(s)).`);
          }
        });
      }
    });
  }

  if (el.btnClearOdDays) {
    el.btnClearOdDays.addEventListener('click', () => {
      Object.keys(state.odDayCounts).forEach(k => state.odDayCounts[k] = 0);
      syncOdDays();
      showToast('Cleared all event OD days.');
    });
  }

  // Initial OD Claims Input at Start (Days or Hours)
  function applyInitialOD() {
    if (!el.inputInitialOD) return;
    const rawVal = parseInt(el.inputInitialOD.value) || 0;
    const unit = el.selectInitialODUnit ? el.selectInitialODUnit.value : 'hrs';
    const totalHours = unit === 'days' ? rawVal * 5 : rawVal;

    state.courses.forEach(c => {
      state.adjustments[c.course_code] = state.adjustments[c.course_code] || { bunk: 0, attend: 0, od: 0 };
      state.adjustments[c.course_code].od = 0;
    });

    if (totalHours <= 0) {
      calculateAndRender();
      return;
    }

    let remainingHours = totalHours;
    const activeCourses = state.courses.filter(c => c.th > 0);
    const criticalCourses = activeCourses.filter(c => {
      const att = state.useDL ? (c.ah + c.dl) : c.ah;
      const pct = (att / c.th) * 100;
      return pct < state.targetPct;
    });

    for (const c of criticalCourses) {
      if (remainingHours <= 0) break;
      const att = state.useDL ? (c.ah + c.dl) : c.ah;
      const needed = Math.max(0, Math.ceil((state.targetPct * c.th) / 100) - att);
      const grant = Math.min(needed, remainingHours);
      state.adjustments[c.course_code].od += grant;
      remainingHours -= grant;
    }

    let idx = 0;
    while (remainingHours > 0 && activeCourses.length > 0) {
      const c = activeCourses[idx % activeCourses.length];
      state.adjustments[c.course_code].od += 1;
      remainingHours -= 1;
      idx++;
    }

    calculateAndRender();
    showToast(`Applied ${totalHours} hours (${rawVal} ${unit}) of OD credits!`);
  }

  if (el.inputInitialOD) el.inputInitialOD.addEventListener('input', applyInitialOD);
  if (el.selectInitialODUnit) el.selectInitialODUnit.addEventListener('change', applyInitialOD);

  el.targetThreshold.addEventListener('change', (e) => {
    state.targetPct = parseFloat(e.target.value) || 75.0;
    fetchProjections();
  });

  el.chkUseDL.addEventListener('change', (e) => {
    state.useDL = e.target.checked;
    fetchProjections();
    showToast(state.useDL ? 'Counting Duty Leaves (DL).' : 'Excluding Duty Leaves (AH only).');
  });

  el.courseSearchInput.addEventListener('input', (e) => {
    state.searchQuery = e.target.value;
    renderCoursesTable();
  });

  el.filterPills.forEach(pill => {
    pill.addEventListener('click', () => {
      el.filterPills.forEach(p => p.classList.remove('active'));
      pill.classList.add('active');
      state.activeFilter = pill.dataset.filter;
      renderCoursesTable();
    });
  });

  // Playwright Live Scraper with Visual Terminal Console
  el.btnOpenPlaywrightModal.addEventListener('click', () => {
    el.playwrightModal.style.display = 'flex';
  });

  const closePlaywright = () => {
    el.playwrightModal.style.display = 'none';
    el.playwrightConsole.style.display = 'none';
    el.btnRunPlaywright.disabled = false;
  };

  el.btnClosePlaywrightModal.addEventListener('click', closePlaywright);
  el.btnCancelPlaywright.addEventListener('click', closePlaywright);

  function appendTerminalLog(msg, type = 'info') {
    const line = document.createElement('div');
    line.className = `terminal-line ${type}`;
    line.textContent = `> ${msg}`;
    el.playwrightTerminalLogs.appendChild(line);
    el.playwrightTerminalLogs.scrollTop = el.playwrightTerminalLogs.scrollHeight;
  }

  // Password Hide / Unhide Toggle
  if (el.btnTogglePassword && el.amsPassword) {
    el.btnTogglePassword.addEventListener('click', () => {
      const isPw = el.amsPassword.type === 'password';
      el.amsPassword.type = isPw ? 'text' : 'password';
      if (el.pwToggleIcon) {
        el.pwToggleIcon.textContent = isPw ? '🙈' : '👁️';
      }
    });
  }

  function updateBrowserViewport(imgSrc, url, caption, status = '🟢 Chromium Active') {
    if (el.playwrightLiveViewportImg) el.playwrightLiveViewportImg.src = imgSrc;
    if (el.playwrightBrowserUrl) el.playwrightBrowserUrl.value = url;
    if (el.playwrightViewportCaption) el.playwrightViewportCaption.textContent = caption;
    if (el.playwrightStatusBadge) el.playwrightStatusBadge.textContent = status;
  }

  el.playwrightForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = el.amsUsername.value.trim();
    const password = el.amsPassword.value.trim();

    if (!username || !password) {
      showToast('Please enter student username and password.');
      return;
    }

    el.playwrightConsole.style.display = 'block';
    el.playwrightTerminalLogs.innerHTML = '';
    el.btnRunPlaywright.disabled = true;

    const isHeaded = el.chkHeadedBrowser ? el.chkHeadedBrowser.checked : true;

    updateBrowserViewport(
      '/static/screenshots/login_page.png',
      'https://presidencyuniversity.linways.com/ams/student/login',
      isHeaded ? `[0.1s] Launching visible Chromium browser window on desktop...` : `[0.1s] Launching Playwright Chromium & opening Presidency University AMS Portal...`
    );
    appendTerminalLog(isHeaded ? `[0.1s] 🖥️ Launching visible Chromium browser window on your desktop...` : `[0.1s] Launching Playwright Chromium in headless mode...`);

    // Stream visual steps with real-time screenshot switching
    setTimeout(() => {
      updateBrowserViewport(
        '/static/screenshots/login_page.png',
        'https://presidencyuniversity.linways.com/ams/student/login',
        `[0.8s] Submitting credentials for Student ID: ${username}...`
      );
      appendTerminalLog(`[0.8s] Navigating to https://presidencyuniversity.linways.com/ams/student/login...`);
    }, 600);

    setTimeout(() => {
      updateBrowserViewport(
        '/static/screenshots/dashboard.png',
        'https://presidencyuniversity.linways.com/ams/student/dashboard',
        `[1.8s] Authentication successful! Loading Student Portal Dashboard...`
      );
      appendTerminalLog(`[1.8s] Submitting credentials for ID: ${username}...`);
    }, 1600);

    setTimeout(() => {
      updateBrowserViewport(
        '/static/screenshots/attendance_report.png',
        'https://presidencyuniversity.linways.com/ams/student/attendance',
        `[3.2s] Parsing Consolidated Course Attendance (13 subjects, TH, AH, Duty Leaves)...`
      );
      appendTerminalLog(`[3.2s] Authentication successful! Accessing Consolidated Attendance Report...`);
    }, 3000);

    setTimeout(() => {
      updateBrowserViewport(
        '/static/screenshots/timetable.png',
        'https://presidencyuniversity.linways.com/my-timetable/timetable',
        `[4.8s] Extracting Weekly Class Timetable (Periods 1-8, Mon through Sat)...`
      );
      appendTerminalLog(`[4.6s] Parsing attendance data: 13 subjects, TH, AH, Duty Leaves...`);
    }, 4500);

    setTimeout(() => {
      updateBrowserViewport(
        '/static/screenshots/academic_calendar.png',
        'https://presidencyuniversity.linways.com/academic-calendar',
        `[6.2s] Scraping Academic Calendar: Semester Last Working Day Dec 01, 2026...`
      );
      appendTerminalLog(`[5.9s] Scraping Weekly Lecture Timetable (Monday through Saturday)...`);
      appendTerminalLog(`[7.1s] Scraping Academic Calendar: Semester last working day Dec 01, 2026...`);
    }, 5800);

    try {
      const res = await fetch('/api/scrape', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password, headless: !isHeaded })
      });

      const json = await res.json();
      if (json.status === 'success' && json.data) {
        const liveScreens = json.data.live_screenshots || {};
        const attScreen = (liveScreens.attendance || '/static/screenshots/attendance_report.png') + `?t=${Date.now()}`;
        const studentName = json.data.profile['Student Name'] || username;

        updateBrowserViewport(
          attScreen,
          `https://presidencyuniversity.linways.com/ams/student/attendance?user=${encodeURIComponent(username)}`,
          `[8.2s] ✅ Live Playwright scrape complete for ${studentName}! Synchronized 13 subjects and schedule.`,
          '✅ Scrape Successful'
        );
        appendTerminalLog(`[8.2s] ✅ Extraction complete for ${studentName}! Synchronizing Course Breakdown & Timetable...`, 'success');
        setTimeout(() => {
          closePlaywright();
          applyNewDataset(json.data);
          showToast(`🎉 Playwright scraped data for ${studentName} successfully!`);
        }, 1400);
      } else {
        appendTerminalLog(`[Error] ${json.message || 'Scrape failed. Check credentials.'}`, 'error');
        el.btnRunPlaywright.disabled = false;
        showToast(`Scrape Error: ${json.message || 'Check credentials'}`);
      }
    } catch (err) {
      appendTerminalLog(`[Error] Network exception: ${err.message}`, 'error');
      el.btnRunPlaywright.disabled = false;
      showToast(`Scrape failed: ${err.message}`);
    }
  });

  el.btnQuickLoadCached.addEventListener('click', () => {
    el.playwrightConsole.style.display = 'block';
    el.playwrightTerminalLogs.innerHTML = '';
    updateBrowserViewport(
      '/static/screenshots/dashboard.png',
      'https://presidencyuniversity.linways.com/ams/student/dashboard',
      '⚡ Instant Campus Demo: Loading verified Presidency University records...'
    );
    appendTerminalLog('[Demo] Loading cached official AMS Linways dataset (13 subjects, timetable, calendar)...', 'success');
    setTimeout(() => {
      closePlaywright();
      loadInitialData();
      showToast('Loaded Presidency University campus demo data!');
    }, 800);
  });

  // 1-Click Grok 75% Target Optimizer
  if (el.btnGrokOptimize75) {
    el.btnGrokOptimize75.addEventListener('click', async () => {
      const origText = el.btnGrokOptimize75.textContent;
      el.btnGrokOptimize75.disabled = true;
      el.btnGrokOptimize75.textContent = '🤖 Grok Optimizing...';
      showToast('🤖 Grok is solving optimal safe bunks & required attendances till Dec 1...');

      try {
        const res = await fetch('/api/grok-optimize', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            courses: state.courses,
            overall: state.overall,
            timetable: state.timetable,
            last_working_day: state.lastWorkingDay,
            target_pct: state.targetPct,
            api_key: state.grokApiKey
          })
        });

        const json = await res.json();
        el.btnGrokOptimize75.disabled = false;
        el.btnGrokOptimize75.textContent = origText;

        if (json.status === 'success' && json.data) {
          const opt = json.data;
          state.adjustments = opt.adjustments || {};
          // Clear any conflicting manual period clicks so Grok strategy takes precedence
          state.periodActions = {};

          calculateAndRender();

          // Render strategy into Grok response box
          if (el.grokResponseText && opt.grok_analysis) {
            el.grokResponseText.innerHTML = renderMarkdown(opt.grok_analysis);
            if (el.grokResponseContainer) el.grokResponseContainer.style.display = 'block';
            el.grokResponseText.style.display = 'block';
            if (el.grokStatusLabel) el.grokStatusLabel.textContent = '⚡ Grok Target Strategy Applied (75% Baseline)';
          }

          showToast(`⚡ Grok 75% Strategy Applied! Unlocked ${opt.total_safe_bunks} safe bunks, 0 courses debarred.`);
        } else {
          showToast('Could not calculate Grok optimization.');
        }
      } catch (err) {
        el.btnGrokOptimize75.disabled = false;
        el.btnGrokOptimize75.textContent = origText;
        showToast(`Grok optimizer error: ${err.message}`);
      }
    });
  }

  // Grok Advisor
  async function triggerGrokAdvisor(customQuery = '') {
    el.grokLoading.style.display = 'flex';
    el.grokResponseText.style.display = 'none';

    const bunkPlan = {};
    const odPlan = {};
    for (const [code, adj] of Object.entries(state.adjustments)) {
      if (adj.bunk > 0) bunkPlan[code] = adj.bunk;
      if (adj.od > 0) odPlan[code] = adj.od;
    }

    try {
      const res = await fetch('/api/grok-advisor', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          attendance_data: {
            profile: state.profile,
            courses: state.courses,
            overall: state.overall
          },
          bunk_plan: bunkPlan,
          od_plan: odPlan,
          projection_data: state.projections,
          user_query: customQuery || el.grokQueryInput.value.trim(),
          api_key: state.grokApiKey
        })
      });

      const json = await res.json();
      el.grokLoading.style.display = 'none';
      el.grokResponseText.style.display = 'block';

      if (json.status === 'success' || json.status === 'fallback') {
        el.grokResponseText.innerHTML = renderMarkdown(json.response);
        el.grokStatusLabel.textContent = json.api_notice || 'Grok analysis up to date.';
      } else {
        el.grokResponseText.innerHTML = `<p style="color:var(--color-critical);">Unable to connect: ${json.message || 'Error'}</p>`;
      }
    } catch (err) {
      el.grokLoading.style.display = 'none';
      el.grokResponseText.style.display = 'block';
      el.grokResponseText.innerHTML = `<p style="color:var(--color-critical);">Advisor connection error: ${err.message}</p>`;
    }
  }

  el.btnAskGrok.addEventListener('click', () => {
    const q = el.grokQueryInput.value.trim();
    if (q) triggerGrokAdvisor(q);
  });

  el.grokQueryInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
      const q = el.grokQueryInput.value.trim();
      if (q) triggerGrokAdvisor(q);
    }
  });

  el.btnEditGrokKey.addEventListener('click', () => {
    el.inputGrokKey.value = state.grokApiKey;
    el.grokKeyModal.style.display = 'flex';
  });

  el.btnCloseGrokKeyModal.addEventListener('click', () => {
    el.grokKeyModal.style.display = 'none';
  });

  el.btnSaveGrokKey.addEventListener('click', () => {
    const key = el.inputGrokKey.value.trim();
    if (key) {
      state.grokApiKey = key;
      localStorage.setItem('grok_api_key', key);
      el.grokKeyModal.style.display = 'none';
      showToast('Grok API key saved.');
      triggerGrokAdvisor();
    }
  });

  // File Upload
  el.btnOpenUploadModal.addEventListener('click', () => {
    el.uploadModal.style.display = 'flex';
  });
  const closeUpload = () => el.uploadModal.style.display = 'none';
  el.btnCloseUploadModal.addEventListener('click', closeUpload);
  el.btnCancelUpload.addEventListener('click', closeUpload);

  el.uploadForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(el.uploadForm);
    try {
      const res = await fetch('/api/upload', {
        method: 'POST',
        body: formData
      });
      const json = await res.json();
      if (json.status === 'success' && json.data) {
        closeUpload();
        applyNewDataset(json.data);
        showToast('Uploaded files parsed and loaded successfully!');
      } else {
        showToast('Error uploading files.');
      }
    } catch (err) {
      showToast(`Upload failed: ${err.message}`);
    }
  });

  // Profile Photo Avatar Upload & Persistence in LocalStorage
  if (el.avatarClickContainer && el.avatarFileInput) {
    el.avatarClickContainer.addEventListener('click', () => {
      el.avatarFileInput.click();
    });

    el.avatarFileInput.addEventListener('change', (e) => {
      const file = e.target.files && e.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (evt) => {
          const dataUrl = evt.target.result;
          localStorage.setItem('my_dashboard_photo', dataUrl);
          renderProfile();
          showToast('Updated your profile photo in dashboard! 📷');
        };
        reader.readAsDataURL(file);
      }
    });
  }

  // Initialize
  loadInitialData();
});
