const messages = document.querySelector("#messages");
const welcomeView = document.querySelector("#welcomeView");
const welcomeStartButton = document.querySelector("#welcomeStartButton");
const demoDisclaimers = document.querySelectorAll("[data-demo-disclaimer]");
const demoPhoneFields = document.querySelectorAll(".demo-phone-field");
const authWelcomeButton = document.querySelector("#authWelcomeButton");
const chatForm = document.querySelector("#chatForm");
const messageInput = document.querySelector("#messageInput");
const sendButton = document.querySelector("#sendButton");
const clearButton = document.querySelector("#clearButton");
const micButton = document.querySelector("#micButton");
const speechToggle = document.querySelector("#speechToggle");
const statusText = document.querySelector("#statusText");
const currentTaskText = document.querySelector("#currentTaskText");
const patientTaskName = document.querySelector("#patientTaskName");
const patientInstructionText = document.querySelector("#patientInstructionText");
const patientTaskMeta = document.querySelector("#patientTaskMeta");
const patientChatArea = document.querySelector("#patientChatArea");
const patientChatToggle = document.querySelector("#patientChatToggle");
const patientChatBackButton = document.querySelector("#patientChatBackButton");
const patientCaregiverChatArea = document.querySelector("#patientCaregiverChatArea");
const patientCaregiverChatToggle = document.querySelector("#patientCaregiverChatToggle");
const patientCaregiverChatBackButton = document.querySelector("#patientCaregiverChatBackButton");
const patientCaregiverChatForm = document.querySelector("#patientCaregiverChatForm");
const patientCaregiverMessageInput = document.querySelector("#patientCaregiverMessageInput");
const patientCaregiverSendButton = document.querySelector("#patientCaregiverSendButton");
const patientCaregiverMessages = document.querySelector("#patientCaregiverMessages");
const reportIssueButton = document.querySelector("#reportIssueButton");
const caregiverReminderToggle = document.querySelector("#caregiverReminderToggle");
const caregiverReminderStatus = document.querySelector("#caregiverReminderStatus");
const caregiverAlertNotificationToggle = document.querySelector("#caregiverAlertNotificationToggle");
const caregiverAlertNotificationStatus = document.querySelector("#caregiverAlertNotificationStatus");
const caregiverSmsToggle = document.querySelector("#caregiverSmsToggle");
const caregiverSmsStatus = document.querySelector("#caregiverSmsStatus");
const caregiverLiveAlert = document.querySelector("#caregiverLiveAlert");
const caregiverLiveAlertTitle = document.querySelector("#caregiverLiveAlertTitle");
const caregiverLiveAlertMessage = document.querySelector("#caregiverLiveAlertMessage");
const caregiverLiveAlertView = document.querySelector("#caregiverLiveAlertView");
const caregiverLiveAlertDismiss = document.querySelector("#caregiverLiveAlertDismiss");
const caregiverNotificationButton = document.querySelector("#caregiverNotificationButton");
const caregiverNotificationBadge = document.querySelector("#caregiverNotificationBadge");
const patientGreeting = document.querySelector("#patientGreeting");
const caregiverGreeting = document.querySelector("#caregiverGreeting");
const caregiverSectionToolbar = document.querySelector("#caregiverSectionToolbar");
const caregiverHomeButton = document.querySelector("#caregiverHomeButton");
const caregiverSectionLabel = document.querySelector("#caregiverSectionLabel");
const caregiverAuraChatLauncher = document.querySelector("#caregiverAuraChatLauncher");
const caregiverHomeSummary = document.querySelector("#caregiverHomeSummary");
const homeCompletedStat = document.querySelector("#homeCompletedStat");
const homeAlertStat = document.querySelector("#homeAlertStat");
const homeHelpStat = document.querySelector("#homeHelpStat");
const homePatientChatStatus = document.querySelector("#homePatientChatStatus");
const caregiverChatNotificationBadge = document.querySelector("#caregiverChatNotificationBadge");
const homeAlertStatus = document.querySelector("#homeAlertStatus");
const homeScheduleStatus = document.querySelector("#homeScheduleStatus");
const homePerformanceStatus = document.querySelector("#homePerformanceStatus");
const homeUpdateStatus = document.querySelector("#homeUpdateStatus");
const homeActivityStatus = document.querySelector("#homeActivityStatus");
const homeDatasetStatus = document.querySelector("#homeDatasetStatus");
const homeClockStatus = document.querySelector("#homeClockStatus");
const homeReminderStatus = document.querySelector("#homeReminderStatus");
const quickButtons = document.querySelectorAll("[data-message]");
const authView = document.querySelector("#authView");
const appContent = document.querySelector("#appContent");
const adminView = document.querySelector("#adminView");
const loginForm = document.querySelector("#loginForm");
const signupForm = document.querySelector("#signupForm");
const adminLoginForm = document.querySelector("#adminLoginForm");
const showLoginButton = document.querySelector("#showLoginButton");
const showSignupButton = document.querySelector("#showSignupButton");
const showAdminButton = document.querySelector("#showAdminButton");
const loginUsername = document.querySelector("#loginUsername");
const loginPassword = document.querySelector("#loginPassword");
const loginCaregiverPassword = document.querySelector("#loginCaregiverPassword");
const loginCaregiverPhone = document.querySelector("#loginCaregiverPhone");
const signupPatientName = document.querySelector("#signupPatientName");
const signupCaregiverName = document.querySelector("#signupCaregiverName");
const signupUsername = document.querySelector("#signupUsername");
const signupPassword = document.querySelector("#signupPassword");
const signupCaregiverPassword = document.querySelector("#signupCaregiverPassword");
const signupCaregiverPhone = document.querySelector("#signupCaregiverPhone");
const adminUsername = document.querySelector("#adminUsername");
const adminPassword = document.querySelector("#adminPassword");
const authStatus = document.querySelector("#authStatus");
const authPreferences = document.querySelector("#authPreferences");
const authRoleInputs = document.querySelectorAll('input[name="authRole"]');
const accountLabel = document.querySelector("#accountLabel");
const activeRoleLabel = document.querySelector("#activeRoleLabel");
const openAdminButton = document.querySelector("#openAdminButton");
const logoutButton = document.querySelector("#logoutButton");
const clockDisplay = document.querySelector("#clockDisplay");
const clockSpeed = document.querySelector("#clockSpeed");
const customClockSpeed = document.querySelector("#customClockSpeed");
const applyCustomSpeedButton = document.querySelector("#applyCustomSpeedButton");
const resetClockButton = document.querySelector("#resetClockButton");
const clockTaskStatus = document.querySelector("#clockTaskStatus");
const clockTaskList = document.querySelector("#clockTaskList");
const languageSelect = document.querySelector("#languageSelect");
const refreshCaregiverButton = document.querySelector("#refreshCaregiverButton");
const resetCaregiverButton = document.querySelector("#resetCaregiverButton");
const caregiverResetStatus = document.querySelector("#caregiverResetStatus");
const clearDatasetButton = document.querySelector("#clearDatasetButton");
const caregiverStatus = document.querySelector("#caregiverStatus");
const caregiverUpdateText = document.querySelector("#caregiverUpdateText");
const recentEventsList = document.querySelector("#recentEventsList");
const alertStatus = document.querySelector("#alertStatus");
const alertList = document.querySelector("#alertList");
const caregiverChatForm = document.querySelector("#caregiverChatForm");
const caregiverMessageInput = document.querySelector("#caregiverMessageInput");
const caregiverSendButton = document.querySelector("#caregiverSendButton");
const caregiverChatMessages = document.querySelector("#caregiverChatMessages");
const caregiverPatientChatForm = document.querySelector("#caregiverPatientChatForm");
const caregiverPatientMessageInput = document.querySelector("#caregiverPatientMessageInput");
const caregiverPatientSendButton = document.querySelector("#caregiverPatientSendButton");
const caregiverPatientMessages = document.querySelector("#caregiverPatientMessages");
const routineForm = document.querySelector("#routineForm");
const routineFormStatus = document.querySelector("#routineFormStatus");
const routineList = document.querySelector("#routineList");
const routineCount = document.querySelector("#routineCount");
const insightGrid = document.querySelector("#insightGrid");
const caregiverInsightSource = document.querySelector("#caregiverInsightSource");
const caregiverTimeInsightList = document.querySelector("#caregiverTimeInsightList");
const caregiverDifficultyInsightList = document.querySelector("#caregiverDifficultyInsightList");
const caregiverDayInsightList = document.querySelector("#caregiverDayInsightList");
const caregiverTaskInsightList = document.querySelector("#caregiverTaskInsightList");
const caregiverTrendInsightList = document.querySelector("#caregiverTrendInsightList");
const caregiverKeyFindings = document.querySelector("#caregiverKeyFindings");
const caregiverRecommendedActions = document.querySelector("#caregiverRecommendedActions");
const caregiverDataNotes = document.querySelector("#caregiverDataNotes");
const datasetPathText = document.querySelector("#datasetPathText");
const datasetSummaryGrid = document.querySelector("#datasetSummaryGrid");
const datasetTableBody = document.querySelector("#datasetTableBody");
const caregiverSubtabs = document.querySelectorAll("[data-caregiver-section]");
const adminSubtabs = document.querySelectorAll("[data-admin-section]");
const caregiverSectionPanels = {
  home: document.querySelector("#caregiverSection-home"),
  chat: document.querySelector("#caregiverSection-chat"),
  patientChat: document.querySelector("#caregiverSection-patient-chat"),
  alerts: document.querySelector("#caregiverSection-alerts"),
  schedule: document.querySelector("#caregiverSection-schedule"),
  performance: document.querySelector("#caregiverSection-performance"),
  update: document.querySelector("#caregiverSection-update"),
  activity: document.querySelector("#caregiverSection-activity"),
  dataset: document.querySelector("#caregiverSection-dataset"),
  clock: document.querySelector("#caregiverSection-clock"),
  reminders: document.querySelector("#caregiverSection-reminders"),
};
const rolePanels = {
  patient: document.querySelector("#patientView"),
  caregiver: document.querySelector("#caregiverView"),
};
const passwordModal = document.querySelector("#passwordModal");
const passwordForm = document.querySelector("#passwordForm");
const passwordTitle = document.querySelector("#passwordTitle");
const passwordInput = document.querySelector("#passwordInput");
const passwordError = document.querySelector("#passwordError");
const passwordSubmitButton = document.querySelector("#passwordSubmitButton");
const cancelPasswordButton = document.querySelector("#cancelPasswordButton");
const adminLoginModal = document.querySelector("#adminLoginModal");
const adminModalForm = document.querySelector("#adminModalForm");
const adminModalUsername = document.querySelector("#adminModalUsername");
const adminModalPassword = document.querySelector("#adminModalPassword");
const adminModalError = document.querySelector("#adminModalError");
const cancelAdminModalButton = document.querySelector("#cancelAdminModalButton");
const adminDatabasePath = document.querySelector("#adminDatabasePath");
const adminAccountCount = document.querySelector("#adminAccountCount");
const adminAccountList = document.querySelector("#adminAccountList");
const adminDatasetTitle = document.querySelector("#adminDatasetTitle");
const adminDatasetSubtitle = document.querySelector("#adminDatasetSubtitle");
const adminExportLink = document.querySelector("#adminExportLink");
const adminSummaryGrid = document.querySelector("#adminSummaryGrid");
const adminDatasetTableBody = document.querySelector("#adminDatasetTableBody");
const adminSectionPanels = {
  datasets: document.querySelector("#adminSection-datasets"),
  dummy: document.querySelector("#adminSection-dummy"),
};
const adminDummyInsightSource = document.querySelector("#adminDummyInsightSource");
const adminDummySummaryGrid = document.querySelector("#adminDummySummaryGrid");
const adminDummyTimeList = document.querySelector("#adminDummyTimeList");
const adminDummyDifficultyList = document.querySelector("#adminDummyDifficultyList");
const adminDummyFindings = document.querySelector("#adminDummyFindings");
const adminDummyActions = document.querySelector("#adminDummyActions");
const adminDummyModelingNotes = document.querySelector("#adminDummyModelingNotes");
const adminBackButton = document.querySelector("#adminBackButton");
const adminLogoutButton = document.querySelector("#adminLogoutButton");
const datasetWarningModal = document.querySelector("#datasetWarningModal");
const datasetWarningForm = document.querySelector("#datasetWarningForm");
const cancelDatasetWarningButton = document.querySelector("#cancelDatasetWarningButton");
const statElements = {
  interactions: document.querySelector("#interactionsStat"),
  markedComplete: document.querySelector("#completedStat"),
  helpRequests: document.querySelector("#helpStat"),
  reminderRequests: document.querySelector("#reminderStat"),
  visualSupport: document.querySelector("#visualStat"),
  confusionFlags: document.querySelector("#confusionStat"),
};
const SpeechRecognition =
  window.SpeechRecognition || window.webkitSpeechRecognition || null;

