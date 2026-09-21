import {
    createBrowserRouter,
} from "react-router"

import App from "@/App"


export const router =
    createBrowserRouter([
        {
            path: "/",
            element: <App />,
        },

        {
            path: "/attendance",
            element: (
                <div>
                    Attendance
                </div>
            ),
        },

        {
            path: "/people",
            element: (
                <div>
                    People
                </div>
            ),
        },

        {
            path: "/reports",
            element: (
                <div>
                    Reports
                </div>
            ),
        },

        {
            path: "/settings",
            element: (
                <div>
                    Settings
                </div>
            ),
        },
    ])