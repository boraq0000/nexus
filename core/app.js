/* ── PAGE ROUTING ── */
let currentUser = JSON.parse(localStorage.getItem('currentUser') || 'null');

function getCurrentUser() {
  if (currentUser) return currentUser;
  const stored = localStorage.getItem('currentUser');
  if (!stored) return null;
  try {
    currentUser = JSON.parse(stored);
  } catch (err) {
    currentUser = null;
  }
  return currentUser;
}

function normalizeRole(role) {
  if (!role) return 'Student';
  const value = String(role).trim().toLowerCase();
  if (value.includes('student')) return 'Student';
  if (value.includes('professor')) return 'Professor';
  if (value.includes('investor')) return 'Investor';
  return 'Student';
}

function escapeHTML(value) {
  if (value === undefined || value === null) return '';
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

function escapeAttribute(value) {
  if (value === undefined || value === null) return '';
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
}

function showPage(name) {
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  const page = document.getElementById('page-' + name);
  if (!page) return;
  page.classList.add('active');

  document.querySelectorAll('.nav-link').forEach(a => {
    a.classList.toggle('active', a.dataset.page === name);
  });

  updateAuthState();
  window.scrollTo({ top: 0, behavior: 'smooth' });

  if (name === 'gallery') renderGallery();
  if (name === 'dashboard') renderDashboard();
}

function toggleMenu() {
  document.getElementById('mobileMenu').classList.toggle('open');
}
function closeMobileMenu() {
  document.getElementById('mobileMenu').classList.remove('open');
}

/* ── MODAL ── */
function openModal(type = 'signin') {
  document.getElementById('loginModal').classList.add('open');
  document.body.style.overflow = 'hidden';

  const title = document.getElementById('modalTitle');
  const signinform = document.getElementById('signinform');
  const signupForm = document.getElementById('signupForm');
  const messageEl = document.getElementById('loginMessage');

  if (messageEl) {
    messageEl.textContent = '';
    messageEl.className = 'modal-message';
  }

  if (type === 'signup') {
    title.innerText = 'Create Account';
    signinform.style.display = 'none';
    signupForm.style.display = 'block';
  } else {
    title.innerText = 'Sign In';
    signinform.style.display = 'block';
    signupForm.style.display = 'none';
  }
}

function closeModal() {
  document.getElementById('loginModal').classList.remove('open');
  document.body.style.overflow = '';
}

function closeModalOutside(e) {
  if (e.target === document.getElementById('loginModal')) {
    closeModal();
  }
}

function selectRole(role, el) {
  document.querySelectorAll('.role-btn').forEach(b => {
    b.classList.remove('active');
  });
  el.classList.add('active');
}

/* ── DATA HELPERS ── */
let GALLERY_PROJECTS = [];
const FALLBACK_PROJECTS = [
  {
    id: 1, name: 'Smart Library Management System',
    category: 'Information Technology', status: 'For Sale',
    desc: 'Comprehensive library management system with AI-powered book recommendations',
    tags: ['React', 'Node.js', 'MongoDB'], rating: 4.8, views: 1240, price: '$5,000',
    icon: 'database'
  },
  {
    id: 2, name: 'Interactive Learning Platform',
    category: 'Computer Science', status: 'For Investment',
    desc: 'Gamified learning platform with real-time progress tracking',
    tags: ['Python', 'Django', 'Vue.js'], rating: 4.9, views: 2100, price: 'Funding Needed',
    icon: 'book'
  },
  {
    id: 3, name: 'Health App for Athletes',
    category: 'Mobile Applications', status: 'For Display',
    desc: 'Track fitness metrics, nutrition, and training schedules',
    tags: ['React Native', 'Firebase'], rating: 4.7, views: 850, price: 'Display Only',
    icon: 'heart'
  }
];

const ICONS = {
  database: `<svg viewBox="0 0 60 60" fill="none"><ellipse cx="30" cy="18" rx="16" ry="7" stroke="#b8922f" stroke-width="2"/><path d="M14 18v12c0 3.87 7.16 7 16 7s16-3.13 16-7V18" stroke="#b8922f" stroke-width="2"/><path d="M14 30v12c0 3.87 7.16 7 16 7s16-3.13 16-7V30" stroke="#b8922f" stroke-width="2"/></svg>`,
  book: `<svg viewBox="0 0 60 60" fill="none"><rect x="12" y="10" width="28" height="38" rx="3" stroke="#b8922f" stroke-width="2"/><path d="M20 10 v38" stroke="#b8922f" stroke-width="1.5"/><line x1="24" y1="20" x2="36" y2="20" stroke="#b8922f" stroke-width="1.5" stroke-linecap="round"/><line x1="24" y1="27" x2="36" y2="27" stroke="#b8922f" stroke-width="1.5" stroke-linecap="round"/></svg>`,
  heart: `<svg viewBox="0 0 60 60" fill="none"><path d="M30 46 C30 46 10 34 10 22a10 10 0 0120 0 10 10 0 0120 0C50 34 30 46 30 46z" stroke="#b8922f" stroke-width="2" stroke-linejoin="round"/></svg>`,
  chart: `<svg viewBox="0 0 60 60" fill="none"><path d="M10 50 L20 35 L30 40 L50 18" stroke="#b8922f" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/><polyline points="40,18 50,18 50,28" stroke="#b8922f" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>`,
  map: `<svg viewBox="0 0 60 60" fill="none"><path d="M30 10 C22 10 16 16.27 16 24c0 10.5 14 28 14 28s14-17.5 14-28C44 16.27 38 10 30 10z" stroke="#b8922f" stroke-width="2"/><circle cx="30" cy="24" r="4" stroke="#b8922f" stroke-width="1.5"/></svg>`,
  lock: `<svg viewBox="0 0 60 60" fill="none"><rect x="16" y="28" width="28" height="22" rx="4" stroke="#b8922f" stroke-width="2"/><path d="M22 28v-8a8 8 0 0116 0v8" stroke="#b8922f" stroke-width="2" stroke-linecap="round"/><circle cx="30" cy="39" r="3" fill="#b8922f"/><line x1="30" y1="42" x2="30" y2="46" stroke="#b8922f" stroke-width="2" stroke-linecap="round"/></svg>`,
};

function badgeClass(status) {
  if (status === 'For Sale' || status === 'Sale') return 'green';
  if (status === 'For Investment' || status === 'Investment') return 'blue';
  return 'gray';
}

function priceClass(status) {
  if (status === 'For Sale' || status === 'Sale') return '';
  if (status === 'For Investment' || status === 'Investment') return 'funding';
  return 'display';
}

function projectCardHTML(p) {
  const title = escapeHTML(p.title || p.name || 'Untitled Project');
  const description = escapeHTML(p.description || p.desc || 'No description available.');
  const category = escapeHTML(p.rank_badge || p.category || 'General');
  const status = escapeHTML(p.status || 'Display');
  const projectId = Number(p.id ?? p.project_id) || 0;
  const priceLabel = escapeHTML(p.price || (status === 'For Investment' ? 'Funding Needed' : '$0'));
  const tagsHTML = (p.tags || []).map(t => `<span>${escapeHTML(t)}</span>`).join('');

  return `
    <div class="project-card" data-name="${escapeAttribute((p.title || p.name || '').toLowerCase())}" data-category="${escapeAttribute(category)}" data-status="${escapeAttribute(status)}">
      <div class="project-thumb">${ICONS[p.icon] || ICONS.chart}</div>
      <div class="project-meta">
        <span class="project-category">${category}</span>
        <span class="badge ${badgeClass(status)}">${status}</span>
      </div>
      <h4 class="project-name">${title}</h4>
      <p class="project-desc">${description}</p>
      <div class="project-tags">${tagsHTML}</div>
      <div class="project-stats"><span>⭐ ${escapeHTML(p.professor_score ?? p.rating ?? 'N/A')}</span><span>👁 ${escapeHTML(Number(p.views || 0).toLocaleString())}</span></div>
      <div class="project-footer">
        <span class="project-price ${priceClass(status)}">${priceLabel}</span>
        <button class="btn-dark-sm" onclick="viewDetails(${projectId})">View Details</button>
      </div>
    </div>
  `;
}

async function fetchJSON(url, options = {}) {
  const res = await fetch(url, options);
  const text = await res.text();
  let data;
  try {
    data = JSON.parse(text);
  } catch (err) {
    throw new Error(`Invalid JSON response from ${url}: ${text.trim().slice(0, 250)}`);
  }

  if (!res.ok || !data.success) {
    throw new Error(data.error || `Request failed with status ${res.status}`);
  }
  return data;
}

async function renderGallery() {
  try {
    const data = await fetchJSON('/api/projects/');
    const list = data.projects.map(project => {
      const statusValue = project.status || 'Investment';
      const displayStatus = statusValue === 'Investment' ? 'For Investment' : statusValue === 'Sale' ? 'For Sale' : statusValue === 'Display' ? 'For Display' : statusValue;
      return {
        ...project,
        title: project.title,
        description: project.description,
        status: displayStatus,
        rank_badge: project.rank_badge || 'General',
        views: project.views || 0,
        professor_score: project.professor_score,
        id: project.id,
        price: statusValue === 'Sale' ? '$5,000' : statusValue === 'Investment' ? 'Funding Needed' : 'Display Only',
        tags: ['Academic', 'University'],
        icon: 'book',
      };
    });
    GALLERY_PROJECTS = list;
    document.getElementById('galleryGrid').innerHTML = list.length ? list.map(projectCardHTML).join('') : '<div style="grid-column:1/-1;text-align:center;padding:60px 0;color:var(--muted);font-size:15px;">No projects available.</div>';
    updateCount(list.length);
  } catch (error) {
    console.warn('Gallery fetch failed:', error);
    GALLERY_PROJECTS = FALLBACK_PROJECTS;
    document.getElementById('galleryGrid').innerHTML = FALLBACK_PROJECTS.map(projectCardHTML).join('');
    updateCount(FALLBACK_PROJECTS.length);
  }
}

function filterProjects() {
  const q = document.getElementById('gallerySearch').value.toLowerCase();
  const cat = document.getElementById('filterCategory').value;
  const status = document.getElementById('filterStatus').value;

  const filtered = GALLERY_PROJECTS.filter(p => {
    const title = (p.title || p.name || '').toLowerCase();
    const desc = (p.description || p.desc || '').toLowerCase();
    const tags = (p.tags || []).map(t => String(t).toLowerCase());
    const matchQ = !q || title.includes(q) || desc.includes(q) || tags.some(t => t.includes(q));
    const matchCat = !cat || (p.rank_badge || p.category || '').toLowerCase() === cat.toLowerCase();
    const matchStatus = !status || p.status === status;
    return matchQ && matchCat && matchStatus;
  });

  document.getElementById('galleryGrid').innerHTML = filtered.length
    ? filtered.map(projectCardHTML).join('')
    : '<div style="grid-column:1/-1;text-align:center;padding:60px 0;color:var(--muted);font-size:15px;">No projects found. Try a different search.</div>';

  updateCount(filtered.length);
}

function updateCount(n) {
  document.getElementById('projectCount').textContent = `${n} Project${n !== 1 ? 's' : ''} Found`;
}

function viewDetails(id) {
  alert('Project details are available in the dashboard for your role.');
}

function setLoginMessage(message, isError = true) {
  const messageEl = document.getElementById('loginMessage');
  if (!messageEl) return;
  messageEl.textContent = message;
  messageEl.classList.toggle('error', isError);
  messageEl.classList.toggle('success', !isError);
}

async function handleLogin(event) {
  event.preventDefault();

  const email = document.getElementById('loginEmail')?.value.trim();
  const password = document.getElementById('loginPassword')?.value;

  if (!email || !password) {
    setLoginMessage('Please enter both email and password.', true);
    return;
  }

  setLoginMessage('Checking credentials...', false);

  try {
    const data = await fetchJSON('/api/login/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });

    console.log('Login response:', data);
    data.user.role = normalizeRole(data.user.role);
    currentUser = data.user;
    console.log('User stored in currentUser:', currentUser);
    localStorage.setItem('currentUser', JSON.stringify(currentUser));
    updateAuthState();
    setLoginMessage('Login successful. Redirecting to dashboard...', false);
    closeModal();
    setTimeout(() => {
      console.log('About to show dashboard, currentUser is:', currentUser);
      showPage('dashboard');
      setLoginMessage('');
    }, 100);
  } catch (error) {
    setLoginMessage(error.message || 'Login failed. Please check your credentials.', true);
    console.error('Login error:', error);
  }
}

async function handleSignup(event) {
  event.preventDefault();

  const name = document.getElementById('signupName')?.value.trim();
  const email = document.getElementById('signupEmail')?.value.trim();
  const password = document.getElementById('signupPassword')?.value;
  const selectedRole = document.querySelector('.role-btn.active')?.getAttribute('data-role') || 'student';
  const roleMap = { student: 'Student', professor: 'Professor', investor: 'Investor' };
  const role = roleMap[selectedRole] || 'Student';

  if (!name || !email || !password) {
    setLoginMessage('Please fill in all fields.', true);
    return;
  }

  setLoginMessage('Creating account...', false);

  try {
    const data = await fetchJSON('/api/signup/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, email, password, role })
    });

    setLoginMessage('Account created successfully! You can now sign in.', false);
    setTimeout(() => {
      openModal('signin');
      setLoginMessage('');
    }, 1500);
  } catch (error) {
    setLoginMessage(error.message || 'Signup failed. Please try again.', true);
    console.error('Signup error:', error);
  }
}

function handleLogout() {
  currentUser = null;
  localStorage.removeItem('currentUser');
  updateAuthState();
  showPage('home');
}

function updateAuthState() {
  const loginBtn = document.getElementById('navLoginBtn');
  const signupBtn = document.getElementById('navSignupBtn');
  const logoutBtn = document.getElementById('navLogoutBtn');
  const dashboardLink = document.querySelector('.nav-link[data-page="dashboard"]');

  if (currentUser) {
    loginBtn.style.display = 'none';
    signupBtn.style.display = 'none';
    logoutBtn.style.display = 'inline-block';
    dashboardLink.style.display = 'inline-block';
  } else {
    loginBtn.style.display = 'inline-block';
    signupBtn.style.display = 'inline-block';
    logoutBtn.style.display = 'none';
    dashboardLink.style.display = 'none';
  }
}

function renderDashboard() {
  const welcome = document.getElementById('dashboardSub');
  const studentPanel = document.getElementById('studentPanel');
  const professorPanel = document.getElementById('professorPanel');
  const investorPanel = document.getElementById('investorPanel');

  if (!welcome || !studentPanel || !professorPanel || !investorPanel) {
    console.error('Dashboard elements not found in DOM');
    return;
  }

  studentPanel.style.display = 'none';
  professorPanel.style.display = 'none';
  investorPanel.style.display = 'none';

  console.log('Current user:', currentUser);

  if (!currentUser) {
    welcome.textContent = 'Please log in to access your dashboard and project workflows.';
    console.log('No user logged in');
    return;
  }

  const role = normalizeRole(currentUser.role);
  currentUser.role = role;
  console.log('Normalized role:', role);
  welcome.textContent = `Welcome back, ${currentUser.name}! You are logged in as ${role}.`;

  if (role === 'Student') {
    console.log('Showing student panel');
    studentPanel.style.display = 'block';
    loadStudentDashboard();
  } else if (role === 'Professor') {
    console.log('Showing professor panel');
    professorPanel.style.display = 'block';
    loadProfessorDashboard();
  } else if (role === 'Investor') {
    console.log('Showing investor panel');
    investorPanel.style.display = 'block';
    loadInvestorProjects();
  } else {
    console.log('Unknown role:', role);
  }
}

async function loadStudentDashboard() {
  await loadProfessorsDropdown();
  await loadStudentsDropdown();
  loadStudentProjects();
}

async function loadProfessorDashboard() {
  await loadStudentsDropdown();
  loadProfessorProjects();
}

async function loadProfessorsDropdown() {
  const select = document.getElementById('projectProfessorId');
  if (!select) return;

  try {
    const data = await fetchJSON('/api/users/?role=professor');
    select.innerHTML = '<option value="">-- Select a Professor --</option>';
    if (data.users && data.users.length > 0) {
      data.users.forEach(user => {
        const option = document.createElement('option');
        option.value = user.user_id;
        option.textContent = user.name;
        select.appendChild(option);
      });
    }
  } catch (error) {
    console.warn('Unable to load professors:', error);
  }
}

async function loadStudentsDropdown() {
  const select = document.getElementById('inviteUserId');
  if (!select) return;

  try {
    const data = await fetchJSON('/api/users/?role=student');
    select.innerHTML = '<option value="">-- Select a Student --</option>';
    if (data.users && data.users.length > 0) {
      data.users.forEach(user => {
        const option = document.createElement('option');
        option.value = user.user_id;
        option.textContent = user.name;
        select.appendChild(option);
      });
    }
  } catch (error) {
    console.warn('Unable to load students:', error);
  }
}

async function loadStudentProjects() {
  const list = document.getElementById('studentProjectsList');
  if (!list) return;

  if (!currentUser) {
    list.innerHTML = '<p>Please sign in to see your student projects.</p>';
    return;
  }

  list.innerHTML = '<p>Loading your projects...</p>';

  try {
    const data = await fetchJSON(`/api/my-projects/?user_id=${currentUser.id}`);
    if (!data.projects.length) {
      list.innerHTML = '<p>No projects yet. Create a new one to get started.</p>';
      return;
    }

    list.innerHTML = data.projects.map(project => {
      const title = escapeHTML(project.title || 'Untitled Project');
      const description = escapeHTML(project.description || 'No description available.');
      const status = escapeHTML(project.status || 'N/A');
      const approvalStatus = escapeHTML(project.approval_status || 'N/A');
      const detailText = project.owner_id === currentUser.id ? ' and manage members' : '';
      const pendingInvite = project.membership_status === 'pending' && project.membership_role === 'member';

      return `
        <div class="dashboard-item" style="cursor: pointer; transition: all 0.2s;">
          <strong>${title}</strong>
          <p>${description}</p>
          <p style="font-size: 12px; color: #999;">Project ID: ${escapeHTML(project.id)}</p>
          <p>Status: ${status} | Approval: ${approvalStatus}</p>
          ${pendingInvite ? `<p style="font-size: 12px; color: #b87c00;">Invitation pending. Accept to join the team.</p>` : ''}
          <div style="display:flex; gap:10px; flex-wrap:wrap; margin-top:8px;">
            <button class="btn-dark-sm" onclick="openProjectModal(${project.id}, ${project.owner_id === currentUser.id})">View Details</button>
            ${pendingInvite ? `<button class="btn-primary" type="button" onclick="respondToInvite(${project.id}, 'accept')">Accept Invite</button><button class="btn-dark-sm" type="button" onclick="respondToInvite(${project.id}, 'reject')">Decline Invite</button>` : ''}
          </div>
        </div>
      `;
    }).join('');
  } catch (error) {
    list.innerHTML = `<p class="error">Unable to load your projects: ${escapeHTML(error.message)}</p>`;
  }
}

function respondToInvite(projectId, action) {
  const currentUser = getCurrentUser();
  if (!currentUser) {
    alert('You must be logged in to respond to an invitation.');
    return;
  }

  fetch(`/api/projects/${projectId}/respond-invite/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      user_id: currentUser.id,
      action,
    }),
  })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        alert(`Invite ${action === 'accept' ? 'accepted' : 'declined'} successfully.`);
        loadStudentProjects();
      } else {
        alert(data.error || 'Unable to respond to invite.');
      }
    })
    .catch(() => {
      alert('Unable to respond to invite.');
    });
}

function openProjectModal(projectId, isOwner) {
  const modal = document.getElementById('projectModal');
  const ownerSection = document.getElementById('projectOwnerSection');
  
  if (isOwner) {
    ownerSection.style.display = 'block';
    // Store projectId for the invite form
    document.getElementById('projectModalContent').dataset.projectId = projectId;
    loadStudentsDropdownForModal();
  } else {
    ownerSection.style.display = 'none';
  }
  
  modal.style.display = 'flex';
  loadProjectMembers(projectId);
  loadProjectGrades(projectId);
}

function closeProjectModal(e) {
  if (e && e.target.id !== 'projectModal') return;
  document.getElementById('projectModal').style.display = 'none';
}

async function loadStudentsDropdownForModal() {
  await loadStudentsDropdown();
}

async function loadProjectMembers(projectId) {
  const membersList = document.getElementById('projectMembersList');
  if (!membersList) return;

  try {
    const data = await fetchJSON(`/api/projects/${projectId}/members/`);
    if (!data.members || data.members.length === 0) {
      membersList.innerHTML = '<p style="color: #999;">No members yet.</p>';
      return;
    }

    membersList.innerHTML = `
      <ul style="list-style: none; padding: 0; margin: 0;">
        ${data.members.map(member => `
          <li style="padding: 10px; border: 1px solid #eee; border-radius: 4px; margin-bottom: 8px; background: #f9f9f9;">
            <strong style="display: block; margin-bottom: 4px;">${escapeHTML(member.name)}</strong>
            <span style="display: block; color: #999; font-size: 12px; margin-bottom: 2px;">${escapeHTML(member.email)}</span>
            <span style="display: block; color: #666; font-size: 12px; margin-bottom: 2px;">Role: <strong>${escapeHTML(member.role_in_project)}</strong></span>
            <span style="display: block; color: #999; font-size: 11px;">Status: ${escapeHTML(member.status)}</span>
          </li>
        `).join('')}
      </ul>
    `;
  } catch (error) {
    membersList.innerHTML = `<p class="error" style="font-size: 12px;">Unable to load members: ${escapeHTML(error.message)}</p>`;
  }
}

async function loadProjectGrades(projectId) {
  const gradesList = document.getElementById('projectGradesList');
  if (!gradesList) return;

  try {
    const data = await fetchJSON(`/api/projects/${projectId}/grades/`);
    if (!data.grades || data.grades.length === 0) {
      gradesList.innerHTML = '<p style="color: #999;">No grades submitted for this project yet.</p>';
      return;
    }

    gradesList.innerHTML = `
      <ul style="list-style: none; padding: 0; margin: 0;">
        ${data.grades.map(grade => `
          <li style="padding: 10px; border: 1px solid #eee; border-radius: 4px; margin-bottom: 8px; background: #fafafa;">
            <strong>${escapeHTML(grade.student_name)} (${escapeHTML(grade.student_role || 'Member')})</strong>
            <div style="font-size: 13px; color: #555; margin-top: 4px;">Score: <strong>${escapeHTML(grade.score_average)}</strong></div>
            <div style="font-size: 13px; color: #555;">Feedback: ${escapeHTML(grade.feedback || 'None')}</div>
            <div style="font-size: 12px; color: #888; margin-top: 4px;">Graded by ${escapeHTML(grade.professor_name)} on ${escapeHTML(grade.evaluation_date || '')}</div>
          </li>
        `).join('')}
      </ul>
    `;
  } catch (error) {
    gradesList.innerHTML = `<p class="error" style="font-size: 12px;">Unable to load grades: ${escapeHTML(error.message)}</p>`;
  }
}

async function loadProfessorProjects() {
  const list = document.getElementById('professorProjectsList');
  if (!list) return;

  if (!currentUser) {
    list.innerHTML = '<p>Please sign in to see assigned professor projects.</p>';
    return;
  }

  list.innerHTML = '<p>Loading assigned projects...</p>';

  try {
    const data = await fetchJSON(`/api/professor-projects/?user_id=${currentUser.id}`);
    if (!data.projects.length) {
      list.innerHTML = '<p>No assigned projects yet.</p>';
      return;
    }

    list.innerHTML = data.projects.map(project => {
      const projectId = Number(project.id);
      const title = escapeHTML(project.title || 'Untitled Project');
      const description = escapeHTML(project.description || 'No description provided.');
      const approval = escapeHTML(project.approval_status || 'N/A');

      return `
      <div class="dashboard-item">
        <strong>${title}</strong>
        <p>${description}</p>
        <p>Project ID: ${escapeHTML(project.id)}</p>
        <p>Approval: ${approval}</p>
        <button class="btn-dark-sm" onclick="approveProject(${projectId}, 'Approved')">Approve</button>
        <button class="btn-dark-sm" onclick="approveProject(${projectId}, 'Rejected')">Reject</button>
        <button class="btn-dark-sm" onclick="toggleGradeForm(${projectId})">Grade Project</button>
        <div id="grade-form-${projectId}" style="display:none; margin-top: 12px; padding-top: 12px; border-top: 1px solid #ddd;">
          <label style="font-size: 13px; margin-bottom: 8px; display: block;">Student Name</label>
          <select id="grade-student-${project.id}" style="width:100%; padding: 8px; margin-bottom: 10px; border: 1px solid #ccc; border-radius: 4px;">
            <option value="">-- Select Student --</option>
          </select>
          <label style="font-size: 13px; margin-bottom: 8px; display: block;">Score</label>
          <input id="grade-score-${project.id}" type="number" placeholder="e.g. 85 or 4.5" style="width:100%; padding: 8px; margin-bottom: 10px; border: 1px solid #ccc; border-radius: 4px;" />
          <label style="font-size: 13px; margin-bottom: 8px; display: block;">Feedback (optional)</label>
          <textarea id="grade-feedback-${project.id}" placeholder="Optional feedback" style="width:100%; padding: 8px; margin-bottom: 10px; border: 1px solid #ccc; border-radius: 4px; font-size: 12px;" rows="2"></textarea>
          <button class="btn-primary" type="button" onclick="submitGrade(${projectId})">Submit Grade</button>
          <button class="btn-dark-sm" type="button" onclick="toggleGradeForm(${projectId})">Cancel</button>
        </div>
      </div>
    `}).join('');
    
    // Load students into all grade forms
    await populateGradeStudentsForAll(data.projects);
  } catch (error) {
    list.innerHTML = `<p class="error">Unable to load assigned projects: ${escapeHTML(error.message)}</p>`;
  }
}

function toggleGradeForm(projectId) {
  const form = document.getElementById(`grade-form-${projectId}`);
  if (form) {
    form.style.display = form.style.display === 'none' ? 'block' : 'none';
  }
}

async function populateGradeStudentsForAll(projects) {
  await Promise.all(projects.map(async project => {
    const select = document.getElementById(`grade-student-${project.id}`);
    if (!select) return;

    try {
      const data = await fetchJSON(`/api/projects/${project.id}/members/`);
      const members = (data.members || []).filter(member => member.status === 'accepted' && ['owner', 'member'].includes(member.role_in_project));

      select.innerHTML = '<option value="">-- Select Student --</option>';

      if (!members.length) {
        const option = document.createElement('option');
        option.value = '';
        option.textContent = '-- No project students available --';
        select.appendChild(option);
        return;
      }

      members.forEach(member => {
        const option = document.createElement('option');
        option.value = member.user_id;
        option.textContent = member.name;
        select.appendChild(option);
      });
    } catch (error) {
      console.warn(`Unable to load members for project ${project.id}:`, error);
      select.innerHTML = '<option value="">-- Unable to load project students --</option>';
    }
  }));
}

async function submitGrade(projectId) {
  const studentSelect = document.getElementById(`grade-student-${projectId}`);
  const scoreInput = document.getElementById(`grade-score-${projectId}`);
  const feedbackInput = document.getElementById(`grade-feedback-${projectId}`);

  const studentId = Number(studentSelect.value);
  const score = Number(scoreInput.value);
  const feedback = feedbackInput.value.trim();

  if (!studentId || !score) {
    alert('Student and score are required.');
    return;
  }

  try {
    await fetchJSON('/api/projects/grade/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        project_id: projectId,
        student_id: studentId,
        professor_id: currentUser.id,
        score_average: score,
        feedback,
      })
    });
    alert(`Grade submitted for ${studentSelect.options[studentSelect.selectedIndex].text}.`);
    toggleGradeForm(projectId);
    loadProfessorProjects();
  } catch (error) {
    alert(`Grading failed: ${error.message}`);
  }
}

async function loadInvestorProjects() {
  const list = document.getElementById('investorProjectsList');
  if (!list) return;

  if (!currentUser) {
    list.innerHTML = '<p>Please sign in to see investor projects.</p>';
    return;
  }

  list.innerHTML = '<p>Loading approved projects...</p>';

  try {
    const data = await fetchJSON('/api/projects/');
    if (!data.projects.length) {
      list.innerHTML = '<p>No approved projects available yet.</p>';
      return;
    }

    list.innerHTML = data.projects.map(project => {
      const title = escapeHTML(project.title || 'Untitled Project');
      const description = escapeHTML(project.description || 'No description available.');
      const status = escapeHTML(project.status || 'N/A');
      const approval = escapeHTML(project.approval_status || 'N/A');
      const projectId = Number(project.id);

      return `
        <div class="dashboard-item">
          <strong>${title}</strong>
          <p>${description}</p>
          <p>Status: ${status} | Approval: ${approval}</p>
          <button class="btn-dark-sm" onclick="investInProject(${projectId})">Invest</button>
          <button class="btn-dark-sm" onclick="rateProject(${projectId})">Rate</button>
        </div>
      `;
    }).join('');
  } catch (error) {
    list.innerHTML = `<p class="error">Unable to load projects: ${escapeHTML(error.message)}</p>`;
  }
}

async function approveProject(projectId, status) {
  try {
    await fetchJSON(`/api/projects/${projectId}/approve/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ approval_status: status })
    });
    loadProfessorProjects();
  } catch (error) {
    alert(`Approval failed: ${error.message}`);
  }
}

