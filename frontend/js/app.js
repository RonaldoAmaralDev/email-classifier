/**
 * Email Classifier - Application JavaScript
 * Classificação Inteligente de Emails
 */

// ===== Sample Emails Data =====
const sampleEmails = {
    suporte: `Prezado Suporte,

Estou enfrentando dificuldades para acessar o sistema de gestão financeira desde ontem às 14h.

Ao tentar fazer login, recebo a mensagem "Erro de autenticação - código 500". Já tentei limpar o cache do navegador e usar outro dispositivo, mas o problema persiste.

Meu usuário é joao.silva@empresa.com e preciso urgentemente acessar os relatórios do trimestre para a reunião de amanhã.

Poderiam verificar o que está acontecendo e me ajudar a resolver?

Obrigado,
João Silva
Departamento Financeiro
Ramal: 2345`,

    status: `Olá equipe,

Gostaria de solicitar uma atualização sobre o status do chamado #45678 aberto na semana passada referente à integração do módulo de pagamentos.

O prazo inicial era para sexta-feira e ainda não recebi nenhum retorno sobre o andamento.

Precisamos dessa funcionalidade operacional até o final do mês para a migração do sistema.

Aguardo retorno,
Maria Santos
Gerente de Projetos`,

    natal: `Prezados colegas,

Com a chegada do fim de ano, gostaria de desejar a todos um Feliz Natal e um próspero Ano Novo!

Que 2024 seja repleto de realizações, saúde e muitas conquistas profissionais e pessoais.

Agradeço a parceria ao longo deste ano e espero que possamos continuar trabalhando juntos com a mesma dedicação.

Boas festas!

Abraços,
Carlos Oliveira
Diretor Comercial`,

    agradecimento: `Olá pessoal!

Gostaria de agradecer a todos que participaram do evento de confraternização da empresa na última sexta-feira.

Foi uma noite muito especial e fico feliz em ver o quanto nossa equipe está unida.

Parabéns a todos pelo excelente trabalho realizado este ano!

Um grande abraço,
Ana Paula
RH`
};

// ===== DOM Elements =====
const elements = {
    // Tabs
    tabBtns: document.querySelectorAll('.tab-btn'),
    tabContents: document.querySelectorAll('.tab-content'),

    // Text Input
    emailText: document.getElementById('emailText'),
    classifyTextBtn: document.getElementById('classifyTextBtn'),

    // File Input
    fileInput: document.getElementById('fileInput'),
    dropZone: document.getElementById('dropZone'),
    selectedFile: document.getElementById('selectedFile'),
    fileName: document.getElementById('fileName'),
    removeFileBtn: document.getElementById('removeFile'),
    classifyFileBtn: document.getElementById('classifyFileBtn'),

    // States
    initialState: document.getElementById('initialState'),
    loadingState: document.getElementById('loadingState'),
    resultsState: document.getElementById('resultsState'),

    // Results
    classificationBadge: document.getElementById('classificationBadge'),
    classificationText: document.getElementById('classificationText'),
    confidenceValue: document.getElementById('confidenceValue'),
    confidenceFill: document.getElementById('confidenceFill'),
    suggestedResponse: document.getElementById('suggestedResponse'),
    keywords: document.getElementById('keywords'),

    // Actions
    copyResponse: document.getElementById('copyResponse'),
    newClassification: document.getElementById('newClassification'),

    // Status
    statusDot: document.getElementById('statusDot'),
    statusText: document.getElementById('statusText'),

    // Samples
    sampleBtns: document.querySelectorAll('.sample-btn')
};

// ===== API Configuration =====
const API_BASE = window.location.origin;

// ===== API Functions =====

/**
 * Check API health status
 */
async function checkStatus() {
    try {
        const response = await fetch(`${API_BASE}/health`);
        const data = await response.json();

        elements.statusDot.classList.remove('offline');
        elements.statusDot.classList.add('online');
        elements.statusText.textContent = data.ai_enabled
            ? 'IA conectada e pronta'
            : 'Modo heurístico (sem API de IA)';
    } catch (error) {
        elements.statusDot.classList.remove('online');
        elements.statusDot.classList.add('offline');
        elements.statusText.textContent = 'Erro de conexão com o servidor';
    }
}

/**
 * Classify email by text content
 * @param {string} text - Email content
 */
async function classifyText(text) {
    showLoading();

    try {
        const response = await fetch(`${API_BASE}/api/classify/text`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ content: text })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Erro ao classificar email');
        }

        const result = await response.json();
        showResults(result);
    } catch (error) {
        showError(error.message);
        showInitial();
    }
}

/**
 * Classify email by file upload
 */
async function classifyFile() {
    showLoading();

    const file = elements.fileInput.files[0];
    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch(`${API_BASE}/api/classify/file`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Erro ao classificar arquivo');
        }

        const result = await response.json();
        showResults(result);
    } catch (error) {
        showError(error.message);
        showInitial();
    }
}

// ===== UI State Functions =====

/**
 * Show loading state
 */
function showLoading() {
    elements.initialState.style.display = 'none';
    elements.resultsState.classList.remove('active');
    elements.loadingState.classList.add('active');
}

/**
 * Show initial state
 */
function showInitial() {
    elements.loadingState.classList.remove('active');
    elements.resultsState.classList.remove('active');
    elements.initialState.style.display = 'block';
}

