import {
    CheckCircle2,
    ScanFace,
} from "lucide-react"

import {
    Badge,
} from "@/components/ui/badge"

import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from "@/components/ui/card"

import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table"

import type {
    AttendanceRecord,
} from "@/features/dashboard/types/dashboard"


type RecentAttendanceTableProps = {
    records: AttendanceRecord[]
}


export function RecentAttendanceTable({
                                          records,
                                      }: RecentAttendanceTableProps) {

    const recentRecords =
        [...records]
            .reverse()
            .slice(0, 10)


    return (

        <Card>

            <CardHeader>

                <CardTitle>
                    Recent Attendance
                </CardTitle>


                <CardDescription>
                    Latest verified check-ins
                    recorded today.
                </CardDescription>

            </CardHeader>


            <CardContent>

                {recentRecords.length === 0 ? (

                    <div
                        className="
              flex
              min-h-52
              flex-col
              items-center
              justify-center
              rounded-lg
              border
              border-dashed
              text-center
            "
                    >

                        <div
                            className="
                mb-3
                flex
                size-10
                items-center
                justify-center
                rounded-full
                bg-muted
              "
                        >

                            <ScanFace
                                className="
                  size-5
                  text-muted-foreground
                "
                            />

                        </div>


                        <p
                            className="
                font-medium
              "
                        >
                            No attendance yet
                        </p>


                        <p
                            className="
                mt-1
                max-w-sm
                text-sm
                text-muted-foreground
              "
                        >
                            Verified attendance
                            records will appear here
                            when people check in.
                        </p>

                    </div>

                ) : (

                    <Table>

                        <TableHeader>

                            <TableRow>

                                <TableHead>
                                    Person
                                </TableHead>

                                <TableHead>
                                    ID
                                </TableHead>

                                <TableHead>
                                    Time
                                </TableHead>

                                <TableHead
                                    className="
                    hidden
                    md:table-cell
                  "
                                >
                                    Verification
                                </TableHead>

                                <TableHead
                                    className="
                    hidden
                    lg:table-cell
                  "
                                >
                                    Status
                                </TableHead>

                            </TableRow>

                        </TableHeader>


                        <TableBody>

                            {recentRecords.map(
                                (record) => (

                                    <TableRow
                                        key={record.id}
                                    >

                                        <TableCell
                                            className="
                        font-medium
                      "
                                        >
                                            {record.person_name}
                                        </TableCell>


                                        <TableCell
                                            className="
                        text-muted-foreground
                      "
                                        >
                                            {record.person_id}
                                        </TableCell>


                                        <TableCell>
                                            {record.time}
                                        </TableCell>


                                        <TableCell
                                            className="
                        hidden
                        md:table-cell
                        text-muted-foreground
                      "
                                        >
                                            {
                                                record.verification_method
                                            }
                                        </TableCell>


                                        <TableCell
                                            className="
                        hidden
                        lg:table-cell
                      "
                                        >

                                            <Badge
                                                variant="secondary"
                                            >

                                                <CheckCircle2 />

                                                Verified

                                            </Badge>

                                        </TableCell>

                                    </TableRow>

                                )
                            )}

                        </TableBody>

                    </Table>

                )}

            </CardContent>

        </Card>

    )
}