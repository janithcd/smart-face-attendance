import {
    ScanFace,
} from "lucide-react"

import {
    PlaceholderPage,
} from "@/components/layout/placeholder-page"


export function Component() {

    return (

        <PlaceholderPage
            title="Attendance"
            description={
                "Run biometric verification and review attendance activity."
            }
            icon={
                <ScanFace
                    className="size-6"
                />
            }
        />

    )
}