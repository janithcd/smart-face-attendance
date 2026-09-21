import {
    Activity,
    RefreshCw,
    ScanFace,
    ShieldCheck,
    UserCheck,
    UserMinus,
    Users,
} from "lucide-react"

import {
    Link,
} from "react-router"

import {
    Button,
} from "@/components/ui/button"

import {
    Badge,
} from "@/components/ui/badge"

import {
    DashboardErrorState,
} from "@/features/dashboard/components/dashboard-error-state"

import {
    DashboardSkeleton,
} from "@/features/dashboard/components/dashboard-skeleton"

import {
    DashboardStatCard,
} from "@/features/dashboard/components/dashboard-stat-card"

import {
    RecentAttendanceTable,
} from "@/features/dashboard/components/recent-attendance-table"

import {
    useDashboardQuery,
} from "@/features/dashboard/queries/use-dashboard-query"


export function Component() {

    const {
        data,
        dataUpdatedAt,
        error,
        isError,
        isFetching,
        isPending,
        refetch,
    } = useDashboardQuery()


    if (isPending) {

        return (
            <DashboardSkeleton />
        )

    }


    if (
        isError ||
        !data
    ) {

        return (

            <DashboardErrorState
                message={
                    error instanceof Error
                        ? error.message
                        : "Unknown API error."
                }
                onRetry={() => {
                    void refetch()
                }}
            />

        )
    }


    const notCheckedIn =
        Math.max(
            data.registered_people -
            data.today_attendance,
            0
        )


    const lastUpdated =
        dataUpdatedAt
            ? new Date(
                dataUpdatedAt
            ).toLocaleTimeString(
                [],
                {
                    hour: "2-digit",
                    minute: "2-digit",
                    second: "2-digit",
                }
            )
            : "—"


    return (

        <section
            className="
        flex
        flex-col
        gap-6
      "
        >

            <div
                className="
          flex
          flex-col
          gap-4
          lg:flex-row
          lg:items-center
          lg:justify-between
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

                        <h1
                            className="
                text-2xl
                font-semibold
                tracking-tight
              "
                        >
                            Dashboard
                        </h1>


                        <Badge
                            variant="outline"
                            className="
                gap-1
                text-emerald-600
                dark:text-emerald-400
              "
                        >

                            <Activity
                                className="size-3"
                            />

                            Live

                        </Badge>

                    </div>


                    <p
                        className="
              mt-1
              text-sm
              text-muted-foreground
            "
                    >
                        Monitor today's biometric
                        attendance and system activity.
                    </p>

                </div>


                <div
                    className="
            flex
            flex-wrap
            items-center
            gap-2
          "
                >

          <span
              className="
              mr-1
              text-xs
              text-muted-foreground
            "
          >
            Updated {lastUpdated}
          </span>


                    <Button
                        variant="outline"
                        size="sm"
                        onClick={() => {
                            void refetch()
                        }}
                        disabled={isFetching}
                    >

                        <RefreshCw
                            className={
                                isFetching
                                    ? "animate-spin"
                                    : ""
                            }
                        />

                        Refresh

                    </Button>


                    <Button
                        size="sm"
                        render={
                            <Link
                                to="/attendance"
                            />
                        }
                    >

                        <ScanFace />

                        Attendance

                    </Button>

                </div>

            </div>


            <div
                className="
          grid
          gap-4
          sm:grid-cols-2
          xl:grid-cols-4
        "
            >

                <DashboardStatCard
                    title="Registered People"
                    value={
                        data.registered_people
                    }
                    description={
                        "Biometric profiles available"
                    }
                    icon={Users}
                />


                <DashboardStatCard
                    title="Present Today"
                    value={
                        data.today_attendance
                    }
                    description={
                        "Verified attendance records"
                    }
                    icon={UserCheck}
                    iconClassName="
            text-emerald-600
            dark:text-emerald-400
          "
                />


                <DashboardStatCard
                    title="Not Checked In"
                    value={
                        notCheckedIn
                    }
                    description={
                        "Registered people not recorded today"
                    }
                    icon={UserMinus}
                    iconClassName="
            text-amber-600
            dark:text-amber-400
          "
                />


                <DashboardStatCard
                    title="System"
                    value={
                        data.system_status
                    }
                    description={
                        "Biometric recognition service"
                    }
                    icon={ShieldCheck}
                    iconClassName="
            text-emerald-600
            dark:text-emerald-400
          "
                />

            </div>


            <RecentAttendanceTable
                records={
                    data.attendance
                }
            />

        </section>

    )
}