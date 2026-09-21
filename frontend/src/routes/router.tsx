import {
    createBrowserRouter,
} from "react-router"

import {
    AppLayout,
} from "@/app/app-layout"

import {
    RouteErrorPage,
} from "@/app/route-error-page"


export const router =
    createBrowserRouter([

        {
            path: "/",

            element: (
                <AppLayout />
            ),

            errorElement: (
                <RouteErrorPage />
            ),

            children: [

                {
                    index: true,

                    lazy: () =>
                        import(
                            "@/features/dashboard/pages/dashboard-page"
                            ),
                },


                {
                    path: "attendance",

                    lazy: () =>
                        import(
                            "@/features/attendance/pages/attendance-page"
                            ),
                },


                {
                    path: "people",

                    lazy: () =>
                        import(
                            "@/features/people/pages/people-page"
                            ),
                },


                {
                    path: "devices",

                    lazy: () =>
                        import(
                            "@/features/devices/pages/devices-page"
                            ),
                },


                {
                    path: "reports",

                    lazy: () =>
                        import(
                            "@/features/reports/pages/reports-page"
                            ),
                },


                {
                    path: "integrations",

                    lazy: () =>
                        import(
                            "@/features/integrations/pages/integrations-page"
                            ),
                },


                {
                    path: "settings",

                    lazy: () =>
                        import(
                            "@/features/settings/pages/settings-page"
                            ),
                },

            ],
        },

    ])