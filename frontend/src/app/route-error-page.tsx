import {
    Link,
    isRouteErrorResponse,
    useRouteError,
} from "react-router"

import {
    AlertTriangle,
} from "lucide-react"


export function RouteErrorPage() {

    const error =
        useRouteError()


    let title =
        "Something went wrong"

    let message =
        "The application could not load this page."


    if (
        isRouteErrorResponse(error)
    ) {

        title =
            `${error.status} ${error.statusText}`

        message =
            typeof error.data === "string"
                ? error.data
                : message

    } else if (
        error instanceof Error
    ) {

        message =
            error.message

    }


    return (

        <div
            className="
        flex
        min-h-screen
        items-center
        justify-center
        bg-background
        p-6
      "
        >

            <div
                className="
          max-w-md
          text-center
        "
            >

                <div
                    className="
            mx-auto
            mb-4
            flex
            size-12
            items-center
            justify-center
            rounded-full
            bg-destructive/10
            text-destructive
          "
                >

                    <AlertTriangle />

                </div>


                <h1
                    className="
            text-2xl
            font-semibold
          "
                >
                    {title}
                </h1>


                <p
                    className="
            mt-2
            text-sm
            text-muted-foreground
          "
                >
                    {message}
                </p>


                <Link
                    to="/"
                    className="
            mt-6
            inline-flex
            h-9
            items-center
            justify-center
            rounded-md
            bg-primary
            px-4
            text-sm
            font-medium
            text-primary-foreground
          "
                >
                    Return to Dashboard
                </Link>

            </div>

        </div>

    )
}