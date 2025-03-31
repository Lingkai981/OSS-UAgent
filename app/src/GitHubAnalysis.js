import React, { useState, useEffect } from "react";
import "./GitHubAnalysis.css";
import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend } from 'recharts';

const GitHubAnalysis = () => {
  const [githubUrl, setGitHubUrl] = useState("");
  const [isProcessing, setIsProcessing] = useState(false);
  const [result1, setResult1] = useState(null);
  const [result2, setResult2] = useState(null);
  const [result3, setResult3] = useState(null);
  const [result4, setResult4] = useState(null);
  const [result5, setResult5] = useState(null);
  const [result6, setResult6] = useState(null);
  const [result7, setResult7] = useState(null);
  const [result8, setResult8] = useState(null);
  const [result9, setResult9] = useState(null);
  const [error, setError] = useState(null);
  const [logs, setLogs] = useState([]);
  const [isLoading1, setIsLoading1] = useState(false);
  const [isLoading2, setIsLoading2] = useState(false);
  const [isLoading3, setIsLoading3] = useState(false);
  const [isLoading4, setIsLoading4] = useState(false);
  useEffect(() => {
    if (result4) {
      setIsLoading1(true);
    }
  }, [result4]);

  useEffect(() => {
    if (result5) {
      setIsLoading1(false); 
      setIsLoading2(true); 
    }
  }, [result5]);

  useEffect(() => {
    if (result6) {
      setIsLoading2(false); 
      setIsLoading3(true);  
    }
  }, [result6]);

  useEffect(() => {
    if (result7) {
      setIsLoading3(false); 
      setIsLoading4(true);  
    }
  }, [result7]);

  useEffect(() => {
    if (result8) {
      setIsLoading4(false);
    }
  }, [result8]);

  const handleAnalyze = async () => {
    if (!githubUrl || isProcessing) return;
    setIsProcessing(true);
    setError(null);
    setLogs([]);
    setResult1(null);
    setResult2(null);
    setResult3(null);
    setResult4(null);
    setResult5(null);
    setResult6(null);
    setResult7(null);
    setResult8(null);
    setResult9(null);



    try {
      const response = await fetch("http://127.0.0.1:5555/api/analyze-github", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ githubUrl }),
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`API Error: ${errorText}`);
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder("utf-8");
      let bufferedData = "";
      const seenLogs = new Set();

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        bufferedData += decoder.decode(value, { stream: true });
        const jsonChunks = bufferedData.split("\n").filter(chunk => chunk.trim() !== "");

        for (const chunk of jsonChunks) {
          try {
            const parsedData = JSON.parse(chunk);

            if (parsedData.status && !seenLogs.has(parsedData.status)) {
              seenLogs.add(parsedData.status);
              setLogs((prevLogs) => [...prevLogs, parsedData.status]);
            } else {
              if ("junior_ready" in parsedData) setResult1(parsedData);
              else if ("intermediate_ready" in parsedData) setResult2(parsedData);
              else if ("senior_ready" in parsedData) setResult3(parsedData);
              else if ("expert_ready" in parsedData) setResult4(parsedData);
              else if ("junior_code" in parsedData) setResult5(parsedData);
              else if ("intermediate_code" in parsedData) setResult6(parsedData);
              else if ("senior_code" in parsedData) setResult7(parsedData);
              else if ("expert_code" in parsedData) setResult8(parsedData);
              else if ("evaluations" in parsedData) setResult9(parsedData); 
            }
          } catch (err) {
            
          }
        }
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="container">
      <div className="input-section">
        <input
          type="text"
          value={githubUrl}
          onChange={(e) => setGitHubUrl(e.target.value)}
          placeholder="Enter GitHub repository URL"
        />
        <button onClick={handleAnalyze} disabled={isProcessing}>
          {isProcessing ? "Analyzing..." : "Evaluate"}
        </button>

        {logs.length > 0 && (
                <ul>
                    {logs.map((log, index) => (
                    <p key={index} style={{ fontWeight: log.includes("**") ? "normal" : "bold" }}>
                        {log}
                    </p>
                    ))}
                </ul>
                )}
      </div>

      <div className="result-section">
        {error && <div className="error">Error: {error}</div>}

        <div className="grid-container">
            
          <div className="grid-item">
            {result1 && (
                <p>
                    {result1.junior_ready}
                </p>
            )}
            {result1 && <img src="/pic/junior.png" alt="Junior Image" />}
            </div>

            <div className="grid-item">
            {result2 && (
                <p>
                    {result2.intermediate_ready}
                </p>
            )}
            {result2 && <img src="/pic/intermediate.png" alt="Junior Image" />}
            </div>

            <div className="grid-item">
            {result3 && (
                <p>
                    {result3.senior_ready}
                </p>
            )}
            {result3 && <img src="/pic/senior.png" alt="Junior Image" />}
            </div>

            <div className="grid-item">
            {result4 && (
                <p>
                    {result4.expert_ready}
                </p>
            )}
            {result4 && <img src="/pic/expert.png" alt="Junior Image" />}
            </div>

            <div className="grid-item">
                {isLoading1 && <div className="loading-spinner"></div>}
                {result5 && (
                    <>
                        <div className="code-display">
                            {result5.junior_code}
                        </div>
                    </>
                )}
            </div>

            <div className="grid-item">
                {isLoading2 && <div className="loading-spinner"></div>}
                {result6 && (
                    <>
                        <div className="code-display">
                            {result6.intermediate_code}
                        </div>
                    </>
                )}
            </div>

            <div className="grid-item">
                {isLoading3 && <div className="loading-spinner"></div>}
                {result7 && (
                    <>
                        <div className="code-display">
                            {result7.senior_code}
                        </div>
                    </>
                )}
            </div>

            <div className="grid-item">
                {isLoading4 && <div className="loading-spinner"></div>}
                {result8 && (
                    <>
                        <div className="code-display">
                            {result8.expert_code}
                        </div>
                    </>
                )}
            </div>

          <div className="grid-item full-width">
            {result9 && (
                            <div className="result-container">
                              <h2>Evaluation Results</h2>
                              <div className="result-item">
                                <span>Platform:</span> {result9.platform}
                              </div>
                              <div className="result-item">
                                <span>Task:</span> {result9.algorithm}
                              </div>
                    
                              {/* Container for Chart and Detailed Analysis */}
                              <div className="evaluation-section">
                                {/* Bar Chart and Analysis Container */}
                                <div className="chart-analysis-container">
                                    {/* Bar Chart Section (Left Side) */}
                                    <div className="chart-container">
                                    <BarChart
                                        width={600} // Fixed width
                                        height={300}
                                        data={result9.evaluations?.map((evaluation, index) => ({
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
                                    </div>

                                    {/* Result Analysis Section (Right Side) */}
                                    <div className="result-analysis-2">
                                    <h3>Result Analysis</h3>
                                    <p>{result9.analysis}</p>
                                    </div>
                                </div>
                                </div>
                    
                              <div className="timestamp">
                                Computation Time: {result9.timestamp}
                              </div>
                            </div>
                          )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default GitHubAnalysis;