class VideoTextExtractor {
    constructor() {
        this.initializeElements();
        this.bindEvents();
        this.loadStoredTranscriptions();
    }

    initializeElements() {
        this.videoUrlInput = document.getElementById('video-url');
        this.extractBtn = document.getElementById('extract-btn');
        this.loadingSection = document.getElementById('loading-section');
        this.resultSection = document.getElementById('result-section');
        this.textOutput = document.getElementById('text-output');
        this.copyBtn = document.getElementById('copy-btn');
        this.saveBtn = document.getElementById('save-btn');
        this.transcriptionList = document.getElementById('transcription-list');
        this.clearHistoryBtn = document.getElementById('clear-history');
        this.detectedLanguage = document.getElementById('detected-language');
        this.videoTitle = document.getElementById('video-title');
        this.extractionTime = document.getElementById('extraction-time');
        this.loadingStatus = document.getElementById('loading-status');
        this.progressFill = document.getElementById('progress-fill');
    }

    bindEvents() {
        this.extractBtn.addEventListener('click', () => this.extractText());
        this.copyBtn.addEventListener('click', () => this.copyText());
        this.saveBtn.addEventListener('click', () => this.saveTranscription());
        this.clearHistoryBtn.addEventListener('click', () => this.clearHistory());
        
        this.videoUrlInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.extractText();
            }
        });

        this.videoUrlInput.addEventListener('input', () => {
            this.validateUrl();
        });
    }

    validateUrl() {
        const url = this.videoUrlInput.value.trim();
        const isValid = this.isValidVideoUrl(url);
        this.extractBtn.disabled = !isValid || !url;
        
        if (url && !isValid) {
            this.videoUrlInput.style.borderColor = '#e74c3c';
        } else {
            this.videoUrlInput.style.borderColor = '#e0e6ed';
        }
    }

    isValidVideoUrl(url) {
        try {
            const urlObj = new URL(url);
            const validDomains = [
                'youtube.com', 'youtu.be', 'vimeo.com', 'dailymotion.com',
                'twitch.tv', 'facebook.com', 'instagram.com', 'tiktok.com'
            ];
            return validDomains.some(domain => 
                urlObj.hostname.includes(domain) || urlObj.hostname.endsWith(domain)
            );
        } catch {
            return false;
        }
    }

    async extractText() {
        const url = this.videoUrlInput.value.trim();
        if (!url || !this.isValidVideoUrl(url)) {
            alert('Please enter a valid video URL');
            return;
        }

        this.showLoading();
        this.extractBtn.disabled = true;

        try {
            const response = await this.callBackendAPI(url);
            this.displayResult(response);
        } catch (error) {
            this.handleError(error);
        } finally {
            this.hideLoading();
            this.extractBtn.disabled = false;
        }
    }

    async callBackendAPI(url) {
        const response = await fetch('http://localhost:8000/extract-text', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ video_url: url })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    }

    showLoading() {
        this.loadingSection.style.display = 'block';
        this.resultSection.style.display = 'none';
        this.simulateProgress();
    }

    hideLoading() {
        this.loadingSection.style.display = 'none';
        this.progressFill.style.width = '0%';
    }

    simulateProgress() {
        let progress = 0;
        const statuses = [
            'Downloading video...',
            'Extracting audio...',
            'Processing with Whisper...',
            'Detecting language...',
            'Generating transcription...',
            'Finalizing...'
        ];
        
        const interval = setInterval(() => {
            progress += Math.random() * 15;
            if (progress > 90) progress = 90;
            
            this.progressFill.style.width = `${progress}%`;
            
            const statusIndex = Math.floor((progress / 100) * statuses.length);
            if (statusIndex < statuses.length) {
                this.loadingStatus.textContent = statuses[statusIndex];
            }
        }, 800);

        setTimeout(() => {
            clearInterval(interval);
            this.progressFill.style.width = '100%';
        }, 10000);
    }

    displayResult(data) {
        this.textOutput.textContent = data.text || 'No text could be extracted from this video.';
        this.detectedLanguage.textContent = `Detected language: ${data.language || 'Unknown'}`;
        this.videoTitle.textContent = data.title || 'Unknown Title';
        this.extractionTime.textContent = new Date().toLocaleString();
        
        this.resultSection.style.display = 'block';
        this.resultSection.scrollIntoView({ behavior: 'smooth' });
    }

    async copyText() {
        try {
            await navigator.clipboard.writeText(this.textOutput.textContent);
            
            const originalText = this.copyBtn.textContent;
            this.copyBtn.textContent = '✅ Copied!';
            this.copyBtn.classList.add('copied');
            
            setTimeout(() => {
                this.copyBtn.textContent = originalText;
                this.copyBtn.classList.remove('copied');
            }, 2000);
        } catch (error) {
            this.fallbackCopyText();
        }
    }

    fallbackCopyText() {
        const textArea = document.createElement('textarea');
        textArea.value = this.textOutput.textContent;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        
        this.copyBtn.textContent = '✅ Copied!';
        setTimeout(() => {
            this.copyBtn.textContent = '📋 Copy Text';
        }, 2000);
    }

    saveTranscription() {
        const transcription = {
            id: Date.now().toString(),
            url: this.videoUrlInput.value,
            title: this.videoTitle.textContent,
            text: this.textOutput.textContent,
            language: this.detectedLanguage.textContent,
            timestamp: new Date().toISOString(),
            preview: this.textOutput.textContent.substring(0, 100) + '...'
        };

        this.addToStorage(transcription);
        this.renderTranscriptionList();
        
        this.saveBtn.textContent = '✅ Saved!';
        setTimeout(() => {
            this.saveBtn.textContent = '💾 Save';
        }, 2000);
    }

    addToStorage(transcription) {
        const stored = JSON.parse(localStorage.getItem('transcriptions') || '[]');
        stored.unshift(transcription);
        
        // Keep only the last 50 transcriptions
        if (stored.length > 50) {
            stored.splice(50);
        }
        
        localStorage.setItem('transcriptions', JSON.stringify(stored));
    }

    loadStoredTranscriptions() {
        this.renderTranscriptionList();
    }

    renderTranscriptionList() {
        const stored = JSON.parse(localStorage.getItem('transcriptions') || '[]');
        
        if (stored.length === 0) {
            this.transcriptionList.innerHTML = '<div class="empty-state">No transcriptions yet</div>';
            return;
        }

        this.transcriptionList.innerHTML = stored.map(item => `
            <div class="transcription-item" data-id="${item.id}">
                <div class="transcription-title">${this.escapeHtml(item.title)}</div>
                <div class="transcription-meta">
                    <span>${item.language}</span>
                    <span>${new Date(item.timestamp).toLocaleDateString()}</span>
                </div>
                <div class="transcription-preview">${this.escapeHtml(item.preview)}</div>
            </div>
        `).join('');

        // Add click events to transcription items
        this.transcriptionList.addEventListener('click', (e) => {
            const item = e.target.closest('.transcription-item');
            if (item) {
                this.loadTranscription(item.dataset.id);
            }
        });
    }

    loadTranscription(id) {
        const stored = JSON.parse(localStorage.getItem('transcriptions') || '[]');
        const transcription = stored.find(item => item.id === id);
        
        if (transcription) {
            this.videoUrlInput.value = transcription.url;
            this.textOutput.textContent = transcription.text;
            this.detectedLanguage.textContent = transcription.language;
            this.videoTitle.textContent = transcription.title;
            this.extractionTime.textContent = new Date(transcription.timestamp).toLocaleString();
            
            this.resultSection.style.display = 'block';
            
            // Highlight selected item
            document.querySelectorAll('.transcription-item').forEach(el => 
                el.classList.remove('active')
            );
            document.querySelector(`[data-id="${id}"]`).classList.add('active');
        }
    }

    clearHistory() {
        if (confirm('Are you sure you want to clear all transcription history?')) {
            localStorage.removeItem('transcriptions');
            this.renderTranscriptionList();
        }
    }

    handleError(error) {
        console.error('Error extracting text:', error);
        
        let errorMessage = 'Failed to extract text from video. ';
        if (error.message.includes('404')) {
            errorMessage += 'Video not found or not accessible.';
        } else if (error.message.includes('network')) {
            errorMessage += 'Network error. Please check your connection.';
        } else {
            errorMessage += 'Please try again or check if the video URL is valid.';
        }
        
        this.textOutput.textContent = errorMessage;
        this.detectedLanguage.textContent = 'Error occurred';
        this.videoTitle.textContent = 'Error';
        this.extractionTime.textContent = new Date().toLocaleString();
        
        this.resultSection.style.display = 'block';
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new VideoTextExtractor();
});