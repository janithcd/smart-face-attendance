import {
    Settings,
} from "lucide-react"

import {
    PlaceholderPage,
} from "@/components/layout/placeholder-page"


export function Component() {

    return (

        <PlaceholderPage
            title="Settings"
            description={
                "Configure recognition, liveness, system, and application preferences."
            }
            icon={
                <Settings
                    className="size-6"
                />
            }
        />

    )
}