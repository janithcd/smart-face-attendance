export type AttendanceRecord = {
    id: number
    person_id: string
    person_name: string
    date: string
    time: string
    verification_method: string
}


export type DashboardData = {
    registered_people: number
    today_attendance: number
    system_status: string
    attendance: AttendanceRecord[]
}