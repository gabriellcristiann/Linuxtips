FROM golang:1.25-alpine AS builder

# RUN apk add --no-cache gcc musl-dev
WORKDIR /app
COPY . /app

RUN go build exporter.go

FROM alpine:3.23.2

COPY --from=builder /app/exporter /app/exporter
EXPOSE 7788
WORKDIR /app

CMD ["./exporter"]