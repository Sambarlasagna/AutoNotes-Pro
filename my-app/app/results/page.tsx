"use client"

import { useSearchParams, useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { CheckCircle, ArrowLeft, Download, FileText } from "lucide-react"
import { Suspense } from "react"

function ResultsContent() {
  const searchParams = useSearchParams()
  const router = useRouter()

  const fileName = searchParams.get("fileName") || "Unknown file"
  const fileSize = searchParams.get("fileSize") || "0"
  const fileSizeMB = (Number.parseInt(fileSize) / 1024 / 1024).toFixed(2)

  const handleBackToHome = () => {
    router.push("/")
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-emerald-100 flex items-center justify-center p-4">
      <div className="w-full max-w-2xl">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">AutoNotes Pro</h1>
          <p className="text-gray-600">Your audio has been processed successfully!</p>
        </div>

        <Card className="shadow-lg">
          <CardHeader className="text-center">
            <div className="flex justify-center mb-4">
              <CheckCircle className="h-16 w-16 text-green-500" />
            </div>
            <CardTitle className="text-green-700">Processing Complete!</CardTitle>
            <CardDescription>Your audio file has been successfully converted to notes</CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="bg-gray-50 p-4 rounded-lg">
              <h3 className="font-semibold text-gray-900 mb-2">File Details:</h3>
              <div className="space-y-1 text-sm text-gray-600">
                <p>
                  <strong>File Name:</strong> {decodeURIComponent(fileName)}
                </p>
                <p>
                  <strong>File Size:</strong> {fileSizeMB} MB
                </p>
                <p>
                  <strong>Status:</strong> <span className="text-green-600">Successfully Processed</span>
                </p>
              </div>
            </div>

            <div className="bg-blue-50 p-4 rounded-lg">
              <h3 className="font-semibold text-blue-900 mb-2 flex items-center gap-2">
                <FileText className="h-5 w-5" />
                Generated Notes Preview:
              </h3>
              <div className="text-sm text-blue-800 space-y-2">
                <p>• Key topics and themes identified</p>
                <p>• Important timestamps marked</p>
                <p>• Action items extracted</p>
                <p>• Summary and conclusions generated</p>
              </div>
            </div>

            <div className="flex gap-3">
              <Button onClick={handleBackToHome} variant="outline" className="flex-1">
                <ArrowLeft className="h-4 w-4 mr-2" />
                Upload Another File
              </Button>
              <Button className="flex-1">
                <Download className="h-4 w-4 mr-2" />
                Download Notes
              </Button>
            </div>
          </CardContent>
        </Card>

        <div className="mt-6 text-center text-sm text-gray-500">
          <p>Your notes are ready for download and have been saved to your account.</p>
        </div>
      </div>
    </div>
  )
}

export default function ResultsPage() {
  return (
    <Suspense
      fallback={
        <div className="min-h-screen bg-gradient-to-br from-green-50 to-emerald-100 flex items-center justify-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-green-600"></div>
        </div>
      }
    >
      <ResultsContent />
    </Suspense>
  )
}
