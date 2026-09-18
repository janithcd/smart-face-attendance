import { useEffect, useState } from "react";
import "./App.css";


type Attendance = {
  id: number;
  person_id: string;
  person_name: string;
  date: string;
  time: string;
  verification_method: string;
};


type DashboardData = {
  registered_people: number;
  today_attendance: number;
  system_status: string;
  attendance: Attendance[];
};


function App() {

  const [data, setData] =
      useState<DashboardData | null>(null);

  const [loading, setLoading] =
      useState(true);

  const [error, setError] =
      useState("");


  async function loadDashboard() {

    try {

      setError("");

      const response = await fetch(
          "http://127.0.0.1:8000/api/dashboard"
      );

      if (!response.ok) {
        throw new Error(
            "Could not load dashboard"
        );
      }

      const result =
          await response.json();

      setData(result);

    } catch (err) {

      setError(
          err instanceof Error
              ? err.message
              : "Unknown error"
      );

    } finally {

      setLoading(false);

    }
  }


  useEffect(() => {

    loadDashboard();

    const interval = setInterval(
        loadDashboard,
        5000
    );

    return () =>
        clearInterval(interval);

  }, []);


  if (loading) {
    return <h2>Loading...</h2>;
  }


  if (error) {

    return (
        <div>
          <h2>Backend connection failed</h2>
          <p>{error}</p>
        </div>
    );

  }


  if (!data) {
    return null;
  }


  return (
      <main>

        <h1>
          Smart Face Attendance
        </h1>

        <p>
          SFace Recognition + MediaPipe
          Liveness Verification
        </p>


        <section>

          <div>
            <h2>
              {data.registered_people}
            </h2>

            <p>
              Registered People
            </p>
          </div>


          <div>
            <h2>
              {data.today_attendance}
            </h2>

            <p>
              Today's Attendance
            </p>
          </div>


          <div>
            <h2>
              {data.system_status}
            </h2>

            <p>
              System Status
            </p>
          </div>

        </section>


        <h2>
          Today's Attendance
        </h2>


        <table>

          <thead>

          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Date</th>
            <th>Time</th>
            <th>Verification</th>
          </tr>

          </thead>


          <tbody>

          {data.attendance.map(
              (record) => (

                  <tr key={record.id}>

                    <td>
                      {record.person_id}
                    </td>

                    <td>
                      {record.person_name}
                    </td>

                    <td>
                      {record.date}
                    </td>

                    <td>
                      {record.time}
                    </td>

                    <td>
                      {record.verification_method}
                    </td>

                  </tr>

              )
          )}

          </tbody>

        </table>

      </main>
  );
}


export default App;