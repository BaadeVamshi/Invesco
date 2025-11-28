import { configureStore } from '@reduxjs/toolkit';
import dashSliceReducer from './slices/DashSlice.js';

export const Store = configureStore({
  reducer: {
    user: dashSliceReducer,
  },
});