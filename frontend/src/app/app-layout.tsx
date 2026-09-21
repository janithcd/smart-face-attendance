import {
    Outlet,
} from "react-router"

import {
    AppHeader,
} from "@/components/layout/app-header"

import {
    AppSidebar,
} from "@/components/layout/app-sidebar"

import {
    SidebarInset,
    SidebarProvider,
} from "@/components/ui/sidebar"


export function AppLayout() {

    return (

        <SidebarProvider>

            <AppSidebar />


            <SidebarInset>

                <AppHeader />


                <div
                    className="
            flex
            flex-1
            flex-col
            gap-6
            p-4
            md:p-6
          "
                >

                    <Outlet />

                </div>

            </SidebarInset>

        </SidebarProvider>

    )
}