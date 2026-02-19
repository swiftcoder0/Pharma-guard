// Switches between Landing Page and the App Views
function selectRole(role) {
    const overlay = document.getElementById('role-overlay');
    const docView = document.getElementById('doctor-view');
    const patView = document.getElementById('patient-view');
    
    overlay.style.opacity = '0';
    setTimeout(() => {
        overlay.style.display = 'none';
        
        if (role === 'doctor') {
            document.body.style.backgroundColor = "#f4f7f6"; 
            docView.style.display = 'block';
        } else {
            document.body.style.backgroundColor = "#0f172a"; 
            patView.style.display = 'block';
        }
    }, 500);
}

// Visual feedback for file upload in Patient View
function updateFileName(input) {
    const textElement = document.getElementById('upload-text');
    const iconElement = document.getElementById('upload-icon');
    
    if (input.files && input.files.length > 0) {
        const fileName = input.files[0].name;
        textElement.innerHTML = `<strong style="color: #4ade80;">✅ File Attached Successfully:</strong><br>${fileName}`;
        iconElement.innerText = "📄"; 
    } else {
        textElement.innerHTML = `Drag & drop your VCF file here or <br><strong>click to upload (.vcf)</strong>`;
        iconElement.innerText = "☁️";
    }
}

// Main logic to analyze DNA
async function analyzeDNA(event, role) {
    if (event) event.preventDefault(); 

    const prefix = role === 'doctor' ? 'doc' : 'pat';
    const fileInput = document.getElementById(`${prefix}-vcf`);
    const drugInput = document.getElementById(`${prefix}-drug`).value.trim();
    const btn = document.getElementById(`${prefix}-btn`);
    const resultsSection = document.getElementById(`${prefix}-results`);

    if (!fileInput.files[0]) { alert("Please upload a VCF file."); return; }
    if (!drugInput) { alert("Please enter a medicine name."); return; }

    btn.innerText = "Analyzing...";
    btn.disabled = true;
    resultsSection.style.display = "block";
    
    if (role === 'doctor') {
        const banner = document.getElementById('doc-banner');
        banner.className = "status-banner";
        banner.style.backgroundColor = "#f39c12"; 
        document.getElementById('doc-status').innerText = "ANALYZING...";
    } else {
        const title = document.getElementById('pat-status');
        title.innerText = "Analyzing your DNA...";
        title.style.color = "#38bdf8";
        document.getElementById('pat-ai').innerText = "Connecting to PharmaGuard AI...";
    }

    const formData = new FormData();
    formData.append("vcf_file", fileInput.files[0]);
    formData.append("drug_name", drugInput);
    formData.append("role", role); 

    try {
         // Make sure you keep the /analyze at the very end!
         const response = await fetch("https://pharma-guard-outj.onrender.com.onrender.com/analyze", {
            method: "POST", body: formData
        });

        if (!response.ok) throw new Error("Server error");
        const data = await response.json();
        
        const isToxic = data.risk_assessment.risk_label.toUpperCase() === "TOXIC";

        if (role === 'doctor') {
            const banner = document.getElementById('doc-banner');
            banner.className = isToxic ? "status-banner bg-toxic" : "status-banner bg-safe";
            document.getElementById('doc-status').innerText = isToxic ? "⚠️ HIGH RISK / TOXIC" : "✅ SAFE TO PRESCRIBE";
            document.getElementById('doc-ai').innerText = data.llm_generated_explanation.summary;
            document.getElementById('doc-gene').innerText = data.pharmacogenomic_profile.primary_gene;
            document.getElementById('doc-pheno').innerText = data.pharmacogenomic_profile.phenotype;
            document.getElementById('doc-rec').innerText = data.clinical_recommendation.action;
        } 
        else {
            const title = document.getElementById('pat-status');
            title.innerText = isToxic ? "⚠️ Warning: Potential Issue Detected" : "✅ Good News: Looks Safe!";
            title.style.color = isToxic ? "#ff6b6b" : "#4ade80"; 
            document.getElementById('pat-ai').innerText = data.llm_generated_explanation.summary;
        }

    } catch (error) {
        console.error("Error:", error);
        alert("Failed to connect to the backend server. Make sure FastAPI is running!");
    } finally {
        btn.innerText = role === 'doctor' ? "Analyze DNA" : "🧬 ANALYZE SAFETY";
        btn.disabled = false;
    }
}