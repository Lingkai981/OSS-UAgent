import React, { useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend } from 'recharts';
import AlgorithmForm from './AlgorithmForm';
import './App.css';

function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleRunAlgorithm = async (params) => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch('http://localhost:5555/api/run', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(params),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();
      if (data.error) throw new Error(data.error);

      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      {/* <div className="header-container">
        <h1>LLM-Driven Usability Evaluation Framework</h1>
      </div> */}

    <div className="left-section">
        <AlgorithmForm onSubmit={handleRunAlgorithm} />
    </div>

    <div className="right-section">
    {loading && <div className="status loading">Evaluating...</div>}

{error && (
  <div className="status error">
    Error: {error}
  </div>
)}
{result && !loading && (
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


      {/* <AlgorithmForm onSubmit={handleRunAlgorithm} /> */}

      
    </div>
  );
}

export default App;