let busyState = false;
let caregiverUnlocked = false;
let isListening = false;
let shouldKeepListening = false;
let spokenRepliesEnabled = "speechSynthesis" in window;
let availableSpeechVoices = [];
let recognition = null;
let finalTranscript = "";
let restartTimer = null;
let clockTimer = null;
let reminderTimer = null;
let caregiverAlertTimer = null;
let signedIn = false;
let signedInAccount = null;
let passwordAction = "unlock";
let datasetUnlocked = false;
let adminSignedIn = false;
let selectedAdminUserId = "";
let lastNotifiedTaskKey = "";
let notificationsEnabled = window.Notification?.permission === "granted";
let caregiverAlertNotificationsEnabled =
  window.localStorage.getItem("auraCaregiverAlertNotificationsEnabled") === "true";
let caregiverAlertBaselineReady = false;
let caregiverAlertStorageKey = "";
let lastCaregiverAlertId = 0;
let caregiverChatReadStorageKey = "";
let lastReadPatientMessageId = 0;
let selectedLanguage = window.localStorage.getItem("auraLanguage") || "auto";
let selectedRole = window.localStorage.getItem("auraRole") === "caregiver"
  ? "caregiver"
  : "patient";
let remindersEnabled = window.localStorage.getItem("auraRemindersEnabled") === "true";

function showAuthMode(mode) {
  const isSignup = mode === "signup";
  const isAdmin = mode === "admin";
  signupForm.hidden = !isSignup;
  loginForm.hidden = isSignup || isAdmin;
  adminLoginForm.hidden = !isAdmin;
  authPreferences.hidden = isAdmin;
  showSignupButton.classList.toggle("is-active", isSignup);
  showLoginButton.classList.toggle("is-active", !isSignup && !isAdmin);
  showAdminButton.classList.toggle("is-active", isAdmin);
  authStatus.textContent = "";
  window.setTimeout(() => {
    if (isSignup) {
      signupPatientName.focus();
      return;
    }
    if (isAdmin) {
      adminUsername.focus();
      return;
    }
    loginUsername.focus();
  }, 0);
}

function selectedAuthRole() {
  return document.querySelector('input[name="authRole"]:checked')?.value === "caregiver"
    ? "caregiver"
    : "patient";
}

function setAuthRole(role) {
  selectedRole = role === "caregiver" ? "caregiver" : "patient";
  authRoleInputs.forEach((input) => {
    input.checked = input.value === selectedRole;
  });
}

function setActiveRole(role) {
  selectedRole = role === "caregiver" ? "caregiver" : "patient";
  Object.entries(rolePanels).forEach(([name, panel]) => {
    const isActive = name === selectedRole;
    panel.hidden = !isActive;
    panel.classList.toggle("is-active", isActive);
  });
  activeRoleLabel.textContent = selectedRole === "caregiver" ? "Caregiver" : "Patient";
}

function setSignedIn(account, role = selectedRole) {
  signedIn = true;
  signedInAccount = account || null;
  adminSignedIn = false;
  setActiveRole(role);
  caregiverUnlocked = selectedRole === "caregiver";
  datasetUnlocked = caregiverUnlocked;
  window.localStorage.setItem("auraSignedIn", "true");
  window.localStorage.setItem("auraUsername", account?.username || "");
  window.localStorage.setItem("auraRole", selectedRole);
  welcomeView.hidden = true;
  authView.hidden = true;
  appContent.hidden = false;
  adminView.hidden = true;
  patientChatArea.hidden = true;
  patientCaregiverChatArea.hidden = true;
  rolePanels.patient.classList.remove("is-chat-open");
  patientChatToggle.textContent = "AURA Chat";
  accountLabel.textContent = account
    ? `${account.patient_name} / ${account.caregiver_name}`
    : "Signed in";
  patientGreeting.textContent = account?.patient_name
    ? `Hi, ${account.patient_name}`
    : "Hi";
  caregiverGreeting.textContent = account?.caregiver_name
    ? `Hi, ${account.caregiver_name}`
    : "Hi";
  window.clearInterval(clockTimer);
  clockTimer = null;
  window.clearInterval(caregiverAlertTimer);
  caregiverAlertTimer = null;
  if (selectedRole === "caregiver") {
    refreshClock();
    clockTimer = window.setInterval(refreshClock, 1000);
    caregiverAlertStorageKey = `auraLastCaregiverAlertId:${account?.username || "default"}`;
    caregiverAlertBaselineReady = window.localStorage.getItem(caregiverAlertStorageKey) !== null;
    lastCaregiverAlertId = Number(
      window.localStorage.getItem(caregiverAlertStorageKey) || 0,
    );
    caregiverChatReadStorageKey = `auraLastReadPatientMessageId:${account?.username || "default"}`;
    lastReadPatientMessageId = Number(
      window.localStorage.getItem(caregiverChatReadStorageKey) || 0,
    );
    checkCaregiverNotifications();
    caregiverAlertTimer = window.setInterval(checkCaregiverNotifications, 2000);
  }
  if (reminderTimer === null) {
    reminderTimer = window.setInterval(checkPatientReminders, 5000);
  }
  updateReminderStatus();
  updateCaregiverAlertNotificationStatus();
  renderSmsSettings();
  fetchPatientState();
  if (selectedRole === "caregiver") {
    switchCaregiverSection("home");
    refreshCaregiverUpdate(false);
    loadPatientCaregiverChat();
    document.querySelector(".caregiver-home-card")?.focus();
  } else {
    document.querySelector(".patient-action")?.focus();
  }
}

function setSignedOut(message = "", showWelcomeScreen = false) {
  signedIn = false;
  signedInAccount = null;
  adminSignedIn = false;
  caregiverUnlocked = false;
  datasetUnlocked = false;
  selectedAdminUserId = "";
  window.localStorage.removeItem("auraSignedIn");
  window.localStorage.removeItem("auraUsername");
  window.clearInterval(clockTimer);
  clockTimer = null;
  window.clearInterval(reminderTimer);
  reminderTimer = null;
  window.clearInterval(caregiverAlertTimer);
  caregiverAlertTimer = null;
  caregiverAlertBaselineReady = false;
  caregiverAlertStorageKey = "";
  lastCaregiverAlertId = 0;
  caregiverChatReadStorageKey = "";
  lastReadPatientMessageId = 0;
  caregiverChatNotificationBadge.hidden = true;
  caregiverLiveAlert.hidden = true;
  lastNotifiedTaskKey = "";
  stopListening();
  welcomeView.hidden = !showWelcomeScreen;
  authView.hidden = showWelcomeScreen;
  appContent.hidden = true;
  adminView.hidden = true;
  patientChatArea.hidden = true;
  patientCaregiverChatArea.hidden = true;
  rolePanels.patient.classList.remove("is-chat-open");
  patientChatToggle.textContent = "AURA Chat";
  passwordModal.hidden = true;
  adminLoginModal.hidden = true;
  datasetWarningModal.hidden = true;
  patientGreeting.textContent = "Hi";
  caregiverGreeting.textContent = "Hi";
  renderSmsSettings();
  setAuthRole(selectedRole);
  showAuthMode("login");
  authStatus.textContent = message;
}

function currentLanguageCode() {
  return selectedLanguage || "auto";
}

function browserLanguageCode() {
  if (currentLanguageCode() !== "auto") {
    return currentLanguageCode();
  }
  return navigator.language || "en-US";
}

function refreshSpeechVoices() {
  if (!("speechSynthesis" in window)) {
    availableSpeechVoices = [];
    return;
  }
  availableSpeechVoices = window.speechSynthesis.getVoices();
}

function normalizedSpeechLanguage(language) {
  return String(language || "").trim().toLowerCase().replaceAll("_", "-");
}

function naturalVoiceScore(voice, requestedLanguage) {
  const voiceLanguage = normalizedSpeechLanguage(voice.lang);
  const targetLanguage = normalizedSpeechLanguage(requestedLanguage);
  const voiceBase = voiceLanguage.split("-")[0];
  const targetBase = targetLanguage.split("-")[0];
  if (!voiceBase || voiceBase !== targetBase) {
    return -1000;
  }

  const name = voice.name || "";
  let score = voiceLanguage === targetLanguage ? 120 : 80;
  if (/natural|neural|enhanced|premium/i.test(name)) {
    score += 110;
  }
  if (/google/i.test(name)) {
    score += 65;
  }
  if (/microsoft/i.test(name)) {
    score += 30;
  }
  if (/aria|jenny|sonia|natasha|guy|ryan|libby|michelle|roger|ava|samantha/i.test(name)) {
    score += 35;
  }
  if (voice.localService === false) {
    score += 20;
  }
  if (voice.default) {
    score += 10;
  }
  if (/espeak|festival|compact|desktop/i.test(name)) {
    score -= 90;
  }
  return score;
}

function bestNaturalVoice(language) {
  if (!availableSpeechVoices.length) {
    refreshSpeechVoices();
  }
  return availableSpeechVoices
    .map((voice) => ({ voice, score: naturalVoiceScore(voice, language) }))
    .filter((candidate) => candidate.score > -1000)
    .sort((left, right) => right.score - left.score)[0]?.voice || null;
}

function setupSpeechVoices() {
  if (!("speechSynthesis" in window)) {
    return;
  }
  refreshSpeechVoices();
  window.speechSynthesis.addEventListener?.("voiceschanged", refreshSpeechVoices);
}

async function loadLanguages() {
  try {
    const response = await fetch("/api/languages");
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || "Could not load languages.");
    }
    languageSelect.innerHTML = "";
    data.languages.forEach((language) => {
      const option = document.createElement("option");
      option.value = language.code;
      option.textContent = language.native === language.name
        ? language.name
        : `${language.name} / ${language.native}`;
      languageSelect.append(option);
    });
    languageSelect.value = data.languages.some((language) => language.code === selectedLanguage)
      ? selectedLanguage
      : "auto";
    selectedLanguage = languageSelect.value;
    updateRecognitionLanguage();
  } catch {
    languageSelect.value = selectedLanguage;
  }
}

