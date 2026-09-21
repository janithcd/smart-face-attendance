import {
    apiGet,
} from "@/lib/api-client"

import type {
    DashboardData,
} from "@/features/dashboard/types/dashboard"


export function getDashboard(
    signal?: AbortSignal
) {

    return apiGet<DashboardData>(
        "/api/dashboard",
        {
            signal,
        }
    )
}