// Enhanced Cancer Treatment Assistant - Professional Chatbot Interface

class CancerChatbot {
    constructor() {
        this.chatMessages = document.getElementById('chatMessages');
        this.initializeEventListeners();
        this.treatmentChart = null;
        this.sideEffectsChart = null;
        this.messageCounter = 0;
        this.isTyping = false;
        this.messageQueue = [];
    }

    initializeEventListeners() {
        // Query form submission
        const queryForm = document.getElementById('queryForm');
        if (queryForm) {
            queryForm.addEventListener('submit', (e) => this.handleQuerySubmit(e));
        }

        // Example query buttons
        const exampleItems = document.querySelectorAll('.example-item');
        exampleItems.forEach(item => {
            item.addEventListener('click', (e) => this.handleExampleClick(e));
        });

        // Quick action buttons
        const quickActions = document.querySelectorAll('.btn-quick-action');
        quickActions.forEach(button => {
            button.addEventListener('click', (e) => this.handleQuickAction(e));
        });

        // Input field enhancements
        const queryInput = document.getElementById('queryInput');
        if (queryInput) {
            queryInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    this.handleQuerySubmit(e);
                }
            });

            // Add typing indicator
            queryInput.addEventListener('input', () => this.handleInputChange());
        }

        // Auto-scroll chat messages
        if (this.chatMessages) {
            this.scrollToBottom();
        }

        // Initialize modern interactions
        this.initializeModernFeatures();
    }

    initializeModernFeatures() {
        // Add intersection observer for animations
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.animationPlayState = 'running';
                }
            });
        }, observerOptions);

        // Observe all messages for animations
        document.querySelectorAll('.message').forEach(message => {
            observer.observe(message);
        });
    }

    handleInputChange() {
        const queryInput = document.getElementById('queryInput');
        const submitBtn = document.getElementById('submitBtn');
        
        if (queryInput.value.trim()) {
            submitBtn.classList.add('btn-send-active');
        } else {
            submitBtn.classList.remove('btn-send-active');
        }
    }

    async handleQuerySubmit(event) {
        event.preventDefault();
        
        const queryInput = document.getElementById('queryInput');
        const query = queryInput.value.trim();
        
        if (!query) {
            this.showAlert('Please enter a question.', 'warning');
            return;
        }

        // Add user message to chat
        this.addUserMessage(query);
        
        // Clear input
        queryInput.value = '';
        
        // Show typing indicator
        this.showTypingIndicator();

        try {
            const response = await this.sendQuery(query);
            this.hideTypingIndicator();
            this.addBotMessage(response);
        } catch (error) {
            this.hideTypingIndicator();
            this.addBotMessage({
                response: `I apologize, but I encountered an error: ${error.message}. Please try again.`,
                entities: {},
                related_data: {}
            });
        }
    }

    handleExampleClick(event) {
        const query = event.currentTarget.getAttribute('data-query');
        const queryInput = document.getElementById('queryInput');
        queryInput.value = query;
        
        // Add a small delay for better UX
        setTimeout(() => {
            document.getElementById('queryForm').dispatchEvent(new Event('submit'));
        }, 100);
    }

    handleQuickAction(event) {
        const query = event.currentTarget.getAttribute('data-query');
        const queryInput = document.getElementById('queryInput');
        queryInput.value = query;
        queryInput.focus();
    }

    async sendQuery(query) {
        const response = await fetch('/api/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: query })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to process query');
        }

        return await response.json();
    }

    addUserMessage(message) {
        this.messageCounter++;
        const messageElement = document.createElement('div');
        messageElement.className = 'message user-message fade-in-up';
        messageElement.innerHTML = `
            <div class="message-avatar">
                <i class="fas fa-user"></i>
            </div>
            <div class="message-content">
                <div class="message-bubble">
                    ${this.formatMessage(message)}
                </div>
                <div class="message-time">${this.getCurrentTime()}</div>
            </div>
        `;
        
        this.chatMessages.appendChild(messageElement);
        this.scrollToBottom();
        this.addMessageAnimation(messageElement);
    }

    addBotMessage(response) {
        this.messageCounter++;
        const messageElement = document.createElement('div');
        messageElement.className = 'message bot-message fade-in-up';
        
        let entityTagsHtml = '';
        if (response.entities && response.entities.length > 0) {
            entityTagsHtml = this.generateEntityTags(response.entities);
        }
        
        let relatedDataHtml = '';
        if (response.related_data && response.related_data.length > 0) {
            relatedDataHtml = this.generateRelatedDataTable(response.related_data);
        }
        
        messageElement.innerHTML = `
            <div class="message-avatar">
                <i class="fas fa-user-md"></i>
            </div>
            <div class="message-content">
                <div class="message-bubble">
                    ${this.formatMessage(response.response)}
                    ${entityTagsHtml}
                    ${relatedDataHtml}
                </div>
                <div class="message-time">${this.getCurrentTime()}</div>
            </div>
        `;
        
        this.chatMessages.appendChild(messageElement);
        this.scrollToBottom();
        this.addMessageAnimation(messageElement);
        
        // Handle charts if data is available
        if (response.chart_data) {
            this.handleChartData(response.chart_data);
        }
    }

    addMessageAnimation(element) {
        element.style.opacity = '0';
        element.style.transform = 'translateY(30px) scale(0.95)';
        
        requestAnimationFrame(() => {
            element.style.transition = 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)';
            element.style.opacity = '1';
            element.style.transform = 'translateY(0) scale(1)';
        });
    }

    formatMessage(message) {
        // Enhanced message formatting with better typography
        return message
            .replace(/\n/g, '<br>')
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/`(.*?)`/g, '<code class="text-primary">$1</code>');
    }

    formatResponseText(text) {
        return text
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/\n\n/g, '</p><p>')
            .replace(/\n/g, '<br>')
            .replace(/^/, '<p>')
            .replace(/$/, '</p>');
    }

    formatEntityTags(entities) {
        let html = '<div class="entity-tags">';
        for (const [type, values] of Object.entries(entities)) {
            if (values && values.length > 0) {
                values.forEach(value => {
                    html += `<span class="entity-tag entity-${type}">
                        <i class="fas fa-tag"></i> ${value}
                    </span>`;
                });
            }
        }
        html += '</div>';
        return html;
    }

    formatRelatedDataInMessage(relatedData) {
        let html = '';

        // Format treatments table
        if (relatedData.treatments && relatedData.treatments.length > 0) {
            html += '<div class="related-data">';
            html += '<h6><i class="fas fa-pills"></i> Treatment Options</h6>';
            html += this.createTreatmentsTable(relatedData.treatments);
            html += '</div>';
        }

        // Format side effects
        if (relatedData.side_effects) {
            html += '<div class="related-data">';
            html += '<h6><i class="fas fa-exclamation-triangle"></i> Side Effects</h6>';
            html += `<button class="btn btn-quick-action" data-bs-toggle="modal" data-bs-target="#sideEffectsModal">
                <i class="fas fa-chart-bar"></i> View Frequency Chart
            </button>`;
            html += '</div>';
        }

        return html;
    }

    createTreatmentsTable(treatments) {
        let html = `
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Treatment</th>
                        <th>Category</th>
                        <th>Effectiveness</th>
                    </tr>
                </thead>
                <tbody>`;

        treatments.slice(0, 5).forEach(treatment => { // Limit to 5 for chat display
            html += `
                <tr>
                    <td><strong>${treatment.treatment_name || treatment.name || 'N/A'}</strong></td>
                    <td>${treatment.category || 'N/A'}</td>
                    <td>${treatment.effectiveness || 'N/A'}</td>
                </tr>`;
        });

        html += `</tbody></table>`;
        
        if (treatments.length > 5) {
            html += `<small class="text-muted"><em>Showing top 5 results. ${treatments.length - 5} more available.</em></small>`;
        }
        
        return html;
    }

    showTypingIndicator() {
        const typingIndicator = document.getElementById('typingIndicator');
        if (typingIndicator) {
            typingIndicator.style.display = 'block';
            this.scrollToBottom();
        }
    }

    hideTypingIndicator() {
        const typingIndicator = document.getElementById('typingIndicator');
        if (typingIndicator) {
            typingIndicator.style.display = 'none';
        }
    }

    scrollToBottom() {
        if (this.chatMessages) {
            setTimeout(() => {
                this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
            }, 100);
        }
    }

    getCurrentTime() {
        const now = new Date();
        return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    createSideEffectsChart(sideEffectsData) {
        const ctx = document.getElementById('sideEffectsChart');
        if (!ctx) return;

        // Destroy existing chart
        if (this.sideEffectsChart) {
            this.sideEffectsChart.destroy();
        }

        const labels = Object.keys(sideEffectsData);
        const data = Object.values(sideEffectsData);
        const colors = [
            '#4a90e2', '#7b68ee', '#ff6b6b', '#4ecdc4', '#ffa726',
            '#9c27b0', '#2e7d32', '#d32f2f', '#f57c00', '#1976d2'
        ];

        this.sideEffectsChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    backgroundColor: colors.slice(0, labels.length),
                    borderWidth: 2,
                    borderColor: '#fff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 20,
                            font: { size: 12 }
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `${context.label}: ${context.parsed}%`;
                            }
                        }
                    }
                }
            }
        });
    }

    showAlert(message, type = 'info') {
        // Create and show Bootstrap alert
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        const container = document.querySelector('.container-fluid');
        container.insertBefore(alertDiv, container.firstChild);

        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }
}

// Treatment Chart Functionality
async function loadTreatmentChart() {
    try {
        const response = await fetch('/api/stats');
        const data = await response.json();

        if (data.treatment_categories) {
            createTreatmentPieChart(data.treatment_categories);
        }
    } catch (error) {
        console.error('Error loading treatment chart:', error);
    }
}

function createTreatmentPieChart(treatmentData) {
    const ctx = document.getElementById('treatmentChart');
    if (!ctx) return;

    const labels = Object.keys(treatmentData);
    const data = Object.values(treatmentData);
    const colors = [
        '#2c5aa0', '#28a745', '#dc3545', '#fd7e14', 
        '#6610f2', '#e83e8c', '#20c997', '#6c757d'
    ];

    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: colors.slice(0, labels.length),
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 15,
                        font: {
                            size: 12
                        }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = ((context.parsed / total) * 100).toFixed(1);
                            return `${context.label}: ${context.parsed} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

// Global function for quick messages
function sendQuickMessage(message) {
    const chatbot = window.cancerChatbot || new CancerChatbot();
    const queryInput = document.getElementById('queryInput');
    if (queryInput) {
        queryInput.value = message;
        chatbot.handleQuerySubmit(new Event('submit'));
    }
}

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    new CancerAssistant();
});
