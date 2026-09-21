import type {
    LucideIcon,
} from "lucide-react"

import {
    Card,
    CardContent,
    CardHeader,
    CardTitle,
} from "@/components/ui/card"


type DashboardStatCardProps = {

    title: string

    value:
        string | number

    description: string

    icon: LucideIcon

    iconClassName?: string
}


export function DashboardStatCard({
                                      title,
                                      value,
                                      description,
                                      icon: Icon,
                                      iconClassName =
                                      "text-primary",
                                  }: DashboardStatCardProps) {

    return (

        <Card>

            <CardHeader
                className="
          flex
          flex-row
          items-center
          justify-between
          space-y-0
        "
            >

                <CardTitle
                    className="
            text-sm
            font-medium
            text-muted-foreground
          "
                >
                    {title}
                </CardTitle>


                <div
                    className="
            flex
            size-9
            items-center
            justify-center
            rounded-lg
            bg-muted
          "
                >

                    <Icon
                        className={`
              size-4
              ${iconClassName}
            `}
                    />

                </div>

            </CardHeader>


            <CardContent>

                <div
                    className="
            text-3xl
            font-semibold
            tracking-tight
          "
                >
                    {value}
                </div>


                <p
                    className="
            mt-1
            text-xs
            text-muted-foreground
          "
                >
                    {description}
                </p>

            </CardContent>

        </Card>

    )
}