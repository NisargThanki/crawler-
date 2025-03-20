import React, { useState } from 'react';
import axios from 'axios';
import './CrawlerForm.css';

const CrawlerForm = () => {
    const [formData, setFormData] = useState({
        crawling_depth: 2,
        max_pages: 10,
        concurrent_requests: 2,
        timeout_seconds: 30,
        selector: 'body'
    });
    const [csvFile, setCsvFile] = useState(null);
    const [isLoading, setIsLoading] = useState  (false);
    const [message, setMessage] = useState('');

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData(prevState => ({
            ...prevState,
            [name]: parseInt(value) || value
        }));
    };

    const handleFileChange = (e) => {
        const file = e.target.files[0]; 
        if (file && !file.name.endsWith('.csv')) {
            setMessage('Please upload a CSV file');
            return;
        }
        setCsvFile(file);
        setMessage('');
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!csvFile) {
            setMessage('Please select a CSV file');
            return;
        }

        setIsLoading(true);
        setMessage('');

        const submitData = new FormData();
        submitData.append('csv_file', csvFile);
        
        // Append other form data
        Object.keys(formData).forEach(key => {
            submitData.append(key, formData[key]);
        });

        try {
            const response = await axios.post('http://localhost:5000/submit-crawler', submitData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });

            if (response.data.success) {
                setMessage('Crawler started successfully! Check results folder for output.');
            }
        } catch (error) {
            setMessage(`Error: ${error.response?.data?.error || error.message}`);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="crawler-form-container">
            <h2>Web Crawler Configuration</h2>
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label>CSV File with URLs:</label>
                    <input 
                        type="file"
                        accept=".csv"
                        onChange={handleFileChange}
                        className="form-control"
                    />
                </div>

                <div className="form-group">
                    <label>Crawling Depth:</label>
                    <input
                        type="number"
                        name="crawling_depth"
                        value={formData.crawling_depth}
                        onChange={handleInputChange}
                        min="1"
                        className="form-control"
                    />
                </div>

                <div className="form-group">
                    <label>Max Pages per Website:</label>
                    <input
                        type="number"
                        name="max_pages"
                        value={formData.max_pages}
                        onChange={handleInputChange}
                        min="1"
                        className="form-control"
                    />
                </div>

                <div className="form-group">
                    <label>Concurrent Requests:</label>
                    <input
                        type="number"
                        name="concurrent_requests"
                        value={formData.concurrent_requests}
                        onChange={handleInputChange}
                        min="1"
                        className="form-control"
                    />
                </div>

                <div className="form-group">
                    <label>Timeout (seconds):</label>
                    <input
                        type="number"
                        name="timeout_seconds"
                        value={formData.timeout_seconds}
                        onChange={handleInputChange}
                        min="1"
                        className="form-control"
                    />
                </div>

                <div className="form-group">
                    <label>CSS Selector:</label>
                    <input
                        type="text"
                        name="selector"
                        value={formData.selector}
                        onChange={handleInputChange}
                        className="form-control"
                    />
                </div>

                <button 
                    type="submit" 
                    disabled={isLoading || !csvFile}
                    className="submit-button"
                >
                    {isLoading ? 'Processing...' : 'Start Crawler'}
                </button>

                {message && (
                    <div className={`message ${message.includes('Error') ? 'error' : 'success'}`}>
                        {message}
                    </div>
                )}
            </form>
        </div>
    );
};

export default CrawlerForm;