async function loadRuntimeConfig() {
  try {
    const response = await fetch("/api/runtime-config");
    const data = await response.json();
    if (!response.ok) {
      return;
    }
    const publicDemo = Boolean(data.publicDemo);
    document.body.classList.toggle("public-demo", publicDemo);
    demoDisclaimers.forEach((element) => {
      element.hidden = !publicDemo;
    });
    demoPhoneFields.forEach((element) => {
      element.hidden = publicDemo;
    });
  } catch (_error) {
    // Local static-file previews do not have a runtime API.
  }
}

async function loadAuthState() {
  try {
    const response = await fetch(
      `/api/auth-state?role=${encodeURIComponent(selectedRole)}`,
    );
    const data = await response.json();
    if (data.authenticated) {
      setSignedIn(data.account, data.role || selectedRole);
      return;
    }
    setSignedOut("", true);
    if (!data.hasAccount) {
      showAuthMode("signup");
    }
  } catch {
    setSignedOut("Sign in is unavailable. Restart the AURA server.");
  }
}

async function submitAuth(endpoint, payload) {
  authStatus.textContent = "Checking";
  const response = await fetch(endpoint, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.error || "Sign in failed.");
  }
  selectedLanguage = languageSelect.value || "auto";
  window.localStorage.setItem("auraLanguage", selectedLanguage);
  updateRecognitionLanguage();
  setSignedIn(data.account, data.role || payload.role || selectedAuthRole());
}

function showPasswordModal(action = "unlock") {
  passwordAction = action;
  passwordError.hidden = true;
  passwordError.textContent = "";
  passwordInput.value = "";
  if (action === "clearDataset") {
    passwordTitle.textContent = "Finalize Dataset Clear";
    passwordSubmitButton.textContent = "Clear Dataset";
  } else {
    passwordTitle.textContent = "Caregiver Access";
    passwordSubmitButton.textContent = "Unlock";
  }
  passwordModal.hidden = false;
  passwordInput.focus();
}

function hidePasswordModal() {
  passwordModal.hidden = true;
  passwordInput.value = "";
}

function switchCaregiverSection(sectionName) {
  const sectionTitles = {
    home: "Caregiver Home",
    chat: "Chat With AURA",
    patientChat: "Patient Chat",
    alerts: "Safety Alerts",
    schedule: "Schedule",
    performance: "Performance Insights",
    update: "AURA Update",
    activity: "Recent Activity",
    dataset: "Patient Dataset",
    clock: "Test Clock",
    reminders: "Reminder Settings",
  };
  if (!caregiverSectionPanels[sectionName]) {
    sectionName = "home";
  }

  caregiverSubtabs.forEach((tab) => {
    const isActive = tab.dataset.caregiverSection === sectionName;
    tab.classList.toggle("is-active", isActive);
    if (isActive) {
      tab.setAttribute("aria-current", "page");
    } else {
      tab.removeAttribute("aria-current");
    }
  });

  Object.entries(caregiverSectionPanels).forEach(([name, panel]) => {
    const isActive = name === sectionName;
    panel.hidden = !isActive;
    panel.classList.toggle("is-active", isActive);
  });

  const isHome = sectionName === "home";
  caregiverSectionToolbar.hidden = isHome;
  caregiverSectionLabel.textContent = sectionTitles[sectionName];
  caregiverAuraChatLauncher.hidden = !isHome;

  if (sectionName === "chat") {
    caregiverMessageInput.focus();
  }
  if (sectionName === "patientChat") {
    loadPatientCaregiverChat().then(() => {
      caregiverPatientMessageInput.focus();
    });
  }
  if (sectionName === "dataset") {
    loadDataset();
  }
  if (sectionName === "clock") {
    refreshClock();
    clockSpeed.focus();
  }
  if (sectionName === "reminders") {
    updateReminderStatus();
    updateCaregiverAlertNotificationStatus();
    renderSmsSettings();
    caregiverReminderToggle.focus();
  }
}

function switchAdminSection(sectionName) {
  adminSubtabs.forEach((tab) => {
    const isActive = tab.dataset.adminSection === sectionName;
    tab.classList.toggle("is-active", isActive);
    tab.setAttribute("aria-selected", String(isActive));
  });

  Object.entries(adminSectionPanels).forEach(([name, panel]) => {
    if (!panel) {
      return;
    }
    const isActive = name === sectionName;
    panel.hidden = !isActive;
    panel.classList.toggle("is-active", isActive);
  });
}

function setBusy(isBusy) {
  busyState = isBusy;
  messageInput.disabled = busyState;
  sendButton.disabled = busyState;
  clearButton.disabled = busyState;
  reportIssueButton.disabled = busyState;
  quickButtons.forEach((button) => {
    button.disabled = busyState;
  });
  updateVoiceButtons();
  updateStatus(busyState ? "Thinking" : null);
}

function setPatientChatOpen(isOpen) {
  setPatientWorkspaceMode(isOpen ? "auraChat" : "main");
}

function setPatientWorkspaceMode(mode = "main") {
  const auraChatOpen = mode === "auraChat";
  const caregiverChatOpen = mode === "caregiverChat";
  patientChatArea.hidden = !auraChatOpen;
  patientCaregiverChatArea.hidden = !caregiverChatOpen;
  rolePanels.patient.classList.toggle("is-chat-open", auraChatOpen || caregiverChatOpen);
  patientChatToggle.textContent = "AURA Chat";

  if (auraChatOpen) {
    messageInput.focus();
    return;
  }
  if (caregiverChatOpen) {
    loadPatientCaregiverChat().then(() => {
      patientCaregiverMessageInput.focus();
    });
    return;
  }
  patientChatToggle.focus();
}

function updateStatus(status) {
  if (status) {
    statusText.textContent = status;
    return;
  }
  statusText.textContent = isListening ? "Listening" : "Ready";
}

function updateVoiceButtons() {
  if (!SpeechRecognition) {
    micButton.disabled = true;
    reportIssueButton.disabled = true;
    micButton.title = "Voice input is not supported in this browser";
    reportIssueButton.title = "Voice input is not supported in this browser";
  } else {
    micButton.disabled = busyState;
    reportIssueButton.disabled = busyState;
    micButton.classList.toggle("is-active", isListening);
    reportIssueButton.classList.toggle("is-active", isListening);
    micButton.title = isListening ? "Stop listening" : "Voice input";
    reportIssueButton.title = isListening ? "Stop listening" : "Report an issue by voice";
  }

  if (!("speechSynthesis" in window)) {
    speechToggle.disabled = true;
    speechToggle.title = "Spoken replies are not supported in this browser";
  } else {
    speechToggle.classList.toggle("is-muted", !spokenRepliesEnabled);
    speechToggle.title = spokenRepliesEnabled
      ? "Spoken replies on"
      : "Spoken replies off";
  }
}

