package main

import (
	"fmt"
	"time"
)

func in_array(arr [24]int, n int) bool {
	for i:=0;i<24;i++ {
		if arr[i] == n {
			return true
		}
	}
	return false
}

func reverse(numbers [81]int) [81]int {
	for i := 0; i < len(numbers)/2; i++ {
		j := len(numbers) - i - 1
		numbers[i], numbers[j] = numbers[j], numbers[i]
	}
	return numbers
}

func main() {
	// Define Sudoku here!!
	var first_array = [9][9]int {
		{5, 3, 0, 0, 7, 0, 0, 0, 0},
		{6, 0, 0, 1, 9, 5, 0, 0, 0},
		{0, 9, 8, 0, 0, 0, 0, 6, 0},
		{8, 0, 0, 0, 6, 0, 0, 0, 3},
		{4, 0, 0, 8, 0, 3, 0, 0, 1},
		{7, 0, 0, 0, 2, 0, 0, 0, 6},
		{0, 6, 0, 0, 0, 0, 2, 8, 0},
		{0, 0, 0, 4, 1, 9, 0, 0, 5},
		{0, 0, 0, 0, 8, 0, 0, 7, 0}}
	var new_array [9][9]int
	var first_array_flat [81]int
	var new_array_flat [81]int
	var plus_one bool
	var num_index int
	var end_index int
	start_time := time.Now()

	for i:=0; i<81; i++ {
		active_num := first_array[i/9][i%9]
		first_array_flat[i] = active_num
		new_array_flat[i] = active_num
		if active_num == 0 {
			end_index = i
		}
	}

	for num_index < 81 {
		var tbt_box [3][3]int
		var crosshair_cells [24]int

		for i:=0;i<81;i++ {
			new_array[i/9][i%9] = new_array_flat[i]
		}
		for i:=0;i<3;i++ {
			for j:=0;j<3;j++ {
				tbt_box[i][j] = new_array[(num_index / 27) * 3 + i][num_index % 9 / 3 * 3 + j]
			}
		}
    	var h_c int
    	var v_c int
    	var b_c int

		for i:=0;i<9;i++ {
			if i != num_index % 9 {
        		crosshair_cells[h_c] = new_array[num_index/9][i]
        		h_c+=1
			}
			if i != num_index / 9 {
				crosshair_cells[8+v_c] = new_array[i][num_index % 9]
        		v_c+=1
			}

			if i != num_index % 3 + num_index / 9 % 3 * 3 {
				crosshair_cells[16+b_c] = tbt_box[i/3][i%3]
				b_c += 1
			}
		}

		if num_index == end_index {
			for i:=0;i<9;i++ {
				if !in_array(crosshair_cells, i+1) {
          			new_array[num_index/9][num_index%9] = i+1
          			break
				}
			}
			end_time := time.Now()
			fmt.Printf("Finished - %dms\n", (end_time.UnixNano() - start_time.UnixNano()) / 1000000)
			for i:=0;i<9;i++ {
				var str = ""
				if i%3==0 && i!=0 {
					fmt.Println("-------|-------|-------")
				}
				for j:=0;j<9;j++ {
					if j%3==0&&j!=0 {
						str += " |"
					}
					str += " " + string(48 + new_array[i][j])
				}
				fmt.Println(str)
			}
		}

		if first_array_flat[num_index] == 0 {
			if plus_one == true {
				new_array_flat[num_index] += 1
				if new_array_flat[num_index] > 9 {
					new_array_flat[num_index] = first_array_flat[num_index]
					for i:=0;i<9;i++ {
            			new_array[i/9][i%9] = new_array_flat[i]
					}
					num_index -= 2
				} else {
					plus_one = false
				}
			}
			for in_array(crosshair_cells, new_array_flat[num_index]) && plus_one == false {
				new_array_flat[num_index] += 1
				if new_array_flat[num_index] > 9 {
					new_array_flat[num_index] = first_array_flat[num_index]
					for i:=0;i<81;i++ {
						new_array[i/9][i%9] = new_array_flat[i]
					}
					num_index -= 2
					plus_one = true
				}
			}
		} else if plus_one == true {
			num_index -= 2
		}
		num_index += 1
	}
}
