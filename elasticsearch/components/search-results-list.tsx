"use client"

import { useState } from "react"
import { Card } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { ExternalLink, ChevronDown, ChevronUp } from "lucide-react"

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

interface SearchResultsListProps {
  results: SearchResult[]
  total: number
  page: number
  pageSize: number
  onPageChange: (page: number) => void
}

export function SearchResultsList({
  results,
  total,
  page,
  pageSize,
  onPageChange,
}: SearchResultsListProps) {
  const [expandedId, setExpandedId] = useState<string | null>(null)

  const totalPages = Math.ceil(total / pageSize)

  const truncateText = (text: string, maxLength = 200) =>
    text.length > maxLength ? `${text.slice(0, maxLength)}...` : text

  const toggleExpand = (id: string) => {
    setExpandedId(prev => (prev === id ? null : id))
  }

  return (
    <div className="space-y-6">
      {/* Results */}
      <div className="space-y-4">
        {results.map((result) => {
          const isExpanded = expandedId === result._id

          return (
            <Card
              key={result._id}
              className="bg-card border-border hover:border-primary/50 transition-all duration-200 p-6"
            >
              <div className="space-y-3">
                {/* Title */}
                <div className="flex items-start justify-between gap-4">
                  <div className="flex-1 min-w-0">
                    <a
                      href={result._source.link}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-2 mb-2"
                    >
                      <h3 className="text-xl font-semibold text-primary hover:underline text-balance">
                        {result._source.title}
                      </h3>
                      <ExternalLink className="w-4 h-4 text-muted-foreground" />
                    </a>
                  </div>

                  <Badge className="bg-primary/20 text-primary">
                    {result._score.toFixed(2)}
                  </Badge>
                </div>

                {/* Meta */}
                <div className="flex items-center justify-between pt-2 border-t border-border">
                  <a
                    href={result._source.link}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-sm text-primary hover:underline truncate"
                  >
                    {result._source.link}
                  </a>

                  {result._source.time && (
                    <span className="text-xs text-muted-foreground whitespace-nowrap">
                      {result._source.time}
                    </span>
                  )}
                </div>

                {/* Description */}
                <p className="text-muted-foreground">
                  {truncateText(result._source.description, 160)}
                </p>

                {/* Content */}
                <div className="text-muted-foreground">
                  <p className={isExpanded ? "" : "line-clamp-3"}>
                    {result._source.content}
                  </p>

                  <button
                    onClick={() => toggleExpand(result._id)}
                    className="mt-2 inline-flex items-center gap-1 text-sm text-primary hover:underline"
                  >
                    {isExpanded ? (
                      <>
                        Thu gọn <ChevronUp className="w-4 h-4" />
                      </>
                    ) : (
                      <>
                        Xem thêm <ChevronDown className="w-4 h-4" />
                      </>
                    )}
                  </button>
                </div>
              </div>
            </Card>
          )
        })}
      </div>

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="flex items-center justify-between pt-4 border-t border-border">
          <span className="text-sm text-muted-foreground">
            Trang {page} / {totalPages} — {total} kết quả
          </span>

          <div className="flex gap-2">
            <Button
              variant="outline"
              size="sm"
              disabled={page === 1}
              onClick={() => onPageChange(page - 1)}
            >
              Trước
            </Button>

            <Button
              variant="outline"
              size="sm"
              disabled={page === totalPages}
              onClick={() => onPageChange(page + 1)}
            >
              Sau
            </Button>
          </div>
        </div>
      )}
    </div>
  )
}
