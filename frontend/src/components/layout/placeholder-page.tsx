import type {
    ReactNode,
} from "react"

import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from "@/components/ui/card"


type PlaceholderPageProps = {
    title: string
    description: string
    icon?: ReactNode
}


export function PlaceholderPage({
                                    title,
                                    description,
                                    icon,
                                }: PlaceholderPageProps) {

    return (

        <section
            className="
        flex
        flex-col
        gap-6
      "
        >

            <div>

                <div
                    className="
            flex
            items-center
            gap-2
          "
                >

                    {icon}

                    <h1
                        className="
              text-2xl
              font-semibold
              tracking-tight
            "
                    >
                        {title}
                    </h1>

                </div>


                <p
                    className="
            mt-1
            text-sm
            text-muted-foreground
          "
                >
                    {description}
                </p>

            </div>


            <Card>

                <CardHeader>

                    <CardTitle>
                        {title}
                    </CardTitle>

                    <CardDescription>
                        Module foundation ready.
                    </CardDescription>

                </CardHeader>


                <CardContent>

                    <div
                        className="
              flex
              min-h-48
              items-center
              justify-center
              rounded-lg
              border
              border-dashed
              text-sm
              text-muted-foreground
            "
                    >
                        This module will be implemented
                        in the next development stages.
                    </div>

                </CardContent>

            </Card>

        </section>

    )
}