function speak(text) {
  if (!spokenRepliesEnabled || !("speechSynthesis" in window)) {
    return;
  }
  window.speechSynthesis.cancel();
  const spokenText = String(text || "")
    .replace(/https?:\/\/\S+/gi, "a link")
    .replace(/[\*_#`]/g, "")
    .replace(/\s+/g, " ")
    .trim();
  if (!spokenText) {
    return;
  }
  const utterance = new SpeechSynthesisUtterance(spokenText);
  const requestedLanguage = browserLanguageCode();
  const voice = bestNaturalVoice(requestedLanguage);
  utterance.lang = voice?.lang || requestedLanguage;
  if (voice) {
    utterance.voice = voice;
  }
  utterance.rate = 0.96;
  utterance.pitch = 1;
  utterance.volume = 1;
  window.speechSynthesis.speak(utterance);
}

function addMessage(role, text) {
  const article = document.createElement("article");
  article.className = `message ${role}`;
  const avatar = document.createElement("div");
  avatar.className = "avatar";
  avatar.setAttribute("aria-hidden", "true");
  avatar.textContent = role === "user" ? "Y" : "A";
  const bubble = document.createElement("p");
  bubble.textContent = text;
  article.append(avatar, bubble);
  messages.append(article);
  messages.scrollTop = messages.scrollHeight;
  if (role === "assistant") {
    updatePatientInstruction(text);
  }
}

function updatePatientInstruction(text) {
  if (!text) {
    return;
  }
  patientInstructionText.textContent = text;
}

function updateCurrentTask(task, instruction = null, dueTask = null) {
  currentTaskText.textContent = task ? `Current task: ${task.task_name}` : "No task started";
  if (task) {
    patientTaskName.textContent = task.task_name;
    patientTaskMeta.textContent = `${task.scheduled_time} · ${task.time_of_day}`;
    updatePatientInstruction(instruction || "Use the buttons below.");
    return;
  }
  if (dueTask) {
    patientTaskName.textContent = dueTask.task_name;
    patientTaskMeta.textContent = `${dueTask.scheduled_time} · ${dueTask.time_of_day}`;
    updatePatientInstruction(`It is time to ${dueTask.task_name}.`);
    return;
  }
  patientTaskName.textContent = "No task open";
  patientTaskMeta.textContent = "Use the buttons below.";
  updatePatientInstruction("I am here with you.");
}

function renderClock(clock) {
  if (!clock) {
    return;
  }
  clockDisplay.textContent = `${clock.date} ${clock.time} (${clock.speed}x)`;
  const speedValue = String(clock.speed);
  const hasPreset = Array.from(clockSpeed.options).some(
    (option) => option.value === speedValue,
  );
  clockSpeed.value = hasPreset ? speedValue : "";
  if (document.activeElement !== customClockSpeed) {
    customClockSpeed.value = speedValue;
  }
  homeClockStatus.textContent = `${clock.speed}x speed`;
}

function renderClockTasks(tasks = []) {
  clockTaskList.innerHTML = "";
  clockTaskStatus.textContent = `${tasks.length} task${tasks.length === 1 ? "" : "s"}`;
  if (tasks.length === 0) {
    const emptyState = document.createElement("p");
    emptyState.className = "empty-state";
    emptyState.textContent = "No active tasks scheduled for today.";
    clockTaskList.append(emptyState);
    return;
  }
  tasks.forEach((task) => {
    const item = document.createElement("article");
    item.className = "clock-task-item";
    item.classList.toggle("is-past", Boolean(task.isPast));
    const time = document.createElement("div");
    time.className = "clock-task-time";
    time.textContent = task.scheduled_time || "";
    const main = document.createElement("div");
    main.className = "clock-task-main";
    const title = document.createElement("strong");
    title.textContent = task.task_name || "Task";
    const meta = document.createElement("span");
    meta.textContent = `${task.time_of_day || "Today"} · ${task.task_category || "Routine"}`;
    main.append(title, meta);
    const wait = document.createElement("div");
    wait.className = "clock-task-wait";
    wait.textContent = task.realTimeUntil || "Now";
    item.append(time, main, wait);
    clockTaskList.append(item);
  });
}

async function refreshClock() {
  if (!signedIn) {
    return;
  }
  try {
    const response = await fetch("/api/clock");
    const data = await response.json();
    renderClock(data.clock);
    renderClockTasks(data.tasks || []);
  } catch {
    clockDisplay.textContent = "Clock unavailable";
    clockTaskStatus.textContent = "Unavailable";
  }
}

async function updateClock(payload) {
  const response = await fetch("/api/clock", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.error || "Could not update clock.");
  }
  renderClock(data.clock);
  renderClockTasks(data.tasks || []);
  if (data.dashboard) {
    renderDashboard(data.dashboard);
  }
  if (data.clock) {
    checkPatientReminders();
  }
}

function updateReminderStatus(message = "") {
  if (!("Notification" in window)) {
    caregiverReminderToggle.disabled = true;
    caregiverReminderToggle.textContent = "Unavailable";
    caregiverReminderStatus.textContent = "Browser notifications are not supported here.";
    homeReminderStatus.textContent = "Unavailable";
    return;
  }
  notificationsEnabled = remindersEnabled && window.Notification.permission === "granted";
  caregiverReminderToggle.disabled = false;
  caregiverReminderToggle.textContent = remindersEnabled ? "On" : "Off";
  caregiverReminderToggle.setAttribute("aria-checked", String(remindersEnabled));
  caregiverReminderToggle.classList.toggle("is-on", remindersEnabled);
  homeReminderStatus.textContent = remindersEnabled ? "On" : "Off";
  if (message) {
    caregiverReminderStatus.textContent = message;
    return;
  }
  if (!remindersEnabled) {
    caregiverReminderStatus.textContent = "Reminders are off for this browser.";
    return;
  }
  if (window.Notification.permission === "denied") {
    caregiverReminderStatus.textContent = "Notifications are blocked in this browser.";
    return;
  }
  caregiverReminderStatus.textContent = notificationsEnabled
    ? "Patient task reminders are on for this browser."
    : "Turn reminders on to allow browser notifications.";
}

async function toggleReminderNotifications() {
  if (!("Notification" in window)) {
    updateReminderStatus();
    return;
  }
  if (remindersEnabled) {
    remindersEnabled = false;
    notificationsEnabled = false;
    window.localStorage.setItem("auraRemindersEnabled", "false");
    updateReminderStatus("Patient task reminders are off.");
    return;
  }
  const permission = await window.Notification.requestPermission();
  remindersEnabled = permission === "granted";
  notificationsEnabled = remindersEnabled;
  window.localStorage.setItem("auraRemindersEnabled", String(remindersEnabled));
  updateReminderStatus(
    remindersEnabled
      ? "Patient task reminders are on."
      : "Reminders were not enabled.",
  );
  if (notificationsEnabled) {
    checkPatientReminders();
  }
}

function updateCaregiverAlertNotificationStatus(message = "") {
  if (!("Notification" in window)) {
    caregiverAlertNotificationToggle.disabled = true;
    caregiverAlertNotificationToggle.textContent = "Unavailable";
    caregiverAlertNotificationStatus.textContent =
      "In-app alerts are active. Browser notifications are unavailable.";
    return;
  }
  const browserAlertsActive =
    caregiverAlertNotificationsEnabled && window.Notification.permission === "granted";
  caregiverAlertNotificationToggle.disabled = false;
  caregiverAlertNotificationToggle.textContent = browserAlertsActive ? "On" : "Off";
  caregiverAlertNotificationToggle.setAttribute(
    "aria-checked",
    String(browserAlertsActive),
  );
  caregiverAlertNotificationToggle.classList.toggle("is-on", browserAlertsActive);
  if (message) {
    caregiverAlertNotificationStatus.textContent = message;
    return;
  }
  if (window.Notification.permission === "denied") {
    caregiverAlertNotificationStatus.textContent =
      "In-app alerts are active. Browser notifications are blocked.";
    return;
  }
  caregiverAlertNotificationStatus.textContent = browserAlertsActive
    ? "In-app and browser caregiver alerts are active."
    : "In-app alerts are active. Browser notifications are off.";
}

async function toggleCaregiverAlertNotifications() {
  if (!("Notification" in window)) {
    updateCaregiverAlertNotificationStatus();
    return;
  }
  if (
    caregiverAlertNotificationsEnabled &&
    window.Notification.permission === "granted"
  ) {
    caregiverAlertNotificationsEnabled = false;
    window.localStorage.setItem("auraCaregiverAlertNotificationsEnabled", "false");
    updateCaregiverAlertNotificationStatus(
      "In-app alerts remain active. Browser notifications are off.",
    );
    return;
  }
  const permission = await window.Notification.requestPermission();
  caregiverAlertNotificationsEnabled = permission === "granted";
  window.localStorage.setItem(
    "auraCaregiverAlertNotificationsEnabled",
    String(caregiverAlertNotificationsEnabled),
  );
  updateCaregiverAlertNotificationStatus(
    caregiverAlertNotificationsEnabled
      ? "In-app and browser caregiver alerts are active."
      : "In-app alerts remain active. Browser notifications were not enabled.",
  );
}

function renderSmsSettings(message = "") {
  const hasPhone = Boolean(signedInAccount?.has_phone);
  const isEnabled = hasPhone && Boolean(signedInAccount?.sms_enabled);
  caregiverSmsToggle.disabled = !signedIn || selectedRole !== "caregiver" || !hasPhone;
  caregiverSmsToggle.textContent = hasPhone
    ? (isEnabled ? "Disable" : "Enable")
    : "Unavailable";
  caregiverSmsToggle.setAttribute("aria-checked", String(isEnabled));
  caregiverSmsToggle.classList.toggle("is-on", isEnabled);

  if (message) {
    caregiverSmsStatus.textContent = message;
    return;
  }
  if (!hasPhone) {
    caregiverSmsStatus.textContent =
      "Add an optional caregiver phone number at login to receive emergency and missed-task texts.";
    return;
  }
  const phoneEnding = signedInAccount.phone_last4
    ? ` ending in ${signedInAccount.phone_last4}`
    : "";
  if (isEnabled && !signedInAccount.sms_service_configured) {
    caregiverSmsStatus.textContent =
      `The phone${phoneEnding} is saved, but the Twilio text service is not configured.`;
    return;
  }
  caregiverSmsStatus.textContent = isEnabled
    ? `Emergency and missed-task texts are on for the phone${phoneEnding}.`
    : `Text messages are disabled for the phone${phoneEnding}.`;
}

async function toggleSmsMessages() {
  if (!signedInAccount?.has_phone) {
    renderSmsSettings();
    return;
  }
  const enable = !Boolean(signedInAccount.sms_enabled);
  caregiverSmsToggle.disabled = true;
  caregiverSmsStatus.textContent = enable
    ? "Enabling text messages..."
    : "Disabling text messages...";
  try {
    const response = await fetch("/api/sms-settings", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ enabled: enable }),
    });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || "Could not update text messages.");
    }
    signedInAccount = data.account;
    renderSmsSettings(
      enable ? "" : "Emergency and missed-task text messages are disabled.",
    );
  } catch (error) {
    renderSmsSettings(error.message || "Could not update text messages.");
  }
}

function playCaregiverAlertPing(isEmergency) {
  try {
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    if (!AudioContext) {
      return;
    }
    const context = new AudioContext();
    const frequencies = isEmergency ? [880, 660, 880] : [720, 720];
    frequencies.forEach((frequency, index) => {
      const oscillator = context.createOscillator();
      const gain = context.createGain();
      const start = context.currentTime + index * 0.22;
      oscillator.type = "sine";
      oscillator.frequency.value = frequency;
      gain.gain.setValueAtTime(0.001, start);
      gain.gain.exponentialRampToValueAtTime(0.18, start + 0.02);
      gain.gain.exponentialRampToValueAtTime(0.001, start + 0.18);
      oscillator.connect(gain);
      gain.connect(context.destination);
      oscillator.start(start);
      oscillator.stop(start + 0.2);
    });
  } catch {
    // The visual alert remains available if audio playback is blocked.
  }
}

function showCaregiverLiveAlert(alert, newAlertCount = 1) {
  const isEmergency = String(alert.severity || "").toLowerCase() === "emergency";
  const isMissedTask = String(alert.reason || "").toLowerCase().includes("missed");
  caregiverLiveAlert.classList.toggle("is-emergency", isEmergency);
  caregiverLiveAlertTitle.textContent = isEmergency
    ? "Emergency alert"
    : isMissedTask
      ? "Missed task alert"
      : "Caregiver alert";
  const taskPrefix = alert.task_name ? `${alert.task_name}: ` : "";
  const countSuffix = newAlertCount > 1 ? ` ${newAlertCount} new alerts received.` : "";
  caregiverLiveAlertMessage.textContent = `${taskPrefix}${alert.reason || "Caregiver review is recommended."}${countSuffix}`;
  caregiverLiveAlert.hidden = false;
  playCaregiverAlertPing(isEmergency);

  if (
    caregiverAlertNotificationsEnabled &&
    "Notification" in window &&
    window.Notification.permission === "granted"
  ) {
    new window.Notification(
      isEmergency ? "AURA Emergency Alert" : isMissedTask ? "AURA Missed Task" : "AURA Caregiver Alert",
      {
        body: caregiverLiveAlertMessage.textContent,
        tag: `aura-caregiver-alert-${alert.alert_id}`,
        renotify: true,
        requireInteraction: isEmergency,
      },
    );
  }
}

async function checkCaregiverNotifications() {
  if (!signedIn || selectedRole !== "caregiver") {
    return;
  }
  try {
    const response = await fetch("/api/caregiver-notifications");
    const data = await readApiJson(response);
    if (!response.ok) {
      return;
    }
    const alerts = data.alerts || [];
    const latestAlertId = Number(data.latestAlertId || 0);
    renderAlerts(alerts);
    renderPatientCaregiverChat(data.patientMessages || []);

    if (!caregiverAlertBaselineReady) {
      caregiverAlertBaselineReady = true;
      lastCaregiverAlertId = latestAlertId;
      window.localStorage.setItem(caregiverAlertStorageKey, String(lastCaregiverAlertId));
      return;
    }
    if (latestAlertId < lastCaregiverAlertId && alerts.length) {
      lastCaregiverAlertId = 0;
    }
    const newAlerts = alerts
      .filter((alert) => Number(alert.alert_id || 0) > lastCaregiverAlertId)
      .sort((left, right) => Number(left.alert_id) - Number(right.alert_id));
    if (!newAlerts.length) {
      return;
    }
    lastCaregiverAlertId = latestAlertId;
    window.localStorage.setItem(caregiverAlertStorageKey, String(lastCaregiverAlertId));
    showCaregiverLiveAlert(newAlerts.at(-1), newAlerts.length);
  } catch {
    // Regular dashboard data remains available if a notification poll fails.
  }
}

function playReminderPing() {
  try {
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    if (!AudioContext) {
      return;
    }
    const context = new AudioContext();
    const oscillator = context.createOscillator();
    const gain = context.createGain();
    oscillator.type = "sine";
    oscillator.frequency.value = 740;
    gain.gain.setValueAtTime(0.001, context.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.16, context.currentTime + 0.02);
    gain.gain.exponentialRampToValueAtTime(0.001, context.currentTime + 0.45);
    oscillator.connect(gain);
    gain.connect(context.destination);
    oscillator.start();
    oscillator.stop(context.currentTime + 0.48);
  } catch {
    // Audio pings are a convenience; notification and speech still work.
  }
}

function notifyDueTask(task, clock) {
  if (!task || !remindersEnabled) {
    return;
  }
  const taskKey = `${clock?.date || ""}:${task.task_id}:${task.scheduled_time}`;
  if (taskKey === lastNotifiedTaskKey) {
    return;
  }
  lastNotifiedTaskKey = taskKey;
  const message = `It is time to ${task.task_name}.`;
  updateCurrentTask(null, null, task);
  caregiverReminderStatus.textContent = message;
  playReminderPing();
  speak(message);
  if (notificationsEnabled && "Notification" in window) {
    new window.Notification("AURA reminder", {
      body: message,
      tag: taskKey,
      renotify: true,
    });
  }
}

