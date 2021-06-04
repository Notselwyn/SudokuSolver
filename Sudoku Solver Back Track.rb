
def main
  # Enter sudoku here!!!
  # The numbers are the cells in the sudoku
  first_array = [
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
  num_index = 0
  plus_one = false
  first_array_flat = []
  new_array = [[], [], [], [], [], [], [], [], []]
  new_array_flat = []
  start = Time.now
  81.times do |i|
    first_array_flat[i] = first_array[i/9][i%9]
    new_array_flat[i] = first_array[i/9][i%9]
    new_array[i/9][i%9] = first_array[i/9][i%9]
  end
  end_index = first_array_flat.reverse.index(0)
  while num_index < 81
    tbt_box = [[], [], []]
    crosshair_cells = []
    81.times do |i|
      new_array[i/9][i%9] = new_array_flat[i]
    end
    3.times do |i|
      3.times do |j|
        tbt_box[i][j] = new_array[(num_index / 27) * 3 + i][num_index % 9 / 3 * 3 + j]
      end
    end
    h_c=0
    v_c=0
    b_c=0
    9.times do |i|
      if i != num_index % 9
        crosshair_cells[h_c] = new_array[num_index/9][i]
        h_c+=1
      end
      if i != num_index / 9
        crosshair_cells[8+v_c] = new_array[i][num_index % 9]
        v_c+=1
      end
      if i != num_index % 3 + num_index / 9 % 3 * 3
        crosshair_cells[16+b_c] = tbt_box[i/3][i%3]
        b_c+=1
      end
    end
    if num_index == 80-end_index
      9.times do |i|
        if not crosshair_cells.include? (i+1)
          new_array[num_index/9][num_index%9] = i+1
          break
        end
      end
      puts "Finished - " + (((Time.now - start) * 1000).to_i).to_s + "ms"
      9.times do |i|
        str = ""
        if i%3==0 && i!=0
          puts "-------|-------|-------"
        end
        9.times do |j|
          if j%3==0&&j!=0
            str += " |"
          end
          str += " " + new_array[i][j].to_s
        end
        puts str
      end
      break
    end
    if first_array_flat[num_index] == 0
      if plus_one == true
        new_array_flat[num_index] += 1
        if new_array_flat[num_index] > 9
          new_array_flat[num_index] = first_array_flat[num_index]
          81.times do |i|
            new_array[i/9][i%9] = new_array_flat[i]
          end
          num_index -= 2
        else
          plus_one = false
        end
      end
      while crosshair_cells.include? new_array_flat[num_index] and plus_one == false
        new_array_flat[num_index] += 1
        if new_array_flat[num_index] > 9
          new_array_flat[num_index] = first_array_flat[num_index]
          81.times do |i|
            new_array[i/9][i%9] = new_array_flat[i]
          end
          num_index -= 2
          plus_one = true
        end
      end
    elsif plus_one == true
      num_index -= 2
    end
    num_index += 1
  end
end

main()