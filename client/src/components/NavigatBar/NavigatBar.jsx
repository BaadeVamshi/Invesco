import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux';
import { resetState } from '../../redux/slices/DashSlice';
import "./NavigatBar.css";

function NavigatBar() {
  // Safely access loginUserStatus, default to false if state.user is not available
  const loginUserStatus = useSelector(state => state.user?.loginUserStatus || false);
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const handleSignOut = () => {
    // Dispatch the logout action to clear user state
    dispatch(resetState());
    // Navigate back to the sign-in page
    navigate('/signin');
  };

  return (
    <div className='navi' style={{ backgroundColor: 'var(--container-bg-color)' }}>
      <ul className='nav justify-content-end m-0 p-0 gap-3 me-2'>
        {loginUserStatus ? (
          // If user is logged in, show only Sign Out
          <li className="nav-item">
            <button className='nav-link btn btn-link' onClick={handleSignOut}>Sign Out</button>
          </li>
        ) : (
          // If user is not logged in, show Home, Sign Up, and Sign In
          <>
            <li className="nav-item">
              <NavLink className='nav-link' to="/">Home</NavLink>
            </li>
            <li className='nav-item'>
              <NavLink className='nav-link' to="signup">Sign Up</NavLink>
            </li>
            <li className='nav-item'>
              <NavLink className='nav-link' to="signin">Sign In</NavLink>
            </li>
          </>
        )}
      </ul>
    </div>
  )
}

export default NavigatBar
