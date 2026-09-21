import {
    Card,
    CardContent,
    CardHeader,
} from "@/components/ui/card"

import {
    Skeleton,
} from "@/components/ui/skeleton"


export function DashboardSkeleton() {

    return (

        <div
            className="
        flex
        flex-col
        gap-6
      "
        >

            <div
                className="
          space-y-2
        "
            >

                <Skeleton
                    className="
            h-8
            w-52
          "
                />

                <Skeleton
                    className="
            h-4
            w-80
            max-w-full
          "
                />

            </div>


            <div
                className="
          grid
          gap-4
          sm:grid-cols-2
          xl:grid-cols-4
        "
            >

                {Array.from({
                    length: 4,
                }).map(
                    (_, index) => (

                        <Card key={index}>

                            <CardHeader>

                                <Skeleton
                                    className="
                    h-4
                    w-28
                  "
                                />

                            </CardHeader>


                            <CardContent
                                className="
                  space-y-3
                "
                            >

                                <Skeleton
                                    className="
                    h-9
                    w-20
                  "
                                />

                                <Skeleton
                                    className="
                    h-3
                    w-36
                  "
                                />

                            </CardContent>

                        </Card>

                    )
                )}

            </div>


            <Card>

                <CardHeader>

                    <Skeleton
                        className="
              h-5
              w-40
            "
                    />

                </CardHeader>


                <CardContent
                    className="
            space-y-4
          "
                >

                    {Array.from({
                        length: 5,
                    }).map(
                        (_, index) => (

                            <Skeleton
                                key={index}
                                className="
                  h-10
                  w-full
                "
                            />

                        )
                    )}

                </CardContent>

            </Card>

        </div>

    )
}