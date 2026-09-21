import {
    useQuery,
} from "@tanstack/react-query"

import {
    getDashboard,
} from "@/features/dashboard/api/dashboard-api"


export const dashboardQueryKey =
    [
        "dashboard",
    ] as const


export function useDashboardQuery() {

    return useQuery({

        queryKey:
        dashboardQueryKey,

        queryFn: ({
                      signal,
                  }) =>
            getDashboard(signal),

        refetchInterval:
            5_000,

        refetchIntervalInBackground:
            false,

    })
}