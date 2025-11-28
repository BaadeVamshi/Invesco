import React, { useState } from 'react';

function UserDashboard() {
  const [mddResult, setMddResult] = useState(null);
  const [waccResult, setWaccResult] = useState(null);
  const handleCalculateMDD = (event) => {
    event.preventDefault();
    const form = event.target;
    const startDate = form.elements['start-date'].value;
    const endDate = form.elements['end-date'].value;
    const selectedStock = form.elements['stock-select'].value;

    if (startDate && endDate && selectedStock) {
      console.log('Calculating MDD for:', { stock: selectedStock, startDate, endDate });
      // Placeholder for MDD calculation logic
      const result = `MDD for ${selectedStock} from ${startDate} to ${endDate} is -XX.XX%`;
      setWaccResult(null);
      setMddResult(result);
      // Here you would typically dispatch an action to your redux store
      // or call an API to perform the calculation.
      // e.g., dispatch(calculateMDD({ startDate, endDate }));
    } else {
      console.log("Please select a stock, start date, and end date.");
      setMddResult("Please select a stock, start date, and end date.");
    }
  };

  const handleCalculateWACC = (event) => {
    event.preventDefault();
    console.log('Calculating WACC...');
    // Placeholder for WACC calculation logic
    const result = `WACC result will be displayed here.`;
    setMddResult(null);
    setWaccResult(result);
  };

  return (
    <div style={{ padding: '20px', color: 'var(--text-color)', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
      <div style={{ width: '100%', maxWidth: '500px', marginTop: '30px', padding: '20px', backgroundColor: 'var(--container-bg-color, #f0f0f0)', borderRadius: '8px', border: '1px solid #ccc' }}>
        <h3>Calculate Maximum Drawdown (MDD)</h3>
        <form onSubmit={handleCalculateMDD}>
          <div style={{ marginBottom: '15px' }}>
            <label htmlFor="stock-select" style={{ display: 'block', marginBottom: '5px' }}>Select Stock</label>
            <select id="stock-select" name="stock-select" required style={{ padding: '8px', backgroundColor: 'var(--input-bg-color, #fff)', color: 'var(--text-color, #000)', border: '1px solid #999', width: '200px' }}>
              <option value="MSFT">MSFT</option>
              <option value="NTFLX">NTFLX</option>
            </select>
          </div>
          <div style={{ marginBottom: '15px' }}>
            <label htmlFor="start-date" style={{ display: 'block', marginBottom: '5px' }}>Start Date</label>
            <input type="date" id="start-date" name="start-date" required style={{ padding: '8px', backgroundColor: 'var(--input-bg-color, #fff)', color: 'var(--text-color, #000)', border: '1px solid #999', width: '200px' }} />
          </div>
          <div style={{ marginBottom: '15px' }}>
            <label htmlFor="end-date" style={{ display: 'block', marginBottom: '5px' }}>End Date</label>
            <input type="date" id="end-date" name="end-date" required style={{ padding: '8px', backgroundColor: 'var(--input-bg-color, #fff)', color: 'var(--text-color, #000)', border: '1px solid #999', width: '200px' }} />
          </div>
          <div style={{ display: 'flex', gap: '10px' }}>
            <button type="submit" style={{ padding: '10px 15px', backgroundColor: 'var(--primary-color, #007bff)', color: '#fff', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
              Calculate MDD
            </button>
            <button type="button" onClick={handleCalculateWACC} style={{ padding: '10px 15px', backgroundColor: 'var(--primary-color, #007bff)', color: '#fff', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
              Calculate WACC
            </button>
          </div>
        </form>
      </div>

      {mddResult && (
        <div style={{ width: '100%', maxWidth: '500px', marginTop: '30px', padding: '20px', backgroundColor: 'var(--container-bg-color, #f0f0f0)', borderRadius: '8px', border: '1px solid #ccc' }}>
          <h3>MDD Result</h3>
          <p>{mddResult}</p>
        </div>
      )}

      {waccResult && (
        <div style={{ width: '100%', maxWidth: '500px', marginTop: '30px', padding: '20px', backgroundColor: 'var(--container-bg-color, #f0f0f0)', borderRadius: '8px', border: '1px solid #ccc' }}>
          <h3>WACC Result</h3>
          <p>{waccResult}</p>
        </div>
      )}
    </div>
  );
}

export default UserDashboard;