async function checkPatientReminders() {
  if (!signedIn) {
    return;
  }
  try {
    const response = await fetch("/api/patient-state");
    const data = await response.json();
    if (!response.ok) {
      return;
    }
    renderClock(data.clock);
    updateCurrentTask(data.currentTask, data.currentInstruction, data.dueTask);
    notifyDueTask(data.dueTask, data.clock);
    if (
      !patientCaregiverChatArea.hidden ||
      caregiverSectionPanels.patientChat?.classList.contains("is-active")
    ) {
      loadPatientCaregiverChat();
    }
  } catch {
    caregiverReminderStatus.textContent = "Reminder check is unavailable.";
  }
}

function setCaregiverChatBusy(isBusy) {
  caregiverMessageInput.disabled = isBusy;
  caregiverSendButton.disabled = isBusy;
}

function addCaregiverChatMessage(role, text) {
  const message = document.createElement("article");
  message.className = `caregiver-chat-message ${role}`;
  message.textContent = text;
  caregiverChatMessages.append(message);
  caregiverChatMessages.scrollTop = caregiverChatMessages.scrollHeight;
}

function renderCaregiverChat(chat = []) {
  caregiverChatMessages.innerHTML = "";
  if (chat.length === 0) {
    addCaregiverChatMessage("assistant", "I can help review the current records.");
    return;
  }
  chat.forEach((message) => {
    addCaregiverChatMessage(
      message.role === "caregiver" ? "caregiver" : "assistant",
      message.message,
    );
  });
}

function renderDirectChat(container, chat = []) {
  container.innerHTML = "";
  if (chat.length === 0) {
    const emptyState = document.createElement("p");
    emptyState.className = "empty-state";
    emptyState.textContent = "No messages yet.";
    container.append(emptyState);
    return;
  }
  chat.forEach((message) => {
    const item = document.createElement("article");
    item.className = `direct-chat-message ${message.sender === "caregiver" ? "caregiver" : "patient"}`;
    const label = document.createElement("span");
    label.textContent = message.sender === "caregiver" ? "Caregiver" : "Patient";
    const body = document.createElement("p");
    body.textContent = message.message || "";
    item.append(label, body);
    container.append(item);
  });
  container.scrollTop = container.scrollHeight;
}

function renderPatientCaregiverChat(chat = []) {
  renderDirectChat(patientCaregiverMessages, chat);
  renderDirectChat(caregiverPatientMessages, chat);
  homePatientChatStatus.textContent = chat.length
    ? `${chat.length} message${chat.length === 1 ? "" : "s"}`
    : "No messages";
  if (selectedRole !== "caregiver") {
    caregiverChatNotificationBadge.hidden = true;
    return;
  }
  const patientMessages = chat.filter((message) => message.sender === "patient");
  const latestPatientMessageId = Math.max(
    0,
    ...patientMessages.map((message) => Number(message.message_id || 0)),
  );
  const patientChatIsOpen = caregiverSectionPanels.patientChat?.classList.contains("is-active");
  if (patientChatIsOpen && latestPatientMessageId > lastReadPatientMessageId) {
    lastReadPatientMessageId = latestPatientMessageId;
    window.localStorage.setItem(
      caregiverChatReadStorageKey,
      String(lastReadPatientMessageId),
    );
  }
  const unreadCount = patientMessages.filter(
    (message) => Number(message.message_id || 0) > lastReadPatientMessageId,
  ).length;
  caregiverChatNotificationBadge.textContent = unreadCount > 99 ? "99+" : String(unreadCount);
  caregiverChatNotificationBadge.hidden = unreadCount === 0;
}

async function readApiJson(response) {
  const text = await response.text();
  try {
    return JSON.parse(text);
  } catch {
    throw new Error(
      response.ok
        ? "The server returned an invalid API response. Restart the AURA server and refresh this page."
        : "This AURA server does not have the latest API route. Restart the server, then refresh this page.",
    );
  }
}

async function loadPatientCaregiverChat() {
  if (!signedIn) {
    return;
  }
  try {
    const response = await fetch("/api/patient-caregiver-chat");
    const data = await readApiJson(response);
    if (!response.ok) {
      throw new Error(data.error || "Could not load patient chat.");
    }
    renderPatientCaregiverChat(data.messages || []);
  } catch (error) {
    renderPatientCaregiverChat([
      {
        sender: "caregiver",
        message: error.message,
      },
    ]);
  }
}

function renderAlerts(alerts = []) {
  alertList.innerHTML = "";
  const alertCount = alerts.length;
  caregiverNotificationBadge.textContent = alertCount > 99 ? "99+" : String(alertCount);
  caregiverNotificationBadge.hidden = alertCount === 0;
  caregiverNotificationButton.setAttribute(
    "aria-label",
    alertCount
      ? `Open caregiver alerts, ${alertCount} notification${alertCount === 1 ? "" : "s"}`
      : "Open caregiver alerts",
  );
  homeAlertStat.textContent = alerts.length;
  homeAlertStatus.textContent = alerts.length
    ? `${alerts.length} alert${alerts.length === 1 ? "" : "s"}`
    : "No alerts";
  if (alerts.length === 0) {
    const emptyState = document.createElement("p");
    emptyState.className = "empty-state";
    emptyState.textContent = "No safety alerts in this session.";
    alertList.append(emptyState);
    alertStatus.textContent = "Ready";
    return;
  }
  alerts.forEach((alert) => {
    const item = document.createElement("article");
    item.className = "alert-item";
    const title = document.createElement("strong");
    title.textContent = `${alert.severity} · ${alert.created_at || alert.date}`;
    const reason = document.createElement("p");
    reason.textContent = alert.reason;
    const textStatus = document.createElement("span");
    textStatus.textContent = alert.text_status || "Text status unavailable";
    item.append(title, reason, textStatus);
    alertList.append(item);
  });
  alertStatus.textContent = `${alerts.length} alert${alerts.length === 1 ? "" : "s"}`;
}

function renderRecentEvents(attempts = []) {
  recentEventsList.innerHTML = "";
  homeActivityStatus.textContent = attempts.length
    ? `${attempts.length} event${attempts.length === 1 ? "" : "s"} today`
    : "Nothing today";
  if (attempts.length === 0) {
    const emptyState = document.createElement("p");
    emptyState.className = "empty-state";
    emptyState.textContent = "No patient activity today.";
    recentEventsList.append(emptyState);
    return;
  }
  attempts.forEach((attempt) => {
    const item = document.createElement("article");
    item.className = "event-item";
    const meta = document.createElement("div");
    meta.className = "event-meta";
    meta.textContent = `${attempt.task_name} · ${attempt.scheduled_time}`;
    const details = document.createElement("p");
    const status = attempt.completed
      ? "Marked complete"
      : attempt.missed
        ? "Missed"
        : "Started";
    details.textContent = `${status}. Reminders: ${attempt.reminders_needed}. Adjusted score: ${attempt.adjusted_performance_score}.`;
    item.append(meta, details);
    recentEventsList.append(item);
  });
}

function updateCaregiverStats(insights = {}) {
  const counts = insights.counts || {};
  statElements.interactions.textContent = counts.total || 0;
  statElements.markedComplete.textContent = counts.completed || 0;
  statElements.helpRequests.textContent = counts.helpRequests || 0;
  statElements.reminderRequests.textContent = insights.tasksNeedingReminders?.length || 0;
  statElements.visualSupport.textContent = counts.missed || 0;
  statElements.confusionFlags.textContent = counts.confusionFlags || 0;
  homeCompletedStat.textContent = counts.completed || 0;
  homeHelpStat.textContent = counts.helpRequests || 0;
  homePerformanceStatus.textContent = insights.adjustedPerformance == null
    ? "No data"
    : `${insights.adjustedPerformance} adjusted`;
  homeDatasetStatus.textContent = `${counts.total || 0} record${counts.total === 1 ? "" : "s"}`;
}

function insightCard(label, value) {
  const card = document.createElement("div");
  card.className = "stat-card";
  const number = document.createElement("span");
  number.textContent = value ?? "Not enough data";
  const text = document.createElement("p");
  text.textContent = label;
  card.append(number, text);
  return card;
}

function renderInsights(insights = {}) {
  const summary = insights.detailSummary || {};
  insightGrid.innerHTML = "";
  [
    ["Task attempts", summary.taskAttempts || 0],
    ["Days recorded", summary.days || 0],
    ["Completion rate", summary.completionRate || "No data"],
    ["Raw average", summary.rawAverage ?? "No data"],
    ["Adjusted average", summary.adjustedAverage ?? "No data"],
    ["Alert rate", summary.caregiverAlertRate || "No data"],
    ["Help request rate", summary.helpRequestRate || "No data"],
    ["Possible confusion", summary.confusionFlags || 0],
    ["Total reminders", summary.totalReminders || 0],
  ].forEach(([label, value]) => {
    insightGrid.append(insightCard(label, value));
  });

  caregiverInsightSource.textContent = summary.taskAttempts
    ? `Based on ${summary.taskAttempts} stored attempts across ${summary.days} day${summary.days === 1 ? "" : "s"}, ${summary.dateRange}.`
    : "No stored patient task attempts are available yet.";

  renderInsightList(caregiverTimeInsightList, insights.timeOfDayDetails || [], [
    ["attempts", "Attempts"],
    ["avgPerformance", "Adjusted average"],
    ["avgRawPerformance", "Raw average"],
    ["avgDifficulty", "Average difficulty"],
    ["completionRate", "Completion rate"],
    ["struggleRate", "Support-need rate"],
    ["avgReminders", "Average reminders"],
    ["helpRate", "Help request rate"],
    ["confusionFlags", "Possible confusion flags"],
  ]);
  renderInsightList(caregiverDifficultyInsightList, insights.difficultyDetails || [], [
    ["attempts", "Attempts"],
    ["avgPerformance", "Adjusted average"],
    ["avgRawPerformance", "Raw average"],
    ["completionRate", "Completion rate"],
    ["struggleRate", "Support-need rate"],
    ["avgReminders", "Average reminders"],
    ["helpRate", "Help request rate"],
  ]);
  renderInsightList(caregiverDayInsightList, insights.dayOfWeekDetails || [], [
    ["attempts", "Attempts"],
    ["avgPerformance", "Adjusted average"],
    ["completionRate", "Completion rate"],
    ["struggleRate", "Support-need rate"],
    ["avgReminders", "Average reminders"],
    ["helpRate", "Help request rate"],
  ]);
  renderInsightList(caregiverTaskInsightList, insights.taskDetails || [], [
    ["attempts", "Attempts"],
    ["avgPerformance", "Adjusted average"],
    ["completionRate", "Completion rate"],
    ["struggleRate", "Support-need rate"],
    ["avgReminders", "Average reminders"],
    ["helpRate", "Help request rate"],
    ["confusionFlags", "Possible confusion flags"],
  ]);
  renderInsightList(caregiverTrendInsightList, insights.trendDetails || [], [
    ["earlierAverage", "Earlier adjusted average"],
    ["recentAverage", "Recent adjusted average"],
    ["change", "Change"],
    ["daysCompared", "Days compared"],
  ]);
  renderBullets(caregiverKeyFindings, insights.keyFindings || []);
  renderBullets(caregiverRecommendedActions, insights.recommendedActions || []);
  renderBullets(caregiverDataNotes, insights.dataNotes || []);
}

