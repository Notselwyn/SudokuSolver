function main () {
    // Enter sudoku here!!!
    const first_array = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 0]
    ]
    let first_array_flat=[];
    let new_array=[[], [], [], [], [], [], [], [], []];
    let new_array_flat=[];

    let num_index=0;
    let plus_one = false;

    const {_,performance} = require('perf_hooks');
    const time_start = performance.now();

    for (let i=0;i<81;i++) {
        let active_num = first_array[parseInt(i/9)][i%9];
        first_array_flat.push(active_num);
        new_array[parseInt(i/9)].push(active_num);
        new_array_flat.push(active_num);
    }

    let end_index = first_array_flat.lastIndexOf(0);
    while (num_index < 81) {
        let tbt_box = [[], [], []];
        let crosshair_cells = [];
        for (let i=0;i<81;i++) {
            new_array[parseInt(i/9)][i%9] = new_array_flat[i];
        }
        for (let i=0;i<3;i++) {
            for (let j=0;j<3;j++) {
                tbt_box[i][j] = new_array[parseInt(num_index / 27) * 3 + i][parseInt(num_index % 9 / 3) * 3 + j]
            }
        }

        let h_c=0;
        let v_c=0;
        let b_c=0;

        for (let i=0;i<9;i++) {
            if (i != num_index % 9) {
                crosshair_cells[h_c] = new_array[parseInt(num_index / 9)][i];
                h_c += 1;
            }
            if (i != parseInt(num_index / 9)) {
                crosshair_cells[8 + v_c] = new_array[i][num_index % 9];
                v_c += 1;
            }
            if (i != num_index % 3 + parseInt(num_index / 9) % 3 * 3) {
                crosshair_cells[16 + b_c] = tbt_box[parseInt(i / 3)][i % 3];
                b_c += 1;
            }
        }

        if (num_index == end_index) {
            for (let i=0;i<9;i++) {
                if (!crosshair_cells.includes(i+1)) {
                    new_array[parseInt(num_index/9)][num_index%9] = i+1;
                    break;
                }
            }
            const time_end = performance.now()
            console.log("Finished - " + parseInt(time_end-time_start) + "ms");
            for (let i=0;i<9;i++) {
                let str = "";
                if (i%3==0 && i!=0) {
                    console.log("-------|-------|-------");
                }
                for (let j=0;j<9;j++) {
                    if (j%3==0&&j!=0) {
                        str += " |";
                    }
                    str += " " + new_array[i][j];
                }
                console.log(str);
            }
            return time_end-time_start;
        }

        if (first_array_flat[num_index] == 0) {
            if (plus_one == true) {
                new_array_flat[num_index] += 1;
                if (new_array_flat[num_index] > 9) {
                    new_array_flat[num_index] = first_array_flat[num_index];
                    for (let i=0;i<9;i++) {
                        new_array[parseInt(i/9)][i%9] = new_array_flat[i];
                    }
                    num_index-=2;
                } else {
                    plus_one = false;
                }
            }

            while (crosshair_cells.includes(new_array_flat[num_index]) && plus_one == false) {
                new_array_flat[num_index] += 1;
                if (new_array_flat[num_index] > 9) {
                    new_array_flat[num_index] = first_array_flat[num_index];
                    for (let i=0;i<81;i++) {
                        new_array[parseInt(i/9)][i%9] = new_array_flat[i];
                    }
                    num_index-=2;
                    plus_one = true;
                }
            }
        } else if (plus_one == true) {
            num_index-=2;
        }
        num_index+=1;
    }
}

main()