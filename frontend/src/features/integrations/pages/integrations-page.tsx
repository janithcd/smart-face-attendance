import {
    Plug,
} from "lucide-react"

import {
    PlaceholderPage,
} from "@/components/layout/placeholder-page"


export function Component() {

    return (

        <PlaceholderPage
            title="Integrations"
            description={
                "Connect external HR, employee, payroll, and management systems."
            }
            icon={
                <Plug
                    className="size-6"
                />
            }
        />

    )
}