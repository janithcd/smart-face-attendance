import {
  Activity,
} from "lucide-react"

import {
  ModeToggle,
} from "@/components/mode-toggle"

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"


function App() {

  return (

      <div
          className="
        min-h-screen
        bg-background
        text-foreground
      "
      >

        <header
            className="
          flex
          items-center
          justify-between
          border-b
          px-6
          py-4
        "
        >

          <div
              className="
            flex
            items-center
            gap-3
          "
          >

            <Activity
                className="
              h-6
              w-6
              text-primary
            "
            />

            <div>

              <h1
                  className="
                font-semibold
              "
              >
                Smart Attendance
              </h1>

              <p
                  className="
                text-sm
                text-muted-foreground
              "
              >
                Biometric Attendance Platform
              </p>

            </div>

          </div>

          <ModeToggle />

        </header>


        <main
            className="
          mx-auto
          max-w-7xl
          p-6
        "
        >

          <Card>

            <CardHeader>

              <CardTitle>
                Frontend Foundation Ready
              </CardTitle>

              <CardDescription>
                React + TypeScript +
                Tailwind + shadcn/ui
              </CardDescription>

            </CardHeader>

            <CardContent>

              <p>
                Our new application architecture
                is ready for the production
                dashboard.
              </p>

            </CardContent>

          </Card>

        </main>

      </div>
  )
}


export default App