import {
    AlertTriangle,
    RefreshCw,
} from "lucide-react"

import {
    Button,
} from "@/components/ui/button"

import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from "@/components/ui/card"


type DashboardErrorStateProps = {
    message: string
    onRetry: () => void
}


export function DashboardErrorState({
                                        message,
                                        onRetry,
                                    }: DashboardErrorStateProps) {

    return (

        <Card>

            <CardHeader>

                <div
                    className="
            mb-3
            flex
            size-10
            items-center
            justify-center
            rounded-lg
            bg-destructive/10
            text-destructive
          "
                >

                    <AlertTriangle
                        className="size-5"
                    />

                </div>


                <CardTitle>
                    Backend unavailable
                </CardTitle>


                <CardDescription>
                    Smart Attendance could not
                    load the latest dashboard data.
                </CardDescription>

            </CardHeader>


            <CardContent>

                <p
                    className="
            mb-4
            text-sm
            text-muted-foreground
          "
                >
                    {message}
                </p>


                <Button
                    variant="outline"
                    onClick={onRetry}
                >

                    <RefreshCw />

                    Retry

                </Button>

            </CardContent>

        </Card>

    )
}