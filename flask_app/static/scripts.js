// Function to upload files
function uploadFiles() {
    const fileInput = document.getElementById('fileInput');
    const files = fileInput.files;
    
    if (files.length === 0) {
        alert("Please select files to upload.");
        return;
    }

    const formData = new FormData();
    for (let i = 0; i < files.length; i++) {
        formData.append('file', files[i]);
    }

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert(data.message);
            updateFileList();
        } else {
            alert("File upload failed.");
        }
    })
    .catch(error => console.error('Error:', error));
}

// Function to update file list
function updateFileList() {
    fetch('/file-list')
    .then(response => response.json())
    .then(data => {
        const fileList = document.getElementById('fileList');
        fileList.innerHTML = '';
        data.files.forEach(file => {
            const li = document.createElement('li');
            li.className = 'list-group-item d-flex justify-content-between align-items-center';
            li.textContent = file;
            const deleteButton = document.createElement('button');
            deleteButton.className = 'btn btn-danger btn-sm';
            deleteButton.textContent = 'Delete';
            deleteButton.onclick = () => deleteFile(file);
            li.appendChild(deleteButton);
            fileList.appendChild(li);
        });
    })
    .catch(error => console.error('Error:', error));
}

// Function to delete a single file
function deleteFile(filename) {
    fetch(`/delete/${filename}`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        updateFileList();
    })
    .catch(error => console.error('Error:', error));
}

// Function to delete all files
function deleteAllFiles() {
    fetch('/delete-all', {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        updateFileList();
    })
    .catch(error => console.error('Error:', error));
}

// Function to process files
function processFiles() {
    fetch('/process', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        const progressBar = document.getElementById('progressBar');
        let progress = 0;
        const interval = setInterval(() => {
            progress += 10;
            progressBar.style.width = `${progress}%`;
            progressBar.textContent = `${progress}%`;
            if (progress >= 100) {
                clearInterval(interval);
                document.getElementById('processResult').textContent = data.message;
            }
        }, 500);
    })
    .catch(error => console.error('Error:', error));
}

// Function to download the XLSX file
function downloadXLSX() {
    fetch('/download-xlsx', {
        method: 'GET'
    })
    .then(response => {
        if (response.ok) {
            response.blob().then(blob => {
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'processed_data.xlsx';
                document.body.appendChild(a);
                a.click();
                a.remove();
            });
        } else {
            alert('Failed to download the XLSX file.');
        }
    })
    .catch(error => console.error('Error:', error));
}

// Initial update of the file list when the page loads
document.addEventListener('DOMContentLoaded', updateFileList);
 