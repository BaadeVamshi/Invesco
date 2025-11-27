import React from 'react';
import { Outlet } from 'react-router-dom';
import NavigatBar from '../NavigatBar/NavigatBar';
import './RootLayout.css';

const RootLayout = () => {
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