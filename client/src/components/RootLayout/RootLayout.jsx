import React, { useEffect } from 'react';
import { Outlet } from 'react-router-dom';
import { useDispatch } from 'react-redux';
import { reloadUserSession } from '../../redux/slices/DashSlice';
import NavigatBar from '../NavigatBar/NavigatBar';
import './RootLayout.css';

const RootLayout = () => {
  const dispatch = useDispatch();

  // This effect runs once when the application loads.
  // It dispatches the action to check for a token in session storage
  // and restore the user's session if a valid token is found.
  useEffect(() => {
    dispatch(reloadUserSession());
  }, [dispatch]);

  return (
    <div className="root-layout">
      <NavigatBar />
      <main className="content">
        <Outlet />
      </main>
      <footer className="app-footer">
        <p>&copy; 2025 Invesco. All rights reserved.</p>
      </footer>
    </div>
  );
};

export default RootLayout;