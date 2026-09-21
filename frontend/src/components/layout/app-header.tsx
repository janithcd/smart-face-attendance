import {
    ChevronRight,
} from "lucide-react"

import {
    useLocation,
} from "react-router"

import {
    ModeToggle,
} from "@/components/mode-toggle"

import {
    getPageTitle,
} from "@/config/navigation"

import {
    Separator,
} from "@/components/ui/separator"

import {
    SidebarTrigger,
} from "@/components/ui/sidebar"


export function AppHeader() {

    const location =
        useLocation()

    const pageTitle =
        getPageTitle(
            location.pathname
        )


    return (

        <header
            className="
        sticky
        top-0
        z-30
        flex
        h-16
        shrink-0
        items-center
        gap-3
        border-b
        bg-background/95
        px-4
        backdrop-blur
        supports-[backdrop-filter]:bg-background/80
        md:px-6
      "
        >

            <SidebarTrigger />


            <Separator
                orientation="vertical"
                className="h-5"
            />


            <nav
                aria-label="Breadcrumb"
                className="
          flex
          min-w-0
          items-center
          gap-2
          text-sm
        "
            >

        <span
            className="
            hidden
            text-muted-foreground
            sm:inline
          "
        >
          Smart Attendance
        </span>


                <ChevronRight
                    className="
            hidden
            size-4
            text-muted-foreground
            sm:block
          "
                />


                <span
                    className="
            truncate
            font-medium
          "
                >
          {pageTitle}
        </span>

            </nav>


            <div
                className="
          ml-auto
          flex
          items-center
          gap-2
        "
            >

                <div
                    className="
            hidden
            items-center
            gap-2
            rounded-full
            border
            px-3
            py-1
            text-xs
            text-muted-foreground
            lg:flex
          "
                >

          <span
              className="
              size-2
              rounded-full
              bg-emerald-500
            "
          />

                    Local environment

                </div>


                <ModeToggle />

            </div>

        </header>

    )
}