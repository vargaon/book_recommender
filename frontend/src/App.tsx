import './App.css';
import BooksCatalogue from './components/BooksCatalogue';
import { ErrorPage } from './components/ErrorPage';
import Root from './components/Root';
import BookProfile, { loader as bookLoader } from './components/BookProfile';
import { useState } from 'react';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import UserPage from './components/UserPage';

function App() {

  const [userId, setUserId] = useState("")

  const router = createBrowserRouter([
    {
      path: "/",
      element: <Root />,
      errorElement: <ErrorPage />,
      children: [
        {
          index: true,
          element: <BooksCatalogue userId={userId} />,
        },
        {
          path: "books/:bookId",
          element: <BookProfile userId={userId} />,
          loader: bookLoader,
        },
        {
          path: "user",
          element: <UserPage userId={userId} setUserId={setUserId} />,
        }
      ]
    }
  ])

  return (
    <RouterProvider router={router} />
  );
}

export default App;