function renderRoutines(routines = []) {
  routineList.innerHTML = "";
  routineCount.textContent = `${routines.length} routine${routines.length === 1 ? "" : "s"}`;
  homeScheduleStatus.textContent = `${routines.length} routine${routines.length === 1 ? "" : "s"}`;
  routines.forEach((routine) => {
    const item = document.createElement("article");
    item.className = "routine-item";
    const header = document.createElement("div");
    header.className = "routine-item-header";
    const title = document.createElement("strong");
    title.textContent = `${routine.scheduled_time} · ${routine.task_name}`;
    const deleteButton = document.createElement("button");
    deleteButton.className = "danger-link-button";
    deleteButton.type = "button";
    deleteButton.textContent = "Delete";
    deleteButton.addEventListener("click", () => deleteRoutine(routine.task_id));
    header.append(title, deleteButton);
    const detail = document.createElement("p");
    detail.textContent = `${routine.task_category}. Difficulty ${routine.task_difficulty}. Importance ${routine.task_importance}.`;
    item.append(header, detail);
    routineList.append(item);
  });
}

function datasetMetric(label, value) {
  const card = document.createElement("div");
  card.className = "stat-card";
  const number = document.createElement("span");
  number.textContent = value ?? "0";
  const text = document.createElement("p");
  text.textContent = label;
  card.append(number, text);
  return card;
}

function statusTextForAttempt(record) {
  if (record.completed) {
    return "Marked complete";
  }
  if (record.missed) {
    return "Missed";
  }
  return "Started";
}

function yesNo(value) {
  return value ? "Yes" : "No";
}

function labelForDatasetColumn(key) {
  const labels = {
    user_id: "User ID",
    date: "Date",
    day_of_week: "Day",
    time_of_day: "Time of Day",
    scheduled_time: "Scheduled",
    task_name: "Task",
    task_category: "Category",
    task_importance: "Importance",
    patient_marked_complete: "Marked Complete",
    reminders_needed: "Reminders",
    help_requested: "Help",
    visual_support_used: "Visual Support",
    confusion_flag: "Possible Confusion",
    time_to_complete_min: "Minutes",
    performance_score: "Performance",
    task_status: "Status",
    caregiver_alert_sent: "Caregiver Alert",
    alert_reason: "Alert Reason",
    recommended_action: "Recommended Action",
    notes: "Notes",
    task_difficulty: "Difficulty",
    difficulty_score: "Difficulty Score",
    struggle_flag: "Struggle Flag",
    struggle_evidence: "Struggle Evidence",
    completion_source: "Completion Source",
    caregiver_verified: "Caregiver Verified",
    device_verified: "Device Verified",
    verified_completion_status: "Verification Status",
    completion_confidence_pct: "Confidence %",
    analysis_note: "Analysis Note",
    difficulty_adjusted_score: "Adjusted Score",
    support_need_score: "Support Need",
    support_need_level: "Support Level",
  };
  return labels[key] || key.replaceAll("_", " ");
}

function renderDatasetHeaders(tableBody, columns = []) {
  const headerRow = tableBody.closest("table")?.querySelector("thead tr");
  if (!headerRow) {
    return;
  }
  headerRow.innerHTML = "";
  columns.forEach((column) => {
    const header = document.createElement("th");
    header.textContent = labelForDatasetColumn(column);
    headerRow.append(header);
  });
}

function renderDatasetRows(tableBody, records = [], columns = []) {
  const activeColumns = columns.length
    ? columns
    : [
        "date",
        "scheduled_time",
        "task_name",
        "task_status",
        "reminders_needed",
        "help_requested",
        "confusion_flag",
        "performance_score",
        "difficulty_adjusted_score",
        "notes",
      ];
  renderDatasetHeaders(tableBody, activeColumns);
  tableBody.innerHTML = "";
  if (records.length === 0) {
    const row = document.createElement("tr");
    const cell = document.createElement("td");
    cell.colSpan = activeColumns.length;
    cell.textContent = "No patient task records yet.";
    row.append(cell);
    tableBody.append(row);
    return;
  }

  records.forEach((record) => {
    const row = document.createElement("tr");
    activeColumns.forEach((column) => {
      const cell = document.createElement("td");
      cell.textContent = record[column] ?? "";
      row.append(cell);
    });
    tableBody.append(row);
  });
}

function renderDataset(dataset) {
  if (!dataset) {
    return;
  }
  const summary = dataset.summary || {};
  const records = dataset.records || [];
  const columns = dataset.columns || [];
  homeDatasetStatus.textContent = `${records.length} record${records.length === 1 ? "" : "s"}`;
  datasetPathText.textContent = dataset.databasePath
    ? `Stored in ${dataset.databasePath}`
    : "Stored in SQLite.";
  datasetSummaryGrid.innerHTML = "";
  [
    ["Records", summary.total || 0],
    ["Marked complete", summary.completed || 0],
    ["Missed", summary.missed || 0],
    ["Help requests", summary.help_requests || 0],
    ["Possible confusion", summary.confusion_flags || 0],
    ["Adjusted avg", summary.adjusted_average ?? "No data"],
  ].forEach(([label, value]) => {
    datasetSummaryGrid.append(datasetMetric(label, value));
  });

  renderDatasetRows(datasetTableBody, records, columns);
}

function renderAdminDataset(dataset) {
  const summary = dataset?.summary || {};
  const records = dataset?.records || [];
  const columns = dataset?.columns || [];
  adminSummaryGrid.innerHTML = "";
  [
    ["Records", summary.total || 0],
    ["Marked complete", summary.completed || 0],
    ["Missed", summary.missed || 0],
    ["Help requests", summary.help_requests || 0],
    ["Possible confusion", summary.confusion_flags || 0],
    ["Adjusted avg", summary.adjusted_average ?? "No data"],
  ].forEach(([label, value]) => {
    adminSummaryGrid.append(datasetMetric(label, value));
  });
  renderDatasetRows(adminDatasetTableBody, records, columns);
}

function renderInsightList(container, items = [], fields = []) {
  container.innerHTML = "";
  if (!items.length) {
    const emptyState = document.createElement("p");
    emptyState.className = "empty-state";
    emptyState.textContent = "No insight data available.";
    container.append(emptyState);
    return;
  }
  items.forEach((item) => {
    const card = document.createElement("article");
    card.className = "admin-insight-item";
    const title = document.createElement("strong");
    title.textContent = item.label;
    card.append(title);
    const metrics = document.createElement("div");
    metrics.className = "insight-metrics";
    fields.forEach(([key, label]) => {
      const row = document.createElement("div");
      row.className = "insight-metric";
      const metricLabel = document.createElement("span");
      metricLabel.textContent = label;
      const metricValue = document.createElement("b");
      metricValue.textContent = item[key] ?? "No data";
      row.append(metricLabel, metricValue);
      metrics.append(row);
    });
    card.append(metrics);
    if (item.interpretation) {
      const note = document.createElement("span");
      note.className = "insight-interpretation";
      note.textContent = item.interpretation;
      card.append(note);
    }
    container.append(card);
  });
}

function renderBullets(container, items = []) {
  container.innerHTML = "";
  if (!items.length) {
    const empty = document.createElement("li");
    empty.textContent = "No notes available.";
    container.append(empty);
    return;
  }
  items.forEach((item) => {
    const li = document.createElement("li");
    li.textContent = item;
    container.append(li);
  });
}

function renderDummyInsights(insights = {}) {
  const summary = insights.summary || {};
  adminDummyInsightSource.textContent = insights.sourceFound
    ? `Based on ${insights.sourcePath}`
    : `Reference file not found at ${insights.sourcePath || "Downloads/Main dataset.xlsx"}. Showing bundled insight summary.`;
  adminDummySummaryGrid.innerHTML = "";
  [
    ["Task attempts", summary.taskAttempts || 0],
    ["Completion rate", summary.completionRate || "No data"],
    ["Avg performance", summary.avgPerformanceScore ?? "No data"],
    ["Alert rate", summary.caregiverAlertRate || "No data"],
    ["Possible confusion", summary.confusionFlags || 0],
    ["Visual supports", summary.visualSupportsUsed || 0],
  ].forEach(([label, value]) => {
    adminDummySummaryGrid.append(datasetMetric(label, value));
  });
  renderInsightList(adminDummyTimeList, insights.timeOfDay || [], [
    ["avgPerformance", "Avg performance"],
    ["completionRate", "Completion rate"],
    ["alertRate", "Alert rate"],
    ["confusionFlags", "Possible confusion flags"],
  ]);
  renderInsightList(adminDummyDifficultyList, insights.difficulty || [], [
    ["avgPerformance", "Avg performance"],
    ["struggleRate", "Struggle rate"],
    ["avgReminders", "Avg reminders"],
    ["attempts", "Attempts"],
  ]);
  renderBullets(adminDummyFindings, insights.keyFindings || []);
  renderBullets(adminDummyActions, insights.recommendedActions || []);
  renderBullets(adminDummyModelingNotes, insights.modelingNotes || []);
}

function renderAdmin(data) {
  const accounts = data?.accounts || [];
  selectedAdminUserId = data?.selectedUserId || "";
  const selectedAccount = accounts.find(
    (account) => account.username === selectedAdminUserId,
  );

  adminDatabasePath.textContent = data?.databasePath
    ? `Stored in ${data.databasePath}`
    : "Stored in SQLite.";
  adminAccountCount.textContent = `${accounts.length} account${accounts.length === 1 ? "" : "s"}`;
  adminAccountList.innerHTML = "";

  if (accounts.length === 0) {
    const emptyState = document.createElement("p");
    emptyState.className = "empty-state";
    emptyState.textContent = "No accounts have been created yet.";
    adminAccountList.append(emptyState);
  }

  accounts.forEach((account) => {
    const button = document.createElement("button");
    button.className = "admin-account-button";
    button.type = "button";
    button.classList.toggle("is-active", account.username === selectedAdminUserId);

    const title = document.createElement("strong");
    title.textContent = account.patient_name || account.username;
    const meta = document.createElement("span");
    const adjusted = account.adjusted_average ?? "No data";
    meta.textContent = `${account.username} · ${account.records || 0} records · Avg ${adjusted}`;
    button.append(title, meta);
    button.addEventListener("click", () => loadAdminDataset(account.username));
    adminAccountList.append(button);
  });

  adminDatasetTitle.textContent = selectedAccount
    ? `${selectedAccount.patient_name}'s Dataset`
    : "Dataset";
  adminDatasetSubtitle.textContent = selectedAccount
    ? `Caregiver: ${selectedAccount.caregiver_name}. User: ${selectedAccount.username}.`
    : "Choose an account.";
  adminExportLink.href = selectedAdminUserId
    ? `/api/admin-export?user_id=${encodeURIComponent(selectedAdminUserId)}`
    : "/api/admin-export";
  adminExportLink.classList.toggle("is-disabled", !selectedAdminUserId);
  renderAdminDataset(data?.dataset);
  renderDummyInsights(data?.dummyInsights);
}

function showAdminView(data) {
  adminSignedIn = true;
  authView.hidden = true;
  appContent.hidden = true;
  adminLoginModal.hidden = true;
  adminView.hidden = false;
  stopListening();
  renderAdmin(data.admin || data);
  switchAdminSection("datasets");
}

function hideAdminModal() {
  adminLoginModal.hidden = true;
  adminModalUsername.value = "";
  adminModalPassword.value = "";
  adminModalError.hidden = true;
  adminModalError.textContent = "";
}