async function investInProject(projectId) {
  const amountValue = prompt('Enter investment amount in USD:');
  if (!amountValue) return;

  const amount = Number(amountValue);
  if (Number.isNaN(amount) || amount <= 0) {
    alert('Please enter a valid investment amount greater than 0.');
    return;
  }

  try {
    await fetchJSON('/api/invest/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ project_id: projectId, investor_id: currentUser.id, amount })
    });
    alert('Investment recorded successfully.');
  } catch (error) {
    alert(`Investment failed: ${escapeHTML(error.message)}`);
  }
}

async function rateProject(projectId) {
  const ratingValue = prompt('Rate this project from 1 to 5:');
  if (ratingValue === null) return;

  const rating = Number(ratingValue);
  if (!Number.isInteger(rating) || rating < 1 || rating > 5) {
    alert('Please provide an integer rating between 1 and 5.');
    return;
  }

  const review = prompt('Optional review:') || '';

  try {
    await fetchJSON('/api/rate/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ project_id: projectId, investor_id: currentUser.id, rating, review })
    });
    alert('Thank you! Your rating was submitted.');
  } catch (error) {
    alert(`Rating failed: ${escapeHTML(error.message)}`);
  }
}

async function prefillInvite(projectId) {
  const projectInput = document.getElementById('inviteProjectId');
  if (projectInput) projectInput.value = projectId;
  const messageEl = document.getElementById('inviteMemberMessage');
  if (messageEl) {
    messageEl.textContent = `Inviting member to project ${projectId}. Enter the student ID and press Send Invite.`;
    messageEl.className = 'dashboard-message';
  }
}

