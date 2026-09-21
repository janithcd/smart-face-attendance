import {
    Users,
} from "lucide-react"

import {
    PlaceholderPage,
} from "@/components/layout/placeholder-page"


export function Component() {

    return (

        <PlaceholderPage
            title="People"
            description={
                "Manage people and their biometric enrollment profiles."
            }
            icon={
                <Users
                    className="size-6"
                />
            }
        />

    )
}