/**
 * Show results state
 * @param {Object} result - Classification result
 */
function showResults(result) {
    elements.loadingState.classList.remove('active');
    elements.initialState.style.display = 'none';
    elements.resultsState.classList.add('active');

    // Classification badge
    const isProdutivo = result.classification === 'Produtivo';
    elements.classificationBadge.className = `classification-badge ${isProdutivo ? 'produtivo' : 'improdutivo'}`;
    elements.classificationBadge.querySelector('i').className = `fas fa-${isProdutivo ? 'check-circle' : 'info-circle'}`;
    elements.classificationText.textContent = result.classification;

    // Confidence
    const confidence = Math.round(result.confidence * 100);
    elements.confidenceValue.textContent = `${confidence}%`;
    elements.confidenceFill.style.width = `${confidence}%`;

    elements.confidenceFill.className = 'confidence-fill';
    if (confidence >= 80) {
        elements.confidenceFill.classList.add('high');
    } else if (confidence >= 60) {
        elements.confidenceFill.classList.add('medium');
    } else {
        elements.confidenceFill.classList.add('low');
    }

    // Suggested response
    elements.suggestedResponse.textContent = result.suggested_response;

    // Keywords
    elements.keywords.innerHTML = result.keywords
        .map(kw => `<span class="keyword-tag">${escapeHtml(kw)}</span>`)
        .join('');
}

/**
 * Show error message
 * @param {string} message - Error message
 */
function showError(message) {
    alert('Erro: ' + message);
}

// ===== Helper Functions =====

/**
 * Escape HTML special characters
 * @param {string} text - Text to escape
 * @returns {string} - Escaped text
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Handle file selection
 * @param {File} file - Selected file
 */
function handleFile(file) {
    const validExtensions = ['.txt', '.pdf'];
    const extension = file.name.toLowerCase().slice(file.name.lastIndexOf('.'));

    if (!validExtensions.includes(extension)) {
        alert('Formato de arquivo não suportado. Use .txt ou .pdf');
        return;
    }

    elements.fileName.textContent = file.name;
    elements.selectedFile.style.display = 'flex';
    elements.classifyFileBtn.disabled = false;
}

/**
 * Clear file selection
 */
function clearFileSelection() {
    elements.fileInput.value = '';
    elements.selectedFile.style.display = 'none';
    elements.classifyFileBtn.disabled = true;
}

/**
 * Reset form to initial state
 */
function resetForm() {
    showInitial();
    elements.emailText.value = '';
    clearFileSelection();
}

/**
 * Copy text to clipboard
 * @param {string} text - Text to copy
 */
async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
        return true;
    } catch (err) {
        console.error('Failed to copy:', err);
        return false;
    }
}

// ===== Event Listeners =====

/**
 * Initialize all event listeners
 */
function initEventListeners() {
    // Tab switching
    elements.tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const tabId = btn.dataset.tab;

            elements.tabBtns.forEach(b => b.classList.remove('active'));
            elements.tabContents.forEach(c => c.classList.remove('active'));

            btn.classList.add('active');
            document.getElementById(`tab-${tabId}`).classList.add('active');
        });
    });

    // Sample emails
    elements.sampleBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const sample = btn.dataset.sample;
            elements.emailText.value = sampleEmails[sample];
        });
    });

    // File upload - click
    elements.dropZone.addEventListener('click', () => {
        elements.fileInput.click();
    });

    // File upload - drag and drop
    elements.dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        elements.dropZone.classList.add('dragover');
    });

    elements.dropZone.addEventListener('dragleave', () => {
        elements.dropZone.classList.remove('dragover');
    });

    elements.dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        elements.dropZone.classList.remove('dragover');

        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFile(files[0]);
        }
    });

    // File input change
    elements.fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFile(e.target.files[0]);
        }
    });

    // Remove file
    elements.removeFileBtn.addEventListener('click', clearFileSelection);

    // Classify text button
    elements.classifyTextBtn.addEventListener('click', () => {
        const text = elements.emailText.value.trim();
        if (!text) {
            alert('Por favor, insira o conteúdo do email');
            return;
        }
        classifyText(text);
    });

    // Classify file button
    elements.classifyFileBtn.addEventListener('click', classifyFile);

    // Copy response button
    elements.copyResponse.addEventListener('click', async () => {
        const text = elements.suggestedResponse.textContent;
        const success = await copyToClipboard(text);

        if (success) {
            elements.copyResponse.innerHTML = '<i class="fas fa-check"></i> Copiado!';
            elements.copyResponse.classList.add('copied');

            setTimeout(() => {
                elements.copyResponse.innerHTML = '<i class="fas fa-copy"></i> Copiar Resposta';
                elements.copyResponse.classList.remove('copied');
            }, 2000);
        } else {
            alert('Erro ao copiar texto');
        }
    });

    // New classification button
    elements.newClassification.addEventListener('click', resetForm);

    // Keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        // Ctrl/Cmd + Enter to classify
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            const text = elements.emailText.value.trim();
            if (text) {
                classifyText(text);
            }
        }
    });
}

// ===== Initialization =====

/**
 * Initialize the application
 */
function init() {
    // Check API status
    checkStatus();

    // Set up periodic status check
    setInterval(checkStatus, 30000);

    // Initialize event listeners
    initEventListeners();
}

// Start the application when DOM is ready
document.addEventListener('DOMContentLoaded', init);
