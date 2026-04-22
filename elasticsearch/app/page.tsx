"use client"

import type React from "react"
import { Suspense, useState, useCallback } from "react"

import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { SearchResultsList } from "@/components/search-results-list"
import { SearchIcon } from "lucide-react"

interface SearchResult {
  _id: string
  _score: number
  _source: {
    title: string
    description: string
    content: string
    time: string
    link: string
  }
}

const PAGE_SIZE = 10

function SearchContent() {
  const [query, setQuery] = useState("")
  const [results, setResults] = useState<SearchResult[]>([])
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(1)

  const [loading, setLoading] = useState(false)
  const [searched, setSearched] = useState(false)

  const fetchSearch = useCallback(
    async (q: string, pageNumber = 1) => {
      setLoading(true)
      try {
        const response = await fetch(
          `http://192.168.10.101:5000/search?q=${encodeURIComponent(q)}&page=${pageNumber}&size=${PAGE_SIZE}`,
          { method: "GET", }
        )
        const data = await response.json()

        setResults(data.hits || [])
        setTotal(data.total.value || 0)
        setPage(pageNumber)
      } catch (error) {
        console.error("Search error:", error)
        setResults([])
        setTotal(0)
      } finally {
        setLoading(false)
      }
    },
    []
  )

  const handleSearch = useCallback(
    async (e: React.FormEvent) => {
      e.preventDefault()
      if (!query.trim()) return

      setSearched(true)
      fetchSearch(query, 1)
    },
    [query, fetchSearch]
  )

  const handleClear = () => {
    setQuery("")
    setResults([])
    setTotal(0)
    setPage(1)
    setSearched(false)
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Hero */}
      <div className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-primary/10 via-transparent to-transparent" />
        <div className="relative max-w-6xl mx-auto px-4 py-24 sm:py-32">
          <div className="text-center space-y-6">
            <h1 className="text-4xl sm:text-6xl font-bold text-foreground">
              Khám phá tài liệu
            </h1>
            <p className="text-lg sm:text-xl text-muted-foreground max-w-2xl mx-auto">
              Tìm kiếm bài viết về thiên văn
            </p>

            <form onSubmit={handleSearch} className="mt-8 max-w-2xl mx-auto">
              <div className="flex gap-2">
                <Input
                  type="text"
                  placeholder="Tìm kiếm theo tiêu đề, mô tả hoặc nội dung..."
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  className="flex-1 h-12"
                />
                <Button type="submit" disabled={loading} className="h-12 px-6">
                  <SearchIcon className="w-5 h-5 mr-2" />
                  Tìm kiếm
                </Button>
              </div>
            </form>
          </div>
        </div>
      </div>

      {/* Results */}
      <div className="max-w-6xl mx-auto px-4 py-12">
        {searched && (
          <div className="space-y-6">
            <div className="flex items-center justify-between">

              {total > 0 && (
                <Button variant="outline" onClick={handleClear}>
                  Xóa
                </Button>
              )}
            </div>

            {loading ? (
              <Card className="p-8 text-center">
                <div className="flex justify-center gap-2">
                  <div className="w-2 h-2 bg-primary rounded-full animate-bounce" />
                  <div className="w-2 h-2 bg-primary rounded-full animate-bounce delay-100" />
                  <div className="w-2 h-2 bg-primary rounded-full animate-bounce delay-200" />
                </div>
              </Card>
            ) : results.length > 0 ? (
              <SearchResultsList
                results={results}
                total={total}
                page={page}
                pageSize={PAGE_SIZE}
                onPageChange={(p) => fetchSearch(query, p)}
              />
            ) : (
              <Card className="p-12 text-center">
                <SearchIcon className="w-12 h-12 mx-auto text-muted-foreground opacity-50" />
                <p className="text-muted-foreground text-lg mt-4">
                  Hãy thử tìm kiếm với từ khóa khác
                </p>
              </Card>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

export default function HomePage() {
  return (
    <Suspense fallback={null}>
      <SearchContent />
    </Suspense>
  )
}
