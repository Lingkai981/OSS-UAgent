import React, { useState } from "react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend } from 'recharts';
import "./NewTestForm.css"; 


const NewTestForm = ({ onAddTest }) => {
  const [testName, setTestName] = useState("");
  const [testPlatform, setTestPlatform] = useState("");
  const [knowledgeBase, setKnowledgeBase] = useState("");
  const [standardCode, setStandardCode] = useState("");
  const [isComputing, setIsComputing] = useState(false);
  const [uploadedFileName1, setUploadedFileName1] = useState("");
  const [uploadedFileName2, setUploadedFileName2] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleFileUpload = (event, setFunction, setFileName) => {
    const file = event.target.files[0];
    if (!file) return;

    setFileName(file.name); 
    const reader = new FileReader();
    reader.onload = (e) => {
      setFunction(e.target.result);
    };
    reader.readAsText(file);
  };

  const handleAddTest = async () => {
    if (!testPlatform || !testName || !knowledgeBase || !standardCode) {
      alert("Please fill in all fields.");
      return;
    }

    setIsComputing(true);
    setError(null);
    setResult(null);

    const testData = { testPlatform, testName, knowledgeBase, standardCode };

    try {
      const response = await fetch("http://127.0.0.1:5555/api/new-test", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(testData),
      });

      if (!response.ok) {
        throw new Error("Failed to submit test");
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsComputing(false);
    }
  };

  return (
    <div className="container">
      <div className="left-section">
        <form className="new-test-form">

          <div className="form-group">
            <label>Platform:</label>
            <input
              type="text"
              value={testPlatform}
              onChange={(e) => setTestPlatform(e.target.value)}
              placeholder="Enter platform name"
              required
            />
          </div>

          <div className="form-group">
            <label>Task:</label>
            <input
              type="text"
              value={testName}
              onChange={(e) => setTestName(e.target.value)}
              placeholder="Enter your task"
              required
            />
          </div>

          <div className="form-group">
            <label>Knowledge Base:</label>
            <textarea
              value={knowledgeBase}
              onChange={(e) => setKnowledgeBase(e.target.value)}
              rows="4"
              placeholder="Enter or upload knowledge base"
            />
            <div className="file-upload">
              <input
                type="file"
                accept=".txt"
                id="knowledgeFile"
                onChange={(e) => handleFileUpload(e, setKnowledgeBase, setUploadedFileName1)}
                hidden
              />
              <label htmlFor="knowledgeFile" className="upload-btn">Upload .txt</label>
              {uploadedFileName1 && <span className="file-name">{uploadedFileName1}</span>}
            </div>
          </div>

          <div className="form-group">
            <label>Standard Code:</label>
            <textarea
              value={standardCode}
              onChange={(e) => setStandardCode(e.target.value)}
              rows="4"
              placeholder="Enter standard code"
            />
            <div className="file-upload">
              <input
                type="file"
                accept=".txt"
                id="codeFile"
                onChange={(e) => handleFileUpload(e, setStandardCode, setUploadedFileName2)}
                hidden
              />
              <label htmlFor="codeFile" className="upload-btn">Upload .txt</label>
              {uploadedFileName2 && <span className="file-name">{uploadedFileName2}</span>}
            </div>
          </div>

          <button
            type="button"
            className="submit-btn"
            onClick={handleAddTest}
            disabled={isComputing}
          >
            {isComputing ? "Evaluating..." : "Evaluate"}
          </button>

          {isComputing && <div className="computing-status">Processing, please wait...</div>}
          
          {error && <div className="status error">Error: {error}</div>}

        </form>
      </div>

      <div className="right-section">
              {result && !isComputing && (
                <div className="result-container">
                  <h2>Evaluation Results</h2>
                  <div className="result-item">
                    <span>Platform:</span> {result.platform}
                  </div>
                  <div className="result-item">
                    <span>Task:</span> {result.algorithm}
                  </div>
        
                  {/* Container for Chart and Detailed Analysis */}
                  <div className="evaluation-section">
                    {/* Bar Chart Section */}
                    <div className="chart-container">

                      <h3>Evaluation Scores</h3>
                      <BarChart
                        width={600} // Fixed width
                        height={300}
                        data={result.evaluations?.map((evaluation, index) => ({
                          name: ["Junior", "Intermediate", "Senior", "Expert"][index],
                          Compliance: evaluation.compliance_score,
                          Correctness: evaluation.correctness_score,
                          Readability: evaluation.readability_score
                        }))}
                      >
                        <XAxis dataKey="name" />
                        <YAxis />
                        <Tooltip />
                        <Legend />
                        <Bar dataKey="Compliance" fill="#8884d8" />
                        <Bar dataKey="Correctness" fill="#82ca9d" />
                        <Bar dataKey="Readability" fill="#ffc658" />
                      </BarChart>
        
                      {/* Display "Analysis" text below the chart */}
                      <div className="result-analysis">
                        <h3>Result Analysis</h3>
                        <p>{result.analysis}</p>
                      </div>
                      
                      <h3>Detailed Analysis</h3>
                      {result.evaluations?.map((evaluation, index) => (
                        <div key={index} className="evaluation-block">
                          <h4>{["Junior", "Intermediate", "Senior", "Expert"][index]}</h4>
                          <p><strong>Strengths:</strong> {evaluation.strengths}</p>
                          <p><strong>Weaknesses:</strong> {evaluation.disadvantage}</p>
                        </div>
                      ))}
                    </div>
                  </div>
        
                  <div className="timestamp">
                    Computation Time: {result.timestamp}
                  </div>
                </div>
              )}
      </div>
    </div>
  );
};

export default NewTestForm;