async function inviteMember(event) {
  event.preventDefault();
  const projectId = Number(document.getElementById('projectModalContent').dataset.projectId);
  const userIdSelect = document.getElementById('inviteUserId');
  const userId = Number(userIdSelect.value);
  const messageEl = document.getElementById('inviteMemberMessage');

  if (!projectId || !userId) {
    messageEl.textContent = 'Member name is required.';
    messageEl.className = 'dashboard-message error';
    return;
  }

  try {
    await fetchJSON(`/api/projects/${projectId}/apply/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id: userId, inviter_id: currentUser.id })
    });
    messageEl.textContent = `Invite sent to ${userIdSelect.options[userIdSelect.selectedIndex].text}!`;
    messageEl.className = 'dashboard-message success';
    userIdSelect.value = '';
    setTimeout(() => {
      loadProjectMembers(projectId);
    }, 500);
  } catch (error) {
    messageEl.textContent = `Unable to send invite: ${error.message}`;
    messageEl.className = 'dashboard-message error';
  }
}

async function gradeProject(projectId) {
  const studentId = prompt('Enter the student user ID for this grade:');
  if (!studentId) return;

  const scoreAverage = prompt('Enter the grade score (e.g. 85 or 4.5):');
  if (scoreAverage === null || scoreAverage.trim() === '') return;

  const feedback = prompt('Enter feedback (optional):') || '';

  try {
    await fetchJSON('/api/projects/grade/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        project_id: projectId,
        student_id: Number(studentId),
        professor_id: currentUser.id,
        score_average: Number(scoreAverage),
        feedback,
      })
    });
    alert('Grade submitted successfully.');
    loadProfessorProjects();
  } catch (error) {
    alert(`Grading failed: ${error.message}`);
  }
}

async function createProject(event) {
  event.preventDefault();
  const title = document.getElementById('projectTitle').value.trim();
  const description = document.getElementById('projectDescription').value.trim();
  const status = document.getElementById('projectStatus').value;
  const professorSelect = document.getElementById('projectProfessorId');
  const professorId = Number(professorSelect.value);
  const badge = document.getElementById('projectBadge').value.trim() || 'General';
  const messageEl = document.getElementById('createProjectMessage');

  if (!title || !description || !professorId) {
    messageEl.textContent = 'Title, description, and professor name are required.';
    messageEl.className = 'dashboard-message error';
    return;
  }

  try {
    await fetchJSON('/api/projects/create/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, description, owner_id: currentUser.id, professor_id: professorId, status, rank_badge: badge })
    });
    const profName = professorSelect.options[professorSelect.selectedIndex].text;
    messageEl.textContent = `Project created successfully with professor ${profName} and pending approval.`;
    messageEl.className = 'dashboard-message success';
    document.getElementById('projectTitle').value = '';
    document.getElementById('projectDescription').value = '';
    document.getElementById('projectBadge').value = '';
    professorSelect.value = '';
    loadStudentProjects();
  } catch (error) {
    messageEl.textContent = `Unable to create project: ${error.message}`;
    messageEl.className = 'dashboard-message error';
  }
}

/* ── INIT ── */
document.addEventListener('DOMContentLoaded', () => {
  updateAuthState();
  showPage('home');

  const loginForm = document.getElementById('signinform');
  if (loginForm) loginForm.addEventListener('submit', handleLogin);
  const signupForm = document.getElementById('signupForm');
  if (signupForm) signupForm.addEventListener('submit', handleSignup);

  const createProjectForm = document.getElementById('createProjectForm');
  if (createProjectForm) createProjectForm.addEventListener('submit', createProject);

  const inviteMemberForm = document.getElementById('inviteMemberForm');
  if (inviteMemberForm) inviteMemberForm.addEventListener('submit', inviteMember);
});

// Close mobile menu on outside click
document.addEventListener('click', (e) => {
  const menu = document.getElementById('mobileMenu');
  const hamburger = document.getElementById('hamburger');
  if (menu.classList.contains('open') && !menu.contains(e.target) && e.target !== hamburger) {
    closeMobileMenu();
  }
});

// Navbar scroll shadow
window.addEventListener('scroll', () => {
  const nav = document.getElementById('navbar');
  nav.style.boxShadow = window.scrollY > 10 ? '0 2px 20px rgba(0,0,0,0.1)' : '';
});
