import React from 'react';

function UserDashboard() {
  const handleCalculateMDD = (event) => {
    event.preventDefault();
    const form = event.target;
    const startDate = form.elements['start-date'].value;
    const endDate = form.elements['end-date'].value;
    const selectedStock = form.elements['stock-select'].value;

    if (startDate && endDate && selectedStock) {
      console.log('Calculating MDD for:', { stock: selectedStock, startDate, endDate });
      // Here you would typically dispatch an action to your redux store
      // or call an API to perform the calculation.
      // e.g., dispatch(calculateMDD({ startDate, endDate }));
    } else {
      console.log("Please select a stock, start date, and end date.");
    }
  };

  return (
    <div style={{ padding: '20px', color: 'var(--text-color)' }}>
      <h2>Welcome Batman</h2>
      
      <div style={{ marginTop: '30px', padding: '20px', backgroundColor: 'var(--container-bg-color, #f0f0f0)', borderRadius: '8px', border: '1px solid #ccc' }}>
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
          <button type="submit" style={{ padding: '10px 15px', backgroundColor: 'var(--primary-color, #007bff)', color: '#fff', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
            Calculate MDD
          </button>
        </form>
      </div>
    </div>
  );
}

export default UserDashboard;
