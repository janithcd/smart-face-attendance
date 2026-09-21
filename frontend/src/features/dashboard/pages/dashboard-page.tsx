import {
    LayoutDashboard,
} from "lucide-react"

import {
    PlaceholderPage,
} from "@/components/layout/placeholder-page"


export function Component() {

    return (

        <PlaceholderPage
            title="Dashboard"
            description={
                "Overview of biometric attendance, people, devices, and system health."
            }
            icon={
                <LayoutDashboard
                    className="size-6"
                />
            }
        />

    )
}