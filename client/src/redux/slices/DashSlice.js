import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';

// Async thunk for user login
export const userLogin = createAsyncThunk('user/login', async (userCred, { rejectWithValue }) => {
    try {
        const backendUrl = import.meta.env.VITE_BACKEND_URL;
        const response = await axios.post(`${backendUrl}/user-api/login`, userCred);
        if (response.data.token) {
            sessionStorage.setItem('token', response.data.token);
        }
        return response.data;
    } catch (error) {
        return rejectWithValue(error.response.data);
    }
});

// NEW: Async thunk for reloading user session
export const reloadUserSession = createAsyncThunk('user/reload', async (_, { rejectWithValue }) => {
    try {
        // Get the token from session storage
        const token = sessionStorage.getItem('token');
        if (!token) {
            return rejectWithValue({ message: "No token found" });
        }

        const backendUrl = import.meta.env.VITE_BACKEND_URL;
        // Include the token in the Authorization header
        const response = await axios.get(`${backendUrl}/user-api/reload`, { headers: { Authorization: `Bearer ${token}` } });
        // On success, the thunk returns the payload from the API
        return response.data;
    } catch (error) {
        return rejectWithValue(error.response.data);
    }
});

const dashSlice = createSlice({
    name: 'dash',
    initialState: {
        isPending: false,
        loginUserStatus: false,
        currentUser: {},
        errorOccurred: false,
        errMsg: ''
    },
    reducers: {
        resetState: (state, action) => {
            state.isPending = false;
            state.loginUserStatus = false;
            state.currentUser = {};
            state.errorOccurred = false;
            state.errMsg = '';
            sessionStorage.removeItem('token');
        }
    },
    extraReducers: (builder) => {
        builder.addCase(userLogin.pending, (state) => {
            state.isPending = true;
        });
        builder.addCase(userLogin.fulfilled, (state, action) => {
            state.isPending = false;
            state.currentUser = action.payload.user;
            state.loginUserStatus = true;
            state.errorOccurred = false;
            state.errMsg = '';
        });
        builder.addCase(userLogin.rejected, (state, action) => {
            state.isPending = false;
            state.currentUser = {};
            state.loginUserStatus = false;
            state.errorOccurred = true;
            state.errMsg = action.payload.message;
        });

        // --- Reducers for the reload thunk ---

        // Add a pending case to handle loading state during session reload
        builder.addCase(reloadUserSession.pending, (state) => {
            state.isPending = true;
        });

        builder.addCase(reloadUserSession.fulfilled, (state, action) => {
            state.isPending = false;
            state.currentUser = action.payload.user;
            state.loginUserStatus = true;
            // Also reset any previous errors on a successful reload
            state.errorOccurred = false;
            state.errMsg = '';
        });

        builder.addCase(reloadUserSession.rejected, (state, action) => {
            state.isPending = false;
            state.currentUser = {};
            state.loginUserStatus = false;
            // Clean up the invalid token from storage on failure
            sessionStorage.removeItem('token');
        });
    },
});

export const { resetState } = dashSlice.actions;
export default dashSlice.reducer;
