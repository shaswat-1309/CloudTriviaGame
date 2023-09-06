import React from 'react';

const Visualize = () => {
  return (
    <div className="container mt-5">
      <h1>Visualization</h1>
      <div>
        {/* Embedding an iFrame to embed looker studio report */}
      <iframe width="600" height="450" src="https://lookerstudio.google.com/embed/reporting/c5815489-1112-4ba1-846e-52835659e2db/page/GCxYD" frameborder="0" style="border:0" allowfullscreen></iframe>
      </div>
    </div>
  );
};

export default Visualize;
