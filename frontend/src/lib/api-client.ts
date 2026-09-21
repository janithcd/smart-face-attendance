const DEFAULT_API_URL =
    "http://127.0.0.1:8000"


const configuredApiUrl =
    import.meta.env.VITE_API_URL?.trim()


export const API_BASE_URL =
    (
        configuredApiUrl ||
        DEFAULT_API_URL
    ).replace(/\/$/, "")


export class ApiError extends Error {

    status: number

    constructor(
        message: string,
        status: number
    ) {

        super(message)

        this.name = "ApiError"
        this.status = status
    }
}


type ApiRequestOptions = {
    signal?: AbortSignal
}


export async function apiGet<T>(
    path: string,
    options: ApiRequestOptions = {}
): Promise<T> {

    const response =
        await fetch(
            `${API_BASE_URL}${path}`,
            {
                method: "GET",

                headers: {
                    Accept: "application/json",
                },

                signal: options.signal,
            }
        )


    if (!response.ok) {

        let message =
            `Request failed with status ${response.status}`

        try {

            const body =
                await response.json() as {
                    detail?: string
                }

            if (body.detail) {
                message = body.detail
            }

        } catch {

            // Ignore non-JSON error bodies.

        }


        throw new ApiError(
            message,
            response.status
        )
    }


    return response.json() as Promise<T>
}