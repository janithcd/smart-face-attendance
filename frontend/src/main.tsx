import {
    StrictMode,
} from "react"

import {
    createRoot,
} from "react-dom/client"

import {
    QueryClientProvider,
} from "@tanstack/react-query"

import {
    RouterProvider,
} from "react-router/dom"

import {
    ThemeProvider,
} from "@/components/theme-provider"

import {
    queryClient,
} from "@/lib/query-client"

import {
    router,
} from "@/routes/router"

import "./index.css"


createRoot(
    document.getElementById(
        "root"
    )!
).render(

    <StrictMode>

        <ThemeProvider
            defaultTheme="system"
            storageKey="smart-attendance-theme"
        >

            <QueryClientProvider
                client={queryClient}
            >

                <RouterProvider
                    router={router}
                />

            </QueryClientProvider>

        </ThemeProvider>

    </StrictMode>
)