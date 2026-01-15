package main

import (
	"log"
	"net/http"

	"github.com/pbnjay/memory"
	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promhttp"
)

func freeMemory() float64 {
	free_memory := memory.FreeMemory()
	return float64(free_memory)
}

func totalMemory() float64 {
	total_memory := memory.TotalMemory()
	return float64(total_memory)
}

var (
	freeMemoryBytesGauge = prometheus.NewGauge(prometheus.GaugeOpts{
		Name:  "memoria_livre_bytes",
		Help: "Quantidade de memória livre em bytes",
	})

	freeMemoryMegasGauge = prometheus.NewGauge(prometheus.GaugeOpts{
		Name:  "memoria_livre_megas",
		Help: "Quantidade de memória livre em megas",
	})

	totalMemoryBytesGauge = prometheus.NewGauge(prometheus.GaugeOpts{
		Name:  "memoria_total_bytes",
		Help: "Quantidade total de memória em bytes",
	})

	totalMemoryGigasGauge = prometheus.NewGauge(prometheus.GaugeOpts{
		Name: "memoria_total_gigas",
		Help: "Total de memoria em gigas",
	})
)

func init() {
	prometheus.MustRegister(freeMemoryBytesGauge)
	prometheus.MustRegister(freeMemoryMegasGauge)
	prometheus.MustRegister(totalMemoryBytesGauge)
	prometheus.MustRegister(totalMemoryGigasGauge)
}

func main() {
	freeMemoryBytesGauge.Set(freeMemory())
	freeMemoryMegasGauge.Set(freeMemory() / 1024 / 1024)
	totalMemoryBytesGauge.Set(totalMemory())
	totalMemoryGigasGauge.Set(totalMemory() / 1024 / 1024 / 1024)
	http.Handle("/metrics", promhttp.Handler())

	log.Fatal(http.ListenAndServe(":7788", nil))
}