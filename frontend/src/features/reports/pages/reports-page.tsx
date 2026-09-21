import {
    BarChart,
} from "lucide-react"

import {
    PlaceholderPage,
} from "@/components/layout/placeholder-page"


export function Component() {

    return (

        <PlaceholderPage
            title="Reports"
            description={
                "Analyze attendance data and generate reports."
            }
            icon={
                <BarChart
                    className="size-6"
                />
            }
        />

    )
}