import {
    Monitor,
} from "lucide-react"

import {
    PlaceholderPage,
} from "@/components/layout/placeholder-page"


export function Component() {

    return (

        <PlaceholderPage
            title="Devices"
            description={
                "Manage attendance kiosks, cameras, and edge devices."
            }
            icon={
                <Monitor
                    className="size-6"
                />
            }
        />

    )
}