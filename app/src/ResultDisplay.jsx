import React from "react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend } from "recharts";
import "./ResultDisplay.css";

const ResultDisplay = ({ result, loading }) => {
  
  if (loading || !result) return null;

  const chartData = result.evaluations?.map((evaluation, index) => ({
    name: ["Junior", "Intermediate", "Senior", "Expert"][index],
    Compliance: evaluation.compliance_score,
    Correctness: evaluation.correctness_score,
    Readability: evaluation.readability_score,
  }));

  return (
    <div className="result-container">
      <h2>Evaluation Results</h2>

      <div className="result-item">
        <span>Platform: </span>
        {result.platform}
      </div>

      <div className="result-item">
        <span>Task: </span>
        {result.algorithm}
      </div>

      <div className="chart-section">
        <h3>Evaluation Scores</h3>
        <BarChart width={600} height={300} data={chartData}>
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey="Compliance" fill="#8884d8" />
          <Bar dataKey="Correctness" fill="#82ca9d" />
          <Bar dataKey="Readability" fill="#ffc658" />
        </BarChart>
      </div>

      <div className="result-analysis">
        <h3>Result Analysis</h3>
        <p>{result.analysis}</p>
      </div>

      <div className="details-section">
        <h3>Detailed Analysis</h3>
        {result.evaluations?.map((evaluation, index) => (
          <div key={index} className="evaluation-block">
            <h4>{["Junior", "Intermediate", "Senior", "Expert"][index]}</h4>
            <p>
              <strong>Strengths:</strong> {evaluation.strengths}
            </p>
            <p>
              <strong>Weaknesses:</strong> {evaluation.disadvantage}
            </p>
            <p>
              <strong>Compliance:</strong> {evaluation.compliance_score}
              <br />
              <strong>Correctness:</strong> {evaluation.correctness_score}
              <br />
              <strong>Readability:</strong> {evaluation.readability_score}
            </p>
          </div>
        ))}
      </div>

      <div className="timestamp">
        <strong>Computation Time:</strong> {result.timestamp}
      </div>
    </div>
  );
};

export default ResultDisplay;
