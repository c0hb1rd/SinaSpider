package main

import (
	"fmt"
	"os/exec"
)

func runSpider(uid int) bool {
	cmd := fmt.Sprintf("Final_Spider.py %d", uid)
	command := exec.Command("/bin/sh", "-c", cmd)
	command.Run()

	return true
}

func main() {
	// cmd := exec.Command("/usr/bin/python", "-c", "Final_Spider.py")

	flag := make(chan bool)

	go func() {
		for uid := 1000000000; uid < 1075567393; uid++ {
			fmt.Printf("[*]Processing %d...\n", uid)
			if uid == 1075567392 {
				flag <- runSpider(uid)
			} else {
				runSpider(uid)
			}
			fmt.Printf("[*]Completion %d.\n", uid)
		}
	}()

	if <-flag {
		fmt.Println("Done")
	}
}

// package main
//
// import (
// 	F "fmt"
// 	"os"
// 	"os/exec"
// 	"syscall"
// )
//
// func runSpider(uid int) {
// 	// cmd := fmt.Sprintf("Final_Spider.py %d", uid)
// 	// command := exec.Command("/usr/bin/python", " ", cmd)
// 	// command.Run()
// }
//
// func main() {
// 	binary, lookErr := exec.LookPath("Final_Spider.py")
// 	if lookErr != nil {
// 		panic(lookErr)
// 	}
//
// 	args := []string{"Final_Spider.py", "1075567392"}
//
// 	env := os.Environ()
//
// 	F.Println("$Final_Spider.py 1075567392")
// 	execErr := syscall.Exec(binary, args, env)
// 	if execErr != nil {
// 		panic(execErr)
// 	}
// }
