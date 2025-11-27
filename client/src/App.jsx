import { useState } from 'react'
import { createBrowserRouter,RouterProvider } from 'react-router-dom'
import RootLayout from './components/RootLayout/RootLayout'
import Home from './components/Home/Home'
import SignUp from './components/SignUp/SignUp'
import SignIn from './components/SignIn/SignIn'
import UserDashboard from './components/UserDashboard/UserDashboard'
import ProtectedRoute from './components/ProtectedRoute'

import './App.css'

function App() {

  let router=createBrowserRouter([
    {
      path:'',
      element:<RootLayout/>,
      children:[
        {
          path:'/',
          element:<Home/>
        },
        {
          path:'signup',
          element:<SignUp/>
        },
        {
          path:'signin',
          element:<SignIn/>
        },
        {
          path:'user-dashboard',
          element:<ProtectedRoute><UserDashboard/></ProtectedRoute>
        }
      ]

    }
  ])

  return (
   <>
    <div className="app-container">
      <RouterProvider router={router}></RouterProvider>
    </div>
    </>
  )
}

export default App
