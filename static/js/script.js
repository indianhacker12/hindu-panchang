document.addEventListener('DOMContentLoaded', function() {
    // Initialize variables
    const datePicker = document.getElementById('date-picker');
    const getPanchangBtn = document.getElementById('get-panchang');
    const panchangDetails = document.getElementById('panchang-details');
    const calendarGrid = document.getElementById('calendar-grid');
    const calendarTitle = document.getElementById('calendar-title');
    const prevMonthBtn = document.getElementById('prev-month');
    const nextMonthBtn = document.getElementById('next-month');
    const upcomingFestivals = document.getElementById('upcoming-festivals');
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabPanes = document.querySelectorAll('.tab-pane');
    const tabLinks = document.querySelectorAll('.tab-link');
    const todayLink = document.getElementById('today-link');
    
    // Set default date to today
    const today = new Date();
    const todayFormatted = formatDate(today);
    datePicker.value = todayFormatted;
    
    // Current calendar view
    let currentYear = today.getFullYear();
    let currentMonth = today.getMonth();
    
    // Initialize
    getPanchang(todayFormatted);
    renderCalendar(currentYear, currentMonth);
    loadUpcomingFestivals();
    
    // Event listeners
    getPanchangBtn.addEventListener('click', function() {
        const selectedDate = datePicker.value;
        getPanchang(selectedDate);
    });
    
    prevMonthBtn.addEventListener('click', function() {
        currentMonth--;
        if (currentMonth < 0) {
            currentMonth = 11;
            currentYear--;
        }
        renderCalendar(currentYear, currentMonth);
    });
    
    nextMonthBtn.addEventListener('click', function() {
        currentMonth++;
        if (currentMonth > 11) {
            currentMonth = 0;
            currentYear++;
        }
        renderCalendar(currentYear, currentMonth);
    });
    
    // Tab functionality
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            const tabId = this.getAttribute('data-tab');
            
            // Remove active class from all buttons and panes
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabPanes.forEach(pane => pane.classList.remove('active'));
            
            // Add active class to current button and pane
            this.classList.add('active');
            document.getElementById(tabId).classList.add('active');
        });
    });
    
    // Tab links in footer
    tabLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const tabId = this.getAttribute('data-tab');
            
            // Activate the tab
            tabButtons.forEach(btn => {
                if (btn.getAttribute('data-tab') === tabId) {
                    btn.click();
                }
            });
            
            // Scroll to tabs
            document.querySelector('.tabs').scrollIntoView({ behavior: 'smooth' });
        });
    });
    
    // Today link
    todayLink.addEventListener('click', function(e) {
        e.preventDefault();
        datePicker.value = todayFormatted;
        getPanchang(todayFormatted);
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
    
    // Function to get panchang for a specific date
    function getPanchang(dateStr) {
        fetch('/api/panchang', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ date: dateStr })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                displayPanchang(data);
            } else {
                panchangDetails.innerHTML = `<p class="error">Error: ${data.error}</p>`;
            }
        })
        .catch(error => {
            panchangDetails.innerHTML = `<p class="error">Error fetching panchang: ${error.message}</p>`;
        });
    }
    
    // Function to display panchang data
    function displayPanchang(data) {
        const date = new Date(data.date);
        const formattedDate = date.toLocaleDateString('en-US', { 
            weekday: 'long', 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric' 
        });
        
        let html = `
            <div>
                <h3><i class="fas fa-calendar-day"></i> Date</h3>
                <p>${formattedDate}</p>
                <p><strong>Hindu Month:</strong> ${data.hindu_month}</p>
            </div>
            <div>
                <h3><i class="fas fa-moon"></i> Tithi</h3>
                <p>${data.tithi} (${data.paksha})</p>
                <p><small>Tithi #${data.tithi_number}</small></p>
                <div class="progress-bar">
                    <div class="progress" style="width: ${data.tithi_completion}%"></div>
                </div>
                <p><small>${Math.round(data.tithi_completion)}% complete</small></p>
            </div>
            <div>
                <h3><i class="fas fa-star"></i> Nakshatra</h3>
                <p>${data.nakshatra}</p>
                <p><small>Nakshatra #${data.nakshatra_number}</small></p>
                <div class="progress-bar">
                    <div class="progress" style="width: ${data.nakshatra_completion}%"></div>
                </div>
                <p><small>${Math.round(data.nakshatra_completion)}% complete</small></p>
            </div>
            <div>
                <h3><i class="fas fa-dharmachakra"></i> Yoga</h3>
                <p>${data.yoga}</p>
                <p><small>Yoga #${data.yoga_number}</small></p>
            </div>
            <div>
                <h3><i class="fas fa-divide"></i> Karana</h3>
                <p>${data.karana}</p>
                <p><small>Karana #${data.karana_number}</small></p>
            </div>
        `;
        
        if (data.festivals && data.festivals.length > 0) {
            html += `
                <div>
                    <h3><i class="fas fa-gifts"></i> Festivals</h3>
                    <ul>
                        ${data.festivals.map(festival => `<li>${festival}</li>`).join('')}
                    </ul>
                </div>
            `;
        }
        
        panchangDetails.innerHTML = html;
        
        // Animate the progress bars
        setTimeout(() => {
            const progressBars = document.querySelectorAll('.progress');
            progressBars.forEach(bar => {
                bar.style.transition = 'width 1s ease-in-out';
            });
        }, 100);
    }
    
    // Function to render calendar
    function renderCalendar(year, month) {
        // Update calendar title
        const monthName = new Date(year, month, 1).toLocaleDateString('en-US', { month: 'long' });
        calendarTitle.textContent = `${monthName} ${year}`;
        
        // Get calendar data from API
        fetch('/api/calendar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ year, month: month + 1 }) // API expects 1-12 for months
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                displayCalendar(data, year, month);
            } else {
                calendarGrid.innerHTML = `<p class="error">Error loading calendar</p>`;
            }
        })
        .catch(error => {
            calendarGrid.innerHTML = `<p class="error">Error: ${error.message}</p>`;
        });
    }
    
    // Function to display calendar
    function displayCalendar(data, year, month) {
        calendarGrid.innerHTML = '';
        
        // Get first day of month
        const firstDay = new Date(year, month, 1);
        const startingDay = firstDay.getDay(); // 0 = Sunday, 1 = Monday, etc.
        
        // Add empty cells for days before the first day of the month
        for (let i = 0; i < startingDay; i++) {
            const emptyCell = document.createElement('div');
            emptyCell.className = 'calendar-day empty';
            calendarGrid.appendChild(emptyCell);
        }
        
        // Add days of the month
        data.days.forEach(day => {
            const dayCell = document.createElement('div');
            dayCell.className = 'calendar-day';
            
            // Check if this is today
            const isToday = (
                year === today.getFullYear() && 
                month === today.getMonth() && 
                day.date === today.getDate()
            );
            
            if (isToday) {
                dayCell.classList.add('today');
            }
            
            // Add date
            const dateDiv = document.createElement('div');
            dateDiv.className = 'date';
            dateDiv.textContent = day.date;
            dayCell.appendChild(dateDiv);
            
            // Add tithi
            const tithiDiv = document.createElement('div');
            tithiDiv.className = 'tithi';
            tithiDiv.textContent = `${day.tithi} (${day.paksha.split(' ')[0]})`;
            dayCell.appendChild(tithiDiv);
            
            // Add nakshatra
            const nakshatraDiv = document.createElement('div');
            nakshatraDiv.className = 'nakshatra';
            nakshatraDiv.textContent = `${day.nakshatra}`;
            dayCell.appendChild(nakshatraDiv);
            
            // Add festivals if any
            if (day.festivals && day.festivals.length > 0) {
                const festivalDiv = document.createElement('div');
                festivalDiv.className = 'festival';
                festivalDiv.innerHTML = `<i class="fas fa-gifts"></i> ${day.festivals.join(', ')}`;
                dayCell.appendChild(festivalDiv);
            }
            
            // Add click event to show panchang for this day
            dayCell.addEventListener('click', function() {
                const clickedDate = formatDate(new Date(year, month, day.date));
                datePicker.value = clickedDate;
                getPanchang(clickedDate);
                
                // Scroll to panchang details
                document.querySelector('.panchang-result').scrollIntoView({ behavior: 'smooth' });
            });
            
            calendarGrid.appendChild(dayCell);
        });
    }
    
    // Function to load upcoming festivals
    function loadUpcomingFestivals() {
        fetch('/api/upcoming-festivals')
            .then(response => response.json())
            .then(data => {
                if (data.success && data.festivals.length > 0) {
                    let html = '<ul>';
                    
                    data.festivals.forEach(festival => {
                        html += `
                            <li>
                                <span class="festival-date">${festival.formatted_date}</span>
                                ${festival.festivals.map(f => `<div>${f}</div>`).join('')}
                            </li>
                        `;
                    });
                    
                    html += '</ul>';
                    upcomingFestivals.innerHTML = html;
                } else {
                    upcomingFestivals.innerHTML = '<p>No upcoming festivals in the next 60 days.</p>';
                }
            })
            .catch(error => {
                upcomingFestivals.innerHTML = `<p class="error">Error loading festivals: ${error.message}</p>`;
            });
    }
    
    // Helper function to format date as YYYY-MM-DD
    function formatDate(date) {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
    }
}); 