async function submitAdminLogin(username, password, errorTarget = authStatus) {
  errorTarget.textContent = "Checking";
  errorTarget.hidden = false;
  const response = await fetch("/api/admin-login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.error || "Admin login failed.");
  }
  errorTarget.textContent = "";
  showAdminView(data);
}

async function loadAdminDataset(userId = selectedAdminUserId) {
  if (!adminSignedIn) {
    return;
  }
  try {
    const url = userId
      ? `/api/admin?user_id=${encodeURIComponent(userId)}`
      : "/api/admin";
    const response = await fetch(url);
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || "Could not load admin datasets.");
    }
    renderAdmin(data);
  } catch (error) {
    adminDatasetTableBody.innerHTML = "";
    const row = document.createElement("tr");
    const cell = document.createElement("td");
    cell.colSpan = 10;
    cell.textContent = error.message;
    row.append(cell);
    adminDatasetTableBody.append(row);
  }
}

function leaveAdminView() {
  adminView.hidden = true;
  if (signedIn) {
    appContent.hidden = false;
    authView.hidden = true;
    return;
  }
  authView.hidden = false;
  appContent.hidden = true;
  showAuthMode("login");
}

function renderDashboard(data) {
  if (!data) {
    return;
  }
  renderClock(data.clock);
  updateCaregiverStats(data.insights);
  caregiverUpdateText.textContent = data.summary || "No summary available yet.";
  caregiverHomeSummary.textContent = data.summary || "No patient activity has been recorded yet.";
  homeUpdateStatus.textContent = "Ready";
  renderRecentEvents(data.todayActivity);
  renderAlerts(data.alerts);
  renderCaregiverChat(data.caregiverChat);
  renderRoutines(data.routines);
  renderInsights(data.insights);
  if (datasetUnlocked && caregiverSectionPanels.dataset?.classList.contains("is-active")) {
    loadDataset();
  }
}

async function loadDataset() {
  if (!datasetUnlocked) {
    return;
  }
  try {
    const response = await fetch("/api/dataset");
    const data = await response.json();
    if (!response.ok) {
      if (response.status === 403) {
        datasetUnlocked = false;
        throw new Error("Sign in through the caregiver interface to view the dataset.");
      }
      throw new Error(data.error || "Could not load dataset.");
    }
    renderDataset(data);
  } catch (error) {
    datasetTableBody.innerHTML = "";
    const row = document.createElement("tr");
    const cell = document.createElement("td");
    cell.colSpan = 10;
    cell.textContent = error.message;
    row.append(cell);
    datasetTableBody.append(row);
  }
}

async function refreshCaregiverUpdate(showLoading = true) {
  if (!signedIn || !caregiverUnlocked) {
    return;
  }
  if (showLoading) {
    caregiverStatus.textContent = "Updating";
  }
  refreshCaregiverButton.disabled = true;
  try {
    const response = await fetch("/api/caregiver");
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || "Could not load caregiver dashboard.");
    }
    renderDashboard(data);
    caregiverStatus.textContent = "Ready";
  } catch (error) {
    caregiverStatus.textContent = "Error";
    caregiverUpdateText.textContent = error.message;
  } finally {
    refreshCaregiverButton.disabled = false;
  }
}

async function resetCaregiverMessagesAndAlerts() {
  resetCaregiverButton.disabled = true;
  caregiverResetStatus.textContent = "Clearing...";
  try {
    const response = await fetch("/api/caregiver-reset", { method: "POST" });
    const data = await readApiJson(response);
    if (!response.ok) {
      throw new Error(data.error || "Could not reset caregiver messages.");
    }
    renderDashboard(data.dashboard);
    renderPatientCaregiverChat(data.patientMessages || []);
    lastReadPatientMessageId = 0;
    if (caregiverChatReadStorageKey) {
      window.localStorage.setItem(caregiverChatReadStorageKey, "0");
    }
    caregiverChatNotificationBadge.hidden = true;
    caregiverLiveAlert.hidden = true;
    caregiverResetStatus.textContent = "Cleared";
  } catch (error) {
    caregiverResetStatus.textContent = error.message;
  } finally {
    resetCaregiverButton.disabled = false;
  }
}

async function deleteRoutine(taskId) {
  if (!window.confirm("Permanently delete this scheduled task?")) {
    return;
  }
  try {
    const response = await fetch("/api/routines/delete", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ task_id: taskId }),
    });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || "Could not delete routine.");
    }
    renderRoutines(data.routines);
    if (data.dashboard) {
      renderDashboard(data.dashboard);
    }
    fetchPatientState();
  } catch (error) {
    caregiverUpdateText.textContent = error.message;
  }
}

async function clearPatientDataset(password) {
  const response = await fetch("/api/dataset-clear", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      password,
      confirm: true,
    }),
  });
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.error || "Could not clear dataset.");
  }
  hidePasswordModal();
  datasetUnlocked = true;
  renderDataset(data.dataset);
  renderDashboard(data.dashboard);
  updateCurrentTask(data.currentTask, data.currentInstruction, data.dueTask);
}

async function sendMessage(message) {
  const trimmedMessage = message.trim();
  if (!trimmedMessage) {
    return;
  }
  stopListening();
  addMessage("user", trimmedMessage);
  messageInput.value = "";
  messageInput.style.height = "auto";
  setBusy(true);
  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message: trimmedMessage,
        language: currentLanguageCode(),
      }),
    });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || "The request failed.");
    }
    addMessage("assistant", data.answer);
    updateCurrentTask(data.currentTask, data.currentInstruction, data.dueTask);
    if (data.dashboard) {
      renderDashboard(data.dashboard);
    }
    if (data.clock) {
      renderClock(data.clock);
    }
    if (trimmedMessage.toLowerCase() === "help") {
      patientInstructionText.textContent = data.answer;
      patientTaskMeta.textContent = data.alert
        ? "Your caregiver received an alert."
        : "Your caregiver has been notified.";
      updateStatus("Caregiver notified");
    }
    speak(data.answer);
  } catch (error) {
    addMessage("assistant", error.message);
  } finally {
    setBusy(false);
    if (patientChatArea.hidden) {
      document.querySelector(".patient-action")?.focus();
    } else {
      messageInput.focus();
    }
  }
}

async function sendCaregiverMessage(message) {
  const trimmedMessage = message.trim();
  if (!trimmedMessage) {
    return;
  }
  addCaregiverChatMessage("caregiver", trimmedMessage);
  caregiverMessageInput.value = "";
  caregiverMessageInput.style.height = "auto";
  setCaregiverChatBusy(true);
  try {
    const response = await fetch("/api/caregiver-chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message: trimmedMessage,
        language: currentLanguageCode(),
      }),
    });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || "The caregiver request failed.");
    }
    addCaregiverChatMessage("assistant", data.answer);
    renderDashboard(data.dashboard);
  } catch (error) {
    addCaregiverChatMessage("assistant", error.message);
  } finally {
    setCaregiverChatBusy(false);
    caregiverMessageInput.focus();
  }
}

async function sendPatientCaregiverMessage(sender, input, button) {
  const trimmedMessage = input.value.trim();
  if (!trimmedMessage) {
    return;
  }
  input.value = "";
  input.style.height = "auto";
  input.disabled = true;
  button.disabled = true;
  try {
    const response = await fetch("/api/patient-caregiver-chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        sender,
        message: trimmedMessage,
      }),
    });
    const data = await readApiJson(response);
    if (!response.ok) {
      throw new Error(data.error || "Could not send message.");
    }
    renderPatientCaregiverChat(data.messages || []);
  } catch (error) {
    renderPatientCaregiverChat([
      {
        sender: "caregiver",
        message: error.message,
      },
    ]);
  } finally {
    input.disabled = false;
    button.disabled = false;
    input.focus();
  }
}

async function saveRoutine() {
  const submitButton = routineForm.querySelector('button[type="submit"]');
  routineFormStatus.textContent = "Saving routine...";
  submitButton.disabled = true;
  const instructions = document
    .querySelector("#routineInstructions")
    .value.split("\n")
    .map((line) => line.trim())
    .filter(Boolean);
  const payload = {
    task_name: document.querySelector("#routineName").value,
    task_category: document.querySelector("#routineCategory").value,
    scheduled_time: document.querySelector("#routineTime").value,
    time_of_day: document.querySelector("#routineTimeOfDay").value,
    task_difficulty: Number(document.querySelector("#routineDifficulty").value),
    task_importance: Number(document.querySelector("#routineImportance").value),
    repeat_schedule: "Daily",
    active: true,
    instructions,
  };
  const response = await fetch("/api/routines", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const data = await readApiJson(response);
  if (!response.ok) {
    submitButton.disabled = false;
    throw new Error(data.error || "Could not save routine.");
  }
  renderRoutines(data.routines);
  if (data.dashboard) {
    renderDashboard(data.dashboard);
  }
  routineForm.reset();
  document.querySelector("#routineTime").value = "09:00";
  document.querySelector("#routineDifficulty").value = "3";
  document.querySelector("#routineImportance").value = "3";
  routineFormStatus.textContent = `Saved ${data.routine?.task_name || "routine"}.`;
  submitButton.disabled = false;
}

function setupSpeechRecognition() {
  if (!SpeechRecognition) {
    updateVoiceButtons();
    return;
  }
  recognition = new SpeechRecognition();
  recognition.continuous = true;
  recognition.interimResults = true;
  recognition.lang = browserLanguageCode();
  recognition.addEventListener("start", () => {
    isListening = true;
    updateVoiceButtons();
    updateStatus();
  });
  recognition.addEventListener("result", (event) => {
    let interimTranscript = "";
    let completedTranscript = "";
    for (let index = event.resultIndex; index < event.results.length; index += 1) {
      const transcript = event.results[index][0].transcript;
      if (event.results[index].isFinal) {
        completedTranscript += transcript;
      } else {
        interimTranscript += transcript;
      }
    }
    if (completedTranscript.trim()) {
      finalTranscript = `${finalTranscript} ${completedTranscript}`.trim();
    }
    messageInput.value = `${finalTranscript} ${interimTranscript}`.trim();
    messageInput.style.height = "auto";
    messageInput.style.height = `${messageInput.scrollHeight}px`;
    if (finalTranscript) {
      const message = finalTranscript;
      finalTranscript = "";
      shouldKeepListening = false;
      if (isListening) {
        recognition.stop();
      }
      sendMessage(message);
    }
  });
  recognition.addEventListener("error", () => {
    shouldKeepListening = false;
    isListening = false;
    updateVoiceButtons();
    updateStatus("Voice stopped");
  });
  recognition.addEventListener("end", () => {
    isListening = false;
    updateVoiceButtons();
    if (shouldKeepListening && !busyState) {
      restartTimer = window.setTimeout(() => {
        restartTimer = null;
        startListening();
      }, 300);
      return;
    }
    updateStatus();
  });
}

function updateRecognitionLanguage() {
  if (recognition) {
    recognition.lang = browserLanguageCode();
  }
}

async function startListening() {
  if (!recognition || busyState) {
    return;
  }
  if (window.location.protocol === "file:") {
    updateStatus("Open AURA through its web server first");
    return;
  }
  window.clearTimeout(restartTimer);
  finalTranscript = "";
  shouldKeepListening = true;
  try {
    updateStatus("Allow microphone");
    if (navigator.mediaDevices?.getUserMedia) {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      stream.getTracks().forEach((track) => track.stop());
    }
    window.speechSynthesis?.cancel();
    recognition.start();
  } catch {
    shouldKeepListening = false;
    isListening = false;
    updateVoiceButtons();
    updateStatus("Microphone blocked");
  }
}

function stopListening() {
  shouldKeepListening = false;
  window.clearTimeout(restartTimer);
  if (!recognition || !isListening) {
    updateVoiceButtons();
    updateStatus();
    return;
  }
  recognition.stop();
}

caregiverSubtabs.forEach((tab) => {
  tab.addEventListener("click", () => {
    switchCaregiverSection(tab.dataset.caregiverSection);
  });
});

caregiverHomeButton.addEventListener("click", () => {
  switchCaregiverSection("home");
  document.querySelector(".caregiver-home-card")?.focus();
});

caregiverAuraChatLauncher.addEventListener("click", () => {
  switchCaregiverSection("chat");
});

adminSubtabs.forEach((tab) => {
  tab.addEventListener("click", () => {
    switchAdminSection(tab.dataset.adminSection);
  });
});

chatForm.addEventListener("submit", (event) => {
  event.preventDefault();
  sendMessage(messageInput.value);
});

caregiverChatForm.addEventListener("submit", (event) => {
  event.preventDefault();
  sendCaregiverMessage(caregiverMessageInput.value);
});

patientCaregiverChatForm.addEventListener("submit", (event) => {
  event.preventDefault();
  sendPatientCaregiverMessage(
    "patient",
    patientCaregiverMessageInput,
    patientCaregiverSendButton,
  );
});

caregiverPatientChatForm.addEventListener("submit", (event) => {
  event.preventDefault();
  sendPatientCaregiverMessage(
    "caregiver",
    caregiverPatientMessageInput,
    caregiverPatientSendButton,
  );
});

routineForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  try {
    await saveRoutine();
  } catch (error) {
    routineFormStatus.textContent = error.message;
    routineForm.querySelector('button[type="submit"]').disabled = false;
  }
});

