import React, { useState } from 'react';

const AlgorithmForm = ({ onSubmit }) => {
  const platformAlgorithmMap = {
    Pregel: ['PageRank', 'SSSP', 'CC'],
    Grape: ['PageRank', 'SSSP', 'LPA', 'TriangleCounting', 'CC'],
    GraphX: ['PageRank', 'SSSP', 'TriangleCounting', 'CC'],
    Gthinker: ['kClique', 'TriangleCounting'], 
    Flash: ['PageRank', 'SSSP', 'CD', 'BC', 'LPA', 'TriangleCounting', 'kClique', 'CC'],
    PowerGraph: ['PageRank', 'SSSP', 'CD', 'BC', 'TriangleCounting', 'CC'],
    Ligra: ['PageRank', 'SSSP', 'CD', 'BC', 'TriangleCounting', 'CC'],
  };

  const [formData, setFormData] = useState({
    platform: 'Pregel',
    algorithm: 'PageRank'
  });

  const handlePlatformChange = (e) => {
    const newPlatform = e.target.value;
    const availableAlgorithms = platformAlgorithmMap[newPlatform];

    setFormData({
      platform: newPlatform,
      algorithm: availableAlgorithms.includes(formData.algorithm) ? formData.algorithm : availableAlgorithms[0] // 确保 algorithm 有效
    });
  };

  const handleAlgorithmChange = (e) => {
    setFormData({ ...formData, algorithm: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit} className="algorithm-form">
        <h2>Integrated Platform</h2>
      <div className="form-group">
        <label>Platform:</label>
        <select 
          value={formData.platform}
          onChange={handlePlatformChange}
        >
          {Object.keys(platformAlgorithmMap).map(platform => (
            <option key={platform} value={platform}>{platform}</option>
          ))}
        </select>
      </div>

      <div className="form-group">
        <label>Task:</label>
        <select
          value={formData.algorithm}
          onChange={handleAlgorithmChange}
        >
          {platformAlgorithmMap[formData.platform].map(algorithm => (
            <option key={algorithm} value={algorithm}>{algorithm}</option>
          ))}
        </select>
      </div>

      <button type="submit" className="submit-btn">Evaluate</button>
    </form>
  );
};

export default AlgorithmForm;
