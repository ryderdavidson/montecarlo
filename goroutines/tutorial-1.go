package main

import (
	"fmt"
	"math"
	"math/rand"
	"sync"
	"time"
)

const size = 100000000

var points [size]float64

var wg sync.WaitGroup

func main() {
	//for sizeInc := 2; sizeInc < 7; sizeInc++ {
	for threadInc := 1; threadInc < 7; threadInc++ {

		//size := int(math.Pow(10, float64(sizeInc)))
		threadNum := int(math.Pow(2, float64(threadInc)))

		for i := 0; i < size; i++ {
			x := rand.Float64()
			y := rand.Float64()
			points[i] = math.Sqrt(x*x + y*y)
		}

		rand.Seed(time.Now().UnixNano())
		count := 0
		channel := make(chan int, size)

		chunk := size / threadNum
		start := chunk + size%threadNum

		startTime := time.Now()

		wg.Add(1)
		go monte(&points, &wg, channel, 0, start)

		for i := 1; i < threadNum; i++ {
			startIndex := start + chunk*(i-1)
			endIndex := startIndex + chunk
			wg.Add(1)
			go monte(&points, &wg, channel, startIndex, endIndex)
		}

		wg.Wait()
		close(channel)
		duration := time.Since(startTime)

		for i := 0; i < threadNum; i++ {
			x := <-channel
			count += x
		}

		fmt.Printf("%-10s%-10v \n", "Number of Points = ", size)
		fmt.Printf("%-10s%-10v \n", "Number of goroutines = ", threadNum)
		fmt.Printf("%-10s%-10v \n", "Count = ", count)
		fmt.Printf("%-10s%-10f \n", "Pi Estimate = ", float64(4*count)/float64(size))
		fmt.Printf("%-10s%-20v \n\n", "Duration = ", duration)
	}

	var input string
	fmt.Scanln(&input)

}

func monte(points *[size]float64, wg *sync.WaitGroup, c chan int, startIndex int, endIndex int) {
	defer wg.Done()
	localCount := 0

	for i := startIndex; i < endIndex; i++ {
		if points[i] <= 1 {
			localCount++
		}
	}

	c <- localCount
}