messageInput.addEventListener("input", () => {
  messageInput.style.height = "auto";
  messageInput.style.height = `${messageInput.scrollHeight}px`;
});

caregiverMessageInput.addEventListener("input", () => {
  caregiverMessageInput.style.height = "auto";
  caregiverMessageInput.style.height = `${caregiverMessageInput.scrollHeight}px`;
});

patientCaregiverMessageInput.addEventListener("input", () => {
  patientCaregiverMessageInput.style.height = "auto";
  patientCaregiverMessageInput.style.height = `${patientCaregiverMessageInput.scrollHeight}px`;
});

caregiverPatientMessageInput.addEventListener("input", () => {
  caregiverPatientMessageInput.style.height = "auto";
  caregiverPatientMessageInput.style.height = `${caregiverPatientMessageInput.scrollHeight}px`;
});

messageInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    chatForm.requestSubmit();
  }
});

caregiverMessageInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    caregiverChatForm.requestSubmit();
  }
});

patientCaregiverMessageInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    patientCaregiverChatForm.requestSubmit();
  }
});

caregiverPatientMessageInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    caregiverPatientChatForm.requestSubmit();
  }
});

quickButtons.forEach((button) => {
  button.addEventListener("click", () => sendMessage(button.dataset.message || ""));
});

patientChatToggle.addEventListener("click", () => {
  setPatientChatOpen(patientChatArea.hidden);
});

patientChatBackButton.addEventListener("click", () => {
  setPatientChatOpen(false);
});

patientCaregiverChatToggle.addEventListener("click", () => {
  setPatientWorkspaceMode("caregiverChat");
});

patientCaregiverChatBackButton.addEventListener("click", () => {
  setPatientWorkspaceMode("main");
});

reportIssueButton.addEventListener("click", () => {
  if (isListening) {
    stopListening();
    return;
  }
  startListening();
});

caregiverReminderToggle.addEventListener("click", () => {
  toggleReminderNotifications();
});

caregiverAlertNotificationToggle.addEventListener("click", () => {
  toggleCaregiverAlertNotifications();
});

caregiverSmsToggle.addEventListener("click", () => {
  toggleSmsMessages();
});

caregiverLiveAlertView.addEventListener("click", () => {
  caregiverLiveAlert.hidden = true;
  switchCaregiverSection("alerts");
});

caregiverLiveAlertDismiss.addEventListener("click", () => {
  caregiverLiveAlert.hidden = true;
});

micButton.addEventListener("click", () => {
  if (isListening) {
    stopListening();
    return;
  }
  startListening();
});

speechToggle.addEventListener("click", () => {
  spokenRepliesEnabled = !spokenRepliesEnabled;
  if (!spokenRepliesEnabled && "speechSynthesis" in window) {
    window.speechSynthesis.cancel();
  }
  updateVoiceButtons();
});

clearButton.addEventListener("click", async () => {
  setBusy(true);
  try {
    await fetch("/api/clear", { method: "POST" });
    messages.innerHTML = "";
    addMessage("assistant", "Conversation memory cleared.");
  } catch {
    addMessage("assistant", "I could not clear the conversation.");
  } finally {
    setBusy(false);
    if (patientChatArea.hidden) {
      document.querySelector(".patient-action")?.focus();
    } else {
      messageInput.focus();
    }
  }
});

refreshCaregiverButton.addEventListener("click", () => refreshCaregiverUpdate());

resetCaregiverButton.addEventListener("click", () => {
  const confirmed = window.confirm(
    "Clear caregiver chat messages and safety alerts? This cannot be undone.",
  );
  if (!confirmed) {
    return;
  }
  resetCaregiverMessagesAndAlerts();
});

clearDatasetButton.addEventListener("click", () => {
  datasetWarningModal.hidden = false;
});

datasetWarningForm.addEventListener("submit", (event) => {
  event.preventDefault();
  datasetWarningModal.hidden = true;
  showPasswordModal("clearDataset");
});

cancelDatasetWarningButton.addEventListener("click", () => {
  datasetWarningModal.hidden = true;
});

showLoginButton.addEventListener("click", () => showAuthMode("login"));

welcomeStartButton.addEventListener("click", () => {
  welcomeView.hidden = true;
  authView.hidden = false;
  window.setTimeout(() => {
    if (!signupForm.hidden) {
      signupPatientName.focus();
      return;
    }
    loginUsername.focus();
  }, 0);
});

authWelcomeButton.addEventListener("click", () => {
  authStatus.textContent = "";
  authView.hidden = true;
  welcomeView.hidden = false;
  welcomeStartButton.focus();
});

showSignupButton.addEventListener("click", () => showAuthMode("signup"));

showAdminButton.addEventListener("click", () => showAuthMode("admin"));

loginForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  try {
    await submitAuth("/api/login", {
      username: loginUsername.value,
      password: loginPassword.value,
      caregiver_password: loginCaregiverPassword.value,
      caregiver_phone: loginCaregiverPhone.value,
      role: selectedAuthRole(),
      language: languageSelect.value || "auto",
    });
    loginPassword.value = "";
    loginCaregiverPassword.value = "";
    loginCaregiverPhone.value = "";
  } catch (error) {
    authStatus.textContent = error.message;
    loginCaregiverPassword.select();
  }
});

signupForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  try {
    await submitAuth("/api/register", {
      patient_name: signupPatientName.value,
      caregiver_name: signupCaregiverName.value,
      username: signupUsername.value,
      password: signupPassword.value,
      caregiver_password: signupCaregiverPassword.value,
      caregiver_phone: signupCaregiverPhone.value,
      role: selectedAuthRole(),
      language: languageSelect.value || "auto",
    });
    signupPassword.value = "";
    signupCaregiverPassword.value = "";
    signupCaregiverPhone.value = "";
  } catch (error) {
    authStatus.textContent = error.message;
    signupCaregiverPassword.select();
  }
});

adminLoginForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  try {
    await submitAdminLogin(adminUsername.value, adminPassword.value, authStatus);
    adminPassword.value = "";
  } catch (error) {
    authStatus.textContent = error.message;
    adminPassword.select();
  }
});

openAdminButton.addEventListener("click", () => {
  adminModalError.hidden = true;
  adminModalError.textContent = "";
  adminModalUsername.value = "";
  adminModalPassword.value = "";
  adminLoginModal.hidden = false;
  adminModalUsername.focus();
});

adminModalForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  adminModalError.hidden = true;
  adminModalError.textContent = "";
  try {
    await submitAdminLogin(
      adminModalUsername.value,
      adminModalPassword.value,
      adminModalError,
    );
    hideAdminModal();
  } catch (error) {
    adminModalError.textContent = error.message;
    adminModalError.hidden = false;
    adminModalPassword.select();
  }
});

cancelAdminModalButton.addEventListener("click", hideAdminModal);

adminBackButton.addEventListener("click", leaveAdminView);

adminLogoutButton.addEventListener("click", async () => {
  try {
    await fetch("/api/admin-logout", { method: "POST" });
  } finally {
    adminSignedIn = false;
    selectedAdminUserId = "";
    leaveAdminView();
  }
});

logoutButton.addEventListener("click", async () => {
  try {
    await fetch("/api/logout", { method: "POST" });
  } finally {
    setSignedOut("Signed out.", true);
  }
});

clockSpeed.addEventListener("change", async () => {
  if (clockSpeed.value === "") {
    customClockSpeed.focus();
    return;
  }
  try {
    await updateClock({ speed: Number(clockSpeed.value) });
  } catch (error) {
    clockDisplay.textContent = error.message;
  }
});

applyCustomSpeedButton.addEventListener("click", async () => {
  const speed = Number(customClockSpeed.value);
  if (!Number.isFinite(speed) || speed < 0) {
    clockDisplay.textContent = "Enter a speed of 0 or higher.";
    customClockSpeed.focus();
    return;
  }
  try {
    await updateClock({ speed });
  } catch (error) {
    clockDisplay.textContent = error.message;
  }
});

customClockSpeed.addEventListener("keydown", (event) => {
  if (event.key === "Enter") {
    event.preventDefault();
    applyCustomSpeedButton.click();
  }
});

resetClockButton.addEventListener("click", async () => {
  try {
    await updateClock({ action: "reset" });
  } catch (error) {
    clockDisplay.textContent = error.message;
  }
});

languageSelect.addEventListener("change", () => {
  selectedLanguage = languageSelect.value || "auto";
  window.localStorage.setItem("auraLanguage", selectedLanguage);
  updateRecognitionLanguage();
});

authRoleInputs.forEach((input) => {
  input.addEventListener("change", () => {
    selectedRole = selectedAuthRole();
  });
});

passwordForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  passwordError.hidden = true;
  passwordError.textContent = "";
  try {
    if (passwordAction === "clearDataset") {
      await clearPatientDataset(passwordInput.value);
      return;
    }
    hidePasswordModal();
  } catch (error) {
    passwordError.textContent = error.message;
    passwordError.hidden = false;
    passwordInput.select();
  }
});

cancelPasswordButton.addEventListener("click", hidePasswordModal);

setupSpeechVoices();
setupSpeechRecognition();
updateVoiceButtons();
setAuthRole(selectedRole);
loadRuntimeConfig();
loadLanguages();
loadAuthState();

function fetchPatientState() {
  fetch("/api/patient-state")
  .then((response) => response.json())
  .then((data) => {
    if (data.error) {
      throw new Error(data.error);
    }
    updateCurrentTask(data.currentTask, data.currentInstruction, data.dueTask);
    notifyDueTask(data.dueTask, data.clock);
    renderClock(data.clock);
  })
  .catch(() => updateCurrentTask(null